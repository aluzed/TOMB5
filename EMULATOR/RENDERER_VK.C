/*
 * Backend Vulkan (RMIG-009/010/011).
 *
 * Pipeline PSX : texture VRAM 16 bits (RG8), vertex buffer, trois shaders
 * de texture (4/8/16 bits) + shader de blit, blends PSX et presentation.
 * Selection par TOMB5_RENDERER=vulkan ; le backend GL reste le defaut.
 */

#include "RENDERER.H"

#if defined(__LP64__) && defined(HAVE_VULKAN)

#include <SDL2/SDL.h>
#include <SDL2/SDL_vulkan.h>
#include <vulkan/vulkan.h>

#include "EMULATOR_PRIVATE.H"
#include "LIBGPU.H"
#include "SHADERS_VK.H"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

extern unsigned short vram[1024 * 512];

#define VK_CHECK(x) do { VkResult r_ = (x); if (r_ != VK_SUCCESS) { \
    std::fprintf(stderr, "[VK] error %d at %s:%d\n", (int)r_, __FILE__, __LINE__); \
    return 0; } } while (0)

#define VK_FORMATS 4
#define VK_BLENDS 5

struct VKState
{
    SDL_Window* window = nullptr;
    VkInstance instance = VK_NULL_HANDLE;
    VkDebugUtilsMessengerEXT debugMessenger = VK_NULL_HANDLE;
    VkSurfaceKHR surface = VK_NULL_HANDLE;
    VkPhysicalDevice physical = VK_NULL_HANDLE;
    VkDevice device = VK_NULL_HANDLE;
    uint32_t queueFamily = 0;
    VkQueue queue = VK_NULL_HANDLE;
    VkSwapchainKHR swapchain = VK_NULL_HANDLE;
    VkFormat format = VK_FORMAT_B8G8R8A8_UNORM;
    VkExtent2D extent = {640, 480};
    std::vector<VkImage> images;
    std::vector<VkImageView> views;
    std::vector<VkFramebuffer> framebuffers;
    VkRenderPass renderPass = VK_NULL_HANDLE;
    VkCommandPool commandPool = VK_NULL_HANDLE;
    std::vector<VkCommandBuffer> commandBuffers;
    VkSemaphore imageAvailable = VK_NULL_HANDLE;
    VkSemaphore renderFinished = VK_NULL_HANDLE;
    VkFence inFlight = VK_NULL_HANDLE;

    int active = 0;
    int renderPassActive = 0;
    int frameFirstScene = 0;
    uint32_t imageIndex = 0;
    float clearR = 0.02f, clearG = 0.04f, clearB = 0.08f;

    /* Pipeline PSX. */
    VkImage vramImage = VK_NULL_HANDLE;
    VkDeviceMemory vramMemory = VK_NULL_HANDLE;
    VkImageView vramView = VK_NULL_HANDLE;
    VkSampler vramSampler = VK_NULL_HANDLE;
    VkBuffer vramStaging = VK_NULL_HANDLE;
    VkDeviceMemory vramStagingMemory = VK_NULL_HANDLE;
    void* vramStagingMapped = nullptr;
    int vramInitialized = 0;

    VkBuffer vertexBuffer = VK_NULL_HANDLE;
    VkDeviceMemory vertexMemory = VK_NULL_HANDLE;
    void* vertexMapped = nullptr;

    VkBuffer blitBuffer = VK_NULL_HANDLE;
    VkDeviceMemory blitMemory = VK_NULL_HANDLE;
    void* blitMapped = nullptr;

    VkDescriptorSetLayout descriptorLayout = VK_NULL_HANDLE;
    VkDescriptorPool descriptorPool = VK_NULL_HANDLE;
    VkDescriptorSet descriptorSet = VK_NULL_HANDLE;
    VkPipelineLayout pipelineLayout = VK_NULL_HANDLE;
    VkShaderModule psxVert = VK_NULL_HANDLE;
    VkShaderModule psx4Frag = VK_NULL_HANDLE;
    VkShaderModule psx8Frag = VK_NULL_HANDLE;
    VkShaderModule psx16Frag = VK_NULL_HANDLE;
    VkShaderModule blitVert = VK_NULL_HANDLE;
    VkShaderModule blitFrag = VK_NULL_HANDLE;
    VkPipeline pipelines[VK_FORMATS][VK_BLENDS] = {};

    int currentFormat = 3;
    int currentBlend = 0;
    VkPipeline boundPipeline = VK_NULL_HANDLE;
    VkBuffer boundVertexBuffer = VK_NULL_HANDLE;

    float projection[16] = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1};
};

static VKState vk;
static int vk_inited = 0;


static VKAPI_ATTR VkBool32 VKAPI_CALL vk_debug_callback(
    VkDebugUtilsMessageSeverityFlagBitsEXT severity,
    VkDebugUtilsMessageTypeFlagsEXT type,
    const VkDebugUtilsMessengerCallbackDataEXT* data,
    void* user)
{
    (void)type; (void)user;
    if (severity >= VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT)
        std::fprintf(stderr, "[VKDBG] %s\n", data->pMessage);
    return VK_FALSE;
}

static bool vk_has_extension(const std::vector<VkExtensionProperties>& list, const char* name)
{
    for (const auto& e : list)
        if (std::strcmp(e.extensionName, name) == 0)
            return true;
    return false;
}

static uint32_t vk_find_memory_type(uint32_t typeBits, VkMemoryPropertyFlags props)
{
    VkPhysicalDeviceMemoryProperties mem;
    vkGetPhysicalDeviceMemoryProperties(vk.physical, &mem);
    for (uint32_t i = 0; i < mem.memoryTypeCount; i++)
        if ((typeBits & (1u << i)) && (mem.memoryTypes[i].propertyFlags & props) == props)
            return i;
    return 0;
}

static int vk_create_buffer(VkDeviceSize size, VkBufferUsageFlags usage,
                            VkBuffer* buffer, VkDeviceMemory* memory, void** mapped)
{
    VkBufferCreateInfo bi{};
    bi.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO;
    bi.size = size;
    bi.usage = usage;
    bi.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    VK_CHECK(vkCreateBuffer(vk.device, &bi, nullptr, buffer));

    VkMemoryRequirements req;
    vkGetBufferMemoryRequirements(vk.device, *buffer, &req);
    VkMemoryAllocateInfo ai{};
    ai.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
    ai.allocationSize = req.size;
    ai.memoryTypeIndex = vk_find_memory_type(req.memoryTypeBits,
                                             VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT |
                                             VK_MEMORY_PROPERTY_HOST_COHERENT_BIT);
    VK_CHECK(vkAllocateMemory(vk.device, &ai, nullptr, memory));
    VK_CHECK(vkBindBufferMemory(vk.device, *buffer, *memory, 0));
    if (mapped)
        VK_CHECK(vkMapMemory(vk.device, *memory, 0, VK_WHOLE_SIZE, 0, mapped));
    return 1;
}

static void vk_image_barrier(VkCommandBuffer cb, VkImage image,
                             VkImageLayout oldLayout, VkImageLayout newLayout,
                             VkPipelineStageFlags srcStage, VkPipelineStageFlags dstStage,
                             VkAccessFlags srcAccess, VkAccessFlags dstAccess)
{
    VkImageMemoryBarrier b{};
    b.sType = VK_STRUCTURE_TYPE_IMAGE_MEMORY_BARRIER;
    b.oldLayout = oldLayout;
    b.newLayout = newLayout;
    b.srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
    b.dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED;
    b.image = image;
    b.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    b.subresourceRange.baseMipLevel = 0;
    b.subresourceRange.levelCount = 1;
    b.subresourceRange.baseArrayLayer = 0;
    b.subresourceRange.layerCount = 1;
    b.srcAccessMask = srcAccess;
    b.dstAccessMask = dstAccess;
    vkCmdPipelineBarrier(cb, srcStage, dstStage, 0, 0, nullptr, 0, nullptr, 1, &b);
}

static VkShaderModule vk_shader_module(const uint32_t* code, size_t bytes)
{
    VkShaderModuleCreateInfo ci{};
    ci.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    ci.codeSize = bytes;
    ci.pCode = code;
    VkShaderModule module;
    if (vkCreateShaderModule(vk.device, &ci, nullptr, &module) != VK_SUCCESS)
        return VK_NULL_HANDLE;
    return module;
}

static VkPipeline vk_create_pipeline(int format, int blend, VkShaderModule vert, VkShaderModule frag)
{
    VkPipelineShaderStageCreateInfo stages[2]{};
    stages[0].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[0].stage = VK_SHADER_STAGE_VERTEX_BIT;
    stages[0].module = vert;
    stages[0].pName = "main";
    stages[1].sType = VK_STRUCTURE_TYPE_PIPELINE_SHADER_STAGE_CREATE_INFO;
    stages[1].stage = VK_SHADER_STAGE_FRAGMENT_BIT;
    stages[1].module = frag;
    stages[1].pName = "main";

    VkVertexInputBindingDescription binding{};
    binding.binding = 0;
    binding.stride = sizeof(Vertex);
    binding.inputRate = VK_VERTEX_INPUT_RATE_VERTEX;

    VkVertexInputAttributeDescription attrs[3]{};
    attrs[0].location = 0;
    attrs[0].binding = 0;
    attrs[0].format = VK_FORMAT_R16G16B16A16_SINT;
    attrs[0].offset = 0;
    attrs[1].location = 1;
    attrs[1].binding = 0;
    attrs[1].format = VK_FORMAT_R8G8B8A8_UINT;
    attrs[1].offset = 8;
    attrs[2].location = 2;
    attrs[2].binding = 0;
    attrs[2].format = VK_FORMAT_R8G8B8A8_UNORM;
    attrs[2].offset = 12;

    VkPipelineVertexInputStateCreateInfo vin{};
    vin.sType = VK_STRUCTURE_TYPE_PIPELINE_VERTEX_INPUT_STATE_CREATE_INFO;
    vin.vertexBindingDescriptionCount = 1;
    vin.pVertexBindingDescriptions = &binding;
    vin.vertexAttributeDescriptionCount = 3;
    vin.pVertexAttributeDescriptions = attrs;

    VkPipelineInputAssemblyStateCreateInfo ia{};
    ia.sType = VK_STRUCTURE_TYPE_PIPELINE_INPUT_ASSEMBLY_STATE_CREATE_INFO;
    ia.topology = VK_PRIMITIVE_TOPOLOGY_TRIANGLE_LIST;

    VkPipelineViewportStateCreateInfo vp{};
    vp.sType = VK_STRUCTURE_TYPE_PIPELINE_VIEWPORT_STATE_CREATE_INFO;
    vp.viewportCount = 1;
    vp.scissorCount = 1;

    VkDynamicState dyn[] = { VK_DYNAMIC_STATE_VIEWPORT, VK_DYNAMIC_STATE_SCISSOR };
    VkPipelineDynamicStateCreateInfo ds{};
    ds.sType = VK_STRUCTURE_TYPE_PIPELINE_DYNAMIC_STATE_CREATE_INFO;
    ds.dynamicStateCount = 2;
    ds.pDynamicStates = dyn;

    VkPipelineRasterizationStateCreateInfo rs{};
    rs.sType = VK_STRUCTURE_TYPE_PIPELINE_RASTERIZATION_STATE_CREATE_INFO;
    rs.polygonMode = VK_POLYGON_MODE_FILL;
    rs.cullMode = VK_CULL_MODE_NONE;
    rs.frontFace = VK_FRONT_FACE_COUNTER_CLOCKWISE;
    rs.lineWidth = 1.0f;

    VkPipelineMultisampleStateCreateInfo ms{};
    ms.sType = VK_STRUCTURE_TYPE_PIPELINE_MULTISAMPLE_STATE_CREATE_INFO;
    ms.rasterizationSamples = VK_SAMPLE_COUNT_1_BIT;

    VkPipelineColorBlendAttachmentState cb{};
    cb.colorWriteMask = VK_COLOR_COMPONENT_R_BIT | VK_COLOR_COMPONENT_G_BIT |
                        VK_COLOR_COMPONENT_B_BIT | VK_COLOR_COMPONENT_A_BIT;
    cb.blendEnable = (blend != 0) ? VK_TRUE : VK_FALSE;
    switch (blend)
    {
    case 1: /* BM_AVERAGE */
        cb.srcColorBlendFactor = VK_BLEND_FACTOR_CONSTANT_COLOR;
        cb.dstColorBlendFactor = VK_BLEND_FACTOR_CONSTANT_COLOR;
        cb.srcAlphaBlendFactor = VK_BLEND_FACTOR_CONSTANT_ALPHA;
        cb.dstAlphaBlendFactor = VK_BLEND_FACTOR_CONSTANT_ALPHA;
        cb.colorBlendOp = VK_BLEND_OP_ADD;
        cb.alphaBlendOp = VK_BLEND_OP_ADD;
        break;
    case 2: /* BM_ADD */
        cb.srcColorBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.dstColorBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.colorBlendOp = VK_BLEND_OP_ADD;
        cb.alphaBlendOp = VK_BLEND_OP_ADD;
        break;
    case 3: /* BM_SUBTRACT */
        cb.srcColorBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.dstColorBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.srcAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.colorBlendOp = VK_BLEND_OP_REVERSE_SUBTRACT;
        cb.alphaBlendOp = VK_BLEND_OP_REVERSE_SUBTRACT;
        break;
    case 4: /* BM_ADD_QUATER_SOURCE */
        cb.srcColorBlendFactor = VK_BLEND_FACTOR_CONSTANT_ALPHA;
        cb.dstColorBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.srcAlphaBlendFactor = VK_BLEND_FACTOR_CONSTANT_ALPHA;
        cb.dstAlphaBlendFactor = VK_BLEND_FACTOR_ONE;
        cb.colorBlendOp = VK_BLEND_OP_ADD;
        cb.alphaBlendOp = VK_BLEND_OP_ADD;
        break;
    default:
        break;
    }

    VkPipelineColorBlendStateCreateInfo cbs{};
    cbs.sType = VK_STRUCTURE_TYPE_PIPELINE_COLOR_BLEND_STATE_CREATE_INFO;
    cbs.attachmentCount = 1;
    cbs.pAttachments = &cb;
    cbs.blendConstants[0] = 0.5f;
    cbs.blendConstants[1] = 0.5f;
    cbs.blendConstants[2] = 0.5f;
    cbs.blendConstants[3] = 0.25f;

    VkGraphicsPipelineCreateInfo pci{};
    pci.sType = VK_STRUCTURE_TYPE_GRAPHICS_PIPELINE_CREATE_INFO;
    pci.stageCount = 2;
    pci.pStages = stages;
    pci.pVertexInputState = &vin;
    pci.pInputAssemblyState = &ia;
    pci.pViewportState = &vp;
    pci.pRasterizationState = &rs;
    pci.pMultisampleState = &ms;
    pci.pColorBlendState = &cbs;
    pci.pDynamicState = &ds;
    pci.layout = vk.pipelineLayout;
    pci.renderPass = vk.renderPass;
    pci.subpass = 0;

    VkPipeline pipeline = VK_NULL_HANDLE;
    if (vkCreateGraphicsPipelines(vk.device, VK_NULL_HANDLE, 1, &pci, nullptr, &pipeline) != VK_SUCCESS)
    {
        std::fprintf(stderr, "[VK] pipeline create failed (format %d blend %d)\n", format, blend);
        return VK_NULL_HANDLE;
    }
    return pipeline;
}

static int vk_create_psx_resources()
{
    /* VRAM 1024x512 RG8 (les mots PSX 16 bits sont vus comme deux octets). */
    VkImageCreateInfo ici{};
    ici.sType = VK_STRUCTURE_TYPE_IMAGE_CREATE_INFO;
    ici.imageType = VK_IMAGE_TYPE_2D;
    ici.format = VK_FORMAT_R8G8_UNORM;
    ici.extent = {1024, 512, 1};
    ici.mipLevels = 1;
    ici.arrayLayers = 1;
    ici.samples = VK_SAMPLE_COUNT_1_BIT;
    ici.tiling = VK_IMAGE_TILING_OPTIMAL;
    ici.usage = VK_IMAGE_USAGE_SAMPLED_BIT | VK_IMAGE_USAGE_TRANSFER_DST_BIT;
    ici.sharingMode = VK_SHARING_MODE_EXCLUSIVE;
    ici.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
    VK_CHECK(vkCreateImage(vk.device, &ici, nullptr, &vk.vramImage));

    VkMemoryRequirements req;
    vkGetImageMemoryRequirements(vk.device, vk.vramImage, &req);
    VkMemoryAllocateInfo ai{};
    ai.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO;
    ai.allocationSize = req.size;
    ai.memoryTypeIndex = vk_find_memory_type(req.memoryTypeBits, VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT);
    VK_CHECK(vkAllocateMemory(vk.device, &ai, nullptr, &vk.vramMemory));
    VK_CHECK(vkBindImageMemory(vk.device, vk.vramImage, vk.vramMemory, 0));

    VkImageViewCreateInfo vci{};
    vci.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
    vci.image = vk.vramImage;
    vci.viewType = VK_IMAGE_VIEW_TYPE_2D;
    vci.format = VK_FORMAT_R8G8_UNORM;
    vci.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    vci.subresourceRange.levelCount = 1;
    vci.subresourceRange.layerCount = 1;
    VK_CHECK(vkCreateImageView(vk.device, &vci, nullptr, &vk.vramView));

    VkSamplerCreateInfo sci{};
    sci.sType = VK_STRUCTURE_TYPE_SAMPLER_CREATE_INFO;
    sci.magFilter = VK_FILTER_NEAREST;
    sci.minFilter = VK_FILTER_NEAREST;
    sci.mipmapMode = VK_SAMPLER_MIPMAP_MODE_NEAREST;
    sci.addressModeU = VK_SAMPLER_ADDRESS_MODE_REPEAT;
    sci.addressModeV = VK_SAMPLER_ADDRESS_MODE_REPEAT;
    sci.addressModeW = VK_SAMPLER_ADDRESS_MODE_REPEAT;
    VK_CHECK(vkCreateSampler(vk.device, &sci, nullptr, &vk.vramSampler));

    if (!vk_create_buffer(1024 * 512 * 2, VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                          &vk.vramStaging, &vk.vramStagingMemory, &vk.vramStagingMapped))
        return 0;
    if (!vk_create_buffer(sizeof(Vertex) * MAX_NUM_POLY_BUFFER_VERTICES,
                          VK_BUFFER_USAGE_VERTEX_BUFFER_BIT | VK_BUFFER_USAGE_TRANSFER_DST_BIT,
                          &vk.vertexBuffer, &vk.vertexMemory, &vk.vertexMapped))
        return 0;
    if (!vk_create_buffer(sizeof(Vertex) * 6, VK_BUFFER_USAGE_VERTEX_BUFFER_BIT,
                          &vk.blitBuffer, &vk.blitMemory, &vk.blitMapped))
        return 0;

    VkDescriptorSetLayoutBinding bind{};
    bind.binding = 0;
    bind.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    bind.descriptorCount = 1;
    bind.stageFlags = VK_SHADER_STAGE_FRAGMENT_BIT;
    VkDescriptorSetLayoutCreateInfo dl{};
    dl.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_LAYOUT_CREATE_INFO;
    dl.bindingCount = 1;
    dl.pBindings = &bind;
    VK_CHECK(vkCreateDescriptorSetLayout(vk.device, &dl, nullptr, &vk.descriptorLayout));

    VkDescriptorPoolSize ps{};
    ps.type = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    ps.descriptorCount = 1;
    VkDescriptorPoolCreateInfo dp{};
    dp.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
    dp.maxSets = 1;
    dp.poolSizeCount = 1;
    dp.pPoolSizes = &ps;
    VK_CHECK(vkCreateDescriptorPool(vk.device, &dp, nullptr, &vk.descriptorPool));

    VkDescriptorSetAllocateInfo dsa{};
    dsa.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_SET_ALLOCATE_INFO;
    dsa.descriptorPool = vk.descriptorPool;
    dsa.descriptorSetCount = 1;
    dsa.pSetLayouts = &vk.descriptorLayout;
    VK_CHECK(vkAllocateDescriptorSets(vk.device, &dsa, &vk.descriptorSet));

    VkDescriptorImageInfo dii{};
    dii.sampler = vk.vramSampler;
    dii.imageView = vk.vramView;
    dii.imageLayout = VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL;
    VkWriteDescriptorSet wds{};
    wds.sType = VK_STRUCTURE_TYPE_WRITE_DESCRIPTOR_SET;
    wds.dstSet = vk.descriptorSet;
    wds.dstBinding = 0;
    wds.descriptorCount = 1;
    wds.descriptorType = VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER;
    wds.pImageInfo = &dii;
    vkUpdateDescriptorSets(vk.device, 1, &wds, 0, nullptr);

    VkPushConstantRange pcr{};
    pcr.stageFlags = VK_SHADER_STAGE_VERTEX_BIT;
    pcr.offset = 0;
    pcr.size = 64;
    VkPipelineLayoutCreateInfo pl{};
    pl.sType = VK_STRUCTURE_TYPE_PIPELINE_LAYOUT_CREATE_INFO;
    pl.setLayoutCount = 1;
    pl.pSetLayouts = &vk.descriptorLayout;
    pl.pushConstantRangeCount = 1;
    pl.pPushConstantRanges = &pcr;
    VK_CHECK(vkCreatePipelineLayout(vk.device, &pl, nullptr, &vk.pipelineLayout));

    vk.psxVert = vk_shader_module(psx_vert_spv, sizeof(psx_vert_spv));
    vk.psx4Frag = vk_shader_module(psx4_frag_spv, sizeof(psx4_frag_spv));
    vk.psx8Frag = vk_shader_module(psx8_frag_spv, sizeof(psx8_frag_spv));
    vk.psx16Frag = vk_shader_module(psx16_frag_spv, sizeof(psx16_frag_spv));
    vk.blitVert = vk_shader_module(blit_vert_spv, sizeof(blit_vert_spv));
    vk.blitFrag = vk_shader_module(blit_frag_spv, sizeof(blit_frag_spv));

    if (!vk.psxVert || !vk.psx4Frag || !vk.psx8Frag || !vk.psx16Frag || !vk.blitVert || !vk.blitFrag)
    {
        std::fprintf(stderr, "[VK] shader module creation failed\n");
        return 0;
    }

    for (int blend = 0; blend < VK_BLENDS; blend++)
    {
        vk.pipelines[0][blend] = vk_create_pipeline(0, blend, vk.blitVert, vk.blitFrag);
        vk.pipelines[1][blend] = vk_create_pipeline(1, blend, vk.psxVert, vk.psx4Frag);
        vk.pipelines[2][blend] = vk_create_pipeline(2, blend, vk.psxVert, vk.psx8Frag);
        vk.pipelines[3][blend] = vk_create_pipeline(3, blend, vk.psxVert, vk.psx16Frag);
    }

    return 1;
}

static void vk_destroy_swapchain()
{
    for (VkFramebuffer fb : vk.framebuffers)
        vkDestroyFramebuffer(vk.device, fb, nullptr);
    vk.framebuffers.clear();
    for (VkImageView v : vk.views)
        vkDestroyImageView(vk.device, v, nullptr);
    vk.views.clear();
    if (vk.renderPass)
    {
        vkDestroyRenderPass(vk.device, vk.renderPass, nullptr);
        vk.renderPass = VK_NULL_HANDLE;
    }
    if (vk.swapchain)
    {
        vkDestroySwapchainKHR(vk.device, vk.swapchain, nullptr);
        vk.swapchain = VK_NULL_HANDLE;
    }
}

int RendererVK_Init(SDL_Window* window)
{
    if (vk_inited)
        return 1;

    vk.window = window;
    if (SDL_Vulkan_LoadLibrary(nullptr) != 0)
    {
        std::fprintf(stderr, "[VK] SDL_Vulkan_LoadLibrary: %s\n", SDL_GetError());
        return 0;
    }

    unsigned int extCount = 0;
    SDL_Vulkan_GetInstanceExtensions(window, &extCount, nullptr);
    std::vector<const char*> extensions(extCount);
    SDL_Vulkan_GetInstanceExtensions(window, &extCount, extensions.data());

    VkApplicationInfo app{};
    app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app.pApplicationName = "TOMB5 Vulkan";
    app.apiVersion = VK_API_VERSION_1_1;

    int debug = getenv("TOMB5_VK_DEBUG") != NULL;
    const char* layers[] = { "VK_LAYER_KHRONOS_validation" };
    if (debug)
    {
        extensions.push_back(VK_EXT_DEBUG_UTILS_EXTENSION_NAME);
    }

    VkInstanceCreateInfo ici{};
    ici.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    ici.pApplicationInfo = &app;
    ici.enabledExtensionCount = (uint32_t)extensions.size();
    ici.ppEnabledExtensionNames = extensions.data();
    if (debug)
    {
        ici.enabledLayerCount = 1;
        ici.ppEnabledLayerNames = layers;
    }
    if (vkCreateInstance(&ici, nullptr, &vk.instance) != VK_SUCCESS)
    {
        std::fprintf(stderr, "[VK] vkCreateInstance failed\n");
        return 0;
    }

    if (debug)
    {
        PFN_vkCreateDebugUtilsMessengerEXT create =
            (PFN_vkCreateDebugUtilsMessengerEXT)vkGetInstanceProcAddr(vk.instance, "vkCreateDebugUtilsMessengerEXT");
        if (create)
        {
            VkDebugUtilsMessengerCreateInfoEXT dci{};
            dci.sType = VK_STRUCTURE_TYPE_DEBUG_UTILS_MESSENGER_CREATE_INFO_EXT;
            dci.messageSeverity = VK_DEBUG_UTILS_MESSAGE_SEVERITY_WARNING_BIT_EXT |
                                  VK_DEBUG_UTILS_MESSAGE_SEVERITY_ERROR_BIT_EXT;
            dci.messageType = VK_DEBUG_UTILS_MESSAGE_TYPE_GENERAL_BIT_EXT |
                              VK_DEBUG_UTILS_MESSAGE_TYPE_VALIDATION_BIT_EXT |
                              VK_DEBUG_UTILS_MESSAGE_TYPE_PERFORMANCE_BIT_EXT;
            dci.pfnUserCallback = vk_debug_callback;
            create(vk.instance, &dci, nullptr, &vk.debugMessenger);
        }
    }

    if (!SDL_Vulkan_CreateSurface(window, vk.instance, &vk.surface))
    {
        std::fprintf(stderr, "[VK] SDL_Vulkan_CreateSurface: %s\n", SDL_GetError());
        return 0;
    }

    uint32_t count = 0;
    vkEnumeratePhysicalDevices(vk.instance, &count, nullptr);
    if (count == 0)
    {
        std::fprintf(stderr, "[VK] no physical device\n");
        return 0;
    }
    std::vector<VkPhysicalDevice> devices(count);
    vkEnumeratePhysicalDevices(vk.instance, &count, devices.data());
    vk.physical = devices[0];

    uint32_t devExtCount = 0;
    vkEnumerateDeviceExtensionProperties(vk.physical, nullptr, &devExtCount, nullptr);
    std::vector<VkExtensionProperties> devExts(devExtCount);
    vkEnumerateDeviceExtensionProperties(vk.physical, nullptr, &devExtCount, devExts.data());
    if (!vk_has_extension(devExts, VK_KHR_SWAPCHAIN_EXTENSION_NAME))
    {
        std::fprintf(stderr, "[VK] missing VK_KHR_swapchain\n");
        return 0;
    }

    uint32_t familyCount = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(vk.physical, &familyCount, nullptr);
    std::vector<VkQueueFamilyProperties> families(familyCount);
    vkGetPhysicalDeviceQueueFamilyProperties(vk.physical, &familyCount, families.data());
    int chosen = -1;
    for (uint32_t i = 0; i < familyCount; ++i)
    {
        VkBool32 present = VK_FALSE;
        vkGetPhysicalDeviceSurfaceSupportKHR(vk.physical, i, vk.surface, &present);
        if ((families[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) && present)
        {
            chosen = (int)i;
            break;
        }
    }
    if (chosen < 0)
    {
        std::fprintf(stderr, "[VK] no graphics/present queue\n");
        return 0;
    }
    vk.queueFamily = (uint32_t)chosen;

    float priority = 1.0f;
    VkDeviceQueueCreateInfo qci{};
    qci.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    qci.queueFamilyIndex = vk.queueFamily;
    qci.queueCount = 1;
    qci.pQueuePriorities = &priority;

    const char* devExt[] = { VK_KHR_SWAPCHAIN_EXTENSION_NAME };
    VkDeviceCreateInfo dci{};
    dci.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
    dci.queueCreateInfoCount = 1;
    dci.pQueueCreateInfos = &qci;
    dci.enabledExtensionCount = 1;
    dci.ppEnabledExtensionNames = devExt;
    if (vkCreateDevice(vk.physical, &dci, nullptr, &vk.device) != VK_SUCCESS)
    {
        std::fprintf(stderr, "[VK] vkCreateDevice failed\n");
        return 0;
    }
    vkGetDeviceQueue(vk.device, vk.queueFamily, 0, &vk.queue);

    uint32_t formatCount = 0;
    vkGetPhysicalDeviceSurfaceFormatsKHR(vk.physical, vk.surface, &formatCount, nullptr);
    std::vector<VkSurfaceFormatKHR> formats(formatCount);
    vkGetPhysicalDeviceSurfaceFormatsKHR(vk.physical, vk.surface, &formatCount, formats.data());
    VkSurfaceFormatKHR surfaceFormat = formats[0];
    for (const auto& f : formats)
        if (f.format == VK_FORMAT_B8G8R8A8_UNORM || f.format == VK_FORMAT_B8G8R8A8_SRGB)
        {
            surfaceFormat = f;
            break;
        }
    vk.format = surfaceFormat.format;

    VkSurfaceCapabilitiesKHR caps{};
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(vk.physical, vk.surface, &caps);
    vk.extent = caps.currentExtent;
    if (vk.extent.width == 0xFFFFFFFFu)
        vk.extent = {640, 480};

    uint32_t imageCount = caps.minImageCount + 1;
    if (caps.maxImageCount > 0 && imageCount > caps.maxImageCount)
        imageCount = caps.maxImageCount;

    VkSwapchainCreateInfoKHR sci{};
    sci.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
    sci.surface = vk.surface;
    sci.minImageCount = imageCount;
    sci.imageFormat = surfaceFormat.format;
    sci.imageColorSpace = surfaceFormat.colorSpace;
    sci.imageExtent = vk.extent;
    sci.imageArrayLayers = 1;
    sci.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
    sci.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
    sci.preTransform = caps.currentTransform;
    sci.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
    sci.presentMode = VK_PRESENT_MODE_FIFO_KHR;
    sci.clipped = VK_TRUE;
    if (vkCreateSwapchainKHR(vk.device, &sci, nullptr, &vk.swapchain) != VK_SUCCESS)
    {
        std::fprintf(stderr, "[VK] vkCreateSwapchainKHR failed\n");
        return 0;
    }

    uint32_t actual = 0;
    vkGetSwapchainImagesKHR(vk.device, vk.swapchain, &actual, nullptr);
    vk.images.resize(actual);
    vkGetSwapchainImagesKHR(vk.device, vk.swapchain, &actual, vk.images.data());

    for (VkImage image : vk.images)
    {
        VkImageViewCreateInfo vci{};
        vci.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
        vci.image = image;
        vci.viewType = VK_IMAGE_VIEW_TYPE_2D;
        vci.format = vk.format;
        vci.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        vci.subresourceRange.levelCount = 1;
        vci.subresourceRange.layerCount = 1;
        VkImageView view;
        VK_CHECK(vkCreateImageView(vk.device, &vci, nullptr, &view));
        vk.views.push_back(view);
    }

    VkAttachmentDescription color{};
    color.format = vk.format;
    color.samples = VK_SAMPLE_COUNT_1_BIT;
    color.loadOp = VK_ATTACHMENT_LOAD_OP_LOAD;
    color.storeOp = VK_ATTACHMENT_STORE_OP_STORE;
    color.stencilLoadOp = VK_ATTACHMENT_LOAD_OP_DONT_CARE;
    color.stencilStoreOp = VK_ATTACHMENT_STORE_OP_DONT_CARE;
    color.initialLayout = VK_IMAGE_LAYOUT_UNDEFINED;
    color.finalLayout = VK_IMAGE_LAYOUT_PRESENT_SRC_KHR;

    VkAttachmentReference colorRef{0, VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL};
    VkSubpassDescription subpass{};
    subpass.pipelineBindPoint = VK_PIPELINE_BIND_POINT_GRAPHICS;
    subpass.colorAttachmentCount = 1;
    subpass.pColorAttachments = &colorRef;

    VkSubpassDependency dep{};
    dep.srcSubpass = VK_SUBPASS_EXTERNAL;
    dep.dstSubpass = 0;
    dep.srcStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
    dep.dstStageMask = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
    dep.dstAccessMask = VK_ACCESS_COLOR_ATTACHMENT_WRITE_BIT;

    VkRenderPassCreateInfo rpci{};
    rpci.sType = VK_STRUCTURE_TYPE_RENDER_PASS_CREATE_INFO;
    rpci.attachmentCount = 1;
    rpci.pAttachments = &color;
    rpci.subpassCount = 1;
    rpci.pSubpasses = &subpass;
    rpci.dependencyCount = 1;
    rpci.pDependencies = &dep;
    VK_CHECK(vkCreateRenderPass(vk.device, &rpci, nullptr, &vk.renderPass));

    for (VkImageView view : vk.views)
    {
        VkFramebufferCreateInfo fci{};
        fci.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
        fci.renderPass = vk.renderPass;
        fci.attachmentCount = 1;
        fci.pAttachments = &view;
        fci.width = vk.extent.width;
        fci.height = vk.extent.height;
        fci.layers = 1;
        VkFramebuffer fb;
        VK_CHECK(vkCreateFramebuffer(vk.device, &fci, nullptr, &fb));
        vk.framebuffers.push_back(fb);
    }

    VkCommandPoolCreateInfo pci{};
    pci.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
    pci.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
    pci.queueFamilyIndex = vk.queueFamily;
    VK_CHECK(vkCreateCommandPool(vk.device, &pci, nullptr, &vk.commandPool));

    vk.commandBuffers.resize(vk.framebuffers.size());
    VkCommandBufferAllocateInfo cbi{};
    cbi.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    cbi.commandPool = vk.commandPool;
    cbi.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    cbi.commandBufferCount = (uint32_t)vk.commandBuffers.size();
    VK_CHECK(vkAllocateCommandBuffers(vk.device, &cbi, vk.commandBuffers.data()));

    VkSemaphoreCreateInfo semci{};
    semci.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
    VkFenceCreateInfo fci{};
    fci.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
    fci.flags = VK_FENCE_CREATE_SIGNALED_BIT;
    VK_CHECK(vkCreateSemaphore(vk.device, &semci, nullptr, &vk.imageAvailable));
    VK_CHECK(vkCreateSemaphore(vk.device, &semci, nullptr, &vk.renderFinished));
    VK_CHECK(vkCreateFence(vk.device, &fci, nullptr, &vk.inFlight));

    if (!vk_create_psx_resources())
    {
        std::fprintf(stderr, "[VK] PSX resources failed\n");
        return 0;
    }

    vk_inited = 1;
    vk.active = 0;
    std::fprintf(stderr, "[VK] backend ready: %ux%u, %u images\n",
                 vk.extent.width, vk.extent.height, actual);
    return 1;
}

void RendererVK_Shutdown()
{
    if (!vk_inited)
        return;
    vkDeviceWaitIdle(vk.device);

    for (int f = 0; f < VK_FORMATS; f++)
        for (int b = 0; b < VK_BLENDS; b++)
            if (vk.pipelines[f][b])
                vkDestroyPipeline(vk.device, vk.pipelines[f][b], nullptr);

    vkDestroyShaderModule(vk.device, vk.psxVert, nullptr);
    vkDestroyShaderModule(vk.device, vk.psx4Frag, nullptr);
    vkDestroyShaderModule(vk.device, vk.psx8Frag, nullptr);
    vkDestroyShaderModule(vk.device, vk.psx16Frag, nullptr);
    vkDestroyShaderModule(vk.device, vk.blitVert, nullptr);
    vkDestroyShaderModule(vk.device, vk.blitFrag, nullptr);
    vkDestroyPipelineLayout(vk.device, vk.pipelineLayout, nullptr);
    vkDestroyDescriptorPool(vk.device, vk.descriptorPool, nullptr);
    vkDestroyDescriptorSetLayout(vk.device, vk.descriptorLayout, nullptr);
    vkDestroyBuffer(vk.device, vk.blitBuffer, nullptr);
    vkFreeMemory(vk.device, vk.blitMemory, nullptr);
    vkDestroyBuffer(vk.device, vk.vertexBuffer, nullptr);
    vkFreeMemory(vk.device, vk.vertexMemory, nullptr);
    vkDestroyBuffer(vk.device, vk.vramStaging, nullptr);
    vkFreeMemory(vk.device, vk.vramStagingMemory, nullptr);
    vkDestroySampler(vk.device, vk.vramSampler, nullptr);
    vkDestroyImageView(vk.device, vk.vramView, nullptr);
    vkDestroyImage(vk.device, vk.vramImage, nullptr);
    vkFreeMemory(vk.device, vk.vramMemory, nullptr);

    vk_destroy_swapchain();
    vkDestroyFence(vk.device, vk.inFlight, nullptr);
    vkDestroySemaphore(vk.device, vk.renderFinished, nullptr);
    vkDestroySemaphore(vk.device, vk.imageAvailable, nullptr);
    vkDestroyCommandPool(vk.device, vk.commandPool, nullptr);
    vkDestroyDevice(vk.device, nullptr);
    if (vk.debugMessenger)
    {
        PFN_vkDestroyDebugUtilsMessengerEXT destroy =
            (PFN_vkDestroyDebugUtilsMessengerEXT)vkGetInstanceProcAddr(vk.instance, "vkDestroyDebugUtilsMessengerEXT");
        if (destroy)
            destroy(vk.instance, vk.debugMessenger, nullptr);
        vk.debugMessenger = VK_NULL_HANDLE;
    }
    vkDestroySurfaceKHR(vk.instance, vk.surface, nullptr);
    vkDestroyInstance(vk.instance, nullptr);
    vk.device = VK_NULL_HANDLE;
    vk_inited = 0;
}

static void vk_upload_vram(VkCommandBuffer cb)
{
    memcpy(vk.vramStagingMapped, vram, 1024 * 512 * 2);

    {
        VkMemoryBarrier mb{};
        mb.sType = VK_STRUCTURE_TYPE_MEMORY_BARRIER;
        mb.srcAccessMask = VK_ACCESS_HOST_WRITE_BIT;
        mb.dstAccessMask = VK_ACCESS_TRANSFER_READ_BIT;
        vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_HOST_BIT,
                             VK_PIPELINE_STAGE_TRANSFER_BIT, 0,
                             1, &mb, 0, nullptr, 0, nullptr);
    }

    if (!vk.vramInitialized)
    {
        vk_image_barrier(cb, vk.vramImage, VK_IMAGE_LAYOUT_UNDEFINED,
                         VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                         VK_PIPELINE_STAGE_TOP_OF_PIPE_BIT,
                         VK_PIPELINE_STAGE_TRANSFER_BIT, 0,
                         VK_ACCESS_TRANSFER_WRITE_BIT);
    }
    else
    {
        vk_image_barrier(cb, vk.vramImage, VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
                         VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                         VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT,
                         VK_PIPELINE_STAGE_TRANSFER_BIT,
                         VK_ACCESS_SHADER_READ_BIT,
                         VK_ACCESS_TRANSFER_WRITE_BIT);
    }

    VkBufferImageCopy copy{};
    copy.imageSubresource.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
    copy.imageSubresource.layerCount = 1;
    copy.imageExtent = {1024, 512, 1};
    vkCmdCopyBufferToImage(cb, vk.vramStaging, vk.vramImage,
                           VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL, 1, &copy);

    vk_image_barrier(cb, vk.vramImage, VK_IMAGE_LAYOUT_TRANSFER_DST_OPTIMAL,
                     VK_IMAGE_LAYOUT_SHADER_READ_ONLY_OPTIMAL,
                     VK_PIPELINE_STAGE_TRANSFER_BIT,
                     VK_PIPELINE_STAGE_FRAGMENT_SHADER_BIT,
                     VK_ACCESS_TRANSFER_WRITE_BIT,
                     VK_ACCESS_SHADER_READ_BIT);
    vk.vramInitialized = 1;
}

static void vk_begin_render_pass(VkCommandBuffer cb)
{
    if (getenv("TOMB5_VK_TRI") != NULL)
    {
        Vertex tri[3] =
        {
            { 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 0, 255 },
            { 1024, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0, 255 },
            { 0, 480, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255 },
        };
        memcpy(vk.blitMapped, tri, sizeof(tri));
        VkMemoryBarrier mb{};
        mb.sType = VK_STRUCTURE_TYPE_MEMORY_BARRIER;
        mb.srcAccessMask = VK_ACCESS_HOST_WRITE_BIT;
        mb.dstAccessMask = VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT;
        vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_HOST_BIT,
                             VK_PIPELINE_STAGE_VERTEX_INPUT_BIT, 0,
                             1, &mb, 0, nullptr, 0, nullptr);
    }

    VkClearValue clear{};
    {
        float cr = vk.clearR, cg = vk.clearG, cbcol = vk.clearB;
        if (getenv("TOMB5_VK_CLEAR") != NULL)
        {
            cr = 0.20f; cg = 0.45f; cbcol = 0.85f;
        }
        clear.color = {{cr, cg, cbcol, 1.0f}};
    }
    VkRenderPassBeginInfo rbi{};
    rbi.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
    rbi.renderPass = vk.renderPass;
    rbi.framebuffer = vk.framebuffers[vk.imageIndex];
    rbi.renderArea.extent = vk.extent;
    rbi.clearValueCount = 1;
    rbi.pClearValues = &clear;
    vkCmdBeginRenderPass(cb, &rbi, VK_SUBPASS_CONTENTS_INLINE);
    vk.renderPassActive = 1;

    if (vk.frameFirstScene)
    {
        VkClearAttachment att{};
        att.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        att.colorAttachment = 0;
        att.clearValue.color = clear.color;
        VkClearRect rect{};
        rect.rect = {{0, 0}, vk.extent};
        rect.layerCount = 1;
        vkCmdClearAttachments(cb, 1, &att, 1, &rect);
        vk.frameFirstScene = 0;
    }

    VkViewport viewport{0, 0, (float)vk.extent.width, (float)vk.extent.height, 0.0f, 1.0f};
    VkRect2D scissor{{0, 0}, vk.extent};
    vkCmdSetViewport(cb, 0, 1, &viewport);
    vkCmdSetScissor(cb, 0, 1, &scissor);

    vkCmdBindDescriptorSets(cb, VK_PIPELINE_BIND_POINT_GRAPHICS, vk.pipelineLayout,
                            0, 1, &vk.descriptorSet, 0, nullptr);

    float w = (float)activeDispEnv.disp.w;
    float h = (float)activeDispEnv.disp.h;
    float a = 2.0f / w;
    float b = -2.0f / h;
    float c = -2.0f;
    float x = -1.0f;
    float y = 1.0f;
    float z = -1.0f;
    float proj[16] = {a, 0, 0, 0, 0, b, 0, 0, 0, 0, c, 0, x, y, z, 1};
    memcpy(vk.projection, proj, sizeof(proj));

    /* Un pipeline doit etre lie avant vkCmdPushConstants (meme layout). */
    VkPipeline initial = vk.pipelines[3][0];
    if (!initial)
        initial = vk.pipelines[1][0];
    if (initial)
    {
        vkCmdBindPipeline(cb, VK_PIPELINE_BIND_POINT_GRAPHICS, initial);
        vk.boundPipeline = initial;
    }
    vkCmdPushConstants(cb, vk.pipelineLayout, VK_SHADER_STAGE_VERTEX_BIT, 0, 64, vk.projection);

    vk.boundVertexBuffer = VK_NULL_HANDLE;

    if (getenv("TOMB5_VK_TRI") != NULL)
    {
        VkDeviceSize off = 0;
        vkCmdBindVertexBuffers(cb, 0, 1, &vk.blitBuffer, &off);
        vkCmdDraw(cb, 3, 1, 0, 0);
    }

    if (getenv("TOMB5_VK_DEBUG") != NULL)
    {
        static int dbg_proj = 0;
        if ((dbg_proj++ % 30) == 0)
            std::fprintf(stderr, "[VK] disp=%dx%d proj a=%.6f b=%.6f\n",
                         activeDispEnv.disp.w, activeDispEnv.disp.h, a, b);
    }
}

static void RendererVK_BeginFrame()
{
    if (!vk_inited || vk.active)
        return;

    vkWaitForFences(vk.device, 1, &vk.inFlight, VK_TRUE, UINT64_MAX);
    vkResetFences(vk.device, 1, &vk.inFlight);

    VkResult acquire = vkAcquireNextImageKHR(vk.device, vk.swapchain, UINT64_MAX,
                                             vk.imageAvailable, VK_NULL_HANDLE, &vk.imageIndex);
    if (acquire == VK_ERROR_OUT_OF_DATE_KHR)
        return;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    vkResetCommandBuffer(cb, 0);
    VkCommandBufferBeginInfo bi{};
    bi.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    vkBeginCommandBuffer(cb, &bi);

    vk_upload_vram(cb);

    vk.renderPassActive = 0;
    vk.frameFirstScene = 1;
    vk.active = 1;

    {
        static int dbg_frames = 0;
        if (getenv("TOMB5_VK_DEBUG") != NULL && (dbg_frames++ % 30) == 0)
            std::fprintf(stderr, "[VK] frame %d extent=%ux%u\n", dbg_frames, vk.extent.width, vk.extent.height);
    }
}
static void RendererVK_EndFrame()
{
    if (!vk_inited || !vk.active)
        return;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    if (vk.renderPassActive)
    {
        vkCmdEndRenderPass(cb);
        vk.renderPassActive = 0;
    }
    vkEndCommandBuffer(cb);

    VkPipelineStageFlags waitStage = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
    VkSubmitInfo si{};
    si.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
    si.waitSemaphoreCount = 1;
    si.pWaitSemaphores = &vk.imageAvailable;
    si.pWaitDstStageMask = &waitStage;
    si.commandBufferCount = 1;
    si.pCommandBuffers = &cb;
    si.signalSemaphoreCount = 1;
    si.pSignalSemaphores = &vk.renderFinished;
    VkResult submit = vkQueueSubmit(vk.queue, 1, &si, vk.inFlight);
    if (submit != VK_SUCCESS)
        std::fprintf(stderr, "[VK] vkQueueSubmit failed: %d\n", (int)submit);

    VkPresentInfoKHR pi{};
    pi.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
    pi.waitSemaphoreCount = 1;
    pi.pWaitSemaphores = &vk.renderFinished;
    pi.swapchainCount = 1;
    pi.pSwapchains = &vk.swapchain;
    pi.pImageIndices = &vk.imageIndex;
    VkResult present = vkQueuePresentKHR(vk.queue, &pi);
    if (present != VK_SUCCESS && present != VK_SUBOPTIMAL_KHR)
        std::fprintf(stderr, "[VK] vkQueuePresentKHR failed: %d\n", (int)present);

    vk.active = 0;
}

static void RendererVK_UpdateVRAM()
{
    /* L'upload est fait dans BeginScene. */
}

static void RendererVK_BlitVRAM()
{
    /* Le blit VRAM sera porte apres le pipeline 3D. */
    if (!vk.active)
        return;
    return;

    u_char l = activeDispEnv.disp.x / 8;
    u_char t = activeDispEnv.disp.y / 8;
    u_char r = activeDispEnv.disp.w / 8 + l;
    u_char b = activeDispEnv.disp.h / 8 + t;

    Vertex blit[6] =
    {
        { +1, +1, 0, 0, r, t, 0, 0, 0, 0, 0, 0 },
        { -1, -1, 0, 0, l, b, 0, 0, 0, 0, 0, 0 },
        { -1, +1, 0, 0, l, t, 0, 0, 0, 0, 0, 0 },
        { +1, -1, 0, 0, r, b, 0, 0, 0, 0, 0, 0 },
        { -1, -1, 0, 0, l, b, 0, 0, 0, 0, 0, 0 },
        { +1, +1, 0, 0, r, t, 0, 0, 0, 0, 0, 0 },
    };
    memcpy(vk.blitMapped, blit, sizeof(blit));

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    {
        VkMemoryBarrier mb{};
        mb.sType = VK_STRUCTURE_TYPE_MEMORY_BARRIER;
        mb.srcAccessMask = VK_ACCESS_HOST_WRITE_BIT;
        mb.dstAccessMask = VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT;
        vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_HOST_BIT,
                             VK_PIPELINE_STAGE_VERTEX_INPUT_BIT, 0,
                             1, &mb, 0, nullptr, 0, nullptr);
    }
    VkPipeline pipe = vk.pipelines[0][0];
    if (pipe)
    {
        vkCmdBindPipeline(cb, VK_PIPELINE_BIND_POINT_GRAPHICS, pipe);
        VkDeviceSize offset = 0;
        vkCmdBindVertexBuffers(cb, 0, 1, &vk.blitBuffer, &offset);
        vkCmdDraw(cb, 6, 1, 0, 0);
    }
    vk.boundPipeline = VK_NULL_HANDLE;
    vk.boundVertexBuffer = VK_NULL_HANDLE;
}

static void RendererVK_Clear(int x, int y, int w, int h, unsigned char r, unsigned char g, unsigned char b)
{
    vk.clearR = r / 255.0f;
    vk.clearG = g / 255.0f;
    vk.clearB = b / 255.0f;
}

static void RendererVK_CopyVRAM(unsigned short* src, int x, int y, int w, int h, int dst_x, int dst_y) {}
static void RendererVK_ReadVRAM(unsigned short* dst, int x, int y, int dst_w, int dst_h) {}

static void RendererVK_SetTexture(TextureID texture, TexFormat texFormat)
{
    switch (texFormat)
    {
    case TF_4_BIT: vk.currentFormat = 1; break;
    case TF_8_BIT: vk.currentFormat = 2; break;
    case TF_16_BIT: vk.currentFormat = 3; break;
    default: vk.currentFormat = 3; break;
    }
}

static void RendererVK_SetBlendMode(BlendMode blendMode)
{
    int b = (int)blendMode;
    if (b < 0 || b >= VK_BLENDS)
        b = 0;
    vk.currentBlend = b;
}

static void RendererVK_UpdateVertexBuffer(const Vertex* vertices, int count)
{
    if (!vk.active || vertices == nullptr || count <= 0)
        return;

    size_t bytes = (size_t)count * sizeof(Vertex);
    if (bytes > sizeof(Vertex) * MAX_NUM_POLY_BUFFER_VERTICES)
        bytes = sizeof(Vertex) * MAX_NUM_POLY_BUFFER_VERTICES;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    const char* src = (const char*)vertices;
    size_t off = 0;
    while (off < bytes)
    {
        size_t chunk = bytes - off;
        if (chunk > 65536)
            chunk = 65536;
        chunk &= ~(size_t)3; /* vkCmdUpdateBuffer exige un multiple de 4 */
        if (chunk == 0)
            break;
        vkCmdUpdateBuffer(cb, vk.vertexBuffer, (VkDeviceSize)off, (VkDeviceSize)chunk, src + off);
        off += chunk;
    }

    VkMemoryBarrier mb{};
    mb.sType = VK_STRUCTURE_TYPE_MEMORY_BARRIER;
    mb.srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT;
    mb.dstAccessMask = VK_ACCESS_VERTEX_ATTRIBUTE_READ_BIT;
    vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_TRANSFER_BIT,
                         VK_PIPELINE_STAGE_VERTEX_INPUT_BIT, 0,
                         1, &mb, 0, nullptr, 0, nullptr);

    {
        static int dbg_vb = 0;
        if (getenv("TOMB5_VK_DEBUG") != NULL && (dbg_vb++ % 120) == 0)
            std::fprintf(stderr, "[VK] vertex update count=%d bytes=%zu\n", count, bytes);
    }
}

static void RendererVK_DrawTriangles(int start_vertex, int triangles)
{
    if (!vk.active || triangles <= 0)
        return;

    int f = vk.currentFormat;
    int b = vk.currentBlend;
    if (f < 1 || f >= VK_FORMATS)
        f = 3;
    if (b < 0 || b >= VK_BLENDS)
        b = 0;

    VkPipeline pipe = vk.pipelines[f][b];
    if (!pipe)
        return;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    if (!vk.renderPassActive)
        vk_begin_render_pass(cb);

    if (getenv("TOMB5_VK_TRI_ONLY") != NULL)
        return;

    if (pipe != vk.boundPipeline)
    {
        vkCmdBindPipeline(cb, VK_PIPELINE_BIND_POINT_GRAPHICS, pipe);
        vk.boundPipeline = pipe;
    }
    if (vk.boundVertexBuffer != vk.vertexBuffer)
    {
        VkDeviceSize offset = 0;
        vkCmdBindVertexBuffers(cb, 0, 1, &vk.vertexBuffer, &offset);
        vk.boundVertexBuffer = vk.vertexBuffer;
    }
    vkCmdDraw(cb, (uint32_t)(triangles * 3), 1, (uint32_t)start_vertex, 0);

    {
        static int dbg_draw = 0;
        static int dbg_tris = 0;
        dbg_tris += triangles;
        if (getenv("TOMB5_VK_DEBUG") != NULL && (dbg_draw++ % 120) == 0)
            std::fprintf(stderr, "[VK] draw start=%d tris=%d total=%d fmt=%d blend=%d\n",
                         start_vertex, triangles, dbg_tris, f, b);
    }
}

static int RendererVK_BeginScene()
{
    /* Une seule passe par frame : begin_frame/end_frame. */
    return 0;
}

static void RendererVK_EndScene()
{
    if (!vk_inited || !vk.active || !vk.renderPassActive)
        return;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    vkCmdEndRenderPass(cb);
    vk.renderPassActive = 0;
    vk.boundPipeline = VK_NULL_HANDLE;
    vk.boundVertexBuffer = VK_NULL_HANDLE;
}

static const RendererBackend vk_backend =
{
    RendererVK_BeginFrame,
    RendererVK_EndFrame,
    RendererVK_BeginScene,
    RendererVK_EndScene,
    RendererVK_BlitVRAM,
    RendererVK_UpdateVRAM,
    RendererVK_Clear,
    RendererVK_CopyVRAM,
    RendererVK_ReadVRAM,
    RendererVK_SetTexture,
    RendererVK_SetBlendMode,
    RendererVK_UpdateVertexBuffer,
    RendererVK_DrawTriangles,
};

extern const RendererBackend* g_renderer;

int RendererVK_Select(SDL_Window* window)
{
    if (!RendererVK_Init(window))
        return 0;
    g_renderer = &vk_backend;
    return 1;
}

int RendererVK_IsActive()
{
    return vk_inited;
}

#else /* !LP64 || !HAVE_VULKAN */

#include <SDL2/SDL.h>

int RendererVK_Init(SDL_Window* window) { (void)window; return 0; }
void RendererVK_Shutdown() {}
int RendererVK_Select(SDL_Window* window) { (void)window; return 0; }
int RendererVK_IsActive() { return 0; }

#endif
