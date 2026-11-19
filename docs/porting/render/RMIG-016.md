# RMIG-016 — Menu debug avancé et budget de performance

Status: **Done** — priorité P2 — confiance Low

Avancement : Terminé pour l’essentiel : timestamps GPU par passe (scène / post) lus à la frame suivante, coût CPU de la frame, budget de frame réglable avec alerte couleur, compteurs de rendu (vertices, triangles, draws, ordering tables) et aperçu VRAM brut. L’overlay ne construit aucune frame ImGui tant qu’il n’a pas été ouvert (coût nul vérifié) et la capture de référence reste identique. L’inspection GTE reste hors périmètre.

## Objectif

Outiller l'analyse : inspection VRAM/GTE, compteurs de passes, heatmap de coût, budget de frame.

## Faits établis

L'émulateur connaît déjà la VRAM, les ordering tables et les états de blending ; il manque une visualisation et des compteurs agrégés.

## Périmètre

Panneau d'inspection (VRAM, textures, OT), compteurs (draw calls, triangles, overdraw), budget par frame.

Hors périmètre : Outils hors jeu (profiler externe).

## Tâches

- [ ] Exposer la VRAM et l'état des ordering tables dans l'overlay.
- [ ] Ajouter des compteurs par passe et un budget de frame paramétrable.
- [ ] Documenter l'usage pour les futures optimisations.

## Critères d’acceptation

- Un développeur peut identifier la passe la plus coûteuse sans profiler externe.
- L'overlay se désactive complètement (coût nul mesuré) quand il est fermé.

## Validation

Captures du panneau + mesure du coût overlay fermé/ouvert.

## Inconnues

Impact mémoire des visualisations sur une cible 64 bits.

## Estimation

2 à 3 jours-personne.

## Dépendances

- RMIG-013

## Preuves

- 2026-11-19 : Profilage : 3 requêtes de timestamp par frame (début, fin de scène, fin de post), relecture après fence, conversion timestampPeriod. Relevé en jeu (niveau 3, 640x480) : GPU scene 0.50 ms, GPU post 0.07 ms, CPU frame 16.80 ms, total 0.57 ms pour un budget de 16.6 ms. Aperçu VRAM via ImGui_ImplVulkan_AddTexture (vue brute R/G). Overlay fermé : aucune frame ImGui construite ; capture 300 frames identique (sha256 63b778f1…) ; F12 ouvert/fermé/ouvert sans assertion. Capture : docs/porting/render/profil-f12.png.

## Références

- `EMULATOR/EMULATOR.C:2164` (tableau vram)
- `SPEC_PSXPC_N/INPUTUIDRAW.C:185` (point d'entrée d'une UI hôte)
