# RMIG-015 — Raytracing matériel (ray_query) avec repli SSR

Status: **Blocked** — priorité P2 — confiance Low

Avancement : Bloqué par la SSR.

## Objectif

Activer des reflets/ombres raytracés sur matériel RT, avec détection d'extension et repli automatique.

## Faits établis

La RTX 2080 Ti expose toutes les extensions RT en 64 bits (mesuré en RMIG-001) ; llvmpipe expose les mêmes mais en logiciel. Le chemin doit donc être optionnel et ne jamais être requis.

## Périmètre

Détection d'extensions, BLAS/TLAS pour la scène, passe ray_query, presets, repli SSR.

Hors périmètre : Pipeline RT complet (ray_tracing_pipeline) dans un premier temps.

## Tâches

- [ ] Détecter les extensions et construire les accélération structures à partir de la géométrie PSX.
- [ ] Implémenter les reflets en ray_query avec niveaux de qualité et de rebonds.
- [ ] Vérifier le repli exact vers SSR quand l'extension ou le matériel manque.

## Critères d’acceptation

- Sur la RTX, les reflets sont visuellement différents et réglables ; sur un GPU sans RT, le jeu reste identique au preset SSR choisi.
- L'absence d'extension ne provoque ni erreur ni écran noir.

## Validation

Journal des extensions au démarrage + captures RT vs SSR + test de repli forcé.

## Inconnues

Coût de reconstruction des accélération structures pour une scène PSX très morcelée.

## Estimation

5 à 8 jours-personne.

## Dépendances

- RMIG-014

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `docs/porting/vulkan-64bit-plan.md:8` (mesures d'extensions RT)
- `EMULATOR/EMULATOR.C:3534` (flux de triangles à alimenter)
