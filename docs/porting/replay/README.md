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

Build 64 bits :

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
| 32 bits, run 1 | `083d24a01588e14023b5f2ddb654dcaee278a58d9ce9e4a7fa443a6d7f7750b6` |
| 32 bits, run 2 | `083d24a01588e14023b5f2ddb654dcaee278a58d9ce9e4a7fa443a6d7f7750b6` |
| 64 bits, run 1 | `675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b` |
| 64 bits, run 2 | `675e2c8da064bfefb4dcb4347f7629d5e114026bb0082c78b584ede61a9b651b` |

L'état de jeu est identique à la capture : Lara
`pos=(90642,4608,52736) room=20 rot=-16384 anim=103 frame=1611` dans les
deux builds. La géométrie et la pose sont donc alignées.

Écart 32/64 (script `scripts/porting/capture_compare.py`) :

```
mean_abs_diff=18.730
global_gain=0.965212
mean_abs_diff_after_gain=18.787
pixels_within_8_after_gain=80234 (26.12%)
```

Le 64 bits est globalement plus sombre, y compris sur le HUD (icône des
pistolets), donc l'écart n'est pas seulement dû à l'éclairage 3D. Il est
documenté ici et reporté dans **RMIG-012** (parité visuelle / retrait
d'OpenGL) : le backend Vulkan devra reproduire la référence 32 bits.

Les BMP sont stockés en PNG dans ce dossier (`ref32.png`, `ref64.png`,
`diff32_64.png`, `side32_64.png`). L'image est verticalement inversée
(`glReadPixels` bas-en-haut), mais la comparaison est cohérente.
