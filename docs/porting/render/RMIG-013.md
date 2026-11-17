# RMIG-013 — ImGui F12 : overlay, stats et interrupteurs

Status: **Blocked** — priorité P1 — confiance Medium

Avancement : Bloqué par les shaders.

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

- à produire (aucune mesure pour l’instant)

## Références

- `SPEC_PSXPC_N/INPUTUIDRAW.C:185` (UI existante dessinée dans le framebuffer PSX)
- `EMULATOR/INPUTUI.C:397` (cycle de vie de l'UI)
