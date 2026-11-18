# RMIG-009 — Backend Vulkan : instance, device, swapchain, présentation

Status: **Done** — priorité P1 — confiance Medium

Avancement : Backend Vulkan intégré au jeu : TOMB5_RENDERER=vulkan crée la fenêtre SDL_WINDOW_VULKAN, initialise l’instance/device/swapchain et présente une image claire via RendererVK_BeginScene/EndScene. Le jeu (simulation, entrées, logs [DRAW]/[LARA]) tourne sans contexte OpenGL. Le chemin GL par défaut reste inchangé (capture RMIG-007 identique). Le pipeline PSX (VRAM/VBO/shaders) reste RMIG-010/011.

## Objectif

Afficher une frame Vulkan vide via SDL2, avec le bon périphérique et sans dépendance à OpenGL.

## Faits établis

SDL2 2.30 (64 bits) et le loader Vulkan sont disponibles ; la machine expose une RTX 2080 Ti et llvmpipe. Le contexte GL actuel est créé avec SDL_WINDOW_OPENGL ; Vulkan exigera SDL_WINDOW_VULKAN et une swapchain explicite.

## Périmètre

Instance, sélection de périphérique, device + queues, swapchain, sémaphores, présent.

Hors périmètre : Pipeline PSX et shaders.

## Tâches

- [ ] Créer l'instance et choisir le périphérique (préférence GPU discret, fallback llvmpipe).
- [ ] Créer device/queues et une swapchain redimensionnable, puis présenter un clear.
- [ ] Gérer proprement resize, vsync et fermeture.

## Critères d’acceptation

- Une fenêtre s'ouvre, présente une couleur unie stable, et se ferme sans erreur de validation.
- Le périphérique choisi est journalisé et le fallback fonctionne.

## Validation

Journal Vulkan (couche de validation) sans erreur + capture.

## Inconnues

Disponibilité de la validation layer en 64 bits, comportement multi-GPU.

## Estimation

2 à 3 jours-personne.

## Dépendances

- RMIG-008

## Preuves

- 2026-11-18 : Smoke test autonome : instance/device/swapchain 640x480, 4 images, 60 frames présentées, sortie 0. Intégration jeu : TOMB5_RENDERER=vulkan + TOMB5_VK_CLEAR=1 -> fenêtre bleue 640x480, [VK] backend ready, boucle de jeu active (logs [DRAW] lvl=3 room=20, [LARA] anim=103), aucun contexte GL. Chemin GL par défaut vérifié : capture déterministe inchangée sha256 675e2c8d…. Builds 32/64 verts, 4188 tests PASS.

## Références

- `EMULATOR/EMULATOR.C:648` (création fenêtre GL)
- `docs/porting/vulkan-64bit-plan.md:60` (étape E)
