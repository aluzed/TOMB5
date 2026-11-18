# RMIG-014 — Reflets screen-space à presets

Status: **Todo** — priorité P2 — confiance Low

Avancement : Bloqué par Vulkan et l'overlay.

## Objectif

Ajouter des reflets réglables (off / bas / moyen / haut) avant de dépendre du RT matériel.

## Faits établis

Le rendu n'a pas de depth buffer hôte (ordre PSX) ; une SSR a besoin d'une profondeur et d'une normale, qu'il faudra produire (passes additionnelles ou reconstruction depuis le z PSX).

## Périmètre

Passe de profondeur, SSR par presets, composite, coût par preset.

Hors périmètre : RT matériel (ticket suivant).

## Tâches

- [ ] Produire une profondeur/normale exploitable pour la scène.
- [ ] Implémenter la SSR avec quatre presets et un coefficient d'intensité.
- [ ] Mesurer le coût de chaque preset et l'exposer dans l'overlay.

## Critères d’acceptation

- Les quatre presets changent visiblement le reflet sans casser la scène PSX d'origine.
- Le preset off redonne exactement l'image de référence.

## Validation

Captures par preset + coût mesuré (ms) dans l'overlay.

## Inconnues

Reconstruction de normale sur un rendu sans depth natif.

## Estimation

3 jours-personne.

## Dépendances

- RMIG-011
- RMIG-013

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/EMULATOR.C:2229` (absence de depth test)
- `docs/porting/vulkan-64bit-plan.md:72` (étape G)
