# RMIG-003 — Typedefs PSX à largeur fixe et garde de tailles (STYPES.H)

Status: **Done** — priorité P0 — confiance Medium

Avancement : Terminé : STYPES.H converti en types à largeur fixe, assert 32 bits préservés, build 64 bits vert.

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

- 2026-11-17 : SPEC_PSXPC_N/STYPES.H : typedefs psx_i32/psx_u32 (int32_t/uint32_t) et conversion des champs (le seul `long` restant est dans DB_STRUCT, structure hôte de buffers, non PSX). static_assert sur les structures sans pointeur (DRIP_STRUCT 24, TEXTURE 16, static_info 28, REQUESTER 20, ITEM_LIGHT 48) pour toutes les ABI, et sur room_info 80 / ITEM_INFO 144 / object_info 64 / creature_info 228 seulement hors LP64 (elles embarquent des pointeurs hôtes). Build 32 bits vert et binaire de hash INCHANGÉ (b9d8e710…). Build 64 bits vert ; l'écran de démarrage Tomb Raider Chronicles s'affiche correctement (capture) et l'assertion ParsePrimitive ne se déclenche plus, il ne reste que des 'Unhandled primitive type' (507 en 20 s) qui relèvent de RMIG-004 (TYPES.H).

## Références

- `SPEC_PSXPC_N/STYPES.H:39` (struct room_info)
- `GAME/SETUP.C:1636` (relocation et floor_data)
