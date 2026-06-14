# Build PSXPC_N avec `DISC_VERSION=1`

Date: 2026-06-14
Story: `docs/stories/RE-005-build-psxpcn-disc-version.md`
Status: build validé, runtime bloqué après lecture de l'image disque

## Commandes reproductibles

Depuis la racine du repo:

```bash
cmake -S . -B BUILD/re005-psxpcn-disc -DDISC_VERSION=ON -DCMAKE_BUILD_TYPE=Release
cmake --build BUILD/re005-psxpcn-disc --parallel 2
```

Build debug utilisé pour le backtrace runtime:

```bash
cmake -S . -B BUILD/re005-psxpcn-disc-debug -DDISC_VERSION=ON -DCMAKE_BUILD_TYPE=Debug
cmake --build BUILD/re005-psxpcn-disc-debug --parallel 2
xvfb-run -a gdb -q -batch -ex run -ex 'bt 20' --args BUILD/re005-psxpcn-disc-debug/SPEC_PSXPC_N/MAIN
```

## Dépendances installées/vérifiées

- `cmake`, `gcc/g++` présents.
- Paquets Linux installés pour le build/runtime: `pkg-config`, `libsdl2-dev`, `libglew-dev`, `libegl1-mesa-dev`, `libgles2-mesa-dev`, `xvfb`, `mesa-utils`, `gdb`.
- Tentative 32-bit: `dpkg --add-architecture i386`, puis installation de `gcc-multilib`, `g++-multilib`, `libsdl2-dev:i386`, `libgl-dev:i386`, `libegl1-mesa-dev:i386`, `libgles2-mesa-dev:i386` réussie. Blocage restant: `libglew-dev:i386` / `libglew2.2:i386` ne sont pas disponibles sur les dépôts configurés, donc le build 32-bit complet n'a pas été validé.

## Correctifs nécessaires pour compiler

- `CMakeLists.txt`: `OPTIONAL_DEFINE()` respecte désormais une valeur passée en cache, donc `-DDISC_VERSION=ON` produit bien `-DDISC_VERSION=1` au lieu d'être écrasé par le défaut `OFF`.
- `EMULATOR/TYPES.H`: le garde d'inclusion ne masque plus le vrai `sys/types.h`; les typedefs legacy qui collisionnent avec glibc ne sont activés que pour `__psx__` ou `PSX_COMPAT_TYPES`.
- `EMULATOR/LIBGPU.C`: correction d'un cast d'adresse via `int` dans `SetDrawMove()` incompatible 64-bit.
- `GAME/SETUP.C` et `SPEC_PSXPC_N/TITSEQ.C`: suppression des glyphes Unicode `↑`/`↓` dans des blocs `#if 0`; GCC les lexait tout de même et les rejetait.
- `EMULATOR/LIBCD.C`: le parseur `.CUE` accepte maintenant `MODE1/2352` ou `MODE2/2352`. Le `TOMB5.CUE` fourni est `TRACK 01 MODE2/2352`, cohérent avec les secteurs CD-ROM XA/PSX manipulés par `struct Sector`.

## Validation build

- Build Release: OK, cible `TombRaiderChronicles_PSXPC_N` construite.
- Binaire: `BUILD/re005-psxpcn-disc/SPEC_PSXPC_N/MAIN`.
- Configuration effective confirmée:
  - `BUILD/re005-psxpcn-disc/CMakeCache.txt`: `DISC_VERSION:BOOL=ON`
  - `flags.make`: `-DDISC_VERSION=1`
- Image disque présente:
  - `TOMB5.CUE`: `TRACK 01 MODE2/2352`
  - `TOMB5.BIN`: 652162560 octets

## Validation runtime

### Sans serveur graphique

```bash
timeout 8s BUILD/re005-psxpcn-disc/SPEC_PSXPC_N/MAIN
```

Résultat: initialisation SDL impossible en headless pur.

```text
[EMU] Initialising Emulator.
[EMU] VERSION: 1.151
[EMU] [Emulator_InitialiseSDL] - Error: Failed to initialise SDL
[EMU] [Emulator_Initialise] - Failed to Intialise SDL
```

### Sous Xvfb

```bash
xvfb-run -a timeout 15s BUILD/re005-psxpcn-disc/SPEC_PSXPC_N/MAIN
```

Résultat: SDL/OpenGL démarre via Mesa llvmpipe, puis crash runtime.

Backtrace Debug:

```text
Thread 1 "MAIN" received signal SIGSEGV, Segmentation fault.
0x0000555555627a06 in RelocateModule (Module=93824994190512, RelocData=0x5a755573c3a4) at /var/www/projects/TOMB5/SPEC_PSXPC_N/FILE.C:115
115     if (*RelocData != -1)
#0  RelocateModule(unsigned long, unsigned long*) at SPEC_PSXPC_N/FILE.C:115
#1  S_LoadLevelFile(int) at SPEC_PSXPC_N/ROOMLOAD.C:100
#2  DoTitle(unsigned char, unsigned char) at GAME/GAMEFLOW.C:971
#3  DoGameflow() at GAME/GAMEFLOW.C:261
#4  main(int, char**) at SPEC_PSXPC_N/PSXMAIN.C:121
```

Avant le correctif `MODE2`, le build Debug s'arrêtait plus tôt sur:

```text
MAIN: EMULATOR/LIBCD.C:413: int ParseCueSheet(): Assertion `!strncmp(string, "MODE1", 5)' failed.
```

Après acceptation de `MODE2`, l'exécution progresse jusqu'à `S_LoadLevelFile()`, ce qui confirme que `TOMB5.CUE` est lu assez loin pour initialiser le chemin CD, mais le runtime 64-bit plante pendant la relocation du module chargé.

## Diagnostic du blocage restant

Le crash `RelocateModule()` est cohérent avec les nombreux casts pointeur ↔ `int`/`unsigned int` visibles dans `SPEC_PSXPC_N` et `GAME` pendant la compilation. Le code semble supposer un espace d'adressage 32-bit; en binaire Linux x86_64, plusieurs adresses sont tronquées ou reconstruites incorrectement.

Prochaine piste recommandée:

1. Rendre le build Linux 32-bit reproductible, ou supprimer/adapter la dépendance GLEW pour permettre `-m32` avec les paquets i386 disponibles.
2. Reconfigurer avec `-DCMAKE_C_FLAGS=-m32 -DCMAKE_CXX_FLAGS=-m32 -DCMAKE_EXE_LINKER_FLAGS=-m32`.
3. Relancer sous Xvfb et vérifier si `RelocateModule()` progresse.

## Acceptance criteria

- [x] Le build réussit.
- [x] `DISC_VERSION=1` est confirmé dans la configuration effective.
- [x] `TOMB5.BIN/TOMB5.CUE` sont présents et le parseur `.CUE` accepte le `MODE2/2352` réel.
- [x] Commande de build reproductible documentée.
- [x] Lancement graphique tenté sous Xvfb.
- [ ] Runtime jouable: bloqué par crash dans `RelocateModule()` en build 64-bit.
