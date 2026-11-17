# RMIG-003 — Typedefs PSX à largeur fixe et garde de tailles (STYPES.H)

Status: **Todo** — priorité P0 — confiance Medium

Avancement : Bloqué par la cible 64 bits.

## Objectif

Rendre les structures de données PSX indépendantes de la largeur de long, en commençant par SPEC_PSXPC_N/STYPES.H.

## Faits établis

SPEC_PSXPC_N/STYPES.H contient 52 long et 39 unsigned long. Ces structures (room_info, FLOOR_INFO, ITEM_INFO) sont relogées depuis le fichier de niveau et comparées par sizeof ; sur LP64 leurs tailles changent silencieusement.

## Périmètre

STYPES.H uniquement : introduction de typedefs explicites et conversion des champs de données PSX, avec static_assert sur les tailles attendues.

Hors périmètre : GAME/TYPES.H (ticket suivant), long locaux, code applicatif.

## Tâches

- [ ] Introduire des typedefs explicites (psx_i32/psx_u32) et convertir les champs des structures de STYPES.H.
- [ ] Ajouter des static_assert sur les tailles des structures critiques, en s'appuyant sur les offsets déjà présents en commentaire.
- [ ] Compiler en 32 bits et vérifier qu'aucune taille ne change (aucune régression).

## Critères d’acceptation

- En 32 bits, les sizeof des structures de STYPES.H sont identiques à l'existant (vérifié par static_assert).
- Les sources qui utilisent ces champs compilent sans modification de sémantique en 32 bits.

## Validation

Build 32 bits complet + tests documentaires (4183) + relevé des tailles avant/après.

## Inconnues

Champs dont la largeur est volontairement celle de l'hôte (pointeurs déguisés).

## Estimation

1 à 2 jours-personne.

## Dépendances

- RMIG-002

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `SPEC_PSXPC_N/STYPES.H:39` (struct room_info)
- `GAME/SETUP.C:1636` (relocation et floor_data)
