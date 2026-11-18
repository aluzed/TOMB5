/*
 * RMIG-009 smoke test: Vulkan instance, device, swapchain and presentation.
 *
 * Not part of the game build yet.  It opens an SDL2 window, creates a
 * swapchain through SDL_Vulkan_CreateSurface, clears the screen and
 * presents a number of frames.  This validates the loader/driver path and
 * provides the skeleton for EMULATOR/RENDERER_VK.C.
 *
 * Build:
 *   g++ -std=c++17 -O2 tools/vulkan_smoke.cpp -o /tmp/vulkan_smoke \
 *       $(sdl2-config --cflags --libs) -lvulkan
 */

#include <SDL2/SDL.h>
#include <SDL2/SDL_vulkan.h>
#include <vulkan/vulkan.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

#define VK_CHECK(x) do { VkResult r = (x); if (r != VK_SUCCESS) { \
    std::fprintf(stderr, "Vulkan error %d at %s:%d\n", (int)r, __FILE__, __LINE__); \
    std::exit(1); } } while (0)

struct Smoke
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
};

static bool has_extension(const std::vector<VkExtensionProperties>& list, const char* name)
{
    for (const auto& e : list)
        if (std::strcmp(e.extensionName, name) == 0)
            return true;
    return false;
}

int main()
{
    if (SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        std::fprintf(stderr, "SDL_Init: %s\n", SDL_GetError());
        return 1;
    }
    if (SDL_Vulkan_LoadLibrary(nullptr) != 0)
    {
        std::fprintf(stderr, "SDL_Vulkan_LoadLibrary: %s\n", SDL_GetError());
        return 1;
    }

    Smoke s;
    s.window = SDL_CreateWindow("Vulkan smoke (RMIG-009)", SDL_WINDOWPOS_CENTERED,
                                SDL_WINDOWPOS_CENTERED, 640, 480,
                                SDL_WINDOW_VULKAN | SDL_WINDOW_SHOWN);
    if (!s.window)
    {
        std::fprintf(stderr, "SDL_CreateWindow: %s\n", SDL_GetError());
        return 1;
    }

    unsigned int sdlExtCount = 0;
    SDL_Vulkan_GetInstanceExtensions(s.window, &sdlExtCount, nullptr);
    std::vector<const char*> extensions(sdlExtCount);
    SDL_Vulkan_GetInstanceExtensions(s.window, &sdlExtCount, extensions.data());

    VkApplicationInfo app{};
    app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app.pApplicationName = "TOMB5 Vulkan smoke";
    app.apiVersion = VK_API_VERSION_1_1;

    VkInstanceCreateInfo ici{};
    ici.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    ici.pApplicationInfo = &app;
    ici.enabledExtensionCount = (uint32_t)extensions.size();
    ici.ppEnabledExtensionNames = extensions.data();
    VK_CHECK(vkCreateInstance(&ici, nullptr, &s.instance));

    if (!SDL_Vulkan_CreateSurface(s.window, s.instance, &s.surface))
    {
        std::fprintf(stderr, "SDL_Vulkan_CreateSurface: %s\n", SDL_GetError());
        return 1;
    }

    uint32_t deviceCount = 0;
    vkEnumeratePhysicalDevices(s.instance, &deviceCount, nullptr);
    if (deviceCount == 0)
    {
        std::fprintf(stderr, "No Vulkan physical device\n");
        return 1;
    }
    std::vector<VkPhysicalDevice> devices(deviceCount);
    vkEnumeratePhysicalDevices(s.instance, &deviceCount, devices.data());

    uint32_t extCount = 0;
    vkEnumerateDeviceExtensionProperties(devices[0], nullptr, &extCount, nullptr);
    std::vector<VkExtensionProperties> devExts(extCount);
    vkEnumerateDeviceExtensionProperties(devices[0], nullptr, &extCount, devExts.data());
    if (!has_extension(devExts, VK_KHR_SWAPCHAIN_EXTENSION_NAME))
    {
        std::fprintf(stderr, "Device lacks VK_KHR_swapchain\n");
        return 1;
    }

    uint32_t familyCount = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(devices[0], &familyCount, nullptr);
    std::vector<VkQueueFamilyProperties> families(familyCount);
    vkGetPhysicalDeviceQueueFamilyProperties(devices[0], &familyCount, families.data());
    int chosen = -1;
    for (uint32_t i = 0; i < familyCount; ++i)
    {
        VkBool32 present = VK_FALSE;
        vkGetPhysicalDeviceSurfaceSupportKHR(devices[0], i, s.surface, &present);
        if ((families[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) && present)
        {
            chosen = (int)i;
            break;
        }
    }
    if (chosen < 0)
    {
        std::fprintf(stderr, "No graphics+present queue\n");
        return 1;
    }
    s.physical = devices[0];
    s.queueFamily = (uint32_t)chosen;

    float priority = 1.0f;
    VkDeviceQueueCreateInfo qci{};
    qci.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO;
    qci.queueFamilyIndex = s.queueFamily;
    qci.queueCount = 1;
    qci.pQueuePriorities = &priority;

    const char* devExt[] = { VK_KHR_SWAPCHAIN_EXTENSION_NAME };
    VkDeviceCreateInfo dci{};
    dci.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO;
    dci.queueCreateInfoCount = 1;
    dci.pQueueCreateInfos = &qci;
    dci.enabledExtensionCount = 1;
    dci.ppEnabledExtensionNames = devExt;
    VK_CHECK(vkCreateDevice(s.physical, &dci, nullptr, &s.device));
    vkGetDeviceQueue(s.device, s.queueFamily, 0, &s.queue);

    uint32_t formatCount = 0;
    vkGetPhysicalDeviceSurfaceFormatsKHR(s.physical, s.surface, &formatCount, nullptr);
    std::vector<VkSurfaceFormatKHR> formats(formatCount);
    vkGetPhysicalDeviceSurfaceFormatsKHR(s.physical, s.surface, &formatCount, formats.data());
    VkSurfaceFormatKHR surfaceFormat = formats[0];
    for (const auto& f : formats)
        if (f.format == VK_FORMAT_B8G8R8A8_UNORM || f.format == VK_FORMAT_B8G8R8A8_SRGB)
        {
            surfaceFormat = f;
            break;
        }
    s.format = surfaceFormat.format;

    VkSurfaceCapabilitiesKHR caps{};
    vkGetPhysicalDeviceSurfaceCapabilitiesKHR(s.physical, s.surface, &caps);
    s.extent = caps.currentExtent;
    if (s.extent.width == 0xFFFFFFFFu)
    {
        s.extent = {640, 480};
    }

    uint32_t imageCount = caps.minImageCount + 1;
    if (caps.maxImageCount > 0 && imageCount > caps.maxImageCount)
        imageCount = caps.maxImageCount;

    VkSwapchainCreateInfoKHR sci{};
    sci.sType = VK_STRUCTURE_TYPE_SWAPCHAIN_CREATE_INFO_KHR;
    sci.surface = s.surface;
    sci.minImageCount = imageCount;
    sci.imageFormat = surfaceFormat.format;
    sci.imageColorSpace = surfaceFormat.colorSpace;
    sci.imageExtent = s.extent;
    sci.imageArrayLayers = 1;
    sci.imageUsage = VK_IMAGE_USAGE_COLOR_ATTACHMENT_BIT;
    sci.imageSharingMode = VK_SHARING_MODE_EXCLUSIVE;
    sci.preTransform = caps.currentTransform;
    sci.compositeAlpha = VK_COMPOSITE_ALPHA_OPAQUE_BIT_KHR;
    sci.presentMode = VK_PRESENT_MODE_FIFO_KHR;
    sci.clipped = VK_TRUE;
    VK_CHECK(vkCreateSwapchainKHR(s.device, &sci, nullptr, &s.swapchain));

    uint32_t actualImages = 0;
    vkGetSwapchainImagesKHR(s.device, s.swapchain, &actualImages, nullptr);
    s.images.resize(actualImages);
    vkGetSwapchainImagesKHR(s.device, s.swapchain, &actualImages, s.images.data());

    for (VkImage image : s.images)
    {
        VkImageViewCreateInfo vci{};
        vci.sType = VK_STRUCTURE_TYPE_IMAGE_VIEW_CREATE_INFO;
        vci.image = image;
        vci.viewType = VK_IMAGE_VIEW_TYPE_2D;
        vci.format = s.format;
        vci.subresourceRange.aspectMask = VK_IMAGE_ASPECT_COLOR_BIT;
        vci.subresourceRange.levelCount = 1;
        vci.subresourceRange.layerCount = 1;
        VkImageView view;
        VK_CHECK(vkCreateImageView(s.device, &vci, nullptr, &view));
        s.views.push_back(view);
    }

    VkAttachmentDescription color{};
    color.format = s.format;
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
    VK_CHECK(vkCreateRenderPass(s.device, &rpci, nullptr, &s.renderPass));

    for (VkImageView view : s.views)
    {
        VkFramebufferCreateInfo fci{};
        fci.sType = VK_STRUCTURE_TYPE_FRAMEBUFFER_CREATE_INFO;
        fci.renderPass = s.renderPass;
        fci.attachmentCount = 1;
        fci.pAttachments = &view;
        fci.width = s.extent.width;
        fci.height = s.extent.height;
        fci.layers = 1;
        VkFramebuffer fb;
        VK_CHECK(vkCreateFramebuffer(s.device, &fci, nullptr, &fb));
        s.framebuffers.push_back(fb);
    }

    VkCommandPoolCreateInfo pci{};
    pci.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO;
    pci.flags = VK_COMMAND_POOL_CREATE_RESET_COMMAND_BUFFER_BIT;
    pci.queueFamilyIndex = s.queueFamily;
    VK_CHECK(vkCreateCommandPool(s.device, &pci, nullptr, &s.commandPool));

    s.commandBuffers.resize(s.framebuffers.size());
    VkCommandBufferAllocateInfo cbi{};
    cbi.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO;
    cbi.commandPool = s.commandPool;
    cbi.level = VK_COMMAND_BUFFER_LEVEL_PRIMARY;
    cbi.commandBufferCount = (uint32_t)s.commandBuffers.size();
    VK_CHECK(vkAllocateCommandBuffers(s.device, &cbi, s.commandBuffers.data()));

    for (size_t i = 0; i < s.commandBuffers.size(); ++i)
    {
        VkCommandBufferBeginInfo bi{};
        bi.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO;
        VK_CHECK(vkBeginCommandBuffer(s.commandBuffers[i], &bi));
        VkClearValue clear{};
        clear.color = {{0.05f + 0.02f * (float)i, 0.10f, 0.18f, 1.0f}};
        VkRenderPassBeginInfo rbi{};
        rbi.sType = VK_STRUCTURE_TYPE_RENDER_PASS_BEGIN_INFO;
        rbi.renderPass = s.renderPass;
        rbi.framebuffer = s.framebuffers[i];
        rbi.renderArea.extent = s.extent;
        rbi.clearValueCount = 1;
        rbi.pClearValues = &clear;
        vkCmdBeginRenderPass(s.commandBuffers[i], &rbi, VK_SUBPASS_CONTENTS_INLINE);
        vkCmdEndRenderPass(s.commandBuffers[i]);
        VK_CHECK(vkEndCommandBuffer(s.commandBuffers[i]));
    }

    VkSemaphoreCreateInfo semci{};
    semci.sType = VK_STRUCTURE_TYPE_SEMAPHORE_CREATE_INFO;
    VkFenceCreateInfo fci{};
    fci.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO;
    fci.flags = VK_FENCE_CREATE_SIGNALED_BIT;
    VK_CHECK(vkCreateSemaphore(s.device, &semci, nullptr, &s.imageAvailable));
    VK_CHECK(vkCreateSemaphore(s.device, &semci, nullptr, &s.renderFinished));
    VK_CHECK(vkCreateFence(s.device, &fci, nullptr, &s.inFlight));

    std::printf("[VK] instance/device/swapchain OK: %ux%u, %u images\n",
                s.extent.width, s.extent.height, actualImages);

    for (int frame = 0; frame < 60; ++frame)
    {
        vkWaitForFences(s.device, 1, &s.inFlight, VK_TRUE, UINT64_MAX);
        vkResetFences(s.device, 1, &s.inFlight);

        uint32_t index = 0;
        VkResult acquire = vkAcquireNextImageKHR(s.device, s.swapchain, UINT64_MAX,
                                                 s.imageAvailable, VK_NULL_HANDLE, &index);
        if (acquire == VK_ERROR_OUT_OF_DATE_KHR)
            break;

        VkPipelineStageFlags waitStage = VK_PIPELINE_STAGE_COLOR_ATTACHMENT_OUTPUT_BIT;
        VkSubmitInfo si{};
        si.sType = VK_STRUCTURE_TYPE_SUBMIT_INFO;
        si.waitSemaphoreCount = 1;
        si.pWaitSemaphores = &s.imageAvailable;
        si.pWaitDstStageMask = &waitStage;
        si.commandBufferCount = 1;
        si.pCommandBuffers = &s.commandBuffers[index];
        si.signalSemaphoreCount = 1;
        si.pSignalSemaphores = &s.renderFinished;
        VK_CHECK(vkQueueSubmit(s.queue, 1, &si, s.inFlight));

        VkPresentInfoKHR pi{};
        pi.sType = VK_STRUCTURE_TYPE_PRESENT_INFO_KHR;
        pi.waitSemaphoreCount = 1;
        pi.pWaitSemaphores = &s.renderFinished;
        pi.swapchainCount = 1;
        pi.pSwapchains = &s.swapchain;
        pi.pImageIndices = &index;
        VkResult present = vkQueuePresentKHR(s.queue, &pi);
        if (present == VK_ERROR_OUT_OF_DATE_KHR || present == VK_SUBOPTIMAL_KHR)
            break;

        SDL_PumpEvents();
        SDL_Event ev;
        while (SDL_PollEvent(&ev))
            if (ev.type == SDL_QUIT)
                frame = 1000;
    }

    vkDeviceWaitIdle(s.device);
    std::printf("[VK] presented, shutting down\n");

    vkDestroyFence(s.device, s.inFlight, nullptr);
    vkDestroySemaphore(s.device, s.renderFinished, nullptr);
    vkDestroySemaphore(s.device, s.imageAvailable, nullptr);
    vkDestroyCommandPool(s.device, s.commandPool, nullptr);
    for (VkFramebuffer fb : s.framebuffers)
        vkDestroyFramebuffer(s.device, fb, nullptr);
    vkDestroyRenderPass(s.device, s.renderPass, nullptr);
    for (VkImageView v : s.views)
        vkDestroyImageView(s.device, v, nullptr);
    vkDestroySwapchainKHR(s.device, s.swapchain, nullptr);
    vkDestroyDevice(s.device, nullptr);
    vkDestroySurfaceKHR(s.instance, s.surface, nullptr);
    vkDestroyInstance(s.instance, nullptr);
    SDL_DestroyWindow(s.window);
    SDL_Quit();
    return 0;
}
