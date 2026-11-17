# RMIG-006 — Pointeur↔entier et fichiers en erreur en -m64

Status: **Done** — priorité P0 — confiance Medium

Avancement : Terminé : les 16 erreurs -m64 sont corrigées, la compilation 64 bits de GAME/ passe.

## Objectif

Éliminer les conversions pointeur/entier non portables et faire compiler tout GAME/ en 64 bits.

## Faits établis

Inspection -m64 -fsyntax-only : sur 200 fichiers GAME/, 4 sont en erreur — COLLIDE.C (7, dont EMULATOR/GTEREG.H:33 et anims non déclaré), SWITCH.C (5), NEWINV2.C (3), OBJLIGHT.C (1).

## Périmètre

Conversions (long)ptr/(int)ptr vers uintptr_t/intptr_t, déclarations manquantes, GTEREG.H.

Hors périmètre : Sémantique de jeu.

## Tâches

- [ ] Corriger GTEREG.H et les quatre fichiers en erreur en -m64.
- [ ] Remplacer les conversions pointeur/entier non portables par uintptr_t/intptr_t.
- [ ] Vérifier que la compilation -m64 passe sur l'ensemble de GAME/ et SPEC_PSXPC_N/.

## Critères d’acceptation

- Aucune erreur -m64 -fsyntax-only sur GAME/ et SPEC_PSXPC_N/.
- Le build 32 bits reste vert et identique fonctionnellement.

## Validation

Rapport de compilation des deux largeurs + tests documentaires.

## Inconnues

Assembleur GTE et macros de registres selon l'architecture.

## Estimation

1 à 2 jours-personne.

## Dépendances

- RMIG-002

## Preuves

- 2026-11-17 : Corrections : collision de macro B (GTEREG.H) avec les paramètres de DIVFP/MULFP renommés en X/Y dans SPEC_PSXPC_N/GETSTUFF.H ; includes manquants ajoutés (SWITCH.C: SPHERE.H+NEWINV2.H ; NEWINV2.C: SPOTCAM.H+LARAFIRE.H ; OBJLIGHT.C: GETSTUFF.H ; COLLIDE.C: DRAW.H pour anims). Build 64 bits complet sans erreur ; build 32 bits recompilé vert avec un binaire de hash inchangé (b9d8e710…), donc aucune régression de code généré.

## Références

- `EMULATOR/GTEREG.H:33` (macro en erreur -m64)
- `GAME/SWITCH.C:248` (TestCollision non déclaré)
- `GAME/COLLIDE.C:648` (anims non déclaré)
