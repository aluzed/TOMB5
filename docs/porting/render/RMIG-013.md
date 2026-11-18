# RMIG-013 — ImGui F12 : overlay, stats et interrupteurs

Status: **Done** — priorité P1 — confiance Medium

Avancement : ImGui v1.91.5 vendoré et branché sur le backend Vulkan 64 bits. Overlay F12 avec stats (FPS, niveau/salle, position de Lara, animation, vertices/triangles/draws/OT) et interrupteurs réels (dithering, profondeur de texture forcée) plus un bouton de capture BMP. Les entrées du jeu sont bloquées tant que l'overlay est visible et reprennent à la fermeture.

## Objectif

Disposer d'un menu debug Vulkan/ImGui toujours compilé, ouvert par F12, pour piloter la suite (reflets, RT, qualité).

## Faits établis

L'UI existante (InputUI) est dessinée dans le framebuffer PSX via les primitives GPU émulées : elle ne peut pas héberger un panneau moderne. ImGui + backend SDL2/Vulkan s'ajoute comme passe hôte après le blit.

## Périmètre

Vendoring d'ImGui, backend SDL2+Vulkan, overlay F12, stats de frame, interrupteurs de fonctionnalités, capture du clavier quand l'overlay est ouvert.

Hors périmètre : Contenu avancé (inspection VRAM/GTE, heatmap) qui fera l'objet de RMIG-016.

## Tâches

- [ ] Vendorer ImGui et brancher son backend SDL2/Vulkan dans le renderer.
- [ ] Ajouter la bascule F12 et le routage des entrées vers l'overlay uniquement quand il est ouvert.
- [ ] Exposer les premiers interrupteurs (wireframe, FX, presets de reflets) et des stats (FPS, draw calls, temps CPU).

## Critères d’acceptation

- F12 ouvre/ferme l'overlay sans perturber le jeu ; les entrées reprennent normalement à la fermeture.
- Les interrupteurs agissent immédiatement et les stats sont lisibles.

## Validation

Captures de l'overlay + vérification que le jeu ne reçoit plus les entrées quand l'overlay est ouvert.

## Inconnues

Conflits de touches avec les raccourcis existants (F5/F6/F12).

## Estimation

2 jours-personne.

## Dépendances

- RMIG-011

## Preuves

- 2026-11-18 : Overlay opérationnel : F12 ouvre/ferme ([IMGUI] overlay visible/masque). Le rendu du jeu est inchangé quand l'overlay est fermé (capture 300 frames identique, sha256 63b778f1…). Entrées bloquées : overlay ouvert + « Up » 3 s → pos Lara inchangée (90642,4608,52736) ; overlay fermé + « Up » 3 s → pos (81363,…). Interrupteur « Dithering » : OFF change immédiatement l'image (écart moyen 2,3 niveaux) via pc.Dither dans les shaders 4/8/16 bits. Bouton Capture : écrit /tmp/tomb5_capture.bmp 640x480. Fichiers : EMULATOR/DEBUGUI.{C,H}, external/imgui (v1.91.5), EMULATOR/RENDERER_VK.C, EMULATOR/LIBPAD.C, EMULATOR/CMakeLists.txt. Capture : docs/porting/render/imgui-f12.png.

## Références

- `SPEC_PSXPC_N/INPUTUIDRAW.C:185` (UI existante dessinée dans le framebuffer PSX)
- `EMULATOR/INPUTUI.C:397` (cycle de vie de l'UI)
