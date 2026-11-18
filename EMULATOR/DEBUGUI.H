#ifndef DEBUGUI_H
#define DEBUGUI_H

/*
 * Overlay de debug (RMIG-013).
 *
 * L'overlay est compile dans le build 64 bits (Vulkan) et active par F12.
 * Les statistiques de jeu sont remplies par le code qui les connait
 * (DRAWPHAS pour la camera/Lara, le backend pour les compteurs de rendu) ;
 * l'overlay ne fait que les afficher.
 */

struct DebugUIStats
{
	int level;
	int room;
	int rooms;
	int posX;
	int posY;
	int posZ;
	int anim;
	int frame;
	int verts;
	int tris;
	int draws;
	int splits;
};

extern DebugUIStats g_debugui_stats;

/* Interrupteurs de debug (agissent immediatement sur le backend Vulkan). */
extern int g_debugui_dither;        /* 1 = dithering PSX, 0 = desactive */
extern int g_port_force_texfmt;     /* -1 = normal, sinon 4 / 8 / 16 bits */
extern int g_debugui_reflections;   /* 0 = aucun, 1..3 = intensite des reflets */

#if defined(HAVE_IMGUI) && defined(HAVE_VULKAN)

struct SDL_Window;
union SDL_Event;
struct VkInstance_T;
struct VkPhysicalDevice_T;
struct VkDevice_T;
struct VkQueue_T;
struct VkRenderPass_T;
struct VkCommandBuffer_T;

typedef struct VkInstance_T* VkInstance;
typedef struct VkPhysicalDevice_T* VkPhysicalDevice;
typedef struct VkDevice_T* VkDevice;
typedef struct VkQueue_T* VkQueue;
typedef struct VkRenderPass_T* VkRenderPass;
typedef struct VkCommandBuffer_T* VkCommandBuffer;

int  DebugUI_Init(SDL_Window* window, VkInstance instance, VkPhysicalDevice physical,
                  VkDevice device, VkQueue queue, unsigned int queueFamily,
                  VkRenderPass renderPass, unsigned int imageCount);
void DebugUI_Shutdown(void);

/* A appeler une fois par frame, avant le debut du render pass. */
void DebugUI_NewFrame(void);
/* A appeler dans le render pass, juste avant vkCmdEndRenderPass. */
void DebugUI_Render(VkCommandBuffer commandBuffer);

/* Traite un evenement SDL ; renvoie 1 si l'overlay l'a consomme. */
int  DebugUI_ProcessEvent(const union SDL_Event* event);

void DebugUI_Toggle(void);
int  DebugUI_IsVisible(void);

#else

#define DebugUI_Init(a, b, c, d, e, f, g, h) (0)
#define DebugUI_Shutdown()
#define DebugUI_NewFrame()
#define DebugUI_Render(a)
#define DebugUI_ProcessEvent(a) (0)
#define DebugUI_Toggle()
#define DebugUI_IsVisible() (0)

#endif

#endif
