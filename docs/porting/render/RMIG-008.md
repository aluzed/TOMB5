# RMIG-008 — Abstraction renderer (interface + sélection)

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Interface RendererBackend introduite (EMULATOR/RENDERER.H) et adaptateur OpenGL (EMULATOR/RENDERER_GL.C). LIBGPU.C utilise g_renderer pour le chemin de draw (begin/end, blit, textures, blending, vertex buffer, triangles). Le capture déterministe RMIG-007 est resté identique après refactor : sha256 675e2c8d…. Reste : isoler le code GL hors de EMULATOR.C et ajouter la sélection Vulkan.

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

- 2026-11-18 : Interface RendererBackend + backend GL adaptateur. LIBGPU.C passe par g_renderer pour le chemin de rendu. Vérification : capture déterministe niveau 3/1800 frames après refactor = sha256 675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b, identique à la référence pré-refactor. Builds 32/64 verts, 4188 tests PASS. Les fonctions VRAM (CopyVRAM) restent appelées directement pour préserver le harnais de test existant.

## Références

- `EMULATOR/EMULATOR.C:3534` (Emulator_DrawTriangles)
- `EMULATOR/EMULATOR.C:2240` (texture VRAM)
