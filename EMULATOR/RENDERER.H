#ifndef RENDERER_H
#define RENDERER_H

#include "EMULATOR.H"

/*
 * Interface minimale consommee par l'emulation GPU PSX (LIBGPU.C).
 *
 * Le backend OpenGL actuel est adapte dans RENDERER_GL.C.  Un backend
 * Vulkan pourra implementer la meme structure sans toucher a LIBGPU.C ni
 * au jeu.  Les fonctions Emulator_Generate* (conversion des primitives)
 * restent communes : elles ne touchent pas a l'API graphique.
 */
typedef struct RendererBackend
{
	void (*begin_frame)(void);
	void (*end_frame)(void);
	int  (*begin_scene)(void);
	void (*end_scene)(void);
	void (*blit_vram)(void);
	void (*update_vram)(void);
	void (*clear)(int x, int y, int w, int h, unsigned char r, unsigned char g, unsigned char b);
	void (*copy_vram)(unsigned short* src, int x, int y, int w, int h, int dst_x, int dst_y);
	void (*read_vram)(unsigned short* dst, int x, int y, int dst_w, int dst_h);
	void (*set_texture)(TextureID texture, TexFormat texFormat);
	void (*set_blend_mode)(BlendMode blendMode);
	void (*update_vertex_buffer)(const Vertex* vertices, int count);
	void (*draw_triangles)(int start_vertex, int triangles);
} RendererBackend;

/*
 * Identifiants de texture logiques utilises par LIBGPU pour separer les
 * groupes de primitives (texture VRAM et texture blanche).  Le backend GL
 * fournit ses propres noms de texture ; le backend Vulkan n'en a pas besoin
 * mais doit garder des valeurs distinctes et stables.
 */
#define PORT_TEXTURE_WHITE 1u
#define PORT_TEXTURE_VRAM  2u

extern const RendererBackend* g_renderer;

/* Selectionne le backend OpenGL existant (defaut). */
void Renderer_SelectGL(void);

#endif
