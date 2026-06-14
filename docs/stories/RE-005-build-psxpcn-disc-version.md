# RE-005 — Valider le build PSXPC_N avec image disque

Status: Blocked — build OK, runtime 64-bit plante dans `RelocateModule()`
Owner: Hermes
Priority: P0
Type: Build/Runtime

## Progress tracker

- [x] Dépendances Linux vérifiées/installées pour build 64-bit: CMake, SDL2, GLEW, EGL/GLES, toolchain.
- [x] Build directory propre créé: `BUILD/re005-psxpcn-disc`.
- [x] CMake configuré avec `DISC_VERSION=1` effectif.
- [x] Compilation Release réussie.
- [x] Binaire généré: `BUILD/re005-psxpcn-disc/SPEC_PSXPC_N/MAIN`.
- [x] Runtime headless pur testé: SDL échoue sans serveur graphique, comme attendu.
- [x] Runtime sous Xvfb testé: SDL/OpenGL démarre.
- [x] `TOMB5.BIN/TOMB5.CUE` présents; `TOMB5.CUE` est `MODE2/2352`.
- [x] Parseur `.CUE` corrigé pour accepter `MODE2/2352` en plus de `MODE1/2352`.
- [x] Blocage runtime documenté avec backtrace Debug.
- [ ] Runtime jouable validé.
- [ ] Build 32-bit validé; tentative bloquée car `libglew-dev:i386` / `libglew2.2:i386` indisponibles sur les dépôts configurés.

## Goal

Compiler et lancer le chemin `PSXPC_N` avec `DISC_VERSION=1` pour vérifier que le repo peut charger `TOMB5.BIN/TOMB5.CUE` directement.

## Context

`CONTRIBUTING.md` indique que pour utiliser un ISO `.BIN/.CUE` avec l'émulateur, les fichiers doivent être nommés `TOMB5.BIN/TOMB5.CUE` et `DISC_VERSION=1`. Dans `SPEC_PSXPC_N/CMakeLists.txt`, `DISC_VERSION` est `OFF` par défaut.

## Result

Le build est validé, avec `DISC_VERSION=1` confirmé dans `flags.make`.

Le runtime progresse sous Xvfb après correction du parseur `.CUE` pour accepter le `MODE2/2352` réel de `TOMB5.CUE`, puis plante en x86_64 dans:

```text
RelocateModule(unsigned long, unsigned long*) at SPEC_PSXPC_N/FILE.C:115
S_LoadLevelFile(int) at SPEC_PSXPC_N/ROOMLOAD.C:100
DoTitle(unsigned char, unsigned char) at GAME/GAMEFLOW.C:971
DoGameflow() at GAME/GAMEFLOW.C:261
main(int, char**) at SPEC_PSXPC_N/PSXMAIN.C:121
```

Diagnostic probable: code `PSXPC_N` fortement 32-bit, avec nombreux casts pointeur ↔ `int`/`unsigned int`; le binaire Linux 64-bit tronque/reconstruit des adresses pendant la relocation.

## Documentation

Détails, commandes et logs résumés dans:

- `docs/reverse/build-psxpcn-disc-version.md`

## Proposed files

- Modified: `CMakeLists.txt`
- Modified: `EMULATOR/TYPES.H`
- Modified: `EMULATOR/LIBGPU.C`
- Modified: `EMULATOR/LIBCD.C`
- Modified: `GAME/SETUP.C`
- Modified: `SPEC_PSXPC_N/TITSEQ.C`
- Created: `docs/reverse/build-psxpcn-disc-version.md`

## Original acceptance criteria

- [x] Le build réussit ou les erreurs restantes sont documentées précisément.
- [x] `DISC_VERSION=1` est confirmé dans la configuration effective.
- [x] Les fichiers `TOMB5.BIN/TOMB5.CUE` sont trouvés par le runtime ou le point de blocage est identifié.
- [x] La commande de build est reproductible.
