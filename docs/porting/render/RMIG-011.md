# RMIG-011 — Shaders GLSL → SPIR-V (4/8/16 bits, blit, perspective, dither, CLUT)

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Capture Vulkan (readback swapchain -> BMP) opérationnelle. La parité 32/GL vs VK sur la scène de référence n’est pas encore acquise : au même état de jeu (Lara pos/anim/frame 1611), l’image GL est bleutée (probable fondu/overlay de cinématique) alors que VK montre la scène de base orangée. Écart mesuré : mean_abs_diff=50.4, gain 0.63, 4.08% de pixels à ±8. Prochaines étapes : rendre les prims non texturées / fondus 2D et aligner le timing de cinématique.

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
- 2026-11-18 : Écran-titre Vulkan rendu via le blit shader (TOMB RAIDER CHRONICLES + menu New Game/Special Features/F6 CONTINUE) et scène 3D niveau 3 via les shaders 4 bits. Sampler REPEAT. Aucun OpenGL. Reste 8/16 bits + readback.
- 2026-11-18 : Readback VK : capture 640x480 BMP via copie swapchain -> buffer host + SDL_SaveBMP, déclenchée par Emulator_RequestScreenshot (TOMB5_CAPTURE). Fichier produit et lisible. Comparaison avec la référence GL au même état (pos/anim/frame identiques) : mean_abs_diff=50.4, gain global 0.63, 4.08% à ±8 ; différence de couleur/ambiance (GL bleuté vs VK orangé) à expliquer (fondu/overlay 2D ou timing de cinématique).

## Références

- `EMULATOR/EMULATOR.C:1709` (gte_shader_4)
- `EMULATOR/EMULATOR.C:1849` (blit_shader)
