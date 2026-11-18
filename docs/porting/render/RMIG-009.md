# RMIG-009 — Backend Vulkan : instance, device, swapchain, présentation

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Outil de validation Vulkan autonome (tools/vulkan_smoke.cpp) : instance, surface SDL2/X11, sélection physique, device + queue graphics/present, swapchain 640x480 (4 images), render pass clear, 60 frames présentées, arrêt propre. Validé sur le driver Vulkan de la machine (lavapipe/NVIDIA). Reste : intégrer ce squelette dans EMULATOR/RENDERER_VK.C et brancher le pipeline PSX.

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

- 2026-11-18 : tools/vulkan_smoke.cpp compile et s’exécute : [VK] instance/device/swapchain OK: 640x480, 4 images ; [VK] presented, shutting down ; exit 0. Script scripts/porting/vulkan_smoke.sh. Le squelette servira de base à RENDERER_VK.C (RMIG-010/011).

## Références

- `EMULATOR/EMULATOR.C:648` (création fenêtre GL)
- `docs/porting/vulkan-64bit-plan.md:60` (étape E)
