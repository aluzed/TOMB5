# RMIG-004 — Conversion des structures de GAME/TYPES.H

Status: **Todo** — priorité P0 — confiance Medium

Avancement : À démarrer (RMIG-003 terminé).

## Objectif

Appliquer la même conversion aux structures de GAME/TYPES.H (le cœur des données de jeu).

## Faits établis

GAME/TYPES.H contient 148 long et 14 unsigned long : lara_info, FLOOR_INFO, SAVEGAME_INFO, lumières, caméra, et surtout PHD_VECTOR/PHD_3DPOS (3 longs = 12 octets) utilisés partout. Constat de RMIG-003 : les structures qui embarquent des pointeurs hôtes (room_info, ITEM_INFO, creature_info) ne peuvent PAS garder la taille du format PSX en LP64 ; il faut lire le format fichier via une structure dédiée plutôt que forcer sizeof.

## Périmètre

GAME/TYPES.H et les structures qu'il définit, avec asserts de taille.

Hors périmètre : Les long locaux des fichiers .C.

## Tâches

- [ ] Convertir les champs des structures de TYPES.H vers les types à largeur fixe.
- [ ] Ajouter les static_assert de taille et vérifier la cohérence avec les offsets documentés.
- [ ] Vérifier que le format de sauvegarde v4 (8658 octets, offsets fixes) reste lisible.

## Critères d’acceptation

- Tailles identiques en 32 bits avant/après, et offsets de sauvegarde inchangés.
- Un chargement de sauvegarde existante (TOMB5.valid_level1.sav) aboutit sans erreur.

## Validation

Build 32 bits + chargement d'une sauvegarde réelle + tests documentaires.

## Inconnues

Structures partagées entre niveaux et blocs de sauvegarde.

## Estimation

2 à 3 jours-personne.

## Dépendances

- RMIG-003

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `GAME/TYPES.H:358` (struct FLOOR_INFO)
- `GAME/PORTSAVE.C:289` (lecture de sauvegarde)
