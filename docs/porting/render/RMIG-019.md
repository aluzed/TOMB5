# RMIG-019 — Zero primitive PSX non geree en 64 bits

Status: **In progress** — priorité P1 — confiance Medium

Avancement : En cours : compteur mesure a 77 messages sur 35 s de mode attractif apres RMIG-018 (702 avant).

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

- 2026-11-17 : Comptage : 77 messages "Unhandled primitive type" sur 35 s de mode attractif 64 bits apres RMIG-018.

## Références

- `EMULATOR/LIBGPU.C:1209` (ParsePrimitive : types non geres)
