# RMIG-012 — Parité visuelle et retrait du chemin OpenGL

Status: **Blocked** — priorité P1 — confiance Medium

Avancement : Bloqué par les shaders.

## Objectif

Valider Vulkan sur des scènes réelles puis supprimer OpenGL du build 64 bits.

## Faits établis

Le remplacement est décidé : aucun backend GL ne doit rester dans la cible 64 bits. La référence de comparaison est produite par RMIG-007.

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

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/PLATFORM/Linux.cmake:5` (dépendances à retirer)
- `EMULATOR/EMULATOR_PLATFORM_SETUP.H:18` (sélection OGL)
