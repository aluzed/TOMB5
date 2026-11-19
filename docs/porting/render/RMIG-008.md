# RMIG-008 — Abstraction renderer (interface + sélection)

Status: **Done** — priorité P1 — confiance Medium

Avancement : Terminé : l’interface `RendererBackend` (RENDERER.H) est la seule dépendance de LIBGPU.C ; le backend OpenGL (RENDERER_GL.C) n’existe plus que dans le build 32 bits, le build 64 bits est Vulkan uniquement et le sélectionne par défaut. Les appels GL ont disparu du build 64 bits (RMIG-012).

## Objectif

Isoler les neuf points d'entrée du rendu derrière une interface, pour brancher Vulkan sans toucher au jeu.

## Faits établis

Le rendu est déjà regroupé dans EMULATOR/EMULATOR.C (init, upload VRAM, vertex buffer, draw triangles, blending, swap) avec des #if OGL/D3D. Aucune abstraction commune n'existe.

## Périmètre

Interface renderer_* (init, frame begin/end, upload texture, update vertices, draw, blend, present) et implémentation OpenGL existante branchée dessus.

Hors périmètre : Vulkan lui-même.

## Tâches

- [ ] Définir l'interface et ses invariants (un draw par ordering table, pas de depth, blending PSX).
- [ ] Brancher l'implémentation OpenGL actuelle derrière l'interface sans changer le rendu.
- [ ] Vérifier la parité visuelle avec la référence RMIG-007.

## Critères d’acceptation

- Le jeu se comporte à l'identique via l'interface (capture identique à la référence).
- Aucun appel GL ne subsiste hors de l'implémentation du backend.

## Validation

Capture comparée + grep des appels GL hors backend.

## Inconnues

Fuites d'état GL (blend, scissor) entre passes.

## Estimation

1 à 2 jours-personne.

## Dépendances

- RMIG-002
- RMIG-007

## Preuves

- 2026-11-19 : Interface RendererBackend consommée par LIBGPU.C (begin/end frame et scene, blit, update_vram, clear, copy/read vram, set_texture, set_blend, update_vertex_buffer, draw_triangles). Build 64 bits : backend Vulkan par défaut, aucun symbole gl* ni libGL/GLEW (vérifié par nm/ldd). Build 32 bits : adaptateur OpenGL conservé comme référence (capture 51d3a1c7… inchangée). Sélection : TOMB5_RENDERER=gl explicitement refusé en 64 bits avec message, pas de repli silencieux.

## Références

- `EMULATOR/EMULATOR.C:3534` (Emulator_DrawTriangles)
- `EMULATOR/EMULATOR.C:2240` (texture VRAM)
