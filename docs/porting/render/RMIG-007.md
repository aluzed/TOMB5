# RMIG-007 — Harnais de comparaison 32 bits / 64 bits

Status: **Blocked** — priorité P1 — confiance Medium

Avancement : Bloqué par la cible 64 bits.

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

- à produire (aucune mesure pour l’instant)

## Références

- `docs/porting/colosseum-walkthrough.md:60` (recette de test)
- `GAME/CONTROL.C:1116` (GetRandomControl)
