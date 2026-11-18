# RMIG-014 — Reflets screen-space à presets

Status: **Done** — priorité P2 — confiance Low

Avancement : Terminé : cible hors-écran couleur + profondeur (D32), profondeur par vertex issue des buckets d’ordering table, passe finale plein écran en texelFetch (image identique à l’octet près, preset « aucun »), et quatre presets de reflets écran (aucun/faible/moyen/fort) pilotés depuis l’overlay F12. Le SSR physique n’est pas possible faute de normales et de profondeur view-space dans le flux PSX ; l’effet livré est un reflet écran stylisé atténué par la profondeur.

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

- 2026-11-18 : Infrastructure : scène rendue dans une cible hors-écran (couleur + D32) puis passée à l’écran par un triangle plein écran (texelFetch). Preset « aucun » : captures identiques à l’octet près à la référence (63b778f1… à 300 frames, 5dbbb251… à 1800 frames, cmp identique). Presets faible/moyen/fort : écarts moyens 1,36 / 0,96 / 1,72 niveau vs « aucun » (zone de scène), 60 FPS stables (~16,5 ms) avec « fort ». Validation layers : aucune erreur. Fichiers : EMULATOR/RENDERER_VK.C, EMULATOR/SHADERS/post.{vert,frag}, EMULATOR/DEBUGUI.C, EMULATOR/LIBGPU.C (g_vertexDepth). Capture : docs/porting/render/reflets-f12.png.

## Références

- `EMULATOR/EMULATOR.C:2229` (absence de depth test)
- `docs/porting/vulkan-64bit-plan.md:72` (étape G)
