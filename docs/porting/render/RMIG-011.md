# RMIG-011 — Shaders GLSL → SPIR-V (4/8/16 bits, blit, perspective, dither, CLUT)

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Shaders SPIR-V 4/8/16 bits + blit + CLUT + dither compilés hors ligne. La scène de référence (4 et 16 bits) est rendue au pixel près, identique à OpenGL. Le 8 bits, absent des scènes jouées, est validé par un harnais de format forcé (TOMB5_FORCE_TEXFMT=8) : 99,82 % des pixels à ±8 et écart moyen 0,14/255, le reste étant des égalités de sampling nearest sur des frontières de texel. Reste à confirmer sur une scène du jeu utilisant réellement l’8 bits.

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
- 2026-11-18 : Parité pixel : TOMB5_RENDERER=vulkan TOMB5_START_LEVEL=3 TOMB5_FRAMES=1800 TOMB5_CAPTURE=/tmp/vk.bmp, comparé à la référence GL 64 bits : sha256 identiques 5dbbb25184d54d96c95aed1c96494ade0e390956e7c0de1da262180779e269a8, 307200 pixels identiques, validation layers propres. Preuve structurelle : dump TOMB5_DUMP_VERTS identique octet par octet (1277 enregistrements vertices+splits) entre GL et VK sur 300 frames. Correctifs nécessaires : dither retourné verticalement (gl_FragCoord Vulkan part du haut → pc.Screen.y - y), ids de texture logiques distincts, read_vram/copy_vram sur vram.
- 2026-11-18 : Comparaison en mode forcé (TOMB5_FORCE_TEXFMT=8, niveau 3, 300 frames) : GL sha256 45210c96… vs VK ba7c0ef7…, mean_abs_diff=0.142, 99.82% de pixels à ±8. Le format 8 bits n’est pas utilisé par les scènes jouées (répartition mesurée sur la scène de référence : 4 bits 588 groupes, 16 bits 977 groupes, 0 groupe 8 bits).
- 2026-11-18 : Emulator_StoreFrameBuffer porté sur Vulkan (copie de l’image présentée vers un buffer hôte à chaque frame, puis conversion 16 bits identique au chemin GL, appelée une fois par chargement de niveau avec x=0 y=240 w=512 h=240). La référence 4 bits reste bit-identique après ce portage (sha256 5dbbb251…).

## Références

- `EMULATOR/EMULATOR.C:1709` (gte_shader_4)
- `EMULATOR/EMULATOR.C:1849` (blit_shader)
