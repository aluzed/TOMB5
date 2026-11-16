# The Colosseum — parcours et recette de test

État au 17 novembre 2026. Ce document résume le **chemin voulu par le
niveau**, les mécaniques à attendre salle par salle, et la recette pour
rejouer/tester sans perdre du temps à réinstrumenter l'environnement.

## 1. Chemin de progression (calculé depuis les données du niveau)

Graphe des portails (`door`) + liens verticaux (`pit_room`/`sky_room`),
obtenu avec `scripts/porting/decode_level_floordata.py` /
`render_level_map.py` :

| salle | sol | contenu / rôle |
| --- | --- | --- |
| 12 | 1024 | **départ** (LARA), corniche |
| 26 | 3072 | puits **sous** la corniche |
| 27 | 3072 | passage |
| 108 | 1024 | 4 triggers (CD 57, objets 29/26) |
| **15** | 1024 | `CLOSED_DOOR1/2`, **GLADIATOR**, `KEY_HOLE1` |
| 18 | 1024 | passage |
| 100 | 512 | 2 triggers (obj 25) |
| **90** | 512 | **ROMAN_GOD** (antenne de 100), `RAISING_BLOCK1` ×2 |
| **102** | 512 | `KEY_HOLE2`, `CLOSED_DOOR2` |
| 110 → 83 → 111 → 85 | 2816 → 4352 → 4352 → 5888 | transitions (CD dans 85) |
| **70** | 7936 | **`PICKUP_ITEM1`** → `TO_FINISH` |

Ordre attendu : lions → gladiateur + clé 1 (15) → portes → réceptacle
(102) → combat du ROMAN_GOD (90) → clé 2 → pierre (70) → fin de niveau.

**Entrée dans la salle 26 mesurée** (`GetFloor` à `y=1024`, `z=53760`,
en partant de la room 12) :

```
x=43520 … x=39936  room=26  (hors grille de la room 12, bascule immédiate)
x=39424            room=26  height=1151  idx=1089
x=38912            room=26  height=1151  idx=1089
x=38400            room=12  height=-32512 (plus de sol)
```

Autrement dit la bascule 12 → 26 se fait à l'**extrémité ouest** de la
corniche (`x≈39424`), sur une marche de l'ordre de 100 à 400 unités — pas
une chute de 2048. C'est un simple pas vers l'ouest en bout de corniche.

**Branche latérale sans issue** : salles 8 / 14 / 25 / 92 (dalles à
temporisation + pont `ANIMATING15_MIP`). Le fameux « bouton du crawlspace »
n'existe pas dans les données.

## 2. Mécaniques à connaître

- **Dalles qui s'effondrent** (`CRUMBLING_FLOOR`) : l'OCB est une
  temporisation (`1, 5, 10, 20, 30, 40, 50, 70, 80, 100, 120`). Stationner
  sur une dalle la fait céder → chute dans les salles 26/14 (`y=6144`,
  mortelle). Il faut traverser sans s'arrêter.
- **Trappes** (`TRAPDOOR1..3`, salles 65/81) : handlers assignés
  (`InitialiseTrapDoor`/`TrapDoorControl`/collisions).
- **Émetteurs de flammes** (salles 20, 59, 81) : `FlameEmitterControl`
  porté (jet OCB négatif, `FireCollision`, `LaraBurn`).
- **Séisme** (salle 8) : `EarthQuake` porté (bounce caméra + réveil des
  émetteurs).
- **Statue / boss** : `ROMAN_GOD` porté et validé (éclairs, shockwaves,
  1000 → 724 PV aux tests).

## 3. Recette de test (Linux32, sans perdre de temps)

```sh
# 1. préparer la sauvegarde de reprise (format v4, 8658 octets)
cp /tmp/opencode/TOMB5.corniche.sav build/porting/data-ntsc/TOMB5.SAV

# 2. lancer avec autoload (le jeu relit la sauvegarde au titre)
cd build/porting/data-ntsc
DISPLAY=:1 SDL_AUDIODRIVER=dummy TOMB5_AUTOLOAD=1 \
  ../../build-gameplay59/build/SPEC_PSXPC_N/MAIN

# 3. capture d'écran de la fenêtre (vérité terrain)
W=$(xdotool search --name "Tomb Raider" | head -1)
import -window $W /tmp/shot.png
```

Points importants :

- `[EMU] Initialising Emulator` peut sortir après **60 à 200 s** (init
  GL/audio) ; stdout est bufferisé. Un log muet n'est pas un blocage —
  préférer une capture de fenêtre.
- **Clavier** (fonctionne depuis le correctif `kbInputs | controllerInputs`) :
  `Up` avant, `x` saut, `c` action, `Left`/`Right` rotation,
  `Shift_R` marche, `Control_L` accroupi.
- Une sauvegarde dont le champ `room` vaut **8** démarre sur une
  cinématique figée ; rester en **room 12** (positions `43364,768,52325` ou
  `43520,768,51712`, `y=768`) qui sont les seules positions de reprise
  vérifiées.

### Piloter sans clavier (déterministe, pour reproduire un point précis)

```gdb
break LaraControl
commands
silent
set var input = 1        # IN_FORWARD ; NE PAS écrire "set input" (sous-commande gdb)
continue
end
```

Bits : `IN_FORWARD=0x1`, `IN_BACK=0x2`, `IN_LEFT=0x4`, `IN_RIGHT=0x8`,
`IN_JUMP=0x10`, `IN_ACTION=0x40`, `IN_WALK=0x80`.
On peut aussi forcer `lara_item->pos.y_rot` (`0`=+z, `0x4000`=+x,
`-16384`=-x, `-32768`=-z) pour changer de cap sans attendre la rotation.

## 4. À implémenter (sans impact bloquant sur ce parcours)

| élément | état | impact |
| --- | --- | --- |
| `ControlScaledSpike` + `DrawScaledSpike` | stubs | dents de la salle 124 et rendu *scalé* des `RAISING_BLOCK` (les blocs restent visibles via le rendu standard) |
| `ControlRollingBall` | stub | la bille de la salle 13 ne roule pas (hors parcours) |
| `SteamLasers`, `Fishtank` | absents | salle 8 (branche latérale) |
| `ControlTeleporter` | stub | téléporteur de la salle 8 (inactif) |
| `DrawWeaponMissile`, `phd_PutPolygons_train` | stubs | arbalète/missiles non rendus |
| Rendu de corde | absent | corde invisible |
| `UpdateFireSparks`, `UpdateGunShells`, `UpdateRats`, `UpdateBats` | stubs | effets/objets secondaires |
| `FixedCamera` | absent | caméras fixes |
| Sélection de niveau | cassée | Trajan's Markets démarre le niveau 1 |
| Audio | non validé | écoute humaine requise |

## 5. Comportement mesuré au bord de la corniche

Depuis la sauvegarde corniche (`43364,768,52325`, `y_rot=-16384`) :

- **saut sur place** (`IN_JUMP` seul) : `state=28` (JUMP_UP), `y` 768 → 14 →
  768, retour exact au point de départ, `speed=2` — le saut vertical ne fait
  pas avancer ;
- **saut + avant** (`IN_FORWARD|IN_JUMP`) : `state=14`
  (GRAB_TO_FALL) puis retour `state=2` **au même endroit** : le rebord est
  agrippable, Lara s'y raccroche ;
- **marche seule** : arrêt net à `x=43109`, qui est le bord de la grille de
  la room 12 (`x_size=5` → fin à `43008`) ; au-delà il n'y a aucun sol.

Pour descendre vers la salle 26 il faut donc une manœuvre volontaire
(agripper le rebord puis se lâcher, ou saut avec élan depuis plus loin) —
c'est le premier point à faire à la main.
