#include "RENDERER.H"
#include "EMULATOR_PRIVATE.H"

/*
 * Adaptateur OpenGL : le code GL/D3D historique reste dans EMULATOR.C.
 * LIBGPU.C ne voit plus que cette interface.
 *
 * Dans le build 64 bits (PORT_VULKAN_ONLY) OpenGL n'est pas compile : ce
 * fichier ne fournit plus qu'un message explicite, aucun backend.
 */
#if defined(PORT_VULKAN_ONLY)

#include "RENDERER.H"
#include <stdio.h>

void Renderer_SelectGL(void)
{
	fprintf(stderr, "[RENDERER] OpenGL absent de ce build (Vulkan uniquement)\n");
}

#else

static void RendererGL_BeginFrame(void) {}
static void RendererGL_EndFrame(void) {}

static const RendererBackend gl_backend =
{
	RendererGL_BeginFrame,
	RendererGL_EndFrame,
	Emulator_BeginScene,
	Emulator_EndScene,
	Emulator_BlitVRAM,
	Emulator_UpdateVRAM,
	Emulator_Clear,
	Emulator_CopyVRAM,
	Emulator_ReadVRAM,
	Emulator_SetTexture,
	Emulator_SetBlendMode,
	Emulator_UpdateVertexBuffer,
	Emulator_DrawTriangles,
};

const RendererBackend* g_renderer = &gl_backend;

void Renderer_SelectGL(void)
{
	g_renderer = &gl_backend;
}

#endif /* !PORT_VULKAN_ONLY */
