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

## 6. Pourquoi Lara n'est pas dessinée dans la zone de la corniche

Observation (capture + gdb, 17 novembre 2026) : dans la zone de la
corniche, on voit le décor et **l'ombre de Lara, mais pas Lara**. La caméra
avance quand on marche (les entrées fonctionnent), donc ce n'est pas un
gel.

Mesures :

```
LD lara_room=12 draw_room=0 InDrawRoom=0 mesh_bits=0xffffffff
LD cam_room=8  cam_type=0 (CHASE)  flip=0
```

- La caméra se résout dans la **room 8** (`GetFloor` sur la position caméra,
  qui est au-dessus de Lara dans un empilement de salles), tandis que
  `lara_item->room_number` vaut **12** : la salle de Lara n'est donc pas
  dans la liste de rendu → `InDrawRoom=0` → elle est **culled**, seule son
  ombre reste.
- La cause est la **sauvegarde** : sa position est hors de la grille de
  cellules de la room 12 (`x=43364` alors que la grille s'arrête à
  `43008`). Le moteur le montre d'ailleurs au chargement :
  `[SAVE] applied saved position: room 26 X 40448 Y 1024 Z 51712` quand on
  tente une position « dans » la room 12 à `y=1024`.
- `GetFloor` à `(40448, y, 51712)` : `y=1024` → **room 26**, `y=1023` →
  **room 12**, `y=768` → **room 12**. La dalle de la corniche est donc
  franchie dès qu'on est pile à sa hauteur (`y >= floor`) : c'est le
  `pit_room` qui prend le relais.

**Conséquence pratique** : il ne faut pas patcher une sauvegarde à la main
dans cette zone (position hors grille ⇒ caméra dans une autre salle ⇒ Lara
invisible). Il faut **jouer** depuis un point valide et faire un `F5` en
jeu : la sauvegarde produite par le moteur contient alors une position
cohérente avec sa salle.

## 7. Point ouvert : un chargement de sauvegarde ressort au titre

Reproduit avec une sauvegarde appliquée en `room 12` (`40448,1023,51712`) :
le niveau 3 **est bien lancé** puis, en quelques frames, on revient au
titre. Traces instrumentées :

```
FL DoTitle Name=0 status=0 complete=0 currentLevel=0 gameMode=1
FL DoLevel Name=3 gfCurrentLevel=3 gameMode=4 fromTitle=1
FL DoTitle Name=0 status=1 complete=0 currentLevel=0 gameMode=0
```

`DoLevel(3)` est donc appelé correctement (`gfGameMode=4` = chargement),
puis `ControlPhase` renvoie **1** : `DoGameflow` réinitialise
(`gfInitialiseGame=1`, `gfCurrentLevel=0`) et rappelle `DoTitle`.

Éliminé par mesure :

- `reset_flag` : jamais écrit (`watch reset_flag` ne déclenche pas) ;
- `gfLevelComplete` : jamais écrit (`watch` ne déclenche pas) ;
- `Gameflow->DemoDisc = 0`, `InputTimeout = 18000` → ce n'est **pas** le
  timeout de démo de `ControlPhase`.

Restent les autres `return 1` de `ControlPhase` (menu pause, `S_Death()`,
ou une branche de `demo_mode`). À trancher avec un point d'arrêt posé sur
les sites `return 1` **dans la boucle in-level** (attention : la table de
lignes de `CONTROL.C` est décalée dans gdb, un `break CONTROL.C:1291`
retombe sur la ligne 1642 — utiliser les numéros de fonction/compteur
plutôt que les lignes). Piste prioritaire : `lara.death_count > 90 →
S_Death()` si la sauvegarde restaure un `death_count` incohérent.

## 8. Démarrer une partie : la touche de validation est `c`, pas `x`

Point qui a bloqué toutes les tentatives de test : dans les menus, la
validation est **`c`** (action), pas `x`.

`EMULATOR/INPUTMAP.C` :

```c
{ "action", "confirm", INPUTMAP_IN_ACTION, INPUTMAP_RAW_CROSS },
{ "jump",   "jump",    INPUTMAP_IN_JUMP,   INPUTMAP_RAW_SQUARE },
```

Les menus testent `RawEdge & IN_CROSS` (bit `0x4000`) : seule la touche
mappée sur l'action (« confirm ») valide. `x` ne produit que
`INPUTMAP_RAW_SQUARE` (saut) et **ne valide rien**.

Recette vérifiée en conditions réelles :

1. lancer le jeu (sans `TOMB5_AUTOLOAD`) ;
2. au titre, appuyer sur **`c`** — éventuellement plusieurs fois à ~4 s
   d'intervalle, car le titre joue une **attract-mode** (demo) pendant
   laquelle les entrées sont ignorées (`title_controls_locked_out`) ;
3. le niveau démarre (`Handle cutseq triggering name: 1` dans le log) et
   Lara est **visible**, caméra derrière elle, contrôles au clavier
   (`Up` avant, `Left`/`Right` rotation, `x` saut, `c` action).

### Sauvegarde F5 : valide, contrairement aux sauvegardes patchées

```
[SAVE] wrote TOMB5.SAV: level 1 room 2 X 46592 Y 0 Z 35779, level data 586 bytes
```

`F5` produit une sauvegarde **cohérente avec la salle** de Lara. C'est la
seule source fiable de point de reprise : les positions écrites à la main
dans `TOMB5.SAV` peuvent être hors grille (⇒ caméra dans une autre salle,
Lara culled — cf. § 6).

Cela confirme au passage que l'invisibilité observée dans la zone de la
corniche est bien un artefact de sauvegarde patchée : en niveau 1, avec une
position valide, Lara se dessine parfaitement.

### Chaîne de démarrage confirmée (captures à l'appui)

```
titre (attract-mode)  --c-->  cinématique d'intro (Lara derrière des barreaux)
                            --> flyby du niveau 1 (caméra haute, Lara minuscule au fond)
                            --> gameplay : caméra derrière Lara, contrôles actifs
```

`Handle cutseq triggering name: 1` dans le log confirme l'exécution du niveau 1.
Un `Up` de 2 s déplace Lara dans la ruelle (vérifié sur capture). `F5`
produit alors une sauvegarde valide.

Sauvegarde de référence ainsi obtenue :
`/tmp/opencode/TOMB5.valid_level1.sav` (level 1, room 2, `46592,0,35779`).

### Précision sur l'invisibilité : ce n'est pas `InDrawRoom`

`InDrawRoom` n'est **jamais écrit** dans le port (déclaré dans `STYPES.H`,
aucune affectation) : la valeur `0` observée ne prouve donc rien. Les
conditions réelles de rendu de Lara (`SPEC_PSXPC_N/DRAWPHAS.C:382`) :

```c
if (objects[LARA].loaded && !(lara_item->flags & 0x40))
    if (lara_item->mesh_bits != 0 && SCNoDrawLara == 0)
        switch (LaraDrawType) { ... DrawLaraL1/L2 ... }
```

Mesures sur la sauvegarde corniche (room 12, position hors grille) :
`SCNoDrawLara = 0`, `lara_item->flags = 0x0`, `mesh_bits = 0xFFFFFFFF`,
`bUseSpotCam = 0`, `current_spline_camera = 2` → **toutes les conditions
de rendu sont réunies**, et pourtant Lara n'apparaît pas (vérifié en
zoomant et en poussant la luminosité ×3 : que du sol).

En revanche, en partie normale (niveau 1, position issue d'une sauvegarde
`F5`), Lara est parfaitement rendue. La différence est donc bien la
**position de sauvegarde invalide** (hors grille de la room 12) qui alimente
le pipeline de matrices de Lara. Conclusion opérationnelle inchangée :
jouer depuis une nouvelle partie, sauvegarder avec `F5`.
