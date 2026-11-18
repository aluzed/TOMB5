# RMIG-011 — Shaders GLSL → SPIR-V (4/8/16 bits, blit, perspective, dither, CLUT)

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Shaders SPIR-V 4/8/16 bits + CLUT + dither compilés par glslc et embarqués (SHADERS_VK.H). Le rendu 4 bits est validé en jeu. Restent : blit VRAM, perspective PGXP et vérification des 8/16 bits.

## Objectif

Porter les shaders générés à l'exécution vers des shaders SPIR-V équivalents.

## Faits établis

Les shaders sont des chaînes C (gte_shader_4/8/16, blit_shader) avec en-têtes GLSL 330/300 es, correction de perspective maison (a_z/a_w), dithering PSX et décodage page/CLUT VRAM dans le fragment shader.

## Périmètre

Conversion des sources, compilation hors ligne en SPIR-V, variantes par profondeur de texture, uniformes de projection.

Hors périmètre : Nouveaux effets (SSR/RT).

## Tâches

- [ ] Extraire les sources GLSL actuelles et les convertir en GLSL Vulkan (set/binding, layouts).
- [ ] Compiler en SPIR-V et charger les modules dans les pipelines.
- [ ] Valider le rendu des trois profondeurs de texture et du blit final.

## Critères d’acceptation

- Les trois variantes (4/8/16 bits) et le blit produisent la même image que la référence OpenGL.
- Aucun shader n'est compilé à l'exécution depuis une chaîne GLSL (ou la compilation runtime est documentée).

## Validation

Comparaison d'image par variante de niveau + validation layer.

## Inconnues

Précision de l'interpolation de perspective et du dithering en SPIR-V.

## Estimation

3 à 4 jours-personne.

## Dépendances

- RMIG-010

## Preuves

- 2026-11-18 : EMULATOR/SHADERS/{psx.vert,psx4.frag,psx8.frag,psx16.frag,blit.vert,blit.frag} + psx_common.glsl, compilés par scripts/porting/gen_vk_shaders.py vers EMULATOR/SHADERS_VK.H. Pipeline 4 bits validé en jeu (textures/CLUT/dither). Blit et perspective restent à brancher.

## Références

- `EMULATOR/EMULATOR.C:1709` (gte_shader_4)
- `EMULATOR/EMULATOR.C:1849` (blit_shader)
