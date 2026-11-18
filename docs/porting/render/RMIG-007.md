# RMIG-007 — Harnais de comparaison 32 bits / 64 bits

Status: **Done** — priorité P1 — confiance Medium

Avancement : Harnais déterministe opérationnel : le jeu exécute N frames de contrôle, applique une entrée scriptée optionnelle (TOMB5_REPLAY), capture l’image (TOMB5_CAPTURE) puis quitte. Deux exécutions du même binaire produisent des BMP identiques (32 bits et 64 bits). La scène de référence niveau 3 à 1800 frames donne le même état de jeu (Lara pos/anim/frame) dans les deux builds ; un écart colorimétrique global subsiste et est documenté pour RMIG-012.

## Objectif

Pouvoir prouver que la migration ne change ni la géométrie, ni l'image, avant de supprimer l'ancien chemin.

## Faits établis

Les sondes gdb existantes (probe_sanity, positions d'items) et les captures de fenêtre donnent déjà des points de comparaison. Il manque un mode déterministe (frame figée) et un hash d'image.

## Périmètre

Mode « frame déterministe » (entrée scriptée, position forcée), capture PNG et hash, comparaison entre les deux binaires.

Hors périmètre : Analyse perceptuelle fine.

## Tâches

- [ ] Définir une scène de référence déterministe (sauvegarde valide + séquence d'entrées fixe).
- [ ] Produire capture + hash pour le build 32 bits puis pour le build 64 bits et comparer.
- [ ] Documenter le seuil d'écart acceptable (géométrie identique, différences de filtrage tolérées).

## Critères d’acceptation

- Deux exécutions de la même scène sur le même binaire donnent des captures identiques (déterminisme prouvé).
- Le rapport 32/64 quantifie les écarts et sert de référence pour la parité Vulkan.

## Validation

Captures et hashes archivés, script réutilisable.

## Inconnues

Déterminisme des effets aléatoires (GetRandomControl) et du timing.

## Estimation

1 jour-personne.

## Dépendances

- RMIG-002
- RMIG-006

## Preuves

- 2026-11-18 : Scène : TOMB5_START_LEVEL=3, 1800 frames de contrôle, capture à la frame 1799. Deux runs 32 bits : sha256 083d24a01588e14023b5f2ddb654dcaee278a58d9ce9e4a7fa443a6d7f7750b6 (identiques). Deux runs 64 bits : sha256 675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b (identiques). État identique 32/64 : Lara pos=(90642,4608,52736) room=20 rot=-16384 anim=103 frame=1611. Écart image 32/64 : mean_abs_diff=18.730, gain global 0.965, 26.12% de pixels à +/-8 après gain ; le 64 bits est plus sombre, y compris le HUD, donc l’écart n’est pas seulement l’éclairage 3D. Captures/README dans docs/porting/replay/ et script scripts/porting/capture_compare.py.

## Références

- `docs/porting/colosseum-walkthrough.md:60` (recette de test)
- `GAME/CONTROL.C:1116` (GetRandomControl)
