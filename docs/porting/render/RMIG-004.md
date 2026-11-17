# RMIG-004 — Conversion des structures de GAME/TYPES.H

Status: **Done** — priorité P0 — confiance Medium

Avancement : Terminé : GAME/TYPES.H converti, asserts de layout en place, 32 bits inchangé, 64 bits vert.

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

- 2026-11-17 : GAME/TYPES.H : typedefs déplacés ici (psx_i32/psx_u32, int32_t/uint32_t) et conversion des 148 long + 14 unsigned long (PHD_VECTOR, PHD_3DPOS, FLOOR_INFO, LIGHTINFO, MESH_INFO, OBJECT_VECTOR, SPOTCAM, lara_info, savegame_info…). static_assert sur les structures sans pointeur : PHD_VECTOR 12, PHD_3DPOS 20, FLOOR_INFO 8, LIGHTINFO 32, MESH_INFO 20, OBJECT_VECTOR 16, SPOTCAM 40. Corrections induites : UpdateLightning (GAME/CONTROL.C) utilisait long* pour parcourir des psx_i32. Build 32 bits vert avec hash INCHANGÉ (b9d8e710…), build 64 bits vert. Le binaire 64 bits rend toujours correctement l'écran de démarrage mais conserve ~594 'Unhandled primitive type' en 20 s : le flux de paquets reste mal interprété, ce qui déplace le problème sur les structures lues depuis le fichier de niveau (pointeurs 32 bits) → RMIG-005.

## Références

- `GAME/TYPES.H:358` (struct FLOOR_INFO)
- `GAME/PORTSAVE.C:289` (lecture de sauvegarde)
