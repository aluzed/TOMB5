# RMIG-016 — Menu debug avancé et budget de performance

Status: **Blocked** — priorité P2 — confiance Low

Avancement : Bloqué par l'overlay.

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

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/EMULATOR.C:2164` (tableau vram)
- `SPEC_PSXPC_N/INPUTUIDRAW.C:185` (point d'entrée d'une UI hôte)
