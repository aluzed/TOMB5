/*
 * Backend Vulkan (RMIG-009/010, etape 1).
 *
 * Cette premiere etape branche une instance/device/swapchain Vulkan dans le
 * jeu et presente une image claire.  Les appels de geometrie PSX
 * (vertex buffer / triangles / textures) sont encore des no-op : ils seront
 * implementes dans RMIG-010/011.  Le backend GL reste le defaut ; il est
 * selectionne par TOMB5_RENDERER=vulkan.
 */

#include "RENDERER.H"

#if defined(__LP64__) && defined(HAVE_VULKAN)

#include <SDL2/SDL.h>
#include <SDL2/SDL_vulkan.h>
#include <vulkan/vulkan.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

#define VK_CHECK(x) do { VkResult r_ = (x); if (r_ != VK_SUCCESS) { \
    std::fprintf(stderr, "[VK] error %d at %s:%d\n", (int)r_, __FILE__, __LINE__); \
    return 0; } } while (0)

struct VKState
{
    SDL_Window* window = nullptr;
    VkInstance instance = VK_NULL_HANDLE;
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
    uint32_t imageIndex = 0;
    float clearR = 0.02f, clearG = 0.04f, clearB = 0.08f;
};

static VKState vk;
static int vk_inited = 0;

static bool vk_has_extension(const std::vector<VkExtensionProperties>& list, const char* name)
{
    for (const auto& e : list)
        if (std::strcmp(e.extensionName, name) == 0)
            return true;
    return false;
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

    VkInstanceCreateInfo ici{};
    ici.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    ici.pApplicationInfo = &app;
    ici.enabledExtensionCount = (uint32_t)extensions.size();
    ici.ppEnabledExtensionNames = extensions.data();
    if (vkCreateInstance(&ici, nullptr, &vk.instance) != VK_SUCCESS)
    {
        std::fprintf(stderr, "[VK] vkCreateInstance failed\n");
        return 0;
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
    color.loadOp = VK_ATTACHMENT_LOAD_OP_CLEAR;
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
    vk_destroy_swapchain();
    vkDestroyFence(vk.device, vk.inFlight, nullptr);
    vkDestroySemaphore(vk.device, vk.renderFinished, nullptr);
    vkDestroySemaphore(vk.device, vk.imageAvailable, nullptr);
    vkDestroyCommandPool(vk.device, vk.commandPool, nullptr);
    vkDestroyDevice(vk.device, nullptr);
    vkDestroySurfaceKHR(vk.instance, vk.surface, nullptr);
    vkDestroyInstance(vk.instance, nullptr);
    vk.device = VK_NULL_HANDLE;
    vk_inited = 0;
}

static int RendererVK_BeginScene()
{
    if (!vk_inited || vk.active)
        return 0;

    vkWaitForFences(vk.device, 1, &vk.inFlight, VK_TRUE, UINT64_MAX);
    vkResetFences(vk.device, 1, &vk.inFlight);

    VkResult acquire = vkAcquireNextImageKHR(vk.device, vk.swapchain, UINT64_MAX,
                                             vk.imageAvailable, VK_NULL_HANDLE, &vk.imageIndex);
    if (acquire == VK_ERROR_OUT_OF_DATE_KHR)
        return 0;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    vkResetCommandBuffer(cb, 0);
    VkCommandBufferBeginInfo bi{};
    bi.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
    vkBeginCommandBuffer(cb, &bi);

    VkClearValue clear{};
    {
        float cr = vk.clearR, cg = vk.clearG, cb = vk.clearB;
        if (getenv("TOMB5_VK_CLEAR") != NULL)
        {
            /* Couleur de test pour verifier la presentation sans le pipeline PSX. */
            cr = 0.20f; cg = 0.45f; cb = 0.85f;
        }
        clear.color = {{cr, cg, cb, 1.0f}};
    }
    VkRenderPassBeginInfo rbi{};
    rbi.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
    rbi.renderPass = vk.renderPass;
    rbi.framebuffer = vk.framebuffers[vk.imageIndex];
    rbi.renderArea.extent = vk.extent;
    rbi.clearValueCount = 1;
    rbi.pClearValues = &clear;
    vkCmdBeginRenderPass(cb, &rbi, VK_SUBPASS_CONTENTS_INLINE);

    vk.active = 1;
    return 1;
}

static void RendererVK_EndScene()
{
    if (!vk_inited || !vk.active)
        return;

    VkCommandBuffer cb = vk.commandBuffers[vk.imageIndex];
    vkCmdEndRenderPass(cb);
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

static void RendererVK_BlitVRAM() {}
static void RendererVK_UpdateVRAM() {}
static void RendererVK_Clear(int x, int y, int w, int h, unsigned char r, unsigned char g, unsigned char b)
{
    vk.clearR = r / 255.0f;
    vk.clearG = g / 255.0f;
    vk.clearB = b / 255.0f;
}
static void RendererVK_CopyVRAM(unsigned short* src, int x, int y, int w, int h, int dst_x, int dst_y) {}
static void RendererVK_ReadVRAM(unsigned short* dst, int x, int y, int dst_w, int dst_h) {}
static void RendererVK_SetTexture(TextureID texture, TexFormat texFormat) {}
static void RendererVK_SetBlendMode(BlendMode blendMode) {}
static void RendererVK_UpdateVertexBuffer(const Vertex* vertices, int count) {}
static void RendererVK_DrawTriangles(int start_vertex, int triangles) {}

static const RendererBackend vk_backend =
{
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
