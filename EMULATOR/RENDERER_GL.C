#include "RENDERER.H"
#include "EMULATOR_PRIVATE.H"

/*
 * Adaptateur OpenGL : le code GL/D3D historique reste dans EMULATOR.C.
 * LIBGPU.C ne voit plus que cette interface.
 */
static const RendererBackend gl_backend =
{
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
