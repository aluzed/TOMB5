/*
 * Overlay de debug ImGui (RMIG-013).
 *
 * Backend Vulkan uniquement (build 64 bits). L'overlay affiche l'etat de jeu
 * (niveau, salle, position de Lara, animation) et les compteurs de rendu de
 * la frame, et sert de point d'ancrage aux futurs interrupteurs (reflets SSR,
 * raytracing, budget de perf).
 */

#include "DEBUGUI.H"

/* Definition commune aux deux builds : DRAWPHAS ecrit toujours dedans. */
DebugUIStats g_debugui_stats = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

int g_debugui_dither = 1;
/* g_port_force_texfmt est defini dans LIBGPU.C (voir DEBUGUI.H). */

#if defined(HAVE_IMGUI) && defined(HAVE_VULKAN)

#include <SDL2/SDL.h>
#include <vulkan/vulkan.h>

#include <imgui.h>
#include <imgui_impl_sdl2.h>
#include <imgui_impl_vulkan.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>

static struct
{
	int          initialized;
	int          visible;
	SDL_Window*  window;
	VkDevice     device;
	VkDescriptorPool descriptorPool;
	unsigned int frameCount;
	unsigned int lastTicks;
	float        fps;
	char         capturePath[512];
	char         status[128];
	int          statusFrames;
} ui;

static void DebugUI_BuildWindow(void)
{
	ImGui::SetNextWindowPos(ImVec2(8, 8), ImGuiCond_Once);
	ImGui::SetNextWindowSize(ImVec2(300, 0), ImGuiCond_Once);
	ImGui::Begin("TOMB5 debug (F12)");

	ImGui::Text("Renderer : Vulkan (64 bits)");
	ImGui::Text("%.1f FPS  (%.2f ms)", ui.fps, ui.fps > 0.0f ? 1000.0f / ui.fps : 0.0f);
	ImGui::Separator();

	ImGui::Text("Niveau %d  salle %d / %d", g_debugui_stats.level,
	            g_debugui_stats.room, g_debugui_stats.rooms);
	ImGui::Text("Lara  pos=(%d, %d, %d)", g_debugui_stats.posX,
	            g_debugui_stats.posY, g_debugui_stats.posZ);
	ImGui::Text("Anim %d  frame %d", g_debugui_stats.anim, g_debugui_stats.frame);
	ImGui::Separator();

	ImGui::Text("Vertices %d", g_debugui_stats.verts);
	ImGui::Text("Triangles %d", g_debugui_stats.tris);
	ImGui::Text("Draws %d  splits %d", g_debugui_stats.draws, g_debugui_stats.splits);
	ImGui::Separator();
	ImGui::Text("Reglages");

	/* Boutons plutot que cases a cocher : cibles larges, et l'etat est
	 * lisible dans le libelle. */
	if (ImGui::Button(g_debugui_dither ? "Dithering : ON" : "Dithering : OFF", ImVec2(-1, 0)))
	{
		g_debugui_dither = g_debugui_dither ? 0 : 1;
		if (getenv("TOMB5_IMGUI_DEBUG") != NULL)
			std::fprintf(stderr, "[IMGUI] dither=%d\n", g_debugui_dither);
	}

	ImGui::TextDisabled("Profondeur de texture");
	const char* fmtLabels[4] = { "normal", "4 bits", "8 bits", "16 bits" };
	for (int i = 0; i < 4; i++)
	{
		if (i > 0)
			ImGui::SameLine();
		bool active = (i == 0 && g_port_force_texfmt < 0) ||
		              (i == 1 && g_port_force_texfmt == 4) ||
		              (i == 2 && g_port_force_texfmt == 8) ||
		              (i == 3 && g_port_force_texfmt == 16);
		if (active)
			ImGui::PushStyleColor(ImGuiCol_Button, ImVec4(0.26f, 0.59f, 0.98f, 0.75f));
		if (ImGui::Button(fmtLabels[i], ImVec2(68, 0)))
		{
			if (i == 0) g_port_force_texfmt = -1;
			else if (i == 1) g_port_force_texfmt = 4;
			else if (i == 2) g_port_force_texfmt = 8;
			else g_port_force_texfmt = 16;
			if (getenv("TOMB5_IMGUI_DEBUG") != NULL)
				std::fprintf(stderr, "[IMGUI] texfmt=%d\n", g_port_force_texfmt);
		}
		if (active)
			ImGui::PopStyleColor();
	}

	if (getenv("TOMB5_IMGUI_DEBUG") != NULL && ui.frameCount % 120 == 0)
	{
		ImGuiIO& dbgio = ImGui::GetIO();
		std::fprintf(stderr, "[IMGUI] mouse=(%.0f,%.0f) down=%d hovered_win=%d\n",
		             dbgio.MousePos.x, dbgio.MousePos.y, (int)dbgio.MouseDown[0],
		             (int)ImGui::IsWindowHovered(ImGuiHoveredFlags_ChildWindows));
	}

	ImGui::Separator();

	ImGui::Text("Capture BMP");
	ImGui::SetNextItemWidth(-60);
	ImGui::InputText("##path", ui.capturePath, sizeof(ui.capturePath));
	ImGui::SameLine();
	if (ImGui::Button("Capture", ImVec2(-1, 0)))
	{
		extern void Emulator_SetScreenshotPath(const char* path);
		extern void Emulator_RequestScreenshot(void);
		Emulator_SetScreenshotPath(ui.capturePath);
		Emulator_RequestScreenshot();
		std::snprintf(ui.status, sizeof(ui.status), "capture demandee : %s", ui.capturePath);
		ui.statusFrames = 120;
	}

	if (ui.statusFrames > 0)
	{
		ui.statusFrames--;
		ImGui::TextWrapped("%s", ui.status);
	}

	ImGui::Separator();
	ImGui::TextDisabled("Reflets SSR / raytracing : RMIG-014/015");
	ImGui::End();
}

int DebugUI_Init(SDL_Window* window, VkInstance instance, VkPhysicalDevice physical,
                 VkDevice device, VkQueue queue, unsigned int queueFamily,
                 VkRenderPass renderPass, unsigned int imageCount)
{
	if (ui.initialized)
		return 1;

	if (instance == VK_NULL_HANDLE || device == VK_NULL_HANDLE || renderPass == VK_NULL_HANDLE)
		return 0;

	IMGUI_CHECKVERSION();
	ImGui::CreateContext();
	ImGuiIO& io = ImGui::GetIO();
	io.IniFilename = nullptr;   /* pas de fichier imgui.ini dans le dossier du jeu */
	io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
	ImGui::StyleColorsDark();

	if (!ImGui_ImplSDL2_InitForVulkan(window))
	{
		std::fprintf(stderr, "[IMGUI] ImGui_ImplSDL2_InitForVulkan a echoue\n");
		return 0;
	}

	VkDescriptorPoolSize poolSizes[] = {
		{ VK_DESCRIPTOR_TYPE_COMBINED_IMAGE_SAMPLER, 64 },
	};
	VkDescriptorPoolCreateInfo poolInfo{};
	poolInfo.sType = VK_STRUCTURE_TYPE_DESCRIPTOR_POOL_CREATE_INFO;
	poolInfo.flags = VK_DESCRIPTOR_POOL_CREATE_FREE_DESCRIPTOR_SET_BIT;
	poolInfo.maxSets = 64;
	poolInfo.poolSizeCount = 1;
	poolInfo.pPoolSizes = poolSizes;
	if (vkCreateDescriptorPool(device, &poolInfo, nullptr, &ui.descriptorPool) != VK_SUCCESS)
	{
		std::fprintf(stderr, "[IMGUI] descriptor pool creation failed\n");
		return 0;
	}

	ImGui_ImplVulkan_InitInfo initInfo{};
	initInfo.Instance = instance;
	initInfo.PhysicalDevice = physical;
	initInfo.Device = device;
	initInfo.QueueFamily = queueFamily;
	initInfo.Queue = queue;
	initInfo.DescriptorPool = ui.descriptorPool;
	initInfo.RenderPass = renderPass;
	initInfo.MinImageCount = imageCount >= 2 ? imageCount : 2;
	initInfo.ImageCount = imageCount;
	initInfo.MSAASamples = VK_SAMPLE_COUNT_1_BIT;

	if (!ImGui_ImplVulkan_Init(&initInfo))
	{
		std::fprintf(stderr, "[IMGUI] ImGui_ImplVulkan_Init a echoue\n");
		return 0;
	}

	if (!ImGui_ImplVulkan_CreateFontsTexture())
	{
		std::fprintf(stderr, "[IMGUI] creation de la texture de police impossible\n");
		return 0;
	}

	ui.window = window;
	ui.device = device;
	ui.initialized = 1;
	ui.visible = 0;
	ui.lastTicks = SDL_GetTicks();
	ui.statusFrames = 0;
	std::snprintf(ui.capturePath, sizeof(ui.capturePath), "/tmp/tomb5_capture.bmp");

	std::fprintf(stderr, "[IMGUI] overlay pret (F12)\n");
	return 1;
}

void DebugUI_Shutdown(void)
{
	if (!ui.initialized)
		return;

	ImGui_ImplVulkan_Shutdown();
	ImGui_ImplSDL2_Shutdown();
	ImGui::DestroyContext();

	if (ui.descriptorPool != VK_NULL_HANDLE)
	{
		vkDestroyDescriptorPool(ui.device, ui.descriptorPool, nullptr);
		ui.descriptorPool = VK_NULL_HANDLE;
	}

	ui.initialized = 0;
	ui.visible = 0;
}

void DebugUI_NewFrame(void)
{
	if (!ui.initialized)
		return;

	unsigned int now = SDL_GetTicks();
	unsigned int delta = now - ui.lastTicks;
	ui.lastTicks = now;

	ui.frameCount++;
	if (delta > 0)
	{
		float instant = 1000.0f / (float)delta;
		ui.fps = (ui.fps <= 0.0f) ? instant : (ui.fps * 0.9f + instant * 0.1f);
	}

	ImGui_ImplVulkan_NewFrame();
	ImGui_ImplSDL2_NewFrame();
	ImGui::NewFrame();

	if (ui.visible)
		DebugUI_BuildWindow();
}

void DebugUI_Render(VkCommandBuffer commandBuffer)
{
	if (!ui.initialized)
		return;

	/* ImGui::Render() doit etre appele a chaque frame, meme si aucun render
	 * pass n'est ouvert (sinon l'assertion de sanity check se declenche). */
	ImGui::Render();

	if (commandBuffer == VK_NULL_HANDLE)
		return;

	ImDrawData* drawData = ImGui::GetDrawData();
	if (drawData != nullptr && drawData->CmdListsCount > 0)
		ImGui_ImplVulkan_RenderDrawData(drawData, commandBuffer);
}

int DebugUI_ProcessEvent(const union SDL_Event* event)
{
	if (!ui.initialized || event == nullptr)
		return 0;

	if (getenv("TOMB5_IMGUI_DEBUG") != NULL && event->type == SDL_MOUSEBUTTONDOWN)
	{
		ImGuiIO& dbgio = ImGui::GetIO();
		std::fprintf(stderr, "[IMGUI] clic (%d,%d) mouse=(%.0f,%.0f) capture_mouse=%d\n",
		             event->button.x, event->button.y,
		             dbgio.MousePos.x, dbgio.MousePos.y,
		             (int)dbgio.WantCaptureMouse);
	}

	ImGui_ImplSDL2_ProcessEvent(event);

	if (event->type == SDL_KEYDOWN && event->key.keysym.scancode == SDL_SCANCODE_F12)
	{
		DebugUI_Toggle();
		return 1;
	}

	return 0;
}

void DebugUI_Toggle(void)
{
	if (!ui.initialized)
		return;
	ui.visible = !ui.visible;
	std::fprintf(stderr, "[IMGUI] overlay %s\n", ui.visible ? "visible" : "masque");
}

int DebugUI_IsVisible(void)
{
	return ui.initialized && ui.visible;
}

#endif
