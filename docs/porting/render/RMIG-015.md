# RMIG-015 — Raytracing matériel (ray_query) avec repli SSR

Status: **Blocked** — priorité P2 — confiance Low

Avancement : Bloqué par une limite de données, pas par Vulkan : le pipeline PSX ne conserve que des coordonnées écran (x, y) et un indice de profondeur par bucket d’ordering table. Il n’y a ni position monde, ni normale, ni BVH exploitable, donc ni SSR physique ni ray_query. Déblocage possible seulement si l’on conserve la géométrie monde/GTE (gros changement du portage) ; l’overlay expose déjà les presets de reflets écran (RMIG-014).

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

- 2026-11-18 : Constat documenté : vertex PSX = écran (x,y) + page/clut/uv/couleur ; profondeur = bucket OT (0..1) sans distance view-space ni normale. Une BVH en espace monde et des normales seraient nécessaires pour ray_query ; ce n’est pas une limitation de Vulkan (extensions disponibles) mais du flux de données émulé.

## Références

- `docs/porting/vulkan-64bit-plan.md:8` (mesures d'extensions RT)
- `EMULATOR/EMULATOR.C:3534` (flux de triangles à alimenter)
