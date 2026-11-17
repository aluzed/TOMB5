# RMIG-019 — Zero primitive PSX non geree en 64 bits

Status: **Done** — priorité P1 — confiance Medium

Avancement : Termine : 0 primitive non geree sur 120 s de mode attractif 64 bits.

## Objectif

Eliminer les messages "Unhandled primitive type" du parseur de primitives en 64 bits.

## Faits établis

Apres RMIG-018, 77 messages sur 35 s de mode attractif (contre 702 avant la correction des layouts). Types observes : 06,07,08,09,10 (code/type2).

## Périmètre

EMULATOR/LIBGPU.C (ParsePrimitive), macros de primitives, eventuels types non implementes.

Hors périmètre : Vulkan.

## Tâches

- [ ] Lister les types exacts restants et le chemin de rendu qui les produit.
- [ ] Ajouter le parsing manquant ou corriger la taille/le type des paquets.
- [ ] Verifier que le compteur tombe a zero sur une session de reference.
- [ ] Comparer la sequence de primitives avec le build 32 bits sur la meme scene.

## Critères d’acceptation

- Aucun "Unhandled primitive type" sur 60 s de mode attractif 64 bits.
- La capture 64 bits reste stable et le log ne contient plus ces types.

## Validation

Comptage dans le log de session + capture.

## Inconnues

Les types 06-10 peuvent venir de primitives legitimes non implementees ou d une taille de paquet erronee.

## Estimation

0,5 a 1 jour-personne.

## Dépendances

- RMIG-018

## Preuves

- 2026-11-17 : Cause : les structures DR_ENV/DR_* et les macros de LIBGPU.H utilisaient encore `u_long` (8 octets en LP64), donc sizeof(DR_ENV) valait 128 au lieu de 64 et les paquets DR_* desynchronisaient la chaine de primitives (types 0x10/0x8C/0xFC/0xFF tires de code MIPS). Apres remplacement de tous les u_long de LIBGPU.H/.C par PSX_ULONG et troncature explicite dans setaddr, les tailles 32/64 sont identiques (P_TAG 12, POLY_F3 24, POLY_FT4 44, POLY_GT4 56, TILE 20, SPRT 24, DR_ENV 64, DR_MOVE 28). Execution 64 bits de 120 s : 0 "Unhandled primitive type", 0 SIGSEGV, 0 stack smashing. Build 32 bits frais vert et execute 40 s sans erreur.

## Références

- `EMULATOR/LIBGPU.C:1209` (ParsePrimitive : types non geres)
