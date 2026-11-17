# RMIG-002 — Cible de build 64 bits sans dépendance 32 bits

Status: **Todo** — priorité P0 — confiance Medium

Avancement : À démarrer.

## Objectif

Configurer et produire un binaire ELF64 à partir du même arbre, sans -m32 ni GLEW i386.

## Faits établis

Les builds actuels sont configurés avec CMAKE_C_FLAGS=-m32 et CMAKE_EXE_LINKER_FLAGS=-m32 ; GLEW et SDL2 pointent vers /usr/lib/i386-linux-gnu. En 64 bits le système fournit SDL2 2.30 et le loader Vulkan ; GLEW 64 bits n'est pas installé et ne sera pas nécessaire puisque Vulkan remplace OpenGL.

## Périmètre

Option CMake (ex. -DTOMB5_64=ON), sélection des dépendances, cible de sortie et script de configuration reproductible.

Hors périmètre : Correction sémantique du code (tickets suivants), backend Vulkan lui-même.

## Tâches

- [ ] Ajouter une option CMake qui n'impose plus -m32 et choisit les dépendances 64 bits (SDL2 système, loader Vulkan, pas de GLEW).
- [ ] Documenter et scripter la configuration neuve (build tree dédié) avec les options du build de référence.
- [ ] Produire un binaire ELF64 même s'il ne va pas encore jusqu'au jeu, et archiver flags + ldd.

## Critères d’acceptation

- Une configuration neuve aboutit et le binaire produit est ELF64 avec ses dépendances résolues en 64 bits.
- Aucun chemin de build existant (32 bits) n'est cassé : les deux configurations coexistent.

## Validation

CMakeCache + flags + file/ldd archivés ; build 32 bits rejoué et tests documentaires verts.

## Inconnues

Disponibilité d'un GLEW 64 bits si le chemin OpenGL devait survivre temporairement.

## Estimation

1 jour-personne.

## Dépendances

- aucune

## Preuves

- à produire (aucune mesure pour l’instant)

## Références

- `EMULATOR/PLATFORM/Linux.cmake:5` (SDL2/OpenGL/GLEW)
- `docs/porting/vulkan-64bit-plan.md:30` (étape D)
