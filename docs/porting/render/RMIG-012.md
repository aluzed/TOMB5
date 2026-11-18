# RMIG-012 — Parité visuelle et retrait du chemin OpenGL

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Débloqué : les shaders SPIR-V sont en place et le backend Vulkan reproduit la référence OpenGL 64 bits au pixel près (y compris après portage de Emulator_StoreFrameBuffer). Reste (a) l’écart 32 bits ↔ 64 bits (64 bits plus sombre, HUD compris : mean_abs_diff=18.730, 26.12% à ±8) et (b) le retrait effectif du chemin OpenGL du build 64 bits.

## Objectif

Valider Vulkan sur des scènes réelles puis supprimer OpenGL du build 64 bits.

## Faits établis

Le remplacement est décidé : aucun backend GL ne doit rester dans la cible 64 bits. La référence de comparaison est produite par RMIG-007. Le harnais RMIG-007 a mesuré un écart 32/64 : mean_abs_diff=18.730, 26.12% de pixels à +/-8 après gain global ; le 64 bits est plus sombre, HUD compris. Cet écart devra être expliqué ou accepté dans la parité Vulkan.

## Périmètre

Comparaison sur plusieurs niveaux (Rome, Colosseum), correction des écarts, retrait des fichiers/dépendances GL.

Hors périmètre : Refonte du gameplay.

## Tâches

- [ ] Comparer au moins trois scènes (titre, niveau 1, Colosseum) entre référence et Vulkan.
- [ ] Corriger les écarts visuels et mesurer le coût par frame.
- [ ] Retirer GLEW/OpenGL du build 64 bits et du CMake.

## Critères d’acceptation

- Écarts visuels documentés et acceptés (aucune régression fonctionnelle).
- Le build 64 bits ne référence plus ni GLEW ni OpenGL (vérifié par ldd et grep).

## Validation

Rapport de comparaison d'images + ldd + revue des dépendances CMake.

## Inconnues

Écarts de filtrage/arrondi entre pilotes.

## Estimation

2 à 3 jours-personne.

## Dépendances

- RMIG-007
- RMIG-011

## Preuves

- 2026-11-18 : Backend Vulkan pixel-identique à OpenGL 64 bits sur la scène de référence (sha256 5dbbb251…, cmp identique). L’écart restant est celui du rendu 32 bits vs 64 bits, indépendant du backend ; à instruire côté conversion couleur/format.

## Références

- `EMULATOR/PLATFORM/Linux.cmake:5` (dépendances à retirer)
- `EMULATOR/EMULATOR_PLATFORM_SETUP.H:18` (sélection OGL)
