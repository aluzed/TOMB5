# RMIG-007 — captures déterministes 32/64 bits

Ce dossier contient la scène de référence et les captures produites par le
harnais déterministe.

## Scène

- Niveau 3 (`TOMB5_START_LEVEL=3`), aucune sauvegarde, aucune entrée.
- 1800 frames de contrôle après le chargement du niveau.
- Capture à la frame 1799 (WMV/BMP lu par `Emulator_TakeScreenshot`).
- Graine aléatoire fixe du jeu (`SetupGame`, `0xD371F947`).

Le harnais est activé par les variables suivantes (lues dans `DoLevel`) :

```
TOMB5_FRAMES=1800
TOMB5_CAPTURE=/tmp/cap.bmp
# optionnel :
TOMB5_REPLAY=fichier     # lignes "frame pad_hex" (pad PSX actif haut)
TOMB5_SAVE_PATH=...      # sauvegarde propre au binaire
```

À la dernière frame, le jeu écrit la capture, affiche
`[REPLAY] captured frame N`, puis quitte avec le code 0.

## Commandes

Build 64 bits (Vulkan par défaut depuis RMIG-012 ; ajouter
`TOMB5_RENDERER=gl` pour capturer avec OpenGL — les deux rendus donnent
le même BMP) :

```
cd build/porting/data-ntsc
DISPLAY=:1 SDL_AUDIODRIVER=dummy TOMB5_AUTOLOAD=1 \
  TOMB5_START_LEVEL=3 TOMB5_FRAMES=1800 TOMB5_CAPTURE=/tmp/cap64.bmp \
  ../build64/SPEC_PSXPC_N/MAIN
```

Build 32 bits :

```
cd build/porting/data-ntsc
DISPLAY=:1 SDL_AUDIODRIVER=dummy TOMB5_AUTOLOAD=1 \
  TOMB5_START_LEVEL=3 TOMB5_FRAMES=1800 TOMB5_CAPTURE=/tmp/cap32.bmp \
  ../build32-check/SPEC_PSXPC_N/MAIN
```

## Résultats (18 novembre 2026)

Deux exécutions du **même** binaire donnent des BMP **identiques** :

| binaire | sha256 |
| --- | --- |
| 32 bits (OpenGL) | `63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b` |
| 64 bits (Vulkan) | `63041e5cbf6dcbbd27377b78d6c63e9593743b17690b3c310fefa146e48e3a9b` |

> **19 novembre 2026** — la référence 64 bits a changé : le correctif `MULFP`
> (multiplication fixe PSX tronquée à 32 bits) répare la position de spline
> des caméras flyby, qui partait en valeurs absurdes en LP64. L'ancienne
> référence `5dbbb251…` correspond à la révision précédente ; elle avait été
> vérifiée identique entre Vulkan et OpenGL 64 bits. Le code du jeu étant
> commun aux deux backends, le correctif modifie les deux de la même façon ;
> re-vérifier la parité GL/Vulkan demanderait un build 64 bits `PORT_ALLOW_GL`.
> La référence 32 bits, elle, ne change pas (`51d3a1c7…`) : en ILP32 `MULFP`
> tronquait déjà naturellement.

> **Correction du 18 novembre 2026** — les hashes publiés auparavant
> (`083d24a0…` en 32 bits et `675e2c8d…` en 64 bits) provenaient d’une
> capture dont les canaux rouge et bleu étaient inversés :
> `glReadPixels(GL_RGBA)` était sauvegardé avec les masques SDL par défaut
> (BGRA). Le rendu OpenGL était correct à l’écran, seule la capture était
> fausse. Les images et hashes ci-dessus sont les références valides ; le
> détail est dans `docs/porting/vulkan-64bit-plan.md` §38.

L'état de jeu est identique à la capture : Lara
`pos=(90642,4608,52736) room=20 rot=-16384 anim=103 frame=1611` dans les
deux builds. La géométrie et la pose sont donc alignées.

**Écart 32/64 : nul.** Depuis les correctifs `MULFP` + pointeurs de meshes
(natte, holsters, joints de peau), les deux builds produisent le **même BMP,
octet pour octet** (même sha256, `cmp` identique, 307 200 pixels identiques).

```
mean_abs_diff=0.000
global_gain=1.000000
pixels_within_8_after_gain=307200 (100.00%)
```

Avant ce correctif l'écart était de `mean_abs_diff=18.730` avec seulement
26,12 % de pixels à ±8 : la caméra flyby partait dans des positions
absurdes en 64 bits.

Le 64 bits est globalement plus sombre, y compris sur le HUD (icône des
pistolets), donc l'écart n'est pas seulement dû à l'éclairage 3D. Il est
documenté ici et suivi dans **RMIG-012** : c'est un écart **32 bits ↔ 64
bits** du rendu commun (le backend Vulkan reproduit, lui, la référence 64
bits au pixel près).

Les BMP sont stockés en PNG dans ce dossier (`ref32.png`, `ref64.png`,
`diff32_64.png`, `side32_64.png`). L'image est verticalement inversée
(`glReadPixels` bas-en-haut) ; le backend Vulkan applique le même
retournement dans `RendererVK_RequestCapture`, les deux captures sont donc
directement comparables.

## Parité Vulkan (18 novembre 2026)

Le backend Vulkan, lancé avec `TOMB5_RENDERER=vulkan` sur la même scène,
produit une capture **octet pour octet identique** à la référence 64 bits
OpenGL (`cmp` sans différence, 307 200 pixels identiques) :

```
TOMB5_RENDERER=vulkan TOMB5_START_LEVEL=3 TOMB5_FRAMES=1800 \
  TOMB5_CAPTURE=/tmp/capvk.bmp ...
# [VK] capture saved /tmp/capvk.bmp (640x480) format=44
# sha256 5dbbb25184d54d96c95aed1c96494ade0e390956e7c0de1da262180779e269a8
```

L'écart 32/64 bits ci-dessus reste, lui, un vrai écart de rendu (64 bits
plus sombre, HUD compris) à traiter dans RMIG-012.
