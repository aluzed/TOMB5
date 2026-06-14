# RE-005 — Valider le build PSXPC_N avec image disque

Status: Done — build OK, runtime non jouable mais blocage documenté précisément
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
- [x] Blocage runtime initial documenté avec backtrace Debug dans `RelocateModule()`.
- [x] Crash `RelocateModule()` expliqué/reproduit: `RELOC=0` effectif, mais `S_LoadLevelFile()` appelait quand même la relocation du `SETUP.MOD` PSX.
- [x] Correctif minimal appliqué: ne relocaliser `SETUP.MOD` que si `RELOC=1`, comme le chemin `SPEC_PSX`.
- [x] Runtime sous Xvfb progresse au-delà de `RelocateModule()` jusqu'à `LoadLevel()`.
- [x] Blocage runtime restant documenté avec backtrace Debug dans `LoadLevel()`.
- [ ] Runtime jouable validé.
- [ ] Build 32-bit validé; tentative bloquée car `libglew-dev:i386` / `libglew2.2:i386` indisponibles sur les dépôts configurés.

## Goal

Compiler et lancer le chemin `PSXPC_N` avec `DISC_VERSION=1` pour vérifier que le repo peut charger `TOMB5.BIN/TOMB5.CUE` directement.

## Context

`CONTRIBUTING.md` indique que pour utiliser un ISO `.BIN/.CUE` avec l'émulateur, les fichiers doivent être nommés `TOMB5.BIN/TOMB5.CUE` et `DISC_VERSION=1`. Dans `SPEC_PSXPC_N/CMakeLists.txt`, `DISC_VERSION` est `OFF` par défaut.

## Result

Le build est validé, avec `DISC_VERSION=1` confirmé dans `flags.make`.

Le runtime progresse sous Xvfb après correction du parseur `.CUE` pour accepter le `MODE2/2352` réel de `TOMB5.CUE`.

Le premier crash x86_64 était dans:

```text
RelocateModule(unsigned long, unsigned long*) at SPEC_PSXPC_N/FILE.C:115
S_LoadLevelFile(int) at SPEC_PSXPC_N/ROOMLOAD.C:100
DoTitle(unsigned char, unsigned char) at GAME/GAMEFLOW.C:971
DoGameflow() at GAME/GAMEFLOW.C:261
main(int, char**) at SPEC_PSXPC_N/PSXMAIN.C:121
```

Diagnostic confirmé: `RELOC=0` est effectif pour `PSXPC_N`, mais `S_LoadLevelFile()` appelait quand même `RelocateModule()` sur des données PSX. Ce chemin est maintenant gardé par `#if RELOC`, comme `SPEC_PSX/ROOMLOAD.C`.

Après ce correctif, le runtime va plus loin et plante dans:

```text
LoadLevel() at GAME/SETUP.C:1204
S_LoadLevelFile(int) at SPEC_PSXPC_N/ROOMLOAD.C:108
DoTitle(unsigned char, unsigned char) at GAME/GAMEFLOW.C:971
DoGameflow() at GAME/GAMEFLOW.C:261
main(int, char**) at SPEC_PSXPC_N/PSXMAIN.C:121
```

Blocage restant: le chargement lit des structures disque PSX contenant des pointeurs/offsets 32-bit dans des types C hôtes (`short*`, `long`, etc.) dont la taille/alignment change en Linux x86_64. Exemple observé: `room[i].data` devient un pointeur invalide lors de la relocation locale des rooms dans `LoadLevel()`.

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
- Modified: `SPEC_PSXPC_N/ROOMLOAD.C`
- Created: `docs/reverse/build-psxpcn-disc-version.md`

## Original acceptance criteria

- [x] Le build réussit ou les erreurs restantes sont documentées précisément.
- [x] `DISC_VERSION=1` est confirmé dans la configuration effective.
- [x] Les fichiers `TOMB5.BIN/TOMB5.CUE` sont trouvés par le runtime ou le point de blocage est identifié.
- [x] La commande de build est reproductible.
