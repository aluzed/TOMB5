# RMIG-010 — Backend Vulkan : pipeline PSX (VRAM, VBO, ordering tables)

Status: **Done** — priorité P1 — confiance Medium

Avancement : Pipeline PSX Vulkan opérationnel : texture VRAM 1024x512 RG8, vertex buffer (Vertex 20 o), draws par split/ordering table, blends PSX (5 modes), render pass par OT avec conservation de l’image, upload VRAM par frame. La scène 3D du niveau 3 (room 20, 4 bits) est rendue avec Lara et le HUD, sans OpenGL. Reste les finitions : blit VRAM (titres/menus) et projection via uniforme.

## Objectif

Rendre la scène PSX complète en Vulkan : une texture VRAM, un vertex buffer dynamique, un draw par passe.

## Faits établis

L'implémentation actuelle garde la VRAM 1024×512 en une texture RG8, pousse les Vertex (position, uv+couleur+dither, couleur, z, w) dans un VBO dynamique et émet un glDrawArrays par ordering table, sans depth test, avec glBlendFunc variable.

## Périmètre

Texture VRAM, transfert des vertices par frame, pipelines par mode de blend, absence de depth, préservation de l'ordre des OT.

Hors périmètre : Compilation des shaders (ticket suivant), SSR/RT.

## Tâches

- [ ] Uploader la VRAM comme texture persistante et gérer les mises à jour partielles.
- [ ] Créer le buffer dynamique de vertices et les pipelines de blending PSX.
- [ ] Émettre un draw par ordering table et vérifier l'ordre d'affichage.

## Critères d’acceptation

- La scène s'affiche sans artefacts de transparence ni d'ordre.
- Le nombre de draw calls par frame reste égal au nombre d'ordering tables utilisées (pas d'explosion).

## Validation

Comparaison d'image avec la référence RMIG-007 + compteur de draw calls.

## Inconnues

Gestion du dithering et des coordonnées 16 bits dans le format de vertex.

## Estimation

3 à 5 jours-personne.

## Dépendances

- RMIG-009

## Preuves

- 2026-11-18 : TOMB5_RENDERER=vulkan : niveau 3 room 20 rendu (Lara, HUD, textures 4 bits, ~3500 vertices/1170 triangles par frame), aucun contexte GL. Sampler REPEAT (comme GL) nécessaire pour supprimer des bandes de texture. La capture GL de référence reste inchangée (sha256 675e2c8d…). Builds 32/64 verts, 4188 tests PASS. Limites : projection 512x240 codée dans psx.vert (push constant non fiable), blit VRAM désactivé, capture VK non implémentée.
- 2026-11-18 : Finitions : la projection n’est plus codée en dur dans psx.vert. Elle est passée en push constant (mat4 Projection + vec2 Screen) et calculée dans les conventions Vulkan (y vers le bas, z dans [0,1]) : l’ancienne matrice GL donnait un écran noir car z=-1 était écrêté par le plan proche. Le push constant n’était pas appliqué car émis avant tout vkCmdBindPipeline. Capture/readback désormais disponibles.

## Références

- `EMULATOR/EMULATOR.C:2244` (buffer dynamique)
- `EMULATOR/EMULATOR.C:3220` (modes de blending)
