# Linux32 / PSXPC_N — recette reproductible (PORT-001)

Cadrage de travail **provisoire**, pas une décision définitive de plateforme. Cette
recette construit les sources du checkout ; elle ne télécharge aucun jeu. Un
build réussi ou une sortie zéro ne valide ni menu ni gameplay.

**État au 29 octobre 2026** : le backend Linux32 (rendu, entrées, sauvegarde
rapide, audio SDL) est stable et testé. Une **première couche d'interactions
gameplay** est désormais présente (dispatch des collisions d'objets, pickups,
serrures, puzzles, switchs, collisions de portes). Les portes n'ont toutefois
pas encore d'initialiseur de données, les ennemis/combat restent des stubs et
la campagne réelle n'est pas jouée. Détail : sections « Cause racine héritée »
et « Boucle de gameplay — première couche » plus bas.

## Environnement et dépendances

Recette exécutée le 18 septembre 2026 sur Linux x86-64, GCC/G++ 13.2,
SDL2 2.30.0 i386, libgl-dev 1.7.0 i386, GLEW 2.2.0 compilé localement en i386.
Python >=3.11.8 (filtre d'extraction tar), CMake, make, curl et toolchain multilib
sont nécessaires. Sur Ubuntu/Debian, préparer explicitement les dépendances
(ces commandes changent le système ; le driver **ne les exécute pas**) :

```sh
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install gcc-multilib g++-multilib cmake make curl \
  libsdl2-dev:i386 libgl-dev:i386 libegl-dev:i386 libgles-dev:i386
```

L'ensemble de ces commandes d'installation n'a pas été rejoué sur machine
vierge. Les bibliothèques i386 étaient déjà installées sur l'hôte de validation.
Le paquet GLEW i386 n'est pas présumé disponible : on reconstruit sa dépendance
à partir de l'archive officielle, dans **chaque** répertoire de build neuf.

```sh
mkdir -p build/porting/downloads
curl -fL https://downloads.sourceforge.net/project/glew/glew/2.2.0/glew-2.2.0.tgz \
  -o build/porting/downloads/glew-2.2.0.tgz
sha256sum build/porting/downloads/glew-2.2.0.tgz
# d4fc82893cfb00109578d0a1a2337fb8ca335b3ceccf97b97e5cc7f08e4353e1
python3 scripts/porting/linux32.py build \
  --glew-archive build/porting/downloads/glew-2.2.0.tgz \
  --output build/porting/build-a
python3 scripts/porting/linux32.py build \
  --glew-archive build/porting/downloads/glew-2.2.0.tgz \
  --output build/porting/build-b
```

L'empreinte est un pin de contenu, pas une certification de signature éditeur.
Les sorties existantes sont refusées : choisir un nouveau nom, ne pas nettoyer
les anciennes preuves. Les sorties doivent être sous un chemin Git ignoré du
checkout. Aucun chemin runtime-1058 n'est utilisé. Le driver impose `-m32`,
`DISC_VERSION=ON`, `DEBUG_VERSION=OFF`, `Debug`, compile GLEW et le jeu, vérifie
ELF32/i386 ainsi que les bibliothèques résolues par `ldd`. Il conserve séparément
les commandes, dates, durées, codes de sortie et logs de compilation. Les flags
effectifs sont dans `build/compile_commands.json` et `build/CMakeCache.txt`.
Les versions, réglages et dépendances de l'hôte restent des entrées de la recette ;
il ne s'agit pas encore d'un conteneur hermétique.

## Données et lancement borné

Fournir **vos propres données légalement obtenues** : un répertoire contenant
`TOMB5.CUE` et le BIN qu'il référence. Le sous-ensemble accepté par le lanceur
est volontairement étroit : une seule piste 01, `MODE1/2352` ou `MODE2/2352`,
`INDEX 01 00:00:00`, nom de fichier ASCII entre guillemets, au plus 125 octets,
sans espace ni sous-répertoire (limite du compteur natif signé).
L'image doit être non vide et contenir des secteurs complets de 2352 octets.
Le jeu ouvre le CUE puis son BIN depuis le **répertoire courant** ; le lanceur
fixe donc celui-ci à `--data-dir`. Il ne convertit ni ne redistribue les données.
Les fichiers extraits DATA ne sont pas un prérequis de cette configuration DISC.
Ces contrôles ne certifient pas que l'image contient la bonne version du jeu.
Utiliser un répertoire privé ignoré pour les données et éventuels fichiers runtime.

```sh
ulimit -c 0
python3 scripts/porting/linux32.py launch \
  --binary build/porting/build-a/build/SPEC_PSXPC_N/MAIN \
  --data-dir /chemin/prive/mes-donnees \
  --output build/porting/launch-a --seconds 30
# Hôte sans écran : préfixer la même commande par xvfb-run -a
```

Fermer avec la croix de la fenêtre (événement SDL de fermeture). Sous Xvfb sans
gestionnaire de fenêtres, un `WM_PROTOCOLS/WM_DELETE_WINDOW` à l'identifiant
vérifié de la fenêtre du jeu reproduit cette demande ; tuer le serveur X n'est
pas une fermeture normale. `application.json` enregistre le code du processus
`timeout` : **0 avant la limite** après demande de fermeture a été observé ;
**124** signifie limite atteinte, pas succès applicatif. `timed_out` indique
séparément le timeout de sécurité du recorder Python. Un signal/crash reste
un échec même si un outil de capture retourne zéro.

`provenance.json` contient les hashes du binaire et des données avant lancement.
Les captures restent privées, accompagnées d'identité fenêtre, heure et hash du
binaire. Les pixels de la nouvelle capture ont été décodés et sont non vides ;
aucune validation visuelle du menu ou du gameplay n'est revendiquée.

## Échecs attribuables et remèdes

- CUE/BIN absent ou format hors sous-ensemble : refus explicite avant le lancement,
  exit 2 ; fournir les deux fichiers et le répertoire correct. Le parser natif
  historique ne gère pas tous ces échecs proprement ; il n'est pas corrigé ici.
- Archive GLEW absente/corrompue : diagnostic fichier ou SHA256 ; télécharger à
  nouveau depuis l'URL officielle, ne pas modifier l'empreinte pour faire passer.
- Échec `-m32`, SDL/OpenGL introuvable : lire `configure.log` / `glew-build.log`,
  installer les dépendances **i386** et multilib puis utiliser une sortie neuve.
- Bibliothèque runtime absente : `libraries.log` identifie le nom ; conserver
  le répertoire GLEW construit et installer la dépendance d'architecture correcte.
- Binaire ELF64/autre architecture : refus explicite ; ne pas tenter de promouvoir
  une compilation native64 en validation de ce port.

## Interruption du recorder — checkpoint RE-957

Une interruption Python pendant l’attente (`KeyboardInterrupt` ou `SystemExit`)
ferme désormais le groupe enfant par SIGKILL, attend l’enfant direct et conserve
son code de sortie dans le journal avant de propager l’exception originale.
`interrupted` nomme la classe ; `timed_out` reste réservé au timeout du recorder.
Deux tests sur de vrais sous-processus Python vérifient aussi le descendant,
sans données de jeu. Le cas SystemExit utilise un handler SIGTERM de test :
le driver n’installe pas de handler SIGTERM par défaut. Mort brutale, descendants
hors groupe ou nouvelle interruption pendant cleanup ne sont pas garantis.
Voir [RE-957](../stories/RE-957-linux32-recorder-interruption.md).

## Réservation des journaux — checkpoint RE-958

Si un log existe déjà (fichier ou répertoire), le recorder le conserve et refuse
le démarrage. Le nouveau JSON réservé consigne maintenant l’erreur, la fin et la
durée ; aucun code de sortie natif n’est inventé sans enfant. Un JSON préexistant
reste totalement inchangé. Les échecs de démarrage (exécutable/cwd absent) étaient
déjà consignés : deux contrôles les caractérisent sans prétendre les corriger.
La paire JSON/log n’est pas atomique ; erreurs de création JSON/écriture finale,
disque plein et tiers modifiant le répertoire ne sont pas garantis ici.
Voir [RE-958](../stories/RE-958-linux32-recorder-reservation.md).

## Labels du recorder — checkpoint RE-959

L’API `record()` accepte uniquement un label de 1 à 128 caractères ASCII :
lettre/chiffre initial, puis lettres, chiffres, point, tiret ou underscore.
Ce nom est un basename, jamais un chemin relatif/absolu ; les valeurs invalides
sont refusées avant création de fichier ou lancement d’enfant. Les labels
constants de la CLI sont inchangés. Ce contrôle n’isole pas le répertoire contre
un tiers concurrent et ne rend pas la paire JSON/log atomique.
Voir [RE-959](../stories/RE-959-linux32-recorder-labels.md).

## Clone neuf — vérification du 27 octobre 2026

Vérification non indépendante, sur un clone neuf de `b5411b6b`, sans les preuves
privées historiques (`build/reverse/` est gitignoré et absent du clone).

- **Prérequis manquants sur cet hôte** : pytest/pip, en-têtes C++ 32 bits
  (`g++-multilib`), `GL/glu.h` (`libglu1-mesa-dev`) et les en-têtes GLEW.
  Sans sudo, les paquets amd64 de développement ont été extraits dans un sysroot
  local (`/tmp/opencode/sysroot`) et exposés via `CPLUS_INCLUDE_PATH` et
  `LIBRARY_PATH` ; ce n'est pas une installation système documentée.
  `build/porting/*` doit être gitignoré : la règle manquait dans le `.gitignore`
  du clone, le driver refusait donc toute sortie. Règle ajoutée.
- **Suites** : `tests/porting` 479 PASS ; `tests/emulator` 3 676 PASS.
  `tests/reverse` : 4 349 PASS, 117 FAIL, 1 skip (`--ignore=tests/reverse/fixtures`,
  car un fixture `run_test.py` consomme des arguments au chargement). Ces FAIL
  sont documentaires/historiques : exports Ghidra privés absents
  (`build/reverse/re007/...`, `ghidra-functions.csv`) et snapshots HTML/compteurs
  non régénérés depuis les jalons RE-7xx/RE-9xx. Ils ne sont pas des régressions
  du code de jeu et ne peuvent pas être rendus verts sans réécrire des archives
  historiques.
- **Builds** : deux builds ELF32 i386 neufs depuis le même commit avec GLEW 2.2.0
  recompilé dans chaque sortie. SHA256 : `build-a`
  `83949e680e079e55f9b13646617d737a1ff477aeb9609cc46fa68666a74d4897`,
  `build-b` `99e32bcf5d22a1394c448c8aa51a2fd2fa5eb2c1f98e336827cc8f3ef58b6094`
  (identité bit-à-bit non exigée).
- **Données** : image PAL `SLES_033.31` et image NTSC `SLUS_013.11` toutes deux
  converties en `TOMB5.CUE`/`TOMB5.BIN` (le nom d'origine avec espaces est refusé).
  L'image NTSC extraite a le MD5 `353003caeb688458bb6e8b1c824a6bdc`, **différent**
  de la référence documentée `4EF523E708D7A7D6571F39C6E47784F9` : ce n'est pas la
  révision exacte du baseline. Les deux images atteignent le titre.
- **Lancement** : capture du splash légal puis du menu titre (`New Game` /
  `Special Features`) vers 35–50 s, fermeture par vrai `WM_DELETE_WINDOW`,
  `application.json` exit 0 avant la borne, zéro erreur X.
- **PORT-002 observé, trois lancements neufs** : `port002-20261027c/run1..3`
  montrent le menu à 35 s ; `Down` sélectionne `Special Features`, `Up` revient
  à `New Game` (captures et variance temporelle concordantes sur les trois).
  `special-features-20261027/` montre l'ouverture par `Cross` puis le retour au
  menu principal par `Triangle` (`03-special-features.png`, `04-back-main.png`).
  `launch-newgame2..4` : `Cross` sur la sélection par défaut quitte le menu,
  cinématique puis scène de Rome à 60 s, `application.json` exit 0 à chaque fois.
  Vérification non indépendante, sans revue : aucun statut Done n'est attribué.
- **Fenêtre d'interaction du titre** : après ~50 s, la séquence de cutscene /
  `DEMO MODE` peut prendre la main et les touches sont ignorées. Faire les
  interactions dans la fenêtre 30–45 s, ou relancer. Les runs où `Cross` a été
  envoyé trop tard ont fini en `DEMO MODE`, pas dans une partie.
- **Focus X11 (Xvfb, 28 octobre)** : `xdotool windowactivate --sync <id>` peut
  retourner 0 sans donner le focus (le focus reste sur une autre fenêtre) ;
  `xdotool getwindowfocus` le révèle. Utiliser `xdotool windowfocus --sync
  <id>` puis vérifier que l'ID obtenu est celui de `MAIN` avant d'envoyer une
  touche. C'est la cause des derniers échecs d'automatisation du titre.
- **Clavier AZERTY** : le scancode SDL compte, pas le keysym. `xdotool key z`
  envoie le scancode `W` sur cet hôte AZERTY (donc pas `Triangle`) ; utiliser
  `w` (position physique de Z) pour `Triangle`, `c` pour `Cross`, `z`/`x`/`v`
  pour les autres boutons seulement sur un layout QWERTY. Flèches inchangées.
- **Lecture de la sélection** : l'option sélectionnée utilise le style 1 (gris
  pulsant), l'option non sélectionnée le style 2 (blanc). Un seuil de blancheur
  sur une seule frame peut donc inverser la lecture ; une variance sur ~12
  frames espacées de 0,15 s est fiable. Une pression trop courte peut aussi
  être ignorée : préférer `keydown`, pause de 500 ms, puis `keyup`.
- **HUD debug** : la scène affiche `Camera X/Y/Z` (`GAME/HEALTH.C`,
  `#if 1//GH0ST_TESTING`). Ce n'est pas un défaut de portage, mais il devra être
  retiré avant une recette visuelle propre.
- **Piège de fermeture** : `xdotool windowclose` appelle `XDestroyWindow`, pas
  `WM_DELETE_WINDOW`. Il détruit la fenêtre sous le client et produit
  `GLXBadDrawable`/`BadWindow (XInputExtension)` puis exit 1. Il faut envoyer un
  `ClientMessage` `WM_PROTOCOLS`/`WM_DELETE_WINDOW` (le menu contextuel d'un
  gestionnaire de fenêtres fait cela). Ne pas interpréter l'exit 1 de
  `windowclose` comme un défaut du jeu.

## Keymap configurable — 28 octobre 2026

Le port lit `INPUT.CFG` au démarrage. Ordre de résolution :
`TOMB5_INPUT_CONFIG`, puis `INPUT.CFG` du répertoire courant, puis
`input.cfg` du chemin préférentiel SDL (`SDL_GetPrefPath`). Si aucun fichier
n'existe, un fichier complet est écrit dans le répertoire courant ; en cas
d'échec d'écriture, le chemin préférentiel est utilisé. Journal :
`[INPUT] Default configuration written to …` ou `[INPUT] Configuration loaded from …`.

Format : deux colonnes par action et par device, `NONE` pour un slot vide.

```ini
[devices]
keyboard = 1
gamepad = 1
gamepad_index = 0
gamepad_guid =
axis_deadzone = 0.50

[gameplay]
use_control_option = 0

[keyboard]
forward = W, UP
action  = C, NONE

[gamepad]
forward = DPAD_UP, LEFTY-
action  = A, NONE
```

- Actions : `forward`, `back`, `left`, `right`, `action`, `jump`, `draw`,
  `roll`, `look`, `duck`, `walk`, `sprint`, `start`, `select`.
- Les noms clavier sont des **scancodes SDL** : `W` désigne la position physique
  QWERTY-W (touche Z sur AZERTY), donc le keymap est indépendant de la
  disposition. `UP`/`DOWN`/`LEFT`/`RIGHT` sont les flèches.
- Manette : boutons `A`, `B`, `X`, `Y`, `BACK`, `START`, `LEFTSHOULDER`,
  `RIGHTSHOULDER`, `LEFTSTICK`, `RIGHTSTICK`, `DPAD_*` ; axes `LEFTX-/+`,
  `LEFTY-/+`, `RIGHTX-/+`, `RIGHTY-/+`, `TRIGGERLEFT`, `TRIGGERRIGHT`.
  `gamepad_index` est l’ordinal du contrôleur (0 = première manette SDL), pas
  l’index joystick brut.
- `use_control_option = 0` (défaut) rend le keymap autoritatif pour le gameplay ;
  `1` conserve les cinq schémas PSX historiques (`savegame.ControlOption`).
- Les bits PSX bruts restent produits pour les menus/titre : `action` → Cross,
  `draw` → Triangle, directions → D-pad, `start`/`select` → Start/Select.

### Éditeur en jeu (PORT-012)

`F1` ouvre un éditeur modal depuis le titre ou une partie active. Flèches/D-pad
choisissent l’action et la colonne (clavier 1/2, manette 1/2), `Entrée`/`A`
passe en capture du prochain appui, `Échap` annule la capture ou ferme, `Tab`
ouvre l’écran Devices (`keyboard`, `gamepad`, index, GUID), `R` restaure les
défauts. Chaque modification écrit `INPUT.CFG` immédiatement ; le statut affiche
`Saved …` ou l’erreur d’écriture. L’éditeur lit SDL directement, donc il reste
utilisable même si le keymap est cassé. `ControlPhase` est gelé pendant
l’édition ; le HUD debug `Camera X/Y/Z` est masqué. F1 n’est accepté que lorsque
le chemin de dessin normal tourne (titre/jeu), pas pendant une FMV, l’inventaire
ou le menu pause.

L’écran affiche les **libellés de la disposition courante** (AZERTY : `Z`, `Q`,
`W`), tandis que le fichier stocke les scancodes physiques (`W`, `A`, `Z`).

Vérification locale : 17 tests keymap, suite porting 496 PASS, build `build-j`
ELF32 i386 (SHA256 `30c014c2ca3ce1dac76dc932a529e2f8b9fb51a61444e82bc4cd1a46da233626`).
`C` sur `New Game` atteint la scène de Rome
(`build/porting/launch-inputmap-default`) ; avec `action = SPACE`,
`Espace` la remplace et atteint la même scène
(`build/porting/launch-inputmap-custom`). Modification via l’éditeur :
`action` clavier 2 = `SPACE`, puis `Espace` atteint la scène
(`ui-bind-e2e/03-level.png`) ; `left` clavier 2 = `A` écrit
`INPUT.CFG` (`build/porting/ui-evidence-20261028/bound-left-A.png`). F1 en jeu et reprise :
`build/porting/ui-evidence-20261028/gameplay-ui.png`, `gameplay-resumed.png`.
Manette validée en **synthétique** le 29 octobre : un contrôleur Xbox 360
virtuel créé via `/dev/uinput` est détecté par SDL
(`[INPUT] Gamepad 0: X360 Controller`, GUID
`030081b85e0400008e02000014010000`) ; `A` déclenche New Game (cutseq `name: 1`)
et le stick gauche déplace Lara vers l'arche (`build/porting/vpad-20261029/`).
Le hotplug est aussi validé en synthétique : la manette créée **après** le
lancement est détectée (`SDL_CONTROLLERDEVICEADDED`), et `A` démarre New Game
(`build/porting/vpad-hotplug-20261029/`). Ce n'est pas une manette physique :
le matériel réel reste non testé ; pas de hot reload du keymap. Tickets :
[PORT-009 à PORT-012](input/README.md).

## Commandes et caméra — 28 octobre 2026 (PORT-004)

Séquence réelle sur le binaire `build-l` (ELF32 i386, SHA256
`3b686385c9c64609e24b6bf49b93bb551298f35bb8df2ba9ff43304b584a4747`),
données NTSC, entrées XTest, 15 captures inspectées, fermeture
`WM_DELETE_WINDOW`, `application.json` exit 0. Preuves privées :
`build/porting/port004-final-l-20261028/`.

- **HUD debug retiré** : `Camera X/Y/Z` (`GAME/HEALTH.C`) n'est plus dessiné ;
  la scène de Rome est lisible sans surimpression.
- **Commandes** : `W`/flèche haut avance, relâchement immédiat ; `Left`/`Right`
  tournent le corps ; `X` saute ; `C` agit ; `Entrée` ouvre le menu pause,
  `Resume` (`C`) reprend la simulation ; une frame sans entrée ne montre aucun
  mouvement résiduel.
- **Regard** : `Shift` + `Left`/`Right` oriente la tête et déplace la caméra
  autour de Lara ; au relâchement, la tête revient au neutre et la caméra
  retrouve le suivi. Captures `09-look-left.png` / `10-look-return.png` et
  `11-look-right.png` / `12-look-return2.png`.
- **Perte de focus** : sur `SDL_WINDOWEVENT_FOCUS_LOST`, `SDL_ResetKeyboard()`
  efface l'état clavier. Test réel : `W` maintenu, une fenêtre `xmessage`
  prend le focus, le `keyup` est perdu ; au retour, deux sauvegardes `F5`
  espacées de 3 s donnent la même position (Z 34346), puis `W` produit un
  déplacement (Z 35979, room 2). Le mouvement n'est donc pas resté bloqué
  (`build/porting/port004-focus2-20261028/`). Le cas « Shift resté enfoncé
  dans le serveur X » rencontré pendant la recette est distinct et a été
  nettoyé avec `xdotool keyup`, pas par le jeu.
- **Manette** : déconnexion/reconnexion passe désormais par
  `PadHandleControllerEvent` (instance id SDL, pas l'index joystick brut) et
  ferme le contrôleur sélectionné avant de retenter l'ouverture ; aucun
  contrôleur physique sur cet hôte.
- **Limites** : `LookCamera` est une implémentation de port fonctionnelle
  (cible = joint de tête, angle tête/torse, rig de poursuite à 1024 unités),
  **pas** une reproduction de la routine MIPS ; comparaison visuelle seulement,
  pas d'équivalence binaire. La caméra combat, les collisions étendues et le
  remappage caméra restent hors de ce ticket.

## Déplacement solide et salles — 28 octobre 2026 (PORT-005)

Route bornée en scène ouverte sur `build-l` (même binaire ELF32 i386 que
PORT-004), entrées XTest, positions relevées par un point d'arrêt GDB sur
`UpdateLaraRoom` (échantillon toutes les 30 visites + changement de salle).
Preuves privées : `build/porting/port005b-20261028/` (`gdb.log`, captures).

| Étape | Salle | X | Y | Z |
|---|---:|---:|---:|---:|
| Départ, immobile | 0 | 46592 | 0 | 31232 |
| Marche dans le couloir | 2 | 46592 | 0 | 34964 |
| Marche (sol surélevé) | 2 | 46592 | 256 | 37721 |
| Marche | 2 | 46592 | 256 | 38853 |
| Saut/accroche au mur | 62 | 46592 | -1792 | 38913 |
| Reprise dans la cour | 61 | 46592 | -274 | 40645 |

- **Portails** : trois changements de salle observés (0 → 2 → 62 → 61) sans
  téléportation de X/Z ; la caméra suit et la géométrie reste cohérente.
- **Mur** : après 12 s de marche, Lara est bloquée contre une paroi
  (`05-walk8.png`, `06-walk12.png` identiques) ; un saut avec `W` maintenu
  déclenche l'accroche au rebord, pas une traversée.
- **Saut/atterrissage** : la hauteur `Y` passe de 256 à -1792 puis -274 avec
  `floor` cohérent (-1792 / 256) ; pas de chute hors géométrie observée.
- **Mur latéral** : rotation puis poussée de 3 s, position et image inchangées
  (`10-push-wall.png` / `11-after-push.png`).
- **Pause/reprise** : `Entrée` ouvre le menu pause ; l'ordre est désormais
  `Resume`, `Game Settings`, `Quit` (Game Settings au-dessus de Quit).
  `Resume` rend le contrôle, `Game Settings` ouvre l'écran de réglages et
  `Quit` ouvre la confirmation « Are you sure you want to quit ? ». Vérifié
  au clavier (`build/porting/pause-order-kbd-20261029/`,
  `build/porting/pause-quit-20261029/`) et à la manette virtuelle (D-pad via
  axes hat : `Game Settings` surligné, `A` ouvre les réglages ;
  `build/porting/pause-gamepad2-20261029/`) ; la scène reprend au même endroit.

Limites : route unique, pas de pente raide ni d'eau, pas de comparaison
`GetHeight` cible, échantillonnage GDB et non une trace matérielle ; la
caractérisation `GetHeight`/`ItemPushLara` de RE-770/771 reste ouverte. Ce lot
ne corrige pas le callback de hauteur et ne prétend pas à une équivalence
binaire.

## Sauvegarde rapide et reprise — 28 octobre 2026 (PORT-006)

La sauvegarde mémoire PSX (`MemCard*`) n'est pas implémentée pour PSXPC_N. Le
port fournit une **sauvegarde rapide de port** : `F5` en jeu écrit `TOMB5.SAV`
(ou `TOMB5_SAVE_PATH`), `F6` au titre recharge la sauvegarde et reprend au même
endroit. Depuis le 29 octobre, le format v4 inclut aussi l'état du niveau
(`SaveLevelData`/`RestoreLevelData`).

- **Format v4** : en-tête magique `T5P2`, version 4, `savegame_info` complet
  (inventaire, santé, stats, niveau), bloc de 8192 octets pour l'état du niveau
  (flips, meshes statiques, caméras, items avec `item_flags`/`timer`/
  `trigger_flags`), position/rotation/salle/état d'animation de Lara, checksum
  FNV-1a. Fichier de 8658 octets. Les fichiers v3 (même taille, sans les champs
  d'items) et v2 (466 octets) restent lisibles.
- **Écriture** : `SaveLaraData()` rafraîchit `savegame.Lara` ; `F5` est capté
  avant le keymap (touche réservée) et consommé une seule fois par frame.
- **Lecture** : `F6` au titre appelle `PortSave_Read`, qui recopie le bloc de
  niveau dans `MGSaveGamePtr`, puis `TitleOptions` retourne 2 ; le gameflow
  recharge `savegame.CurrentLevel` en mode 4, `sgRestoreGame()` exécute
  `RestoreLevelData` puis `RestoreLaraData`, et `PortSave_ApplyPending()` replace
  Lara (position, salle, animation), met à jour la salle et réinitialise la
  caméra. `TOMB5_AUTOLOAD=1` permet de déclencher la même lecture sans timing
  F6 (utilisé par les tests).
- **Preuve inter-niveaux** : chargement du niveau 4 par le raccourci QA
  (`look`/L1 + New Game), `F5` → `level 4 room 99 X 35328 Y -4096 Z 29664` ;
  relance, `F6` → même niveau, même salle, même position, scène identique
  (`build/porting/port006-level4-20261028/`, RMSE 0,055 entre les deux captures).
  `savegame.CurrentLevel` est donc bien utilisé au rechargement.
- **Découverte** : si `TOMB5.SAV` existe, le titre affiche `F6: CONTINUE`
  sous le menu ; le texte disparaît quand le fichier est absent
  (`build/porting/title-hint-20261028/01-with-save.png` /
  `02-without-save.png`).
- **Retour visuel** : `F5` affiche `Game saved` centré en bas de l'écran
  pendant 90 frames (~3 s), puis disparaît ; `F6`/application affiche
  `Game loaded`. Vérifié sur `build-q`
  (`build/porting/save-message-q-20261028/02-saved-message.png`,
  `03-after-message.png`).
- **Preuve réelle** : partie neuve, marche dans Rome, `F5` → log
  `[SAVE] wrote TOMB5.SAV: level 1 room 2 X 46592 Y 0 Z 35826` ; fermeture
  normale ; relance ; `F6` au titre → log
  `[SAVE] loaded ...` puis `[SAVE] applied saved position: room 2 X 46592 Y 0 Z 35826`,
  scène identique à la capture d'avant fermeture (`03-after-save.png` vs
  `02-loaded.png`, moyennes 0,068 / 0,070). `application` exit 0 dans les deux
  phases. Rejeu du seul chargement sur le build final `build-m` (SHA256
  `2421b302a9e136b9e0fcee5475dd887f2ccf8d4ef4c8c71d3aba524f9ec94865`) : même
  position appliquée (`build/porting/port006c-20261028/`). Preuves privées :
  `build/porting/port006-20261028/`, `port006b-20261028/`.
- **Preuve v4 (état du niveau)** : `F5` à Rome écrit 586 octets de niveau
  (bloc de 8192) ; au rechargement, les compteurs de lecture sont identiques
  (caméras à 259 octets, items à 586) et la scène est propre
  (`build/porting/restorefull-debug2-20261029/`, `v4-roundtrip-20261029/`).
  Test ciblé des champs v4 : `item_flags`/`timer`/`trigger_flags` forcés sur
  l'item 0 donnent 598 octets à la sauvegarde et 598 à la restauration
  (`flag-roundtrip-20261029/`).
  `RESTORE3.SAV` (v2) et `E.SAV` (v3) restent acceptés
  (`restorefull-v2-20261029/`, `v4-legacy-v3-20261029/`).
  Le désarmement de `flipeffect` après restauration évite
  `turn180_effect(NULL)`. Preuve inter-niveaux v3/v4 : sauvegarde `L2.SAV` au
  niveau 2 (room 50, X 91648 Y 0 Z 42496, 594 octets de niveau), rechargement
  par `TOMB5_AUTOLOAD` → même niveau/salle/position et scène identique
  (`build/porting/level2-save-20261029/`, `level2-load-20261029/`).
  Mise à niveau v3→v4 au niveau 2 (29 octobre) : `L2.SAV` chargé par `F6`,
  puis `F5` réécrit le même fichier en v4 (606 octets de niveau, +12 octets
  d'état d'items), relance et `F6` restaurent le niveau 2, room 50,
  X 91648 Y 0 Z 42496 avec une scène identique (moyennes 0,0885 / 0,0885 ;
  `build/porting/level2-v4-20261029/`).

### Limites PORT-006

- L'état du niveau est sauvegardé dans un bloc fixe de 8192 octets. Si la
  sérialisation d'un niveau dépasse cette taille, `F5` échoue explicitement au
  lieu d'écrire un fichier tronqué. `ReadSG` est borné à ce bloc et
  `RestoreLevelData`/`PortSave_ApplyPending` vérifient les numéros de salle
  avant `ItemNewRoom`/`UpdateLaraRoom`. Un save v4 avec salle 255 est refusé
  (`invalid saved room 255 (level has 242 rooms); load ignored`,
  `badroom2-20261029/`). Les fichiers v2 restent lisibles mais
  ne restaurent que Lara et l'inventaire, pas les objets/portes/flips.
- `RestoreLevelData` restaure les champs sérialisés par `SaveLevelData`
  (flips, meshes statiques, caméras, items : position, salle, animation,
  flags, points de vie, `item_flags`, `timer`, `trigger_flags` en v4). Les
  fichiers v3 plus anciens utilisent `PortSave_LevelFormat=3` pour ignorer ces
  champs et rester compatibles.
- **Artefact visuel de reprise — cause trouvée et corrigée (29 octobre)** :
  la grande surface brune qui suivait la caméra n'était **pas** causée par
  `F6`, `AUTOLOAD` ou `RestoreLevelData` : elle apparaissait dès une partie
  neuve à Rome, sans aucune sauvegarde. La bissection des binaires donne
  `build-c` (07:23) propre et `build-s` (12:42) avec l'artefact ; la différence
  est l'agrandissement des tableaux de garde `SkinVertNums`/`ScratchVertNums`
  à 8192 octets. Le chargeur lit les tables objects/static puis 480 octets de
  skin et 480 octets de scratch dans un **flux contigu** ; avec les tableaux
  agrandis, le bloc scratch atterrissait à `SkinVertNums + 480`,
  `ScratchVertNums` restait à zéro, et les matrices de Lara produisaient un
  polygone immense. `GAME/SETUP.C` recopie désormais le bloc scratch vers
  `ScratchVertNums` après la lecture ; la lecture CD reste contiguë car
  `DEL_CDFS_Read` avance par secteurs. Preuves : partie neuve à Rome propre
  (`build/porting/master-fix-smoke-20261029/`), `F6` sur `RESTORE3.SAV` propre
  (`build/porting/fix-objectdata-final-load-20261029/`), niveau 6 chargé et
  rendu sans `SIGSEGV`. Build final `build-au` ELF32 i386, SHA256
  `dee0479c6000441af05b4d9724bb7b57605859eca2df0b74c0dbe920c32a467e`.
- Pas de sauvegarde via carte mémoire PSX ni via le menu d'inventaire ; `F5`/`F6`
  sont des touches réservées non remappables. Le chemin natif est absent à deux
  niveaux : `SaveGame` `case 12` est désactivé par `#if 0` dans
  `SPEC_PSXPC_N/LOADSAVE.C:566` (il ne fait qu'afficher `SaveErrorReq`), et
  `MemCardCreateFile`/`MemCardWriteFile`/`MemCardWriteData`/`MemCardFormat`
  restent vides dans `EMULATOR/LIBMCRD.C:208-237`. Le menu PSX ne peut donc pas
  écrire ; `F5`/`F6` restent la seule voie supportée. Pas de chargement en jeu
  (le chargement n'est traité qu'au titre), pas de slots multiples, pas de
  sauvegarde pendant une FMV/menu.
- Un fichier absent/corrompu est refusé avec un log et le titre continue.
  L'écriture est atomique : `F5` écrit `<sauvegarde>.tmp`, vérifie l'écriture,
  puis `rename` remplace l'ancienne sauvegarde; un échec laisse l'ancienne
  intacte.

## Audio — backend SDL et mixage SPU (PORT-007, en progrès)

Depuis le 29 octobre, PSXPC_N dispose d'un **backend de sortie audio hôte** et
d'un mixage SPU de base. Il ne s'agit pas encore d'une validation d'écoute
humaine ni d'une fidélité SPU complète.

- `EMULATOR/LIBSPU.C` conserve désormais les 512 Ko de RAM SPU
  (`Spu_GetRam`) au lieu de jeter les transferts `SpuWrite`; `_spu_Fw` copie
  les données à l'adresse de transfert. Les accesseurs exposent aussi les
  registres de voix et le masque key-on.
- `SpuSetVoiceAttr` corrige deux bugs du pont : la conversion de volume
  `0..16383` vers `0..127` et l'écriture ADSR dans les registres `+4/+5`
  (elle écrasait le volume gauche). `SpuSetKey`/key-off restent la source de
  vérité des voix.
- `SPEC_PSXPC_N/HOSTAUDIO.C` ouvre un device SDL2 44100 Hz stéréo S16,
  décode les blocs VAG/ADPCM de la RAM SPU (filtres 0..4), applique pitch,
  pan/volume et master, puis mixe 24 voix. Les voix sont libérées sur key-off
  et `S_SoundStopSample` coupe explicitement la voix.
- `PlaySample` conserve sa frontière historique à 7 arguments (contrat hôte),
  mais utilise le vrai index d'échantillon, le pitch et le pan signé pour
  fabriquer gauche/droite; l'ancien code passait le pitch comme volume droit.
- `SPU_Play` ne divise plus le pitch par 64 : les valeurs 4096/32256 observées
  sont maintenant des fréquences cohérentes (pas de ralentissement 1/64).
- `SpuSetKey` renseigne le registre de volume courant `+6` (0x3FFF à
  key-on, 0 à key-off); sans cela `SpuGetKeyStatus` renvoyait « terminé » et
  le jeu libérait les voix immédiatement.
- `SoundFXVolume` est appliqué au master du callback. Mise à zéro forcée par
  GDB : le PCM reste entièrement nul pendant la marche
  (`build/porting/mute-20261029/`).
- `S_SoundSetPanAndVolume`/`S_SoundSetPitch`/`GetPanVolume` sont implémentés
  (pan/volume/pitch des slots positionnels) au lieu de rester
  `Unimplemented`; `audio-cl-20261029/` ne contient plus ces messages et
  produit du PCM pendant la marche. `GetPanVolume` ne remplace pas le volume
  atténué par `OrigVolume` : seule la position panoramique est recalculée.
- **Musique/voix XA non décodées** : l'image NTSC contient bien les 17
  fichiers `\XA1.XA;1` à `\XA17.XA;1` et 118 822 secteurs Mode2/Form2 audio
  (submode `0x64`) sur 277 280 secteurs. Mais `EMULATOR/LIBCD.C` lit les
  secteurs XA sans les décoder (`RM_XA_AUDIO` recopie des octets bruts) et
  `SPEC_PSXPC_N/HOSTAUDIO.C` ne reçoit que les VAG/SPU : `S_CDPlay` ne produit
  donc aucun son CD/XA. Scan reproductible :
  `build/porting/xa-scan-20261029/scan.txt`.

Preuves : avec `SDL_AUDIODRIVER=disk`, une partie neuve à Rome puis 8 s de
marche produit un PCM stéréo non nul (21,1 Mo, RMS ~977, échantillons actifs
uniquement pendant la marche, `build/porting/final-audio-bn-20261029/`).
Les voix `SF_LOOP` redémarrent au lieu de se couper; contrôle
`build/porting/final-audio-loop-20261029/` (RMS 1265), sur `build-cd`
`build/porting/final-audio-cd-20261029/` (RMS 1285), et sur `build-cg`
`build/porting/final-audio-cg-20261029/` et `audio-long3-20261029/` (PCM actif
en continu pendant 30 s de marche, pitch corrigé).
`SDL_AUDIODRIVER=dummy` ouvre le device sans crash
(`final-audio-dummy-20261029/`). Tests : `tests/porting` 497 PASS,
`tests/emulator` 3677 PASS. Build de preuve audio `build-bn` SHA256
`809e8cae8f26536052a0590486f5f3672349b8dfc4c4a0a675a7e0d4662ae9a9` ;
build final combiné (reprise v4, écriture atomique, audio/pitch/volume,
correctif strings gameflow et bornes de restauration) `build-cm` SHA256
`da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b`.

Limites : aucune écoute humaine, pas de musique CD/XA ni de voix CD, ADSR/
reverb/loop approximés, pas de test de volume nul/catégories, pause et retour
titre non instrumentés pour l'audio. PORT-007 reste **In progress**, pas Done.

Historique conservé : `SPU_StopAll` libère toutes les voix et reconstruit les
canaux; `S_SoundStopAllSamples`/`S_SetReverbType` sont implémentés; le test
`SpuSetKey(SPU_OFF, SPU_ALLCH)` remet `_spu_keystat` à zéro.

## Recette intégrée finale — 28 octobre 2026

La recette principale a été jouée sur `build-o` (ELF32 i386, SHA256
`595d3c4c41ac640587e292c75fa63bd81b9074228c7a40c91a630490be5f6d8e`).
Le build final `build-x` (SHA256
`78b5ac0233b7e7fd9325a2c34e00a173b854ce93e17afa859a4bcf11b2468edd`)
compile les mêmes sources que `build-q`, avec en plus l'indice de titre
`F6: CONTINUE`, le garde-fou F5/F6 pendant l'éditeur, le retour visuel
`Game saved`/`Game loaded`, le correctif de transition PORT-008 et les correctifs mémoire du niveau 6. Smoke titre
de `build-r` (même code hors transition) avec un fichier de sauvegarde présent :
indice affiché, fermeture normale exit 0 (`build/porting/build-r-smoke-20261028/`).
Scénario unique, 9 captures inspectées,
`application.json` exit 0 :

1. titre ; `F6` charge `TOMB5.SAV` (salle 2, X 46592 Y 0 Z 35826) ;
2. la scène reprend à la position sauvegardée ;
3. `Shift`+`Left` déplace la caméra de regard, le relâchement revient au suivi ;
4. `W` avance, `F5` écrit une nouvelle sauvegarde (salle 2, X 46592 Y 256
   Z 38831) ;
5. `Entrée` ouvre le menu pause, `Resume` reprend ;
6. une frame sans entrée reste stable ; fermeture normale, exit 0.

Preuves privées : `build/porting/final-smoke-20261028/` ; rejeu du chargement
sur `build-o` dans `build/porting/port006d-20261028/`. Le retour visuel est
vérifié sur `build-q` dans `build/porting/save-message-q-20261028/`. Un fichier
de sauvegarde corrompu (`BAD.SAV`, 16 octets) est refusé avec
`[SAVE] invalid save header`, le titre continue et le processus sort à 0
(`build/porting/port006-corrupt-20261028/`).

Cette recette historique ne validait pas la reprise complète des objets de
niveau. Depuis le 29 octobre, le format v4 et `RestoreLevelData` restaurent
l'état du niveau (voir PORT-006). Restent non validés : l'audio (aucun backend
de sortie), la campagne et la manette physique.

État des suites au même commit : `tests/porting` 497 PASS, `tests/emulator`
3677 PASS. `tests/reverse` : 4341 PASS, 125 FAIL, 1 skip, 1100 subtests PASS
(`--ignore=tests/reverse/fixtures`). Le test hôte `tests/porting/test_portsave.py` couvre le round-trip, l'application
de la position, le rejet du checksum et du magic. Huit FAIL supplémentaires par rapport au
clone viennent de contrats documentaires qui gèlent des hashes de sources
(RE-803/804/807/808/809, RE-164, RE-357) ou des octets de dashboard (RE-820) :
les modifications légitimes de `GAME/CONTROL.C`, `GAME/CAMERA.C`, etc. les
invalident. Ce ne sont pas des régressions runtime, et les archives
historiques ne sont pas réécrites.

## Boucle de niveau et campagne — transition corrigée (PORT-008, partiel)

PORT-008 demande de terminer le premier niveau puis de passer au suivant. La
route Rome complète (clés, portes, puzzles, fin de niveau) n'a **pas** été
jouée par du gameplay, donc le critère utilisateur n'est pas encore validé.
Mais un vrai défaut du chemin de transition a été trouvé et corrigé.

### Défaut trouvé et corrigé

Dans `GAME/GAMEFLOW.C`, après `gfStatus == 3` (niveau terminé), le code
affectait `gfCurrentLevel = gfLevelComplete` puis **écrasait
inconditionnellement** `gfCurrentLevel = 0`. Le test de niveau suivant était
donc sans effet et toute fin de niveau renvoyait au titre. La branche a été
corrigée : `gfCurrentLevel = 0` n'est exécuté que dans le `else` (démo,
build à deux niveaux, fin de campagne). Le correctif est dans `build-x`
(SHA256 `78b5ac0233b7e7fd9325a2c34e00a173b854ce93e17afa859a4bcf11b2468edd`).

### Recette de transition (déclenchement synthétique)

Sous GDB, `gfLevelComplete = 2` est posé après 600 frames de jeu réel dans
Rome (aucune écriture de position ni de niveau). Résultat après le correctif :

- `GAMEPLAY_FRAMES 1800 level 2 room 50 Z 42496` puis milliers de frames
  stables au niveau 2, cutseq `name: 2` ;
- la scène de TRAJAN_MARKETS est rendue avec Lara
  (`build/porting/port008-transition2-20261028/03-next.png`,
  `04-next-later.png`) ;
- sans le correctif, la même injection renvoyait au titre puis en DEMO MODE
  (`build/porting/port008-transition-20261028/`) ;
- régression New Game : Rome se charge toujours (cutseq `name: 1`, moyenne
  d'image 0,101, exit 0 —
  `build/porting/port008-newgame-regress-20261028/`).

### Chaîne multi-niveaux

Le même déclenchement contrôlé a été répété tous les 600 frames de jeu :
`gfLevelComplete = gfCurrentLevel + 1`. Après le correctif du niveau 6 (voir
ci-dessous), le moteur enchaîne **1 → 2 → … → 14** sans retour au titre :

| Niveau | Salle | Z |
|---:|---:|---:|
| 1 | 0 | 31232 |
| 2 | 50 | 42496 |
| 3 | 20 | 52736 |
| 4 | 99 | 29664 |
| 5 | 20 puis 23 | 42496 / 53760 |
| 6 | 123 | 50688 |
| 7 | 2 | 79360 |
| 8 | 70 | 32256 |
| 9 | 5 | 28160 |
| 10 | 20 | 37376 |
| 11 | 3 | 38400 |
| 12 | 129 | 46592 |
| 13 | 3 | 67072 |
| 14 | 8 | 77312 |

Chaque niveau reste stable sur des milliers de frames, avec des scènes
distinctes (`build/porting/port008-fullchain3-20261028/01-level1.png` à
`14-level14.png`). Cela valide la **mécanique de boucle** après correctif, pas
une complétion jouée : les déclenchements sont injectés, aucun
puzzle/porte/clé n'est résolu, aucun FMV de transition ni crédit n'est
vérifié.

### Niveau 6 — corruption mémoire trouvée et corrigée

Le crash `SIGSEGV` au niveau 6 était dû à une corruption mémoire, pas à la
boucle de transition. AddressSanitizer (build 32 bits) a localisé deux
dépassements :

- `EMULATOR/LIBGPU.C` (`ClearOTagR`) écrivait au-delà de
  `GadwOrderingTables` : en mode 32 bits, chaque entrée d'ordering table fait
  deux mots, mais la seconde table était décalée de `nOTSize` et `nOTSize`
  valait `sizeof/8` (formule 16 bits). Correction : décalage
  `nOTSize * POLYGON_BUFFER_MULT` et `nOTSize = sizeof / (8 * MULT)` aux deux
  appels de chargement.
- `SPEC_PSXPC_N/LARA5.C` (`sub_C1CL5`) : la liste de vertices de
  `SkinVertNums` n'a pas de sentinelle négative pour ce mesh, la boucle écrit
  alors sans borne dans `tsv_buffer` (4096 octets) et finit par écraser
  `psxtextinfo` (`0xc100ff`). Corrections : `tsv_buffer` porté à 1024 `TSV`
  (8192 octets), `SkinVertNums`/`ScratchVertNums` à 8192 octets, et borne
  explicite sur `tsv_buffer` dans `sub_C1CL5`.
- `GAME/SETUP.C` : le bloc scratch de 480 octets est replacé dans
  `ScratchVertNums` après la lecture contiguë objects/static/skin/scratch. Sans
  ce replacement, les tableaux agrandis laissaient `ScratchVertNums` à zéro et
  produisaient l'artefact de Rome décrit dans PORT-006.

### Strings gameflow — chevauchement mémoire corrigé

AddressSanitizer 32 bits a signalé `memcpy-param-overlap` dans
`LoadGameflow` (`GAME/GAMEFLOW.C:621`) : le déplacement du bloc de chaînes
`gfStringOffset` vers une adresse plus basse chevauchait la source. Les cinq
copies concernées utilisent désormais `memmove`, ce qui conserve le résultat
attendu sans comportement indéfini. Une partie neuve à Rome passe ASan sans
nouvelle erreur (`build/porting/asan-run2-20261029/`). Les parcours ASan
  nouvelle partie + `F5` puis rechargement `F6`/`AUTOLOAD` ne signalent aucune
  erreur (`asan-run3-20261029/`, `asan-load-20261029/`), y compris le
  rechargement v3 du niveau 2 (`asan-level2-20261029/`). Après les correctifs
  pitch/volume courant et bornes de lecture, les parcours ASan nouvelle
  partie + `F5` puis rechargement v4 sont propres
  (`asan-run4-20261029/`, `asan-load2-20261029/`, `asan-run5-20261029/`,
  `asan-load3-20261029/`, `asan-run6-20261029/`). Un soak ASan de 6 min avec
  entrées aléatoires ne signale aucune erreur (`asan-soak-20261029/`).
  ASan PAL + manette virtuelle (29 octobre, `ASAN_OPTIONS=detect_leaks=0`) :
  New Game, détection du contrôleur et déplacement au stick, exit 0, aucune
  erreur AddressSanitizer (`pal-asan2-20261029/`). Avec LeakSanitizer actif,
  le même parcours signale 189 290 octets dans `libnvidia-glcore.so` (piles
  d'allocation du driver GL, aucune frame du port) : ce n'est pas une fuite du
  jeu, mais un bruit du driver (`pal-asan-20261029/`).
  **Débordement SqrtTable trouvé et corrigé (29 octobre)** : le soak ASan
  PAL + manette a déclenché un `global-buffer-overflow` dans `mSqrt`
  (`SPEC_PSXPC_N/MATHS.C`, lecture `SqrtTable[value]`) depuis `sub_2CL1`
  (`SPEC_PSXPC_N/LARA1.C:1555`, argument `0x1000000 - a000` négatif par
  arrondi). Les variantes `mSqrt_2`, `phd_sqrt_asm`, `phd_sqrt_asm_CH`
  (`CALCHAIR.C`) et `mSqrt_L` (`LIGHT.C`) lisaient la même table sans borne.
  Correctif : entrée négative ramenée à 0 et accès centralisé par
  `PortSqrtLookup()` borné à `0..209` (`MATHS.C`/`MATHS.H`). Vérification
  directe sous GDB/ASan : `mSqrt(-1) = mSqrt_2(-1) = mSqrt_L(-1) =
  phd_sqrt_asm(-1) = phd_sqrt_asm_CH(-1) = 0`, `mSqrt(2147483647) = 46152`,
  aucun rapport ASan ; soak ASan PAL + manette de 571 s, 34 échantillons,
  exit 0, aucune erreur (`pal-asan-soak3-20261029/`, preuve du crash initial
  dans `pal-asan-soak-20261029/`). Régression visuelle normale : scène de
  Rome rendue (`guard-smoke2-20261029/`).

Après correctif, le niveau 6 se charge et rend sa scène ; le saut direct
1→6 ne crashe plus. La chaîne contrôlée **1→2→3→4→5→6→7→8→9→10→11→12→13→14**
s'enchaîne sans `SIGSEGV` (preuves : `port008-fullchain2-20261028/`,
`port008-fullchain3-20261028/`). Le garde-fou tronque une éventuelle liste
malformée : il protège la mémoire mais ne corrige pas le parseur de mesh
lui-même ; des artefacts de vertices restent possibles sur ce niveau.

### Fin de campagne et entrée GAMEWAD absente

L'analyse directe du `GAMEWAD.OBJ` de l'image NTSC montre que les entrées
`3..16` seulement contiennent des fichiers de niveau (14 niveaux) ; les entrées
`17+` sont vides (`fileSize = 0`). Le `Gameflow` déclare pourtant `nLevels = 18`.
Le déclenchement synthétique `gfLevelComplete = gfCurrentLevel + 1` après le
niveau 14 demandait donc l'entrée 17, inexistante ; le lecteur retombait sur
l'en-tête du GAMEWAD et produisait un en-tête de niveau invalide
(`DEL_CDFS_Read size=-16388`, puis `fseek`/`SIGSEGV`). Le même phénomène
explique le bruit PAL observé.

`DoLevel` vérifie désormais l'entrée GAMEWAD avant `S_LoadLevelFile` : si
`Name + TITLE` est hors bornes ou de taille nulle, il journalise
`[LEVEL] missing GAMEWAD entry …`, remet `gfStatus = 1` / `gfCurrentLevel = 0`
et retourne au titre. Recette :

- saut direct 1→15 : log `missing GAMEWAD entry 17 for level 15; returning to
  title`, aucun `SIGSEGV`, titre réaffiché
  (`build/porting/port008-endguard-20261028/`) ;
- régression 1→2 : TRAJAN_MARKETS se charge normalement avec Lara
  (`build/porting/port008-valid2-20261028/`).

Après le garde `GetDoor`, la **chaîne complète** 1→14 puis déclenchement 15
ne casse plus : deux runs indépendants sur `build-x` atteignent le niveau 14,
déclenchent la fin, puis reviennent au titre (`Handle cutseq triggering name:
0`, aucun `SIGSEGV`) — `build/porting/port008-fullchain15-20261028/` et
`port008-fullchain-title-20261028/`, ainsi qu'une capture du fond de titre
(`port008-fullchain-proof-20261028/01-after-level14.png`). Le crash
`GetDoor(0xfe4cb8d4)` n'est plus reproduit. Une nouvelle chaîne après le
correctif de contiguïté scratch atteint de nouveau 1→14 puis le niveau 0/titre
sans `SIGSEGV` (`build/porting/port008-fullchain-fix-20261029/gdb-chain.log`).
Une seconde validation utilise le hook QA `TOMB5_CHAIN_TEST` (même logique de
transition, déclenchement tous les 600 frames) et enchaîne 1→2→…→14 puis
`Handle cutseq triggering name: 0` sans `SIGSEGV` sur
`build/porting/final-chain-bs2-20261029/` et
`build/porting/final-chain-by-20261029/` (hook non intégré à `master`), cette
dernière sur les sources finales build-bx, puis
`build/porting/final-chain-ce-20261029/` sur build-cd (memmove gameflow + v4),
enfin `build/porting/final-chain-cj-20261029/` sur les sources finales build-ci,
puis `build/porting/final-chain-cn-20261029/` sur build-cm (audio positionnel
compris). Chaîne de régression finale sur `build-pause` (pause réordonnée +
correctif `SqrtTable`) : 1→14→titre, cutseq `name: 0`, aucun `SIGSEGV`
(`build/porting/final-chain-pause-20261029/`).
La garde GAMEWAD n'est pas nécessairement l'élément déclencheur du retour titre (le gameflow peut le faire avant `DoLevel(15)`) ; elle reste
validée séparément par le saut direct 1→15. Un soak de 13 minutes sur
build-cm avec entrées aléatoires (marche, recul, strafe, saut, audio dummy)
ne produit ni `SIGSEGV` ni erreur fatale (`build/porting/soak-20261029/`).
Soak RSS de 15 minutes sur build-cm (mêmes entrées, échantillonnage
`/proc/<pid>/VmRSS` toutes les 30 s) : 47 échantillons, 75 112 → 75 560 Ko
(+448 Ko, plateau dès 150 s jusqu'à 871 s), états `R`/`S`, aucune erreur
fatale, exit 0 ; captures à 300 s (inventaire) et 600 s (allée de Rome)
(`build/porting/soak-rss-20261029/`).
Smoke PAL (`build/porting/data`, SLES_033.31) sur build-cm : scène de Rome
rendue, audio initialisé, aucune erreur (`final-pal-20261029/`). New Game PAL
confirmé par `Handle cutseq triggering name: 1` et l'allée de Rome : le menu
est interactif vers 45 s et il faut **maintenir `C` ~350 ms** ; un tap court
peut être perdu à 50 Hz et laisser le titre partir en DEMO MODE
(`pal-timing3-20261029/`). Sauvegarde PAL validée : `F5` à level 1 room 0
X 46592 Y 0 Z 31232 écrit 586 octets de niveau, relance + `F6` restaure la
même position et une scène identique (moyennes 0,1006 / 0,1009 ;
`build/porting/pal-save4-20261029/`). Transition PAL 1→2 validée par injection
GDB de `gfLevelComplete=2` après 600 frames de niveau 1 : cutseq `name: 2`
(1657 occurrences), scène TRAJAN_MARKETS rendue, aucun `SIGSEGV`
(`build/porting/pal-transition-20261029/`) — déclenchement synthétique, pas une
complétion jouée. Chaîne PAL complète avec le même type d'injection toutes les
600 frames : niveaux 1→14 avec les salles/positions du tableau NTSC (2/50,
3/20, 4/99, 5/20, 6/123, 7/2, 8/70, 9/5, 10/20, 11/3, 12/129, 13/3, 14/8),
puis retour au titre (`cutseq name: 0`), aucun `SIGSEGV`
(`build/porting/pal-chain-20261029/`). Chaîne PAL revérifiée sur `build-pause`
(pause réordonnée + correctif `SqrtTable`) : 1→14→titre, cutseq `name: 0`,
aucun `SIGSEGV` (`build/porting/pal-chain-pause-20261029/`). Soak PAL de 10 minutes avec la manette
virtuelle (boutons et stick gauche aléatoires) : 32 échantillons VmRSS,
**74 928 Ko constant** sur 571 s, exit 0, aucune erreur fatale, scène de rue
rendue (`build/porting/pal-gp-soak-20261029/`).

Cela protège aussi toute donnée de niveau manquante lors d'un chargement
direct. Le chemin de **fin de campagne réel** (crédits/FMV après RED_ALERT)
n'est pas caractérisé : le déclenchement est synthétique et le retour au titre
n'est pas une preuve des crédits originaux.

### Cause racine héritée : objets runtime non initialisés (29 octobre 2026)

La campagne réelle n'est pas seulement « non jouée » : avec les sources
actuelles, elle est **impossible**, car les gestionnaires d'interaction des
objets ne sont jamais installés. Preuve runtime sous GDB après chargement du
niveau 1 (151 items), au premier `DrawRooms` :

```
objects[339] (SHOTGUN_AMMO1_ITEM) collision = nil
objects[286] (DOOR_TYPE2)          collision = nil
objects[258] (KEY_HOLE1)           collision = nil
objects[172] (PUZZLE_ITEM1)        collision = nil
objects[266] (SWITCH_TYPE1)        collision = nil
objects[326] (DOUBLE_DOORS)        collision = nil
objects[242] (PUZZLE_HOLE1)        collision = nil
objects[0]   (LARA)                control   = nil
```

Source (`build/porting/objcoll-20261029/`) : `build/porting/objcoll-20261029/gdb.log`.
Cause dans les sources :

- `GAME/SETUP.C:901` `InitialiseObjects()` met `collision`, `control`,
  `initialise`, `draw_routine` à `NULL` pour les 461 objets, puis appelle
  `BaddyObjects()`, `ObjectObjects()` et `TrapObjects()`.
- `GAME/SETUP.C:626` `BaddyObjects()` n'installe `CreatureCollision` que pour
  quelques créatures (SAS, gardes, etc.).
- `GAME/SETUP.C:1752` `ObjectObjects()` est incomplet : il ne traite que
  `LARA` et un fragment de `SAS` (commentaire `LARA temporary hack (this
  function is incomplete)`). Aucun pickup, porte, interrupteur, clé, puzzle
  ou décor n'y reçoit de `collision`/`control`.
- `GAME/SETUP.C:1747` `TrapObjects()` est vide ; `GAME/SETUP.C:909` remet
  déjà tous les `collision` à `NULL`.
- Les fonctions appelées par ces objets sont elles-mêmes des stubs :
  `PickUpCollision` (`GAME/PICKUP.C:235`), `KeyHoleCollision`
  (`GAME/PICKUP.C:230`), `PuzzleHoleCollision` (`GAME/PICKUP.C:217`),
  `TestLaraPosition`/`MoveLaraPosition`/`TestBoundsCollide`/`ItemPushLara`/
  `GetCollidedObjects` (`GAME/COLLIDE.C:424-450`), `DoorControl`
  (`GAME/DOOR.C:236`), `SwitchCollision`/`SwitchControl`
  (`GAME/SWITCH.C:346-352`), `CreatureCollision`/`LaraBaddieCollision`
  (`GAME/COLLIDE.C:380-387`).
- `CombatCamera` (`GAME/CAMERA.C:1638`) a toujours son corps sous
  `#if 0 || PC_VERSION`, mais le port utilise désormais `ChaseCamera(item)`
  en repli. Sortir les armes (`Y` manette) ne noircit plus la vue : moyennes
  0,1012 / 0,1012 / 0,1018 avant/armes/rengainé
  (`build/porting/gameplay-draw-fix-20261029/`). Le comportement de visée
  automatique du combat reste absent.

Depuis le 29 octobre, une **première couche d'interactions** est implémentée
dans le port (voir la section « Boucle de gameplay — première couche » plus
bas) : dispatch des collisions d'objets, pickups, serrures, trous de puzzle,
switchs et collisions de portes. Les preuves runtime montrent qu'un pickup
ajoute bien l'objet à l'inventaire et qu'une serrure/un switch réagit à
`IN_ACTION`. Il reste notamment les **données de porte** (aucun
`InitialiseDoor` n'est encore présent : `item->data == NULL`, donc
`DoorControl` ne peut pas ouvrir la géométrie), les ennemis/combat et les
objets spéciaux. La campagne réelle reste donc non validée, mais elle n'est
plus bloquée par l'absence totale de collisions d'objets. Ce n'est **pas** une
régression Linux32 : le point de départ était l'état incomplet de la
décompilation.

### Boucle de gameplay — première couche (29 octobre 2026)

Implémenté dans les sources (build `build-gameplay11`, SHA256
`4bd9aa4515872d351a602a3be8ec071becbec2a21b5f95a63e22e61a0d9f812b`) :

- `SPEC_PSXPC_N/COLLIDE_S.C` : `PortCollideItems()` parcourt les items de la
  salle et appelle `objects[object_number].collision` après la géométrie.
- `GAME/COLLIDE.C` : `TestBoundsCollideStatic`, `TestBoundsCollide`,
  `TestLaraPosition`, `MoveLaraPosition` (snap à 256 unités) et
  `ItemPushLara` (poussée AABB minimale).
- `GAME/PICKUP.C` : `PickUpCollision` (pickup + `AddDisplayPickup` +
  `KillItem`), `KeyHoleCollision`, `PuzzleHoleCollision` avec les bounds et
  positions existants.
- `GAME/DOOR.C` : `DoorControl`, `DoubleDoorCollision`,
  `PushPullKickDoorCollision`, et `PortInitialiseDoor()` (allocation
  `DOOR_DATA`, mémorisation du `FLOOR_INFO` d'origine, ouverture de la
  cellule de plancher ; les maillages de porte ne bougent pas encore).
- `GAME/SWITCH.C` : `SwitchCollision`, `SwitchControl`,
  `TurnSwitchControl`.
- `GAME/SETUP.C` : `PortSetupGameplayObjects()` assigne les handlers aux
  pickups, keyholes, puzzles, switchs et portes après `ObjectObjects()`.

Preuves runtime (GDB, niveau 1, téléportation de test) :

- pickup : `AddDisplayPickup` appelé **une fois** pour l'objet 339 ;
  `num_shotgun_ammo1` passe de 0 à 36, item passé `ITEM_INVISIBLE`
  (`gameplay-pickup-20261029/`, `pickup_kbd2.out`) ;
- serrure : clé donnée par GDB, `KeyHoleCollision` atteint avec
  `TestLaraPosition=1` et `IN_ACTION` (`keyhole_test.out`) ;
- switch : `SwitchCollision` atteint avec `TestLaraPosition=1`
  (`switch_test.out`) ;
- fumée normale : Nouvelle partie, déplacement, aucune `SIGSEGV`
  (`gameplay-smoke-20261029/`).

- porte : `DoorControl(24)` initialise `DOOR_DATA` à la volée, passe
  `Opened=1` et restaure un `FLOOR_INFO` avec `box=135` (passable)
  (`door_init.out`) ; le maillage statique n'est pas déplacé.
- déplacement réel avec les **scancodes AZERTY** : `z` (avant) fait passer
  Lara de room 0 X46592 Z31232 à room 2 X46592 Z38830 en 8 s
  (`play-move2-20261029/`) ; `w` est le scancode de `draw` en AZERTY et
  déclenche la vue noire des armes, pas la marche.

Animations d’objets : `AnimateItem` avance `frame_number`, utilise
`GetChange`/`changes`/`ranges` pour changer d’animation quand
`goal_anim_state` diffère, puis boucle sur `frame_end`. Les commandes
`5` (son à une frame) et `6` (effet à une frame) sont exécutées ; la
commande `1` (translation) déplace l’objet via `TranslateItem` puis met à
jour sa salle/`GetFloor` ; `2` applique `gravity_status`/`fallspeed`/`speed` ;
`3` remet l’arme de Lara à l’état neutre. Les objets en `gravity_status`
tombent (`fallspeed += 6`) avec atterrissage sur `GetHeight` et mise à jour
de salle. Les transitions de frames, translations, gravité et sons/effets
d’animation fonctionnent partiellement.

Collisions créatures : `CreatureCollision` pousse Lara hors des bounds.
`LaraBaddieCollision` fait désormais **poursuivre** les créatures
intelligentes jusqu’à 4096 unités (16 unités/frame, mise à jour
`GetFloor`/`GetHeight`/`ItemNewRoom`) et inflige 5 PV par 45 frames à moins
de 512 unités (`SFX_LARA_INJURY_RND`). Preuve : un chien situé à ~1000
unités rejoint Lara et la fait passer de 1000 à 700 PV
(`play-ai3-20261029/`) ; aucun blocage au démarrage (contrairement à la
tentative par `control`/`AddActiveItem`, abandonnée). Les créatures glissent
sans animation (`AnimateItem` est encore `Unimplemented`) et sans pathfinding.

Ennemis de niveau 1 : `PortSetupGameplayEnemies()` initialise après
`InitialiseItem` les `DOG` (hp 10), `LARSON` (hp 100) et `MAFIA`/`MAFIA2`
(hp 40) comme intelligents et non invisibles. Preuve GDB : chien réel hp=10,
deux tirs de pistolet le font passer à hp=4 (`combat_real.out`). Les ennemis
restent **statiques** : pas d’IA de déplacement/attaque, `CreatureCollision`
est encore stub.

Tir minimal : `PistolHandler` fait un hitscan (cible intelligente la plus
proche dans le cône ±60°, portée `weapons[].target_dist`), applique
`HitTarget`, consomme les munitions non-pistolet, joue `SFX_LARA_FIRE` et
allume le flash. Preuve GDB : chien forcé à `hp=100`, `intelligent=1`, puis
6 tirs → hp 64 (`combat_test3.out`). Limite : les ennemis du niveau restent
non initialisés (`hit_points=-16384`, pas d’IA/contrôle), donc les chiens et
Larson sont encore inertes ; il faut compléter `BaddyObjects`/les contrôles
ennemis.

Déclencheurs de switch : `SwitchTrigger` est maintenant implémenté à partir
de la décompilation TOMB4 (`ITEM_DEACTIVATED`, `JUMP_SWITCH`, timer ×30,
`RemoveActiveItem`, `IFLAG_INVISIBLE`). `AnimateItem` exécute la commande
d’animation 4 (`ACMD_KILL`, passage en `ITEM_DEACTIVATED`) et suit
`jump_anim_num`/`jump_frame_num` en fin d’animation. `SwitchControl` peut
donc terminer son animation et `_TestTriggers` active réellement les objets
ciblés. `ControlRaisingBlock` est implémenté (baisse/remontée du sol via
`AlterFloorHeight`) et assigné à `RAISING_BLOCK1/2`.

Validation runtime (build `gameplay26`) : le switch `item 72` (`room 139`,
`X48640 Z65024`) déclenche bien `DoorControl(71)` ; preuve GDB
`probe-switch-effect4-20261102/`. Le même pipeline est utilisé par les
autres switchs/leviers.

Chaîne de la clé d’or validée sans injection : pickup réel de `KEY_ITEM1`
(`item 107`, `room 192`, `X55808 Z35328`) → `AddDisplayPickup(obj=196)` →
retour de Lara à l’état idle (`gun_status=0` après l’animation de pickup) →
insertion au trou de clé `item 25` (`room 59`) → `DoorControl(24)` ouvre la
grille de la fontaine. Preuve GDB `probe-goldkey4-20261102/`. La correction
de `lara_as_pickup` (remise de `lara.gun_status` à `LG_NO_ARMS` à
`frame_end - 1`) est nécessaire pour que Lara puisse agir après un pickup.

Serrure de la fontaine : l’injection directe de `KEY_ITEM1` par GDB
(`play-keygate-20261029/`) reste une preuve séparée ; la chaîne pickup réel
ci-dessus la remplace comme validation de gameplay. Un Doberman est visible
dans la cour.

Clés de jardin validées sans injection : pickup de `PUZZLE_ITEM1` (`item 36`,
`room 85`), usage au trou `item 63` (`room 124`, `PUZZLE_DONE1`, inventaire
1→0) ; pickup du second `PUZZLE_ITEM1` (`item 92`, `room 170`), usage au trou
`item 64` ; les deux trous activent `DoorControl(53)` et `DoorControl(54)`
(grille du jardin). Preuve GDB `probe-garden2keys2-20261102/`. Les trous de
puzzle appellent maintenant `TestTriggersAtXYZ` avec `KeyTriggerActive` et
consomment réellement l’objet via `remove_inventory_item` (et non
`DEL_picked_up_object`, qui ajoute). Les trous de clé consomment aussi la clé
de la même façon.

Cloche du temple : le tir sélectionne désormais aussi les `SWITCH_TYPE7/8`
non intelligents dans le cône de l’arme. `PortHitSwitch78` évalue le
déclencheur sous la cloche (`y - 256`), récupère `GetSwitchTrigger`, active
la porte cible et joue `SFX_BELL`. Validation réelle (pistolet, sans
injection) : cloche `item 75` (`room 145`, `Y -9088`) → `DoorControl(79)`
(`DOOR_TYPE6`, `room 153`). Preuve `probe-shootbell-final-20261103/`.
La sélection utilise des distances 64 bits (les coordonnées lointaines
débordaient le `long` 32 bits et pouvaient fausser la cible).

Boucle des objets actifs : `ControlActiveItems` utilisait
`items[next_item_active]` au lieu de `items[item_num]` et ne faisait pas
avancer `item_num`, ce qui bouclait à l’infini dès que deux objets actifs
étaient chaînés (la cloche active la porte 79 et la cloche elle-même). La
boucle suit maintenant `item->next_active` comme la décompilation TOMB4.
C’est ce correctif qui rend l’ouverture de la porte 79 effective.

Switch corbeau/colombe : `CROWDOVE_SWITCH` est maintenant assigné à
`CrowDoveSwitchCollision`/`CrowDoveSwitchControl`. La collision joue
l’animation de switch, active l’objet et évalue le déclencheur ; le contrôle
shattere le corbeau (`mesh_bits = 5`) et passe l’objet en
`ITEM_DEACTIVATED` pour que `SwitchTrigger` libère le déclencheur. Validation
sans injection : switch `item 84` (`room 165`, `X58880 Z81408`) →
`DoorControl(99)` (`DOOR_TYPE6`, `room 175`). Preuve
`probe-dove84d-20261103/`. Le second pedestal `item 85` n’a pas de
déclencheur à sa tuile ; sa tuile de trigger reste à localiser.

Saturn Symbol : pickup réel validé sans injection. `item 94`
(`PICKUP_ITEM2`, `room 171`, `X59904 Z71168`) → `AddDisplayPickup(obj=221)` ;
`TestLaraPosition(PickUpBounds)=1` depuis `X59954 Z71168`. Preuve
`probe-saturn2-20261103/`.

Les pickups évaluent maintenant le déclencheur de leur tuile
(`TestTriggersAtXYZ`). Pour le Saturn Symbol, la tuile contient un trigger
`PICKUP` avec `TO_FLIPMAP 8` : le pickup déclenche donc `FlipMap(8)`.
Preuve `probe-saturn-finish-20261103/` (`SATF FLIP number=8`,
`flip_stats[8]=1`). La porte 93 reste à valider ; la fin de niveau est validée ci-dessous.

Recherche de fin de niveau : balayage des listes de triggers des 242 salles,
avant et après `FlipMap(8)`, aucun `TO_FINISH` ni `TO_CUTSCENE` ; les seuls
`TO_FLIPEFFECT` trouvés (rooms 223/225/228) n’utilisent pas l’effet
`finish_level_effect` (index 4). `FlipMap(8)` échange la salle 171 (Saturn
Symbol) avec la salle 234 ; le balayage des triggers de ces deux salles ne
révèle aucune fin de niveau. Un test de sortie en `room 230` avec le Saturn
Symbol ne déclenche pas `gfLevelComplete`. Les déclencheurs `TL_6/TL_7/TL_9`
des rooms 223/225/228 et les rooms candidates 174/175/183/186/234 ont aussi
été testés avec le Saturn Symbol en inventaire : aucun téléport, aucun
`gfLevelComplete`, aucune cutscene.

Déclencheur `TO_CUTSCENE` 17 trouvé dans la `room 116`
(`X59904`, `Z55808` à `Z61952`). Avec le Saturn Symbol, il appelle
`NeatAndTidyTriggerCutscene(17, 0)`. Deux blocages de port empêchaient
la cutscene de démarrer : `lara.look` est forcé à TRUE chaque frame
(hack d’entrée PSXPC) et la fonction `NeatAndTidyTriggerCutscene`
n’avait pas de branche par défaut `cutseq_num = value`. Après
correctif (`input & IN_LOOK` au lieu de `lara.look`, défaut
`cutseq_num = value`), la cutscene 17 (= `CUT_ANDREA1`) se charge
(`Load_and_Init_Cutseq num=17`) et se joue réellement (capture
cinématique `play-ending-20261104/ending-00.png`).

La cutscene 17 n’est pas la fin du niveau. La fin réelle est le
`TO_CUTSCENE` **16** (`CUT_ANDREA2`) situé sur la tuile de sortie de la
`room 171` après `FlipMap(8)` (`X59904`, `Z69120`). Séquence validée :
pickup réel du Saturn Symbol → `FlipMap(8)` → déplacement sur la tuile de
sortie → `Load_and_Init_Cutseq(16)` → cutscene jouée →
**`gfLevelComplete=2`**. Preuve `play-exit16-20261104/` : `E16 LOAD num=16`,
`E16 COMPLETE value=2`, captures `exit-*.png`. Le niveau 1 (Streets of Rome)
est donc terminé par la cutscene réelle, sans synthèse.

Transition de niveau validée : après `gfLevelComplete=2`, le gameflow charge
le niveau 2 (`gfCurrentLevel == 2`, Trajan’s Markets). Preuve
`play-level2c-20261104/attempt1.log` (`L2 LEVEL2`) et capture
`play-level2c-20261104/attempt1.png` (Lara dans un couloir de pierre, revolver
au sol). Le niveau 1 est donc entièrement bouclé jusqu’au niveau suivant.

Départ du niveau 2 (Trajan’s Markets) vérifié : `room 50`, position
`X91648 Y0 Z42496`, salle `X87040 Z38912` (6×6). Preuve
`level2-start-20261104/level2-start.png` et `level2-items-20261104/`. Les
objets proches inventoriés : `item 6` (`REVOLVER_AMMO_ITEM`, room 2),
`item 19` (`LASERSIGHT_ITEM`, room 25) ; aucun `REVOLVER_ITEM` dans la salle
de départ.

Pickups du niveau 2 validés :
- `item 19` (`LASERSIGHT_ITEM`, room 25, `X89600 Y-512 Z47616`) →
  `AddDisplayPickup(obj=351)` ; preuve `level2-laser2-20261104/` ;
- `item 2` (`CROWBAR_ITEM`, room 1, `X89600 Y-512 Z36352`) →
  `AddDisplayPickup(obj=240)` ; preuve `level2-crowbar-20261104/` ;
- `item 115` (`SHOTGUN_ITEM`, room 135, `X70144 Y0 Z48640`) →
  `AddDisplayPickup(obj=338)` ; preuve `level2-shotgun-20261104/`.
Les trois tests confirment `L2 LEVEL2 start room=50`, `TestLaraPosition=1` et
le pickup effectif.

Poulie : `PulleyCollision` est implémenté (port TOMB4) et assigné à
`PULLEY`. Test niveau 2, `item 27` (`PULLEY`, room 33, `X81408 Y-2048
Z25088`) : Lara entre `STATE_LARA_PULLEY` (104), animation 339
(`GRAB`), puis passe à l’animation 340 (`PULL`) ; `trigger_flags` décroît de
1 à 0. Preuve `level2-pulley4-20261105/` (frames 7028→7057, `trig=0`).

Le déclencheur de la tuile de la poulie est : type spécial 20, puis
`SWITCH` sur `item 27` (`flags=0x3E00`) avec pour cibles `item 11`
(`TRAPDOOR1`), `item 15`/`16` (`ANIMATING3_MIP`), `item 17` (`ANIMATING4`)
et un `TO_FLYBY` de valeur 1. Preuve `trig27-20261105/`. C’est le mécanisme
d’engrenage. Test complémentaire : `SPOTCAMS 1` est bien appelé après la
traction (`level2-pulley-gear-20261105/`). En revanche, les objets cibles
restent `status=0`, `active=0` : `item 11` (`TRAPDOOR1`), `item 15`/`16`
(`ANIMATING6_MIP`) et `item 17` (`ANIMATING7`) n’ont pas de routine de
contrôle assignée dans le port, donc `AddActiveItem` les laisse inactifs.
Le flyby est déclenché, mais l’activation visuelle des engrenages reste
incomplète.

Diagnostic complémentaire : en appelant directement `_TestTriggers` sur la
tuile de la poulie avec `items[27].status = ITEM_DEACTIVATED`, les cibles
reçoivent bien `flags=15904` (`0x3E20`) et `status=1`, mais restent
`active=0` : `AddActiveItem` ne les ajoute pas car leur `control` est NULL.
L’assignation générique `ControlAnimatingSlots = AnimateItem` à
`TRAPDOOR1..3` et aux `ANIMATING` non-MIP a été testée puis **revertée** :
elle provoque un SIGSEGV dans `iRotSuperPackedYXZ_AI` (données de frame
invalides pour ces objets). Preuve `trigger-pulley-20261105/`.

Seconde poulie (`item 36`, room 51, `X72192 Y-2048 Z25088`) : la traction
fonctionne aussi (`STATE_LARA_PULLEY` 104, anim 339→340, `trigger_flags`
1→0), mais aucun `DoorControl` ni flyby n’est observé ensuite. Le trigger
de sa tuile est un `SWITCH` sur `item 36` (`flags=0x3E00`) dont la seule
cible est `item 18` (`RAISING_COG`, room 24, `X74240 Y3072 Z32256`).
`RAISING_COG` n’avait alors pas de routine de contrôle dans le port, donc
`AddActiveItem` le laisse inactif : la porte circulaire n’est pas déclenchée.
Preuves `pulley36-direct5-20261105/` et `trig36-20261105/`.

### Poulie, engrenages et RAISING_COG (5 novembre 2026, build-gameplay56)

Le diagnostic précédent identifiait à tort `item 18` comme `HIGH_OBJECT1`.
La table d’objets compilée et la sonde runtime donnent `item 18 = RAISING_COG`
(389, room 24, `X74240 Y3072 Z32256`). Les cibles du trigger de la poulie 27
sont `item 11 = TRAPDOOR1` (106), `item 15`/`16 = ANIMATING3_MIP` (421) et
`item 17 = ANIMATING4` (422) ; le `TO_FLYBY 1` est conservé.

Correctifs fondés sur `GAME`/`SPEC_PSXPC_N` et sur les preuves runtime :

- `GetSwitchTrigger` : `trigger_index` est lu après `GetFloor`/`GetHeight`, et
  la boucle examine chaque mot de trigger (`data++`) au lieu de sauter les
  mots impairs. Sans ces deux corrections, `InitialiseRaisingCog` ne voyait
  pas la poulie 27 (`n=0` puis `n=2` au lieu de `n=3`).
- `_TestTriggers` : le marqueur `TRIGTRIGGER_TYPE` est désormais un verrou
  (retour immédiat tant que `IFLAG_TRIGGERED` 0x20 n’est pas posé), conforme
  au code PC. `ControlTriggerTriggerer` pose/efface ce bit.
- `InitialiseRaisingCog` / `ControlRaisingCog` portés. L’initialisation
  croisée est rejouée après la boucle `InitialiseItem` car l’initialisation
  de la poulie 27 remettait `item_flags[1]` à zéro
  (`PortInitialiseRaisingCogs`).
- `ControlRaisingCog` ne retire l’objet actif qu’à la fin de la troisième
  étape. Avec le retrait après chaque étape (code PC brut), le cog s’arrêtait
  à `item_flags[0]=1` et la poulie 27 restait verrouillée ; la séquence réelle
  prouve les trois étapes.
- `ControlAnimatingSlots` / `InitialiseAnimatingSlots` : première
  implémentation (cas `trigger_flags` 0, 2, 333, 555 et animation active).
  Assignation limitée à `LVL5_TRAJAN_MARKETS` pour
  `ANIMATING3_MIP`/`ANIMATING4` et `TRAPDOOR1..3` : l’assignation globale
  `ANIMATING1..16` faisait crasher le plan du titre via `ANIMATING4`
  (`iRotSuperPackedYXZ_AI`). Les branches `111/222/666/667/668/777/888`
  restent à porter.

Séquence réelle validée (`sequence-real2-20261105/`) : traction poulie 36,
cog actif (`SPOTCAMS 9`), `item_flags[0]` 0→1→2→3, `y` 3072→2304,
`item 27` déverrouillée (`item_flags[1]` 1→0), `item 28` actif, traction
poulie 27, engrenages actifs (`items 11/15/16/17 status=1 active=1
flags=15904`), `ANIMATING4` avance jusqu’à la frame 62, `SPOTCAMS 1` actif.
Aucun SIGSEGV. La suite (`flipmap[3]`, `flipmap[8]`, `gfLevelComplete`) reste
à 0 au moment de l’activation des engrenages.

Le flyby `SPOTCAMS 1` se poursuit ensuite et déclenche un `TO_FLIPMAP 3` :
`flipmap[3]` passe à `15872` (`0x3E00`). Les rooms concernées sont **147** et
**163**, de même emprise (`X75776 Z21504`, 7×5 secteurs, `Y-2048..-4096`) ;
la room 163 contient `item 119` (`UZI_AMMO_ITEM`, `X78336 Y-2048 Z27136`).
La porte circulaire ouvre donc l’accès à la récompense (munitions Uzi),
sans changer `flipmap[8]` ni `gfLevelComplete`. Preuves
`sequence-real2-20261105/`, `flyby-state-20261105/` et
`flip3-rooms-20261106/`.

Le même flyby contient deux entrées `TO_FLIPMAP` (3 et 4). Le code
d’origine ne conservait qu’un seul `flip` et n’appliquait que le dernier.
`_TestTriggers` collecte désormais les flips (`PortRecordFlip`) et applique
chacun d’eux à la fin du trigger. Résultat validé : `FlipMap(3)` et
`FlipMap(4)` sont tous deux appelés, `flip_stats[3]=1` et `flip_stats[4]=1`.
Les rooms **52/176** (`X75776 Z21504`, `Y1280..-2048`, porte circulaire) et
**147/163** (`Y-2048..-4096`, munition Uzi `item 119`) sont permutées.
La collecte de `item 119` fonctionne (`num_uzi_ammo` 30→60, `status=3`).
Preuve `multiflip-20261106/`.

Vue après permutation depuis la room 52 (`X79360 Y1792 Z24064`) :
`room52-20261106/screenshot.png` montre l’escalier/passage dégagé derrière
la porte circulaire.

Diagnostic de navigation : après le flyby, `bDisableLaraControl` reste à 1
tant que la séquence de spotcam n’est pas terminée. Le flyby se termine
naturellement au 6e échantillon (`spot=0`, `dis=0`), donc le contrôle revient
sans patch. En forçant `bUseSpotCam=0` trop tôt, le contrôle restait bloqué ;
en laissant la séquence finir (ou en remettant `bDisableLaraControl=0` pour
la sonde), Lara marche normalement (`input=0x1`, déplacement dans la room 52).
Le graphe de portes du niveau donne plusieurs routes depuis la poulie 27.
Parcours **réellement marché** après le flyby, sans téléportation pendant la
marche : **room 33 → 223 → 18 → 21**, en maintenant `Up`.
Positions relevées : `81408,-2048,25600` (room 33) → `81408,-2048,28439`
(room 223) → `81408,8,29878` puis `81408,1280,30149` (room 18) →
`81408,1024,32001` (room 21) → `81408,1024,34727` (room 21, près de la
trappe `item 11` et des engrenages). Le joueur atteint donc la zone des
engrenages par la porte ouverte. Preuve `walk33-20261106/`.

Autre route issue du graphe : **33 → 223 → 221 → 163 → 164 → 166** pour la
chambre Uzi et la suite.

Exploration réelle dans la room 21 : `(81408,1024,34727)` →
`(83215,1024,32869)` → `(85915,1024,33093)`, toujours en room 21. Les portes
de la room 21 ciblent 18, 225 et 22 ; le passage vers la room 22/23 (objets et
engrenages) n’est pas encore franchi. Preuve `walk21c-20261106/`.

Données de room utiles (`rooms212223-20261106/`) :
- room 21 : `X78848 Z30720`, 6×8, portes 18/18/225/22 ; plusieurs cellules ont
  `sky_room=225`, donc une ouverture de plafond vers la room 225.
- room 22 : `X79872 Z30720`, 6×7, une porte vers 21.
- room 23 : `X69632 Z30720`, 6×8, portes 224/224/224/16/16/24 et
  `sky_room=224` sur plusieurs cellules.
La suite probable est donc room 21 → room 225 par l’ouverture/les escaliers,
puis 225 → 3/223/21.

Données de la room 225 (`room225-20261106/`) : `X79872 Z30720`, 6×7,
`minfloor=-2048`, `maxceiling=-4352`, portes 21/223/223/3, et `pit_room=21`
sur de nombreuses cellules : la room 225 est juste au-dessus de la room 21,
reliée par un trou. Une tentative de montée depuis le centre de la room 21
avec `Up+Action` donne `input=0x100041` mais Lara reste immobile
(`state=2`, `anim=103`, position inchangée) ; l’escalade n’est pas encore
trouvée.

Room 223 (`room223-20261106/`) : `X78848 Z26624`, 6×7, `minfloor=-2048`,
portes 18/33/225/225/18/221, et `pit_room=18` sur les cellules x2–5, z1–4.
La marche vers le nord depuis l’entrée de la room 33 tombe donc dans la
room 18. Le déplacement vers l’ouest est bloqué vers `x≈80997`.

Les portails ont été décodés (`doorsfull-20261106/`, format
`AdjoiningRoom + Normal + 4 vertices`) :
- room 223 → 221 : paroi ouest, `x≈79871`, `z=28672..31744`,
  `y=-2048..0`. Le portail est derrière la fosse ; il faut probablement
  sauter sur l’étroite corniche ouest.
- room 221 → 163 : paroi nord, `x≈77824..78848`, `z≈27647`.
- room 21 → 225 : ouverture horizontale à `y≈-2048`,
  `x=80896..86016`, `z=31744..36864`.
- room 163 → 164 : `x≈77776..78848`, `z≈23551`.

La route room 223 → 221 n’est pas encore franchie par la fosse ; elle a été
validée depuis la corniche ouest (téléportation de test au point
`80500,-2048,30000`, puis marche réelle) :
**room 223 → 221** (`79325,-1729,30000`) → chute dans **room 15**
(`78342,1280,30000`) → **room 16** (`75679,1280,30000`) →
**room 23** (`72198,1024,32797` puis `71640,1024,34161`).
Le joueur atteint donc la **zone des engrenages (room 23)** par la marche.
Preuve `walk23b-20261106/`.

Portails room 16 → 23 : `x=71680..72704` et `x=73728..75776`, `z≈31744`.
Portails room 23 → 224 : plans horizontaux `x=71680..72704`/`73728..75776`,
`z=31744..35840`. Portail room 23 → 24 : `x=70656..75776`,
`z=32768..34816`, normale `-y`.

Structure verticale (`room224-20261107/`) :
- room 224 : `X69632 Z30720`, 6×8, `minfloor=-2048`, portes
  23/23/23/222/222/154/232, `pit_room=23`, `sky_room=232`.
- room 24 : `X69632 Z30720`, 6×7, `minfloor=3072`, `maxceiling=1024`,
  porte 23, `sky_room=23` (salle basse en cul-de-sac).
- room 222 : `X69632 Z26624`, 6×8, `minfloor=-2048`, portes
  224/224/16/51/168/16/221, `pit_room=16`.
- room 232 : `X69632 Z30720`, 6×8, `minfloor=-4096`, `maxceiling=-6144`,
  portes 205/224/168, `pit_room=224`.
- room 154 : `X70656 Z34816`, 5×6, `minfloor=-2048`, portes
  203/83/224/205/84.
La room 23 (floor 1024) est sous la room 224 (floor -2048) ; la suite
demande donc une montée par un trou/escalier ou un passage par 222/232.

Retour vers le marché bas : depuis la room 15 (`78000,1280,28500`), la marche
vers le sud traverse le portail et entre dans la **room 52** à
`78000,1280,27447`, puis descend à `78000,256,22629` (room 52).
Le portail **room 52 → 161** est à `z≈22527`, `x=76800..79872`, normale `+z`.
Le joueur s’arrête à `z=22629`, juste avant le portail. Essais réels :
- `Up+Jump` : Lara saute sur place (`state=28`) mais ne franchit pas ;
- `Up+Duck` : elle passe en rampement (`state=80`, `anim=263`) et recule
  légèrement à `z=22729`, puis reste bloquée.
Le passage 52 → 161 demande donc un alignement/geste plus précis (ou un
téléport de validation). La room 161 contient `item 118`
(`ANIMATING1`, `78336,256,22016`). Preuves `walk52route-20261107/`,
`walk161-20261107/` et `walk161c-20261107/`.

Depuis la room 161 (`78336,256,22016`), la marche vers le nord traverse :
**161 → 52** (`78336,256,23304`) → **15** (`78336,1280,27675`) →
**17** (`78336,1024,33503`) → **46** (`78336,1024,36417`) →
**9** (`78336,256,39331`) → **10** (`78336,256,40788`) →
**207** (`78336,0,45159`) → **219** (`76395,0,46181` puis
`71781,0,46528`). Le joueur atteint donc la room 219 en marchant.
Preuve `walk161n-20261107/`.

Room 219 : `item 138` = `DOOR_TYPE3` à `76288,0,46592` et
`item 139` = `PICKUP_ITEM4` à `71168,0,47616`. Le joueur s’arrête à
`71781,0,46528`, à proximité de l’objet et de la porte. Preuve
`walk219-20261107/`.

Collecte validée (`pickup139-20261107/`) : `item 139` (`PICKUP_ITEM4`)
passe à `status=3` ; `DEL_picked_up_object` exécute la branche
`PICKUP_ITEM4` (`lara.pickupitems |= 8`, son de secret `CDA_XA1_SECRET`).
C’est donc un **secret**. La porte `item 138` (`DOOR_TYPE3`) reste à
`status=0`, `anim=601`, `state=0`, `goal=0` : elle n’est pas encore ouverte.

En marchant vers l’est depuis la room 219 à `z=46528`, Lara passe à côté de
la porte 138 (`z=46592`) et entre dans la **room 207** (`77487,0,46528`),
puis s’arrête à `78747,0,46528`. Preuve `walkdoor138-20261107/`.
Le portail **room 207 → 201** est horizontal : `x=76800..78848`,
`z=44032..48128`. Les cellules 7–10 et 13–16 de la room 207 ont
`sky_room=201`, et les mêmes cellules de la room 201 ont `pit_room=207` :
les deux rooms sont **superposées avec un trou**, pas une simple marche.
Room 207 : `minfloor=0` ; room 201 : `minfloor=-1024`.
Le joueur s’arrête à `x=78747,z=46528`, cellule 15, **juste sous le trou**.
Essais de saut (`jump201-20261107/`, `jump201b-20261107/`) : Lara entre
effectivement dans la room 201 en vol (`room=201`, `y≈-954/-884`), mais
retombe dans la room 207. Pour rester en 201, il faut atterrir sur une
cellule solide : la room 201 a des murs en x3 et des trous x1–2/z1–4 ;
les cellules solides sont x0 et la bordure z0. Un saut lancé vers l’est
(x≈77000 → 79000) ou un passage par la bordure z0 est nécessaire.
Preuve `floors207-20261107/`.

Essai complémentaire au sud (`jump201c-20261108/`) : depuis
`78747,0,44500` face au sud, le saut ne monte pas dans 201 ; il traverse
la limite et retombe dans la room 10 (`78747,0,43259`), puis 9/46/17/15/52.
Le bord z0 n’est donc pas une corniche grimpable. La room 201 reste
accessible seulement en vol, sans atterrissage maîtrisé. Il faut soit une
étude géométrique du trou (maillage/échelle), soit une autre route.

La pile de rooms autour de 207/201 est un empilement 5D :
- room 46 (`minfloor=1024`) a `sky_room=214` ; room 214
  (`minfloor=-1024`) est au-dessus, avec `pit_room=46` ;
- room 214 → 213 est horizontal (`z≈38912`, `x=76800..80896`) ;
- room 213 → 209 est horizontal (`z≈39936`, `x=76800..80896`) ;
- room 12/45 sont encore au-dessus (`minfloor=-2048`), reliées à 214/213.

Sans vue du maillage ou d’un walkthrough, les sauts à l’aveugle dans ces
trous ne permettent pas de déterminer la route prévue.

Le walkthrough Stella confirme les objectifs de Trajan’s Markets : les trois
`PICKUP_ITEM4` (items 14/88/139) sont les **golden roses** (secrets), et la
**golden coin** est `item 122` = `PUZZLE_ITEM3` (obj 174) en room 166
(`83456,-1024,19968`). Collecte validée (`coin122-20261112/`) :
`lara.puzzleitems[2]` 0→1, `item.status=3`.

Placement validé (`hole42b-20261112/`, `hole42c-20261112/`) :
`item 42` = `PUZZLE_HOLE3` (obj 244) en room 63 (`78336,-1024,15872`).
`PuzzleDone` le transforme en `PUZZLE_DONE3` (obj 252, `status=2`,
`flags=15904`) et active la **porte item 113** (obj 288, room 134,
`76288,0,37376`) : `status=1`, `flags=15904`. C’est la porte « qui s’ouvre
ailleurs » du walkthrough. Aucun flipmap n’est modifié.

Tentative de traversée (`walk134-20261113/`) : `DoorControl(113)` initialise
`data` et laisse `status=1`, `flags=15904`, `anim=601`, `frame=0`.
Le téléport à `76288,0,37900` est reassigné en **room 83** (`y=-2048`) ;
la marche sud s’arrête à `76288,-2048,35941`. La porte est donc bien
activée, mais son franchissement relève encore de l’empilement 5D
(room 134 vs room 83).

Données de rooms (`rooms134b-20261113/`) :
- room 134 : `X70656..75776`, `Z34816..41984`, `minfloor=0`, sol principal 0.
- room 83 : `X74752..80896`, `Z34816..37888`, `minfloor=-2048`.
- la porte 113 (`76288,0,37376`) est juste à l’est de la room 134, entre
  134 (haut, y=0) et 83 (bas, y=-2048).
L’approche correcte est donc depuis la room 134, à `x≈75000, y=0,
z=37376`, en marchant vers l’est à travers la porte.

Traversée validée (`walk134c-20261113/`) : depuis
`75000,0,37376` (room 134), la marche est passe par `76335,0,37376`
(room 134, au-delà de la porte 113) puis `77792,256,37376` (room 46) et
s’arrête à `78747,768,37376`. La porte de la golden coin est donc bien
franchie et ramène dans la zone de la cour (room 46).

Retour à la rue pavée validé (`walk0-20261113/`) : depuis
`78747,768,37376` (room 46), marche nord puis est :
`78747,256,40027` (room 10) → `81614,256,42988` (room 0) →
`83118,0,43975` (room 0, rue pavée). La boucle de la golden coin est
donc bouclée.

Prochaine zone : la rue pavée, la petite porte du mur blanc, l’allée et
le bassin. Les symboles VENUS/MARS sont probablement parmi les objets
`PUZZLE_ITEM` restants :
- item 49 (`PUZZLE_ITEM5`) room 64, `55808,1792,34304` ;
- item 63 (`PUZZLE_ITEM4`) room 69, `45568,1792,43520` ;
- item 129 (`PUZZLE_ITEM1`) room 196, `56832,4864,52736`.
La room 70 contient le mécanisme `ANIMATING5` et la trappe `item 71`
(Mouth of Truth), près du bassin.

Symboles VENUS/MARS validés (`symbols-20261113/`) :
- `item 49` = `PUZZLE_ITEM5` (room 64) collecté : `puzzleitems[4]=1`,
  `status=3` ;
- `item 63` = `PUZZLE_ITEM4` (room 69) collecté : `puzzleitems[3]=1`,
  `status=3` ;
- placement dans `item 95` (`PUZZLE_HOLE4`) et `item 96`
  (`PUZZLE_HOLE5`) : objets 253/254 (`PUZZLE_DONE4/5`), `status=1`,
  `flags=15904`.

Aucun flipmap n’est modifié et aucune porte de la plage 284–295 ne change
d’état après le placement. Les triggers des deux réceptacles ciblent
cependant `item 106` (`CLOSED_DOOR1`, obj 300, room 116,
`51712,-256,27136`) en plus des effets (portal, flammes, X-ray).

Correctif moteur (`build-gameplay58`, `closeddoor-20261113/`) :
`PortSetupGameplayObjects` assigne désormais `DoorControl` / `DoorCollision`
aux objets `CLOSED_DOOR1..CLOSED_DOOR6` (non-MIP), comme le setup PC.
Après placement des symboles, `item 106` passe à `status=1`,
`flags=15904`, `data` initialisé, et `DoorControl(106)` l’anime. Le contrôle
manquait auparavant (`control == NULL`), ce qui laissait la porte inactive.
La traversée réelle de cette porte reste à jouer.

Remarque build : le build propre échoue encore sur des déclarations
préexistantes (`anims` dans COLLIDE.C, `GetFloor` dans OBJLIGHT.C, `input`
dans TRAPS.C, `TestCollision`/`GLOBAL_*` dans SWITCH.C). `build-gameplay58`
a été produit en recompilant uniquement `SETUP.C` puis en reliant les objets
de `build-gameplay57`.

Tentative de téléportation dans la room 201 à `77500,-1024,43500` :
`UpdateLaraRoom` reassigne la room à **10** (empilement 5D des rooms), puis
la marche nord retombe dans la room 207 et s’arrête à `77500,0,48031`.
Le téléport direct dans 201 n’est donc pas fiable ; il faut passer par une
cellule solide ou par une autre route.

Route alternative identifiée : la room 209 est reliée à la **room 10**
(porte 10 de la room 209), elle-même déjà traversée lors du grand parcours
(`78336,256,40788`). Cela permettrait d’éviter le trou 207 → 201 et
d’enchaîner **209 → 206/210/213**. Preuve `walk209b-20261107/`.
La room 52 est la salle basse ; la room 163 (munition Uzi) est au-dessus
(`sky_room=163` dans plusieurs cellules de la room 52). Les portes de la
room 163 ciblent 52, 221 et 164. Le parcours joué à travers 223/221/163
reste à effectuer. Preuves `doors52-20261106/`, `doors33-20261106/`,
`roomgraph-20261106/` et `navwalk-20261106/`.

Porte au crowbar : `item 0` (`DOOR_TYPE1`, room 0, `X81408 Z43520`,
`trigger_flags=2`). Avec le crowbar en inventaire et
`GLOBAL_inventoryitemchosen=CROWBAR_ITEM`, `DoorControl(0)` est activé
(`status=1`, `flags=15904`, `goal_anim_state=1`). Preuve
`level2-crowbardoor0e-20261104/`. La séquence crashe toutefois ensuite dans
`DEL_CalcLaraMatrices_Interpolated_ASM` (`lara.right_arm.frame_base`,
animation 403) : l’état d’animation des bras après l’ouverture au crowbar
reste incomplet. L’ouverture n’est donc pas validée de bout en bout.

Le mécanisme `SWITCH_TYPE7` item 72 n’est plus présenté comme « Mouth of
Truth » : son effet vérifié est l’ouverture de la porte 71. La qualification
de panneau Mouth of Truth et la route jouée jusqu’au panneau restent à
établir.

Repérage (téléportation de test, **pas** un parcours joué) : la **cour de la
fontaine** est la `room 59` autour de `X54000 Z41000 Y256` ; un Doberman et
la grille verrouillée y sont visibles (`play-tp59-20261029/01.png`). La
`room 69` est un toit/point de vue sur la ville, pas la fontaine
(`play-tp69-20261029/`). La route jouée jusqu’à cette cour reste à établir.

Parcours réel effectué sans téléportation (29 octobre) :
`room 0` (départ) → `room 2` (cour) → **`room 59` (cour de la fontaine,
fontaine visible, X55074 Z38072)** → `room 16` (ruelle sud, grille/barreaux,
X54373 Z44029). Autre branche : `room 0` → `room 2` → `room 11` (zone
**Opera Backstage**, caisse en bois et passerelle) → `room 3` → `room 44`.
Les flèches `Up/Down/Left/Right` sont les entrées fiables (les lettres AZERTY
`q`/`d` donnent des rotations ambiguës dans les tests automatisés). Preuves :
`play-east-fountain-20261029/`, `play-courtyard-20261029/`,
`play-room1-20261029/`, `play-train-20261029/`.

Limites immédiates : le maillage des portes reste statique
(`PortInitialiseDoor` n'ouvre que le plancher), ennemis/combat toujours
stubs, objets spéciaux (`CrowDoveSwitch`, `SearchObject`, `UnderwaterDoor`,
`SequenceDoor`) non couverts, et campagne réelle non jouée.

### Ce qui reste non validé

Le déclenchement est synthétique : il prouve la **mécanique de transition**
et la boucle 1→14→titre, pas une fin de niveau atteinte en jouant. Aucun FMV de
transition, crédit de fin ni sauvegarde de progression inter-niveaux n'est
validé. Le raccourci QA `look`/L1 + New Game charge le niveau 4
(`build/porting/port008-level4-20261028/`) ; `walk`/R1 retombe sur Rome.
PORT-008 reste partiel : boucle mécanique 1→14→titre et garde GAMEWAD validées,
mais fin de campagne réelle (crédits/FMV) non caractérisée. La cause racine est
la non-initialisation des gestionnaires d'objets décrite ci-dessus : tant que
`ObjectObjects`/`TrapObjects` et les handlers pickup/collision/switch/door ne
sont pas reconstruits, aucune campagne réelle n'est exécutable.

## Évidence du 18 septembre

Bundle privé : `build/reverse/autonomy-20260918-0830/`. Deux builds neufs `build-a`
et `build-b`, GLEW recompilé séparément, source jeu HEAD `fe5037a2`, exit 0.
`run-a/application.json` : lancement natif du premier binaire, fermeture demandée
via WM_DELETE_WINDOW, sortie 0 avant la borne ; captures privées à 5/15/25 s.
Les 16 tests initiaux du driver passent après RED de contrat (driver initialement
absent). La revue indépendante a rejoué avec succès un troisième build ELF32 et
30 tests, puis identifié la limite du nom CUE : test frontière 125/126 écrit RED,
préflight corrigé sans patch du jeu. Le rejeu ne comprenait pas de runtime.
Cela industrialise build/lancement et préflight, **pas** un correctif gameplay.
PORT-001 reste en cours : acceptation visuelle complète non établie ;
PORT-002/menu et gameplay non validés.


## Analyse géométrie Trajan's Markets, empilement 5D 207/201/214/213 (données, 2026-11-08, non validée en jeu)

Extraction NTSC USA LBA 18404 (252 rooms) via `offsetRoomInfo`/`roomInfoLength`. Puits `207(75776,43008,-1024) sky=201 → 201 pit=207,sky=199 → 199 pit=201,sky=200 → 200 pit=199` : aucun sol atterrissable (201 intérieur tout `pit=207`). Aucun `CLIMB`/`MONKEY` floor_data dans la zone. Hub `209(sky=11,pit=10, portails 10/11/201/206/210/213)` : `207→10` plat, `10→209` +256u (sky/pit). Montées +1024u sans `CLIMB` (rebord à valider) : nord `213(sky=45)→45`, `214(sky=12)→12` (vers `202`) ; est `210→48/211→49/212→5` (`212↔50` départ). Route plausible : `207→10→209` puis branche nord ou est ; **validation moteur requise**. Détail : [runtime-level.md](runtime-level.md).

### Porte des symboles franchie et fin de Trajan's Markets (13 novembre 2026, build-gameplay58)

Géométrie corrigée de la salle des symboles (`geom-20261113/`, `geo2-20261113/`) :

- `room 116` (X50176..56320, Z21504..31744), sol principal `y=-256`.
  Les deux réceptacles sont aux cellules `xx=1 zz=4` (X51200..52224,
  Z25600..26624) et `xx=1 zz=6` (Z27648..28672). Les triggers `KEY` 2907 et
  2915 ciblent `item 95`/`item 96` puis `item 106` (`CLOSED_DOOR1`) et les
  effets 103/102/101/97 (flamme, X-ray, portal).
- Le passage ouest de la salle est la cellule `xx=0 zz=5`
  (X50176..51200, Z26624..27648), avec `index` de porte vers `room 70`.
  La porte `item 106` est placée à `51712,-256,27136`, juste devant ce
  passage ; les deux réceptacles l'encadrent au nord et au sud.
- Le moteur `GetFloor` PSX est **transposé** : `index = zz + xx*x_size`
  (`x_size` = nombre de cellules en Z, `y_size` = nombre en X). Les dumps
  antérieurs qui utilisaient `zz*x_size+xx` étaient donc transposés.

Traversée réelle de la porte (`walkgate-20261113/`) : après placement des
deux symboles (même chemin que le jeu : `PuzzleDone` + `_TestTriggers` sur
les cellules des réceptacles), `DoorControl(106)` anime la porte
(`status=1`, `flags=15904`, `anim=613`). Depuis `52000,-256,27136` face à
l'ouest, la marche réelle passe `room 116 → room 70` à `x=50585`, puis
`room 204` à `x=49097` (`y` passe de `-256` à `1536` par le trou
`pit_room=204`). Elle s'arrête à `x=47205` : la cellule `xx=5 zz=2` de la
room 204 (`X46080..47104`) a `floor=1536`, `ceiling=0` et un `index` de
porte vers la room 70 ; elle est traitée comme un mur plein. Les sauts
successifs ne la franchissent pas (`spike-20261113/`, `spike2-20261113/`,
`spike3-20261113/`).

Géométrie de la caverne finale :

- la rangée `zz=2` de la room 204 est un pont surélevé à `y=1536` avec six
  `TEETH_SPIKES` (items 132–137, X44544..50688, Z27136) ; `TEETH_SPIKES`
  n'a aucun contrôle/collision dans le port, mais le pont est coupé par la
  cellule solide ci-dessus ;
- à l'ouest, `room 241` (X40960..44032, Z25600..28672) forme la corniche
  intermédiaire (`y=0/2304/3584`) et sa cellule `xx=0 zz=1` ouvre sur
  `room 233` ;
- `room 233` (X33792..43008, Z25600..28672) est un couloir descendant dont
  le sol remonte vers l'ouest de `2304` à `9728` ; le trigger `TO_FINISH`
  (idx 5606) est en `xx=4 zz=1`, soit **X37888, Z26624** ;
- le déclencheur final est donc bien `FINISH:0` en room 233, et non une
  porte de la plage 284–295.

Fin de niveau et transition (`finish-20261113/`, `levelend2-20261113/`) :
depuis `42100,2304,27136` (room 233), la pente déclenche le glissement
scripté (`state=24`, `anim=70`) vers l'ouest : `42100 → 41029 → 39958 →
38887`, `y` 2304 → 6680. En entrant dans la cellule du trigger,
`gfLevelComplete` passe à **3** ; `DoLevel` est ensuite appelé avec
`name=3` et `gfCurrentLevel=3` : **The Colosseum** est chargé.

Limites honnêtes de ce jalon : le pont à pointes n'a pas été franchi en
marche/saut (mur plein en X46080..47104) ; la fin a été atteinte en
téléportant Lara sur la dernière pente, puis le glissement et le trigger
`TO_FINISH` sont exécutés par le moteur. Les symboles ont été posés par
sonde (`PuzzleDone` + `_TestTriggers`), pas par navigation d'inventaire.
La traversée réelle porte 106 → room 70 est, elle, jouée.

### Entrée dans The Colosseum — repérage (13 novembre 2026, build-gameplay58)

Après la fin de Trajan's Markets, `DoLevel(name=3, gfCurrentLevel=3)` charge
le niveau 3. État de départ relevé (`level3-recon-20261113/`) :
`lara room=1 pos=96768,-384,52736`, 125 rooms, 110 items.

Objets utiles du début de niveau :

- `item 100` = `PUSHABLE_OBJECT1` en room 112, `79360,4864,54784`
  (bloc à anneau de la première salle secrète) ;
- `item 99` = `PICKUP_ITEM4` (golden rose) en room 112,
  `81408,4864,57856` ;
- `item 5` = `TELEPORTER` et items 6–19 = `CRUMBLING_FLOOR`/`EARTHQUAKE`
  en room 8 autour de `X40448..43520, Z51712..53760` (effondrement
  au-dessus de la lave) ;
- `item 75` = `PICKUP_ITEM4`, `item 124` = six `TEETH_SPIKES`
  (salle finale), etc.

Parcours réellement joué au démarrage (`level3walk-20261113/`) : le
glissement d'introduction part de `96768,-384,52736` (room 1), traverse
`room 20` (`x≈92025..85435`, `y` 3718 → 4352), puis `room 2` et s'arrête à
`77925,4351,52736` (cellule `xx=3 zz=2` de la room 2). La marche vers
l'ouest y est bloquée ; le carrefour de la room 2 ouvre au nord
(`zz=0` → rooms 22/5) et au sud (`zz=3` → rooms 19/4). Le bloc
`PUSHABLE_OBJECT1` est au sud de ce carrefour (`Z54784`).

Limite identifiée : `PUSHABLE_OBJECT1..5` n'ont ni `initialise`, ni
`control`, ni `collision` dans `PortSetupGameplayObjects` ; le premier
secret (golden rose item 99) et le passage du bloc ne sont donc pas
jouables tant que ce comportement n'est pas porté depuis la source PC.
C'est le prochain travail moteur pour The Colosseum.

### Blocs poussables portés — The Colosseum (13 novembre 2026, build-gameplay59)

`PUSHABLE_OBJECT1..5` n’avaient ni `initialise`, ni `control`, ni
`collision`. Portage depuis `game/moveblok.cpp` de la source PC :

- nouveau module `GAME/MOVEBLOK.C` / `MOVEBLOK.H` :
  `InitialiseMovingBlock`, `MovableBlock`, `MovableBlockCollision`,
  `TestBlockPush`, `TestBlockPull` ;
- `PortCollidedObjects` : sous-ensemble local de `GetCollidedObjects`
  (la version globale du port est un stub ; les blocs ne consultent que
  la liste d’items, sans statiques) ;
- `PortSetupGameplayObjects` assigne ces trois handlers à
  `PUSHABLE_OBJECT1..PUSHABLE_OBJECT5` (`save_position`, `save_flags`).

Réception jouée (`push100e-20261113/`, `push100f-20261113/`,
`build-gameplay59`, SHA256 `52c73c373ee86ed6c5c3a08e60eb14c51cb9350550f38797079551f759b0b4a3`) :

- `item 100` (bloc à anneau, room 112, `79360,4864,54784`), bounds
  `[-512,512,-1024,0,-512,512]` ;
- depuis le sud (`55300,4864,54784` face au nord), `MovableBlockCollision`
  accroche Lara : `MoveLaraPosition` la cale à `79360,4864,55391`,
  `state=38` (`PUSHABLE_GRAB`), `anim=120` ;
- à la fin de l’animation ready (frame 2067), `IN_FORWARD` déclenche
  `state=36` (`PUSHABLE_PUSH`), `anim=123`, `item 100.status=1` ;
- le bloc suit la main : `z` 54784 → 54583 → 54427 → 54346 → 54092 →
  53929 → 53790, puis se cale à **53760** (−1024) ; Lara sort par
  `anim=417` (`PUSHABLE_PUSH_TO_STAND`) et `TestTriggers` est appelé à la
  nouvelle position ; `item 100.status` revient à 0.
- L’approche par le nord échoue : le snap place Lara à `54177`, que
  `UpdateLaraRoom` réassigne à la **room 19** alors que le bloc est en
  room 112 ; `PortCollideItems` n’appelle donc plus le handler et la
  transition ready→push ne part pas. C’est une limite de l’empilement de
  rooms, pas du portage.

Limite préexistante confirmée : `GetSpheres` est `UNIMPLEMENTED()` dans
`SPEC_PSXPC_N/SPHERES.C`, donc `TestCollision` renvoie toujours 0 et
`ObjectCollision` ne repousse pas Lara contre les objets. Le bloc peut
être traversé si Lara marche dedans sans être accrochée ; l’accroche
`TestLaraPosition`/`MoveLaraPosition` fonctionne, elle. Prochain travail :
`GetSpheres` pour rétablir la collision solide générale.

Le secret lui-même (golden rose `item 99`, room 112,
`81408,4864,57856`) n’a pas encore été ramassé : le bloc a seulement été
poussé d’une case vers le nord. Le build propre reste bloqué par les
déclarations préexistantes ; `build-gameplay59` a été produit en
recompilant `MOVEBLOK.C` et `SETUP.C` puis en ajoutant l’objet au
`link.txt` de `build-gameplay58`.

### Premier secret de The Colosseum — état (13 novembre 2026)

Après le portage des blocs poussables, le bloc `item 100` a été poussé
d’une case (`z 54784 → 53760`) puis Lara a été replacée dans la case
libérée `79360,4864,54784` face au sud-est (`rose99-20261113/`). La marche
atteint `81570,4864,58071` (room 112) sans obstacle : le passage vers la
salle du secret est donc ouvert après la poussée.

Le ramassage de la golden rose `item 99` (`81408,4864,57856`) échoue de
peu (`rose99b-20261113/`) : `PickUpCollision` exige
`MoveLaraPosition`, qui tolère 256 unités ; la cible est
`z = 57856 - 100 = 57756` et Lara s’arrête à `z = 58022`, soit 266 unités.
`TestLaraPosition` passe, mais le snap échoue de 10 unités. Le pas de
marche (`Shift_R`) n’a pas fonctionné dans l’automatisation
(`input=0x2c0`, sans `IN_FORWARD`) et les tentatives suivantes sont
restées bloquées sur le démarrage titre (cutscene 11 en boucle, trois
essais). Le ramassage reste donc à rejouer en téléportant Lara sur la
cible exacte `81408,4864,57756` puis en maintenant Action.

Mise à jour : la golden rose a été ramassée (`rose99h-20261113/`).
Le téléport à `81408,4864,57400` subit le décalage de collision habituel
(+356 en Z) et laisse Lara à `57756`, exactement la cible de
`PickUpPosition` (`item 99` est en `57856`, `z - 100`). Maintien
d’Action : `PickUpCollision` cale Lara (`MoveLaraPosition`), passe
`state=39` (`STATE_LARA_PICKUP`) et `item 99.status=3`
(`ITEM_INVISIBLE`). Le premier secret de The Colosseum est donc validé
après la poussée du bloc.

### Sols qui s’effondrent — The Colosseum (13 novembre 2026, build-gameplay59)

`FALLING_BLOCK`, `FALLING_BLOCK2` et `CRUMBLING_FLOOR` n’étaient pas
assignés, alors que `FallingBlock`, `FallingBlockCollision`,
`FallingBlockFloor` et `FallingBlockCeiling` existent déjà dans
`GAME/TRAPS.C`.

- `PortInitialiseFallingBlock2` (`mesh_bits = 1`) a été ajouté dans
  `GAME/MOVEBLOK.C` : `TRAPS.C` ne peut pas encore être recompilé
  (`COLLIDE.C` dépend d’un `MoveLaraPositionToItem` absent des objets
  de build57, et l’include GTEREG casse la compilation stricte).
- `PortSetupGameplayObjects` assigne le contrôle, la collision, le
  `floor`/`ceiling` et les sauvegardes à
  `FALLING_BLOCK..CRUMBLING_FLOOR`, avec un cast ABI-compatible pour
  `FallingBlockFloor/Ceiling` (`long*` → `int*`).

Essai runtime (`crumble-20261113/`, `crumble2-20261113/`) : depuis
`40000,0,52224` (room 12, puis room 8 à `y=256`), le trigger de la
room 14 active bien les items 6–12 et 14–18 (`status=1`, `active=1`) ;
leurs `y` tremblent (0 → 2 → 7 → 9). Le mécanisme d’effondrement est
donc branché.

Il déclenche toutefois un **SIGSEGV dans `FlameControl`**
(`GetLaraJointPos` sur l’effet de brûlure), via
`QuickControlPhase → ControlPhase`. La chute dans la lave active
`LavaBurn`/`FlameControl`, et le chemin de brûlure de Lara est
incomplet dans le port. Prochain correctif : sécuriser
`GetLaraJointPos`/`FlameControl` pour les effets de feu, avant de
rejouer la traversée du gouffre de lave.

Build : `build-gameplay59`, SHA256
`9b604c38fceea138c2e96c7d2f6257e20a23ccc69a535108bab9ab5d9fecc965`,
**4177 PASS**.

Isolement du crash (`burn2-20261113/`) : un `LaraBurn()` forcé au
démarrage de The Colosseum crée bien l’effet de feu
(`lara.burn=1`, `effects` valide) et **ne provoque pas de SIGSEGV**
dans `FlameControl` sur 120 s. Le crash du test `crumble2` n’est donc pas
le chemin de brûlure seul : il dépend des items `CRUMBLING_FLOOR` /
`FallingBlock` et des effets qu’ils manipulent pendant l’effondrement
(`FlameControl` sur un slot d’effet dont l’état a été corrompu par
l’effondrement). Prochaine investigation : instrumentation de
`FallingBlock`/`KillItem`/`RemoveActiveItem` pendant l’effondrement,
avec un backtrace complet des registres et de la pile.

Tentative de recompilation propre de `TRAPS.C` : `PSXINPUT.H` ajouté
(corrige l’erreur préexistante `input`), et deux définitions **faibles**
ajoutées dans `MOVEBLOK.C` (`SetLaraPosition`, `MoveLaraPositionToItem`,
copiées de `GAME/COLLIDE.C`) pour combler les symboles absents du
`COLLIDE.C.o` de build57. `TRAPS.C` compile et se lie
(`build-gameplay59`, SHA256
`ef47e93331245163904e384a2c8a8ae92b15e44cf3dd6461e6598d67af7f66f1`).

Le crash change de forme (`crumble4/`, `crumble5-20261113/`) : il devient
un SIGSEGV reproductible dans `DrawAggregatedSplits`
(`EMULATOR/LIBGPU.C:436`) via `VSync → LOAD_VSyncHandler → DrawOTag`,
avec une taille de lecture CD **négative** (`DEL_CDFS_Read size=-16388`)
et une pile qui remonte à `DoTitle`/`LoadLevel`. Ce n’est plus
`FlameControl` : l’effondrement + la lave corrompent l’état mémoire
(probablement via `FallingBlock`/`KillItem`/effets), et le symptôme
dépend de l’objet `TRAPS.C` lié. Prochaine étape : instrumentation de
`FallingBlock`/`KillItem`/`AddActiveItem` et de `effects` pendant
l’effondrement, avec un build entièrement propre pour éliminer les
objets hétérogènes.

Franchissement du premier gouffre (`crumble6-20261113/`) : le trigger
d’effondrement se prend en regardant vers l’**est** (`y_rot=0x4000`),
pas vers l’ouest. Depuis `40000,0,52224` (room 12), Lara entre dans la
room 8, les dalles s’activent (`status=1`), elle saute (`state=3`) quand
la grille commence à tomber, puis se réceptionne à `y=768` et poursuit
jusqu’à `43931,768,52224` (room 12). Les items 6–12 et 14–18 finissent
`active=0` (tombés). **Aucun SIGSEGV.**

Le crash `FlameControl`/`DrawAggregatedSplits` des essais précédents
venait donc de la direction opposée : en marchant vers l’ouest depuis la
cellule de trigger, Lara sortait de la zone et tombait dans la lave
derrière, déclenchant la mort puis le rechargement de niveau corrompu.
Le chemin prévu (est) est, lui, franchissable.

Suite immédiate après le gouffre (`crosswalk-20261113/`, `climb-20261113/`) :
Lara poursuit jusqu’à `43931,768,52224` (room 12) puis bute sur
l’issue fermée ; les sauts simples (`state=15/28`) retombent au même
point. Le passage prévu est donc bien le **rebord au-dessus de la fosse
de lave** : saut vers l’est avec Action maintenue pour s’y suspendre,
puis shimmy vers la gauche, passage du coin et rétablissement dans le
conduit.

Attention : l’extension de test a rencontré un crash **intermittent**
`DrawAggregatedSplits` (`LIBGPU.C:436`) via
`VSync → LOAD_VSyncHandler → DrawOTag` et une pile
`DEL_CDFS_Read/LoadLevel/DoTitle` au démarrage du niveau 3, avant même
le déplacement de Lara. Le franchissement du gouffre, lui, a réussi dans
une exécution (`crumble6`). Ce crash de transition/rechargement doit être
traité séparément de la géométrie du niveau.

Essai de suspension (`hang2-20261113/`) : en maintenant **Action + Up**
et en tapant Saut pendant la traversée, Lara enchaîne les accroches de
rebord (`state=11 REACH`) et monte le long du puits :
`y 258 → 419 → 1145 → 2522 → 4095 → 5789 → 6015` (rooms 8/12/26/14),
puis meurt (`state=8`) à `43513,6015,52224`. Les mécaniques
d’accroche/relèvement fonctionnent donc, mais l’automatisation
« saut+Action en boucle » grimpe trop haut au lieu de faire le
shimmy latéral prévu. Il faut une séquence contrôlée : une accroche,
`Left` pour longer, passage du coin, puis `Up+Action` pour se rétablir
dans le conduit.

Essais supplémentaires (`hang3-20261113/`, `hang4-20261113/`) : la
détection d’état par lecture du log (`state=11`) est trop grossière
pour déclencher le shimmy au bon moment ; selon le timing, Lara est
envoyée en diagonale puis retombe dans le puits (`state=8` à
`41719,5980,54164`, room 14). Les accroches (`state=11`) et la montée
fonctionnent, mais la séquence hang → shimmy → coin → pull-up demandera
un pilotage par waypoints (ou des captures) plutôt qu’un simple
tap+lecture de log.

Confirmation (`hang5-20261113/`) : avec `Action+Up` et un tap Saut
toutes les 0,6 s, Lara ne passe jamais en `state=10 HANG` : chaque
accroche (`state=11`) est suivie d’un nouveau saut, d’où la montée du
puits jusqu’à la mort à `43513,6015,52224`. La séquence correcte est
donc : **un seul saut** vers le rebord (Action maintenue), puis arrêt
immédiat des taps et relâchement de `Up` pour laisser le hang s’établir,
avant `Left` (shimmy) et `Up+Action` (rétablissement). L’automatisation
actuelle ne peut pas distinguer le premier `state=11` des suivants
depuis le log ; il faut un retour d’état plus fin (lecture mémoire par
frame plutôt que parsing du log).

Nouvelle mesure (`hang6-20261113/`) avec relâchement immédiat des
touches dès `state=11` : le saut est déclenché à `42444,419`, l’accroche
apparaît à `42907,1145`, puis **même avec `input=0x0`** Lara continue de
monter `2522 → 4095 → 5789` en `state=9` et meurt à `43513,6015`
(rooms 26/14). Ce n’est donc pas un problème de timing d’entrée : c’est
la collision/empilement des rooms 12/26/14 qui la propulse vers le haut
pendant `REACH`. Prochaine investigation : `lara_col_reach` /
`GetLaraCollisionInfo` / `ShiftItem` dans cet empilement, avant toute
automatisation hang/shimmy.

Instrumentation de l’accroche (`edge2-20261114/`) : au moment du
`REACH` sur le rebord, `pos=42914,1049,52224`, `fallspeed=90`,
`front_floor=-281`, `front_ceiling=-4383`, `mid_floor=4839`,
`mid_ceiling=-4383`, `coll_type=1`. `LaraTestEdgeCatch` renvoie **0**
(pas de franchissement de frontière 256 : `hdif = pos.y + bounds[2]`
reste dans le même octet après ajout de `fallspeed`). L’accroche n’a
donc pas lieu sur cette frame ; la montée observée ensuite vient des
frames suivantes / du `ShiftItem` dans l’empilement, pas d’un seul
`edge` géant. La sonde `finish` a par ailleurs provoqué un SIGSEGV
artificiel au retour de `LaraTestEdgeCatch` (`eax=0`) : il faudra une
instrumentation non intrusive (breakpoint temporaire + logique dans la
source) pour la suite.

Mesure du déplacement (`shift-20261114/`) : pendant le `REACH`,
`ShiftItem` ne produit **aucun** déplacement vertical (`shift.y = 0` à
chaque frame) ; seuls des `shift.x = -47` corrigent la position
latérale. Pourtant `pos.y` monte régulièrement (`497 → 545 → 599 → …
→ 1715`) et `mid_floor` décroît (5391 → 4173), ce qui signifie que la
vitesse verticale est **négative (vers le haut)** sur toute la durée du
`REACH`. Le saut déclenché par `Up+Action+Saut` au bord a donc une
trajectoire ascendante anormalement longue : Lara dépasse le rebord,
continue à monter, et meurt plus haut. Ce n’est pas `ShiftItem` ni un
`edge` géant : c’est la vitesse du saut/`fallspeed` en `REACH`.
Prochain essai : saut à l’arrêt (sans `Up`) ou simple chute contrôlée
depuis le bord, avec `Action` pour l’accroche.

### Géométrie du puits et exploration visuelle (14 novembre 2026)

Dump `grid3-20261114/` (rooms 8/12/14/26/27, orientation corrigée) :

- room 12 (`x=37888,z=50176`) : la corniche où se tient Lara est la cellule
  `xx=5 zz=2` (`43008..44032, 52224..53248`), sol **768** ; les cellules
  `xx=1..4, zz=1..3` ont `floor=1024` et `pit_room=26` (plateforme
  surélevée de 256, avec puits vers la room 26) ;
- room 8 (`x=38912,z=50176,y=-1024`) : sols 0 avec `pit_room=12` et
  `sky_room=25` ;
- room 26 (`x=37888,z=49152,y=1024`) : sols 1024–3072, avec
  `pit_room=14` au centre ;
- room 14 (`x=38912,z=50176,y=3072`) : sols ~5120–6144, `pit_room=26`.

Exploration manuelle avec journal `probe_play2` :

1. téléport sur la corniche `43109,768,52540` face à l’ouest ;
2. en avançant, Lara chute dans la room 8 et se réceptionne à
   `42593,256,52540` (room 8, `state=2`) ;
3. marche vers l’ouest jusqu’à `40314,256,52540`, devant un grand
   relief étoilé et un **bloc rouge** (candidat bouton) ;
4. l’appui Action n’a pas été enregistré dans les échantillons
   (`input=0x0`), puis le jeu a basculé sur
   `DOLEVEL name=121 gfCurrentLevel=18 complete=128` et le processus a
   disparu : transition/rechargement corrompu, cohérent avec le bug de
   mort/rechargement déjà observé.

Conclusion : le puits est franchi en tombant de la corniche 768 vers la
room 8 (256), qui contient le relief/levier ; l’instabilité de
transition reste le principal obstacle à une traversée continue.

Analyse statique de la transition corrompue : `gfCurrentLevel` devient 18
parce que `gfStatus==3` fait `gfCurrentLevel = gfLevelComplete`, et
`gfLevelComplete` vaut ici **128** (0x80) — valeur impossible pour une
fin normale (`gfCurrentLevel + 1`). `gfCurrentLevel=18` sort ensuite de la
table `gfScriptOffset[]`, et `DoLevel(gf[3],gf[4])` reçoit un couple
garbage (`name=121`). Aucune affectation normale de `gfLevelComplete` ne
produit 128 : il s’agit d’une **corruption mémoire** (octet écrasé), pas
d’une valeur de gameflow. Piste : instrumenter les écritures sur
`gfLevelComplete`/les structures voisines pendant l’effondrement et la
chute, ou exécuter cette section avec un build entièrement propre.

### Correctif : débordement de la file `ItemNewRooms` (14 novembre 2026)

Watchpoints (`watch2-20261114/`) : pendant la chute des dalles,
`FallingBlock` appelle `KillItem` et `ItemNewRoomNo` dépasse **200**
(201, 202, 203…). La file `ItemNewRooms[256][2]` déborde alors et
l’écriture hors bornes écrase `gfLevelComplete` à **128** ; le gameflow
passe `gfCurrentLevel=18`, `DoLevel` reçoit un nom garbage (121) et le
jeu se termine.

Correctif défensif basé sur cette preuve : toutes les écritures dans
`ItemNewRooms` sont bornées par `ItemNewRoomNo < 256`
(`EffectNewRoom`, `KillEffect`, `KillItem`, `ItemNewRoom` dans
`GAME/ITEMS.C` et `SPEC_PSXPC_N/COLLIDE_S.C`).

Validation (`watch3-20261114/`) : même séquence (corniche → room 8 →
relief/bouton → Action + 6 s) avec le build corrigé
(SHA256 `1276c879abd1b116efeae11152654c772de38bec1eb0bbad58f98736bfd1211c`) :
**aucun `GFLC128`**, aucun `DOLEVEL` parasite, le jeu reste au niveau 3
et Lara est vivante à `40037,256,52540`. Tests : **4177 PASS**.

La cause racine de l’afflux (>200 entrées dans une frame) reste à
identifier : elle suggère une boucle ou des doublons dans la liste
active des dalles. Le garde-fou empêche la corruption mémoire et la
transition invalide.

### Cause racine de l’afflux : désenchaînement incorrect (14 novembre 2026)

`RemoveActiveItem` utilise une boucle « prédécesseur » correcte, mais
`KillItem` et `KillEffect` utilisaient une boucle fautive :
```
for (linknum = items[next_item_active].next_active; ...)
    if (linknum == item_num) items[linknum].next_active = item->next_active;
```
Elle ne retire pas l’élément de la chaîne (elle réécrit son propre
`next_active`). L’élément tué reste donc dans la liste active ; comme
`item->active` est remis à FALSE, `AddActiveItem` le réinsère au début →
**doublons** à chaque frame → la boucle de contrôle appelle
`FallingBlock` des centaines de fois → `ItemNewRoomNo` dépasse 256.

Correctif (même schéma que la source PC et `RemoveActiveItem`) :
- `KillItem` : liste active et liste d’items de room ;
- `KillEffect` : liste active FX et liste FX de room.

Validation (`watch4-20261114/`, build
SHA256 `74bcbe08beea961af02fc408b10fb118decba9c22f69924715735b7e74a27348`) :
sur la même séquence, **aucun `INRN BAD` (>200)**, aucun `GFLC128`,
aucun `DOLEVEL` parasite ; seul le chargement normal `name=3` apparaît.
La corruption mémoire est éliminée à la racine (le garde-fou `< 256`
reste en défense). Lara meurt ensuite à `40337,6144` (room 14) sur le
chemin de brûlure/lave, qui reste un problème distinct.

### Correction d’interprétation de l’axe Y (14 novembre 2026)

Dans le moteur TR, **Y croît vers le bas** : les suites
`2522 → 4095 → 5789 → 6144` observées après le rebord ne sont pas une
propulsion vers le haut mais une **chute dans la fosse de lave**. Les
morts à `43513,6015` / `41719,5980` / `40337,6144` sont donc des chutes
au fond du puits, pas un bug de vitesse verticale. Le comportement
`FallingBlock` (`pos.y_pos += item_flags[1]`) fait bien descendre les
dalles ; l’interprétation « montée » des notes précédentes est corrigée
ici.

Conséquence de route : après le gouffre, marcher vers l’ouest depuis la
corniche `43109,768` fait descendre sur la plateforme `floor=1024` puis
dans les trous `pit_room=26` de la room 12, jusqu’à la lave. Le passage
correct reste l’accroche au rebord (hang) puis le shimmy, à déclencher
depuis le bord exact de la corniche.

Précision sur l’accroche (`LaraDeflectEdgeJump`, `GAME/LARA.C`) : le
`state=14 GRAB_TO_FALL` observé en sautant depuis la corniche
`43109,768` correspond à un saut qui heurte une **face avant**
(`CT_FRONT`) avec `mid_floor <= 128` : Lara rebondit et retombe, elle
n’accroche pas. L’accroche réelle se fait dans `lara_col_reach` quand
`IN_ACTION` est maintenu et que `LaraTestEdgeCatch` renvoie une arête
(`edge = (pos.y + bounds[2]) & -STEP_L`). Depuis cette corniche, le saut
avec Action percute le mur du puits : la bonne approche reste à
déterminer (bord exact, saut sans Action puis Action, ou chute
contrôlée) et devra être testée avec retour visuel.

### Reproductibilité du franchissement (14 novembre 2026)

Trois nouvelles tentatives (`hangA/hangB/hangC`) montrent que le
franchissement du gouffre est **très sensible au timing** : selon le
moment du saut, Lara retombe dans la fosse (`state=8`, `y≈5888`) avant
d’atteindre la corniche. Le saut réussi de `crumble6` n’est pas
reproductible à volonté avec des taps clavier en temps réel, et le
téléport direct sur la corniche `43109,768` est réécrit par
`UpdateLaraRoom` vers la room 8 (`42593,256`), donc inutilisable tel
quel.

Pour étudier l’accroche de corniche de façon déterministe, il faut :
- soit un **save/load rapide** (F5/F6) une fois la corniche atteinte ;
- soit désactiver les dalles pour la session de test (instrumentation)
  afin d’isoler le hang ;
- soit un pilotage par numéro de frame plutôt que par temps réel.
Les tentatives d’accroche elles-mêmes (marche avec Action, saut avec
Action, Action+Back) n’ont pas encore été exécutées depuis la corniche
réelle.

### Session visuelle avec dalles inertes (14 novembre 2026)

Pour isoler l’accroche, `objects[CRUMBLING_FLOOR].control = 0` est posé
au chargement du niveau 3 : les dalles restent solides. Lara parcourt
alors **de façon fiable** `40000,0 → 43931,768` (room 12) sans mourir.

Enseignements du harnais :
- `xdotool` ne délivre les touches que si `windowactivate --sync` puis
  `windowfocus --sync` sont appelés **juste avant** chaque touche ;
  `import` (capture) vole le focus et il faut le reprendre.
- Le breakpoint de log `CF W` avec `$w >= 160` détache GDB trop tôt et
  coupe le retour d’état ; il faut augmenter la borne pour les sessions
  longues.

Cartographie visuelle de la salle (room 12, après le pont) :
- grande salle de pierre, **grande porte en bois/portcullis fermée**
  (l’issue), bannière rouge, fenêtre grillagée en hauteur ;
- **fosse de lave** au centre/bord, avec la corniche où se tient Lara ;
- de l’autre côté du petit gouffre : le **relief vert étoilé** avec le
  bloc rouge (déjà atteint par chute dans une session précédente) ;
- niches sombres latérales (candidats crawlspace).

Les sauts tentés depuis le bord de la fosse n’ont pas franchi le petit
gap (Lara reste au bord). Prochain essai : saut lancé depuis plus loin,
ou accroche du rebord d’en face (`doorsill`) puis shimmy vers la niche
de gauche.

### Corniche : mur franc à l’ouest (14 novembre 2026)

Depuis la corniche réelle (`43364,768` puis marche jusqu’à
`43109,768,52325`, room 12, yrot=-16384), la cellule `xx=4`
(`41984..43008`) est un **mur** : `floor=1024`, `ceiling=0` (masse
pleine). Les essais :
- `Action+Up` : aucun déplacement (`state=2`) ;
- `Up` seul : bloqué (`state=2`) ;
- `Up+Saut` : `state=15` puis `state=14 GRAB_TO_FALL` — le saut est
  défléchi par `LaraDeflectEdgeJump`, pas d’accroche.

Le passage ouest depuis la corniche n’est donc pas le hang attendu. La
fosse visible en contrebas correspond aux rooms 26/14 ; le « doorsill »
doit être le rebord de la plateforme 1024, à atteindre depuis l’autre
côté (room 8 / relief), ou via une exploration nord/sud de la corniche.

### Point de reprise rapide à la corniche (14 novembre 2026)

`F5` fonctionne en jeu et écrit `TOMB5.SAV` :
`[SAVE] wrote TOMB5.SAV: level 3 room 12 X 43364 Y 768 Z 52325`.
La sauvegarde capture donc l’état exact de la corniche. En revanche,
`F6` est refusé pendant le jeu (`load ignored during gameplay; press F6
at the title`) : le rechargement rapide ne se fait qu’au **titre**. Pour
les expériences d’accroche, il faut donc relancer le jeu et presser F6
au titre — bien plus court que refaire le gouffre.

La corniche est par ailleurs un cul-de-sac à l’ouest (mur) et bordée de
trous `pit_room=26` au nord/sud (`floor=1024`, `pit` en zz1/zz3). Le
« doorsill » est à chercher depuis la plateforme 1024 ou l’autre côté du
puits.

### Cause du blocage à la corniche : `TestLaraVault` manquant (14 novembre 2026)

La corniche est un creux à `y=768` entouré de cellules à `floor=1024`
(**marche de 256**). Ni la marche (`Up`), ni `Action+Up`, ni le saut
(`Up+Saut` → `GRAB_TO_FALL`) ne la franchissent. La cause est identifiée :

`TestLaraVault` (`GAME/LARA.C`) contient tout le code PSX dans un bloc
`#if 0` et se termine par `return 0;`. Or c’est cette fonction qui gère
le **vault/step-up** (montée de marche, appui, passage par-dessus un
obstacle bas). Sans elle, toute marche de 256 est un mur et les sauts
sont défléchis.

Prochain travail moteur : porter `TestLaraVault` depuis le bloc ASM PSX
présent dans le fichier (ou la source PC), puis revalider la corniche et
les marches du niveau. C’est probablement le déblocage clé de cette zone
et de plusieurs autres.

### Port de `TestLaraVault` et harnais d’autoload rapide (15 novembre 2026)

#### Moteur : `TestLaraVault` portée

`GAME/LARA.C` terminait `TestLaraVault` par `return 0;` (tout le code
PSX sous `#if 0`). La fonction est maintenant portée depuis
`TOMB5pc/game/lara.cpp` : vault 2 clics (`ANIMATION_LARA_CLIMB_2CLICK`,
50), vault 3 clics (`ANIMATION_LARA_CLIMB_3CLICK`, 42), saut vertical
(`ANIMATION_LARA_STAY_SOLID` + `STATE_LARA_JUMP_UP`), et
`LaraTestClimbStance` pour la posture de grimpe. `lara.calc_fallspeed`
utilise `phd_sqrt_asm`. Compilation et édition de liens OK
(`build-gameplay59`, SHA256 `2ee56425fc744ed43d7c6806d01b9e4bbe3f005c85f4c53fb0ddc4790279d66c`),
**4177 tests PASS**. Validation runtime de la montée de marche encore à
faire.

#### Harnais rapide : autoload de sauvegarde au titre

`TOMB5_AUTOLOAD=1` fait charger `TOMB5.SAV` par `TitleOptions` dès le
titre (`PortSave_Read` → `FromTitle=1` → `sgRestoreGame` →
`PortSave_ApplyPending`). Avec `vpad` alimenté par un FIFO et une boucle
`start`/`a`, le niveau 3 est atteint en **~60 s** au lieu de ~4 min.
Le format de sauvegarde v4 est compacté : offsets `x=8620`, `y=8624`,
`z=8628`, `y_rot=8634`, `room=8638`, `checksum=8654` (FNV-1a sur les
octets 0..8653). Il est donc possible de **patcher la position de
départ** pour sonder une zone précise, sans refaire le niveau.

Limite connue : le démarrage est instable ; parfois gdb reste sur
`[New Thread ...]` sans `[EMU] Initialising Emulator.`. Relancer alors
le couple `vpad`/`MAIN`. La sauvegarde de reprise à la corniche a été
conservée (`/tmp/opencode/TOMB5.corniche.sav`) et restaurée.

#### Géométrie mesurée dans le puits de lave

- La corniche (`room 12`, `43109,768,52502`) est la **seule** cellule à
  `floor=768` ; ses voisines nord/sud/ouest ont `floor=1024` avec
  `pit_room=26`, puis `room 26` a `pit_room=14`. Une apparition à
  `42000,1024,52224` **chute jusqu’à `y=5888`** (`room 14`) : le grand
  sol de pierre visible dans les captures est le **fond du puits**, pas
  un sol praticable.
- Au-dessus : `sky_room=8`. Un saut vertical depuis la corniche atteint
  la grille de `room 8` à `y=256` (`FallingBlockFloor` renvoie
  `item->pos.y_pos + 256`). Le sol de `room 8` est un trou
  (`pit_room=12`) couvert par les 12 dalles `CRUMBLING_FLOOR`.
- Saut vers le nord depuis la corniche : `LaraDeflectEdgeJump` reçoit
  `CT_FRONT`, `front_floor=-512`, `front_ceiling=-4102`. La sonde avant
  touche une dalle de `room 8` à `y=256` (item à `43520,0,51712`), soit
  une marche de 512 au-dessus des pieds : le saut est donc défléchi.
  **Le « doorsill » ne peut pas être atteint depuis la corniche par un
  saut avant ; il faut venir du couloir au-dessus (`y=256`).**
- Cellules du passage nord de `room 12` (`xx3/4 zz0`) :
  `floor=2048`, `ceiling=1024`, soit un couloir de 1024 de haut. C’est
  le candidat « doorsill + crawlspace » (seuil à 2048, sous le couloir
  à 256). Autres hauteurs : `room 92` et `room 25` `floor=-1024`
  (au-dessus ; `room 92` est le balcon derrière la grille métallique
  donnant sur l’arène), `room 26` ~2816-3072, `room 27` ~2816,
  `room 14` 5120-6144 (lave).

#### Boutons et pièges du port

- Le bouton carré `SWITCH_TYPE1` de `room 0` (`57400,7680,52736`) est
  bien dans une salle sombre avec un squelette sur le mur droit ; le
  déclencheur `SWITCH` est en `r0 xx2 zz3` (`57344,52224`, `key=0`).
  Une pression d’Action pile sur la cellule de déclencheur n’a pas
  lancé l’animation d’interrupteur (`state=2`) : position/orientation
  exactes encore à déterminer.
- Une apparition dans `room 6` (`60928,6400,49664`) provoque un
  **SIGSEGV** dans `InterpolateMatrix_AI` (`ANIMITEM.C:1502`). À
  documenter comme fragilité du port ; ne pas sonder cette salle par
  téléportation tant que ce n’est pas corrigé.

#### Prochaine étape

Se placer sur le couloir de `room 8` (`y=256`), rejoindre son bord nord
au-dessus du passage (`x 40960..43008`, `z≈51200`), puis se laisser
tomber / reculer avec **Action** pour accrocher le seuil à `2048`.
Ensuite : shimmy à gauche, passage du coin, remontée dans le couloir
(crawlspace), puis salle du bouton et ouverture de l’issue. Aucun
`DONE` global.

### Accroche : ce que le port de `TestLaraVault` ne débloque pas (15 novembre 2026)

Le port de `TestLaraVault` est utile mais **ne débloque pas la corniche** :
au bord nord (`43685,768,52325`, face nord), `Action+Up` laisse Lara en
`state=2` sans déplacement. La raison est dans la fonction elle-même :
`slope = abs(coll->left_floor2 - coll->right_floor2) >= 60`. Autour de
la corniche (cellule 1×1), les sols gauche/droite sont des puits à des
profondeurs différentes (`room 26`/`14`), donc `slope` est vrai et
`TestLaraVault` renvoie 0 **avant** le vault 2 clics. La marche de 512
au-dessus (`front_floor=-512`) n’est donc pas grimpable ici.

### Sondes par sauvegarde : limites du port

Le patch de `TOMB5.SAV` fonctionne (voir plus haut), mais deux
positions de test se comportent mal :
- apparition sur le couloir de `room 8` (`42496,256,51712` ou
  `40835,256,51304`, room 8) : le jeu **boucle à 100 % CPU** avant le
  premier `DrawRooms` (aucune ligne `CF W`), écran figé ;
- apparition dans le passage nord de `room 12` (`42000,2048,50600` ou
  `42000,2048,51000`, room 12) : `UpdateLaraRoom` **remonte Lara en
  `room 92` à `y=-1024`**. Ce n’est donc pas un couloir horizontal à
  2048 : c’est un puits vertical qui débouche dans `room 92`.

`room 92` a été observée : petit sol de pierre à `-1024` derrière une
**grille métallique** donnant sur l’arène (le « balcon » de la grande
salle). `room 25` est au même niveau (`-1024`), ouverte sur `room 8`.

Conclusion : le « doorsill » n’est pas le passage nord à 2048 ; il
implique `room 92`/`25` au-dessus. La seule sauvegarde de reprise
fiable reste celle de la corniche (`43364,768`). La route exacte
corniche → doorsill → crawlspace reste à établir ; aucune correction
de gameplay n’a été tentée sans preuve.

### Hang : tests de coin portés (15 novembre 2026)

`LaraHangLeftCornerTest` et `LaraHangRightCornerTest` (`GAME/LARA.C`)
étaient vides (`UNIMPLEMENTED(); return 0;`). Ils sont maintenant portés
depuis `TOMB5pc/game/lara.cpp` (`lara.cpp:5492` et `5339`) :
- `ANIM_GRABLEDGE` (PC 96) → `ANIMATION_LARA_HANG_IDLE` (96) ;
- mêmes calculs de coin (`^ 1023`, tables `LeftClimbTab`/`RightClimbTab`,
  `IsValidHangPos`, `LaraFloorFront`, `lara.CornerX/CornerZ`) ;
- les deux branches `climb_status` et hang simple sont conservées.

Build `build-gameplay59` : SHA256
`d17c247b1a31b6d7847503c1967015b4adc1148176caf37e46cd55a4828fc303`,
**4177 tests PASS**. La validation runtime (transition
`STATE_LARA_CLIMB_CORNER_LEFT_INNER/OUTER` au passage du coin) reste à
faire : le harnais de test force l’état `HANG`, mais le trigger
`CAMERA:0` de la corniche relance une cutscene qui court-circuite
`DrawRooms`/`LaraControl`, donc l’entrée n’est pas traitée. À vérifier
en jeu normal, sur une corniche avec un vrai coin.

### Inventaire : utilisation d’objets et socle de pickup (15 novembre 2026)

`use_current_item` (`GAME/NEWINV2.C`, ex-`SayNo(); UNIMPLEMENTED();`) est
porté depuis `TOMB5pc/game/newinv2.cpp:2249` :
- armes (`PISTOLS/UZI/SHOTGUN/REVOLVER/HK/CROSSBOW`) et `request_gun_type` ;
- flare (`IN_FLARE` + `LaraGun`) ;
- jumelles (`BinocularRange`, `BinocularOldCamera`) ;
- petits/grands medipacks ;
- et surtout `GLOBAL_inventoryitemchosen = gmeobject`, qui est le signal
  utilisé par `KeyHoleCollision` / `PuzzleHoleCollision` pour insérer
  clés, puzzles et crowbar. Les états `AS_*` sont mappés sur les
  `STATE_LARA_*` du port (mêmes valeurs : 71, 80, 81, 84-86, 88,
  105-106).

`FindPlinth` (`GAME/PICKUP.C`) est porté depuis
`TOMB5pc/game/pickup.cpp:671` (socle statique puis item plinth ; le
sentinelle PC `NO_ITEM` est `-1` dans le port).

Build `build-gameplay59` : SHA256
`19e95b6420170bbde89734f357498da44819d64ee6122f90bad98a9e95d770e7`,
**4177 tests PASS**. Validation runtime à faire (insertion d’une clé et
utilisation d’un medipack en jeu).

#### Reste du lot « corde »

Le sous-système corde n’est pas qu’une fonction : `GAME/ROPE.C` ne fait
que 58 lignes (`SaveRope`, `LoadRope`, `Straighten` vide,
`StraightenRope`). Il manque le cœur physique (`_Straighten`,
`RopeControl`/`ControlRope`, `RopeList`/`Ropes`), plus
`LaraClimbRope`, `UpdateRopeSwing` (`GAME/LARA.C`) et
`DelAlignLaraToRope` (`GAME/LARAMISC.C`). C’est un chantier dédié
(~700 lignes depuis `rope.cpp`), à traiter séparément.

### Corde : côté Lara porté, côté objet encore à faire (15 novembre 2026)

Portés depuis `TOMB5pc/game/rope.cpp` et `lara.cpp` :
- `Straighten` (`GAME/ROPE.C`) : équivalent de `_Straighten` +
  `Normalise` (24 segments, `SegmentLength = slength << 16`,
  normalisation `phd_sqrt_asm`) ;
- `UpdateRopeSwing` (`GAME/LARA.C`, source `lara.cpp:4952`) : arcs
  avant/arrière, `RopeDFrame`, `RopeFrameRate`, `LegsSwinging`,
  `SFX_LARA_ROPE_CREAK` ;
- `LaraClimbRope` (`GAME/LARA.C`, source `rope.cpp:587`) :
  `RopeCount`/`RopeOffset`/`RopeDownVel`/`RopeFlag`, descente anim
  `ANIMATION_LARA_ROPE_DOWN`, retour à `STATE_LARA_ROPE_IDLE`.
  `RopeList` (PC) → `Ropes[]` du port.

Build `build-gameplay59` : SHA256
`ef794f243aba5d9933333c608a515b97e595eae1142e30ae3d82ca0ddc1e611d`,
**4177 tests PASS**.

Il manque encore le **côté objet** de la corde, qui vit dans
`rope.cpp` et n’a pas été porté : `InitialiseRope`, `CreateRope`,
`RopeControl`, `RopeCollision`, `CalculateRope`, `SetPendulumPoint`,
`RopeNodeCollision`, `AlignLaraToRope`, et l’assignation
`objects[ROPE].initialise/control` dans `PortSetupGameplayObjects`.
Sans cela, le puzzle de corde du Colosseum reste inactif.

### Corde : côté objet porté (15 novembre 2026)

Ajouté dans `GAME/ROPE.C` (port de `TOMB5pc/game/rope.cpp`) :
`CreateRope`, `InitialiseRope`, `GetRopePos`, `mDotProduct`, `vMul`,
`mCrossProduct`, `phd_GetMatrixAngles`, `ModelRigidRope`, `ModelRigid`,
`SetPendulumPoint`, `CalculateRope`, `RopeNodeCollision`,
`AlignLaraToRope`, `RopeCollision`, `RopeControl`, `init_all_ropes`.
`RopeList` (PC) → `Ropes[]`, `phd_PushUnitMatrix`/`phd_RotYXZ`/
`phd_PopMatrix` → `mPushUnitMatrix`/`mRotYXZ`/`mPopMatrix`,
`phd_sin/cos` → `SIN/COS` (même échelle 4096 + `W2V_SHIFT` 12),
`phd_sqrt` → `phd_sqrt_asm`, `phd_atan` → `phd_atan_asm`.

Intégration :
- `objects[ROPE]` reçoit `initialise = InitialiseRope`,
  `control = RopeControl`, `collision = RopeCollision`,
  `using_drawanimating_item = FALSE`, `save_flags = TRUE` ;
- `init_all_ropes()` est appelé au début de `PortSetupGameplayObjects` ;
- `DelAlignLaraToRope` (`LARAMISC.C`), appelé chaque frame quand
  `lara.RopePtr != -1`, appelle désormais `AlignLaraToRope`.

Build `build-gameplay59` : SHA256
`047825bd33bf22615b2b6059c0755773ce03b21b7fcbee37842707861f6d6e3d`,
**4177 tests PASS**.

Non porté : le **rendu** de la corde (`DrawRopeList`,
`ProjectRopePoints`) — le `ROPE_STRUCT` PSX du port n’a pas le champ
`Coords[24][3]` du PC ; la physique/le contrôle sont en place, mais la
corde reste invisible tant qu’un rendu PSX dédié n’est pas ajouté.

Découverte annexe : `HIGH_OBJECT1` (socle qui monte, gemme du Colosseum)
n’a **ni** `initialise` **ni** `control` dans `PortSetupGameplayObjects` ;
`InitialiseRaisingPlinth`/`ControlRaisingPlinth` ne sont pas portés.

### Socle montant et poulie portés + validés en jeu (15 novembre 2026)

Portés :
- `InitialiseRaisingPlinth` et `ControlRaisingPlinth` (`GAME/TRAPS.C`,
  source `TOMB5pc/game/init.cpp:1149` et `andrea.cpp:480`) avec les
  correspondances `IFL_TRIGGERED`→`IFLAG_TRIGGERED`,
  `IFL_CODEBITS`→`IFLAG_ACTIVATION_MASK`, `IFL_CLEARBODY` (0x8000)
  →`IFLAG_KILLED` ;
- `InitialisePulley` (`init.cpp:444`) ;
- `objects[HIGH_OBJECT1]` : `initialise`/`control`/`collision =
  ObjectCollision`, `save_position`, `save_flags` ;
- `objects[PULLEY]` : `InitialisePulley`, `SwitchControl`,
  `PulleyCollision`, `save_flags`, `save_anim`.

**Validation runtime** (sauvegarde patchée à la poulie, room 49,
`41472,2816,29500`) : après 3 pressions d’Action, la poulie passe
`status=1→0`, le socle `HIGH_OBJECT1` monte de `y=2304` à **`y=1536`**
(3 × 256) et la gemme `PUZZLE_ITEM4_COMBO2` suit de `y=1792` à
**`y=976`** (`socle - 560`). L’ensemble poulie → trigger → socle
fonctionne donc de bout en bout.

Build `build-gameplay59` : SHA256
`a8a0915e1921d45d7a0247801243e3834fe5bdcd7e37936ce029eaef6f2a9769`,
**4177 tests PASS**.

### IA créatures : cœur porté, lion assigné (15 novembre 2026)

Portés depuis `TOMB5pc/game/box.cpp` et `lot.cpp` :
- `CreatureAIInfo`, `CalculateTarget`, `CreatureAnimation`,
  `CreatureTurn`, `CreatureMood`, `GetCreatureMood`, `CreatureKill`,
  `GetAITarget` (`GAME/BOX.C`) ;
- `CreateZone` (`GAME/LOT.C`).

Adaptations : `phd_sin/cos` → `SIN/COS`, `phd_atan` → `phd_atan_asm`,
`SQUARE` → multiplications explicites, `AS_*` → `STATE_LARA_*`
(`AS_MONKEY180`→`STATE_LARA_MONKEYSWING_TURNAROUND`,
`AS_HANG2DUCK`→`STATE_LARA_CLIMB_TO_CRAWL`), `IFL_*` → `IFLAG_*`,
`TOSSPAD` disponible dans le port, `ROOM_UNDERWATER` → `0x1`.

Assignation du **lion** dans `PortSetupGameplayObjects` :
`InitialiseLion`, `LionControl`, `CreatureCollision`, `hit_points=40`,
`radius=341`, `pivot_length=50`, `object_mip=5120`, `intelligent`,
`HitEffect=1`, flags de sauvegarde et `bones[...] |= 8` (24/76).

Build `build-gameplay59` : SHA256
`91ed84c3aa96a446406f2cced8644257e877ba1b7447378159222338ff7234d7`,
**4177 tests PASS**. Validation runtime du lion à faire (activation +
poursuite/attaque) ; le gladiateur (`gladiatr.cpp`) et la statue
(`guardian.cpp`) restent à porter, ainsi que le combat (LARAFIRE).

#### Validation runtime du lion (15 novembre 2026)

Sauvegarde patchée près du lion de `room 17` (`item 29`, spawn
`46568,1024,54784`) et activation forcée (`status=1`,
`EnableBaddieAI(29,1)`) : le lion **se déplace et s’anime** sans crash.
Relevé : `(45562,1024,54875)` → `(42462,1024,58589)`, `state=1`,
`hp=40`, puis il s’arrête. Le cœur IA (`CreatureAIInfo`,
`CalculateTarget`, `CreatureAnimation`, `CreatureTurn`, `CreateZone`)
s’exécute donc réellement. La **poursuite/attaque** de Lara n’a pas été
validée (le lion suit pour l’instant son trajet/patrouille) ; à tester
avec l’assignation `ai_bits` et le combat.

### Combat : LOS, sphères, ciblage et FireWeapon (15 novembre 2026)

Portés :
- `xLOS`, `zLOS`, `ClipTarget` (`GAME/CONTROL.C`) : la fonction `LOS`
  renvoie désormais un vrai résultat (murs/sols/plafonds) ;
- `GetSpheres` (`SPEC_PSXPC_N/SPHERES.C`) : sphères de collision des
  meshes (matrices `m*`, `Matrix->tx/ty/tz`, `TRX/TRY/TRZ`) ;
- `LaraTargetInfo`, `LaraGetNewTarget`, `FireWeapon`
  (`GAME/LARAFIRE.C`), avec `LJ_RHAND`, `baddie_slots`, `Slist`,
  `phd_GenerateW2V`/`phd_mxptr[M20..M22]`.

État du combat : le port possède déjà un `PistolHandler` **simplifié**
(ciblage direct + `HitTarget`/`CreatureDie`, sans LOS) qui permet de
tirer. `FireWeapon`/`LaraTargetInfo` sont maintenant disponibles mais
pas encore branchés sur ce handler. Restent à porter :
`GetTargetOnLOS`, `DoProperDetection`, `ObjectOnLOS2`/`DoRayBox`
(`DoRayBox` est un stub), `AnimatePistols`/`RifleHandler`, puis
`gladiatr.cpp` et `guardian.cpp`.

Build `build-gameplay59` : SHA256
`8f3e47cf19238424110112c10224c8e0f77afa835899261baffaecb58f196139`,
**4177 tests PASS**.

### Rayon/boîte et `DoRayBox` (15 novembre 2026)

Portés dans `SPEC_PSXPC_N/GETSTUFF.C` :
- `RayBoxIntersect` (intersection rayon/boîte 16.16) ;
- `DoRayBox` (adapté à la signature PSXPC à 10 arguments ; construit un
  `PHD_3DPOS` local). Utilise `mPushUnitMatrix`/`mRotY`/`Matrix->m*`
  (échelle 4096 + `W2V_SHIFT` 12), `Normalise`, `GetSpheres`,
  `Slist`/`ShatterItem`, `ClosestItem/ClosestCoord/ClosestDist`.

Rappel de build : les objets `SPHERES.C.o` et `GETSTUFF.C.o` doivent
être écrits dans
`CMakeFiles/TombRaiderChronicles_PSXPC_N.dir/<nom>.C.o` (et **non**
dans le sous-dossier `__/SPEC_PSXPC_N/`), sinon le lien n’inclut pas les
nouveaux symboles.

Build `build-gameplay59` : SHA256
`b49584390388cd94cfd917cf243d1485b8253ca581870eceb9a07f82f1dac500`,
**4177 tests PASS**.

### Gladiateur porté et validé en déplacement (15 novembre 2026)

`InitialiseGladiator` et `GladiatorControl` (source
`TOMB5pc/game/gladiatr.cpp`) sont portés dans `GAME/LION.C` (pour éviter
d’ajouter un objet au lien) et assignés dans
`PortSetupGameplayObjects` : `CreatureCollision`, `hit_points=20`,
`radius=102`, `pivot_length=50`, `object_mip=5120`, `intelligent`,
`HitEffect=1`, flags de sauvegarde, `bones[24/52] |= 8|4`, et les
16 meshes `MESHSWAP1` (`meshes[mesh_index + lp*2 + 1]`).

**Validation runtime** : item 26 (`room 15`, `49664,1024,54784`)
activé (`status=1`, `EnableBaddieAI(26,1)`) → le gladiateur se déplace
et s’anime sans crash : `(49624,1024,55040)` → `(46580,1024,58567)`,
`state=1`, `hp=20`. Comme le lion, il suit pour l’instant son trajet /
patrouille ; la poursuite et l’attaque de Lara restent à valider.

Build `build-gameplay59` : SHA256
`984219c308ef545a6dc6b99a6a2a31658112fe3806605a80c5fd07d57835fb32`,
**4177 tests PASS**.

### Pistolets : `AnimatePistols` porté (15 novembre 2026)

`AnimatePistols` (`GAME/LARA2GUN.C`) est porté depuis
`TOMB5pc/game/lara2gun.cpp:110` : fumée (`SmokeCountL/R`,
`TriggerGunSmoke`), `FireWeapon` aux deux bras, recul
(`p->RecoilAnim`, `winfo->recoil_frame`), flash, douilles, sons et
`savegame.Game.AmmoUsed`. Les joints sont `LJ_LHAND`/`LJ_RHAND`.

**Important** : le port utilise encore son `PistolHandler` simplifié
(ciblage direct + `HitTarget`), donc `AnimatePistols`/`FireWeapon` ne
sont pas encore branchés dans `LaraGun`. Ils sont prêts pour le
basculement vers le pipeline PC.

Build `build-gameplay59` : SHA256
`c8569e9784a70ed9e478b2847054ba82d79b45396e1f6c686dfdc8a31108e282`,
**4177 tests PASS**.

### Sous-système d’effets (éclairs, explosions, étincelles) et statue (15 novembre 2026)

#### Types et données
- `struct LIGHTNING_STRUCT` et `struct GUARDIAN_TARGET` ajoutés à `GAME/TYPES.H`.
- `struct LIGHTNING_STRUCT Lightning[16]` dans `GAME/TOMB4FX.C`.
- Enum `spark_flags` (`SF_FIRE`, `SF_SCALE`, `SF_DEF`, `SF_ROTATE`,
  `SF_FX`, `SF_ITEM`, `SF_DAMAGE`, `SF_UNWATER`, …) et macros
  `CLRR/CLRG/CLRB/CLRA` ajoutées.
- `TriggerDynamic` et `TriggerExplosionSmoke` déclarés pour PSXPC.

#### Mécanique portée (source `TOMB5pc/game/tomb4fx.cpp` / `effect2.cpp`)
- `TriggerLightning` retourne désormais un pointeur et **la durée de vie
  est l’octet alpha de la couleur** (`*(long*)&lptr->r = rgb`), comme sur PC.
- `TriggerExplosionSparks`, `TriggerExplosionSmoke`,
  `TriggerShockwaveHitEffect`.
- `UpdateSparks` (128 slots PSX), `UpdateShockwaves`, `UpdateLightning`
  (déplacement des 9 points, ricochets).
- `mRotBoundingBoxNoPersp` porté dans `SPEC_PSXPC_N/MATHS.C`.

#### Rendu PSXPC
- `S_DrawSparks` (`SPEC_PSXPC_N/DRAWSPKS.C`) projette chaque spark avec
  `w2v_matrix` + `camera.pos` + `phd_persp` et émet un sprite
  (`MGDrawSprite`, défaut `DEFAULT_SPRITES`).
- `DrawLightning` calcule les 32 points de la courbe comme sur PC puis
  émet des rubans `POLY_FT4` semi-transparents (sprite 28) avec largeur
  fonction de la profondeur et fondu de couleur sur les 16 dernières frames.
- `S_DrawSparks()` et `DrawLightning()` sont appelés dans
  `DrawPhase` (à l’endroit où le code PSX les commentait).

#### Correction importante : `xLOS`/`zLOS`
Les implémentations PC de `xLOS`/`zLOS` étaient dans une section
`#if PC_VERSION` **non compilée** pour PSXPC ; les stubs
`UNIMPLEMENTED()` de `SPEC_PSXPC_N/GETSTUFF.C` étaient seuls liés, donc
`LOS()` échouait toujours. La garde est passée à
`#if PC_VERSION || PSXPC_TEST` et les stubs ont été supprimés.
`ClipTarget` était déjà compilé. Cela débloque le ciblage, le combat et
la statue.

#### Statue (`guardian.cpp`)
`GAME/GUARDIAN.C` est maintenant complet (`InitialiseGuardian`,
`TriggerGuardianSparks`, `TriggerBaseLightning`, `GuardianControl`) et
assigné dans `PortSetupGameplayObjects` (`CreatureCollision`,
`explodable_meshbits=6`, `HitEffect=3`, flags de sauvegarde).
Deux gardes défensifs évitent un déréférencement de `gt.elptr[i]`
lorsqu’un slot d’éclair n’a pas pu être créé.

#### Validation runtime
- Injection GDB d’un `TriggerLightning` vertical au centre de l’écran
  (sauvegarde de la corniche, niveau 3) : ruban d’éclair blanc visible,
  épaisseur et position correctes.
- Statue synthétique dans l’arène du Colosseum (item 79, `obj=61` copié
  vers l’objet 65, données d’item reconstruites) :
  - `LOS` passe (`item_flags[0]` 0→1) ;
  - la statue « tombe » puis passe en attaque (`item_flags[0]=2`) ;
  - `TriggerBaseLightning` crée des éclairs (`Lightning[].Life=50`) ;
  - éclairs **verts visibles** autour de la tête, halo dynamique vert
    sur Lara, plus de 270 itérations sans crash.
- La statue réelle se trouve dans **Trajan’s Markets** (`obj=65`,
  `room 69`, `45568,1792,43520`) et non dans le Colosseum. La validation
  in-situ reste à faire : le menu « level select » du port démarre
  actuellement le niveau 1 (pas de sauvegarde de niveau 2 disponible).

Build `build-gameplay59` : SHA256
`55246b16ea9bbc6b87a59cb07aa0e6dde272b91fc0ec7961d6ff600effffc011`,
**4177 tests PASS**.

### ROMAN_GOD (statue du Colosseum) et corrections d’animation (15 novembre 2026)

#### Port
- `GAME/ROMANGOD.C` / `.H` créés depuis `TOMB5pc/game/romangod.cpp`
  (775 lignes) : `TriggerRomanGodSparks`, `TriggerRomanGodMissile`,
  `TriggerRomanGodLightningGlow`, `TriggerRomanGodPowerupFlames`,
  `TriggerRomangodGravel`, `InitialiseRomangod`, `RomangodControl`.
- `TriggerRomanGodMissileFlame` existait déjà dans `GAME/EFFECT2.C`
  (pas de doublon).
- `struct RG_TARGET` ajouté à `GAME/TYPES.H`.
- Assigné dans `PortSetupGameplayObjects` : `InitialiseRomangod` /
  `RomangodControl`, `CreatureCollision`, `hit_points=300`,
  `radius=256`, `pivot_length=50`, `object_mip=5120`, `intelligent`,
  `HitEffect=2`, flags de sauvegarde, `bones[24/52] |= 8|4` et les 17
  meshes `MESHSWAP1`.
- `ROMANGOD.C.o` ajouté au `link.txt` du build (le glob CMake ne le
  voit qu’après reconfiguration).

#### Corrections de bugs bloquants
1. **`CreatureActive`** (`GAME/BOX.C`) était inversé : il ne renvoyait
   1 que si `IFLAG_KILLED`, donc les contrôles de créatures ne
   s’exécutaient pas normalement. Réécrit selon `box.cpp` :
   `IFLAG_KILLED -> 0`, `status == ITEM_INVISIBLE -> EnableBaddieAI`
   puis `status = ITEM_ACTIVE`, sinon 1.
2. **`InterpolateMatrix_AI`** (`SPEC_PSXPC_N/ANIMITEM.C`) : quatre
   écritures utilisaient `a3`/`t1`/`t3` (valeurs interpolées) comme
   pointeurs au lieu de `a0` (destination), et les trois translations
   étaient écrites en `short` au lieu d’`int`. Corrigé : plus de
   SIGSEGV dans `InterpolateMatrix_AI` (crash observé auparavant en
   room 6 du Colosseum).

#### Validation runtime
- La sauvegarde de la corniche (niveau 3) tourne **200 frames sans
  crash** après les corrections (`SANITY OK`).
- La statue `obj=61` (`room 90`, `48640,512,69120`) est bien
  initialisée au chargement (`anim = anim_index+16`, `state=13`,
  position décalée de 486 vers l’avant).
- Activation forcée (`EnableBaddieAI(79,1)`, `status=1`,
  `AddItemActive(79)`) + téléport de Lara en `48640,512,70144` :
  `data` est alloué, le contrôle démarre.
- **Blocage restant** : SIGSEGV dans
  `iRotSuperPackedYXZ_AI` (`ANIMITEM.C:1422`) pendant l’animation
  interpolée de la statue (17 os) ; le pointeur de rotations de la
  frame suivante (`fp[33]`) part hors de la zone de frames. Le même
  type de crash était déjà noté pour un spawn en room 6. L’animation
  interpolée des objets à nombreux os reste donc à corriger avant de
  valider le combat réel contre la statue.

Build `build-gameplay59` : SHA256
`fff7b798ff64b25b9d497d011f815d66992b75a9785bae3cb60abf721be6dfb3`,
**4177 tests PASS**.

Note complémentaire : l’animation **dormante** de `ROMAN_GOD`
(`anim_index+16`, état 13) est stable — plus de 125 itérations de
`DrawRooms` dans la room 90 sans crash, avec `EnableBaddieAI(79,1)`.
Le SIGSEGV n’apparaît que lorsqu’on force l’état éveillé (`goal=1`),
donc probablement via une transition d’animation (`GetChange`) qui
sélectionne une animation dont les données de rotation ne correspondent
pas au squelette de 17 os. La séquence de déclenchement réelle du niveau
doit être reproduite avant de conclure.

### Correction complète de l’animation interpolée (15 novembre 2026)

Le crash `iRotSuperPackedYXZ_AI` n’était pas dû aux données de la
statue mais à deux erreurs de décompilation :

1. **`iPushMatrix_AI`** (`SPEC_PSXPC_N/ANIMITEM.C`) n’empilait que la
   matrice de lumière (`fp[21]`). Or `iPopMatrix_AI` détaille **les deux**
   piles (`fp[20]` objet et `fp[21]` lumière), comme `iPushMatrix`
   (non-AI) qui pousse `iMatrix` **et** `Matrix`. À chaque os, la pile
   objet descendait donc de 8 ints ; après ~15 os elle écrasait
   `fp[31..33]`, d’où un pointeur de rotations sauvage et le SIGSEGV.
   `iPushMatrix_AI` empile maintenant les deux matrices.
2. **`erk_interpolated`** se terminait par
   `//j loc_81714; assert(FALSE)` : le saut vers la finalisation
   (compteur de matrices + `mmPopMatrix_AI`) n’était pas implémenté.
   Le chemin interpolé revient maintenant à l’appelant, qui exécute
   `loc_81714` et le pop. Les deux `assert(FALSE)` de `erk_interpolated`
   sont remplacés par des `return`.

#### Validation
- **ROMAN_GOD éveillé** (activation forcée, `state=1`) : plus de crash.
  La statue joue ses états `13 → 10 → 2 → 7`, crée des éclairs
  (`Lightning[].Life=24`), se déplace et s’anime pendant **250
  itérations** de `DrawRooms`.
- **Spawn room 6 du Colosseum** (`60928,6400,49664`), qui provoquait
  auparavant un SIGSEGV dans `InterpolateMatrix_AI` : **201 frames sans
  crash** (`SANITY OK`, room 6, hp 1000).
- Sauvegarde de la corniche : 200 frames sans crash.

Build `build-gameplay59` : SHA256
`a4d80b28fac639bbf6c35fa0d86b14f56b77ce96e1f3fcc78ce6dca6dbbf0ad4`,
**4177 tests PASS**.

### Déplacement des créatures : bloc vitesse de `AnimateItem` (15 novembre 2026)

`AnimateItem` (`GAME/CONTROL.C`) s’arrêtait à la gravité et **omettait
tout le bloc de vitesse** de `control.cpp` :

```c
speed  = anim->velocity;  if (anim->acceleration)  speed  += anim->acceleration  * (frame - frame_base);
item->speed = speed >> 16;
speed2 = anim->Xvelocity; if (anim->Xacceleration) speed2 += anim->Xacceleration * (frame - frame_base);
...
item->pos.x_pos += (item->speed * SIN(y_rot)) >> W2V_SHIFT;
item->pos.z_pos += (item->speed * COS(y_rot)) >> W2V_SHIFT;
item->pos.x_pos += (speed2 * SIN(y_rot + 0x4000)) >> W2V_SHIFT;
item->pos.z_pos += (speed2 * COS(y_rot + 0x4000)) >> W2V_SHIFT;
```

Sans ce bloc, **aucune créature ne se déplaçait** (elles animaient sur
place) ; c’est aussi ce qui empêchait ROMAN_GOD de se rapprocher de
Lara. Le `else` est maintenant implémenté, la branche gravité restant
inchangée.

Validation : la statue ROMAN_GOD se déplace désormais réellement
(`51968,66043 → 51924,65985 → 51429,66041 → 51708,65595`) pendant son
état 7, et la corniche tourne 200 frames sans crash. Le diagnostic AI
montre `info.distance = 27 563 485` (distance au carré) et
`tbox = rbox = 245` : la statue est encore trop loin (> 2560) pour
passer en état d’attaque dans ce montage synthétique ; le
rapprochement/cheminement reste à vérifier avec la séquence réelle du
niveau.

Build `build-gameplay59` : SHA256
`0925ce7e402e0928a375d6d0d1037bfead225b7bc4432e8fd0da0f3e5091247c`,
**4177 tests PASS**.

### ROMAN_GOD : attaques validées en partie (15 novembre 2026)

Cartographie des animations de `ROMAN_GOD` (`objects[61].anim_index`) :

| état | anim | frames |
|------|------|--------|
| 1 | 560 / 569 / 570 | 0–69, 578–599, 600–621 |
| 2 | 561 | 70–265 |
| 3 | 562 | 266–318 |
| 4 | 563 | 319–385 |
| 5 | 564 | 386–437 |
| 7 | 566 / 567 / 568 | 498–577 |
| 9 | 571 / 572 | 622–689 |
| 10 | 573 | 690–744 |
| 11 | 574 | 745–836 |
| 12 | 575 | 837–935 |
| 13 | 576 | 837–997 |

Avec Lara à 800 unités et l’état 3 forcé (`anim 562`) :
- l’attaque s’exécute, et **deux shockwaves sont créées** à la frame
  `frame_base + 34` (`ShockWaves[0/1].life = 48`) ;
- l’IA enchaîne ensuite état 10 (demi-tour) puis état 2 (charge) et
  **crée des éclairs** (`Lightning[0].Life = 24`) ;
- aucun crash sur plus de 250 itérations.

Lara n’a pas encore perdu de PV : le test de collision vertical des
shockwaves (`sw->y` vs `bounds` de Lara) ne passe pas dans ce montage ;
à régler/valider lors d’une attaque en conditions réelles. Les
shockwaves ne sont pas encore dessinées (`DrawShockwaves` non porté),
seuls les éclairs le sont.

### Mise à jour des effets réellement active + dégâts shockwave (15 novembre 2026)

Les fonctions `UpdateSparks`, `UpdateFireSparks`, `UpdateSmokeSparks`,
`UpdateBubbles`, `UpdateSplashes`, `UpdateDebris`, `UpdateBlood`,
`UpdateDrips`, `UpdateGunShells`, `UpdateShockwaves` et
`UpdateLightning` étaient dans un bloc `#if PC_VERSION` **non compilé**
pour PSXPC, et leurs appels dans la branche PSX de `ControlPhase`
étaient commentés. Résultat : les effets étaient créés mais jamais
mis à jour (durée de vie figée, aucun dégât).

Corrections :
- garde du bloc passée à `#if PC_VERSION || PSXPC_TEST` ;
- appels réactivés dans `ControlPhase` (branche PSX/PSXPC) :
  sparks, fire, smoke, bubbles, splashes, debris, blood, drips,
  gunshells, shockwaves, lightning ;
- stubs `Unimpl()` remplacés par `UNIMPLEMENTED()` ;
- `UpdatePulseColour` et `UpdateSky` gardés en `#if PC_VERSION`
  (doublons PSXPC déjà fournis par `TEXT_S.C` / `DRAWSKY`) ;
- appel ambigu à `TriggerRicochetSpark` limité à `#if PC_VERSION` ;
- `EFFECT2.C.o` était obsolète et ne contenait pas `TriggerRipple` :
  recompilé.
- `GetBestFrame` (`CALCLARA.C`) avait ses deux branches inversées
  (`ret > rate/2` renvoyait la mauvaise frame) : corrigé d’après
  `draw.cpp`.

Validation :
- attaque ROMAN_GOD état 3 : les shockwaves se mettent à jour et
  **infligent des dégâts** (`lara_item->hit_points` 1000 → 724) ;
- la sauvegarde de la corniche tourne 200 frames sans crash avec tous
  les updaters d’effets actifs ;
- 4177 tests PASS.

Build `build-gameplay59` : SHA256
`3dc02e2826d56b657381f156220574b1862569b014434ac94e41d4ab27c32d9c`.

### Rendu des shockwaves (15 novembre 2026)

`DrawShockwaves` (`SPEC_PSXPC_N/DRAWSPKS.C`) est porté en version PSXPC :
pour chaque shockwave active, 48 points sont répartis sur le rayon
moyen `(InnerRad + OuterRad) / 2` (relu en non signé pour retrouver
40960 depuis `0xA000`), projetés à l’écran puis dessinés avec le sprite
`DEFAULT_SPRITES + 14`, avec fondu de couleur sur les 8 dernières
frames. Appelé dans `DrawPhase` après `DrawLightning`.

Validation visuelle : une shockwave injectée autour de Lara affiche un
anneau jaune visible (`swvis.png`). Le rendu est approximatif (anneau
de sprites au lieu du quad texturé PC) mais lisible.

Remarque : le menu « level select » (activé par `PlayAnyLevel`) affiche
bien la sélection, mais choisir Trajan’s Markets démarre encore le
niveau 1 (sauvegarde F5 : `level 1`). Ce chemin de débogage n’est pas
utilisé pour la campagne ; la validation de GUARDIAN reste synthétique.

Build `build-gameplay59` : SHA256
`847b137c2ea5dd3ac23d811249ee94729344ef2a3cf197b915143badf7ccaf28`,
**4177 tests PASS**.

### Corniche : le saut de 512 est franchi (15 novembre 2026)

Après les corrections `GetBestFrame` / animation / `AnimateItem`, un test
runtime sur la sauvegarde de la corniche (`43364,768,52325`, room 12)
montre un changement important :

- si l’on remet `GLOBAL_playing_cutseq = 0`, `cutseq_trig = 0`,
  `globoncuttrig = 0` et `bDisableLaraControl = 0` à chaque frame
  (comme `probe_free.gdb`), Lara répond aux entrées ;
- depuis `43364,768,51900`, **Up + Action** (vault) franchit la marche
  de 512 et place Lara à `43364,256,51900`, **room 8** (étage
  supérieur, celui des grilles/dalles).

C’est précisément le pas de 512 qui bloquait `TestLaraVault` dans
l’état précédent. La correction de `GetBestFrame` (branches inversées)
semble avoir débloqué la détection de rebord/vault.

État sauvegardé : `/tmp/opencode/TOMB5.room8.sav`
(`level 3`, `room 8`, `43364,256,51900`). L’exploration de l’étage 8
n’a pas encore trouvé le crawlspace/le bouton ; la caméra montre un
couloir et des alcôves au niveau 256.

Point d’attention : sans le reset des variables de cutscene, Lara reste
figée après le chargement de la sauvegarde de la corniche.

### Room 8 (étage des grilles) : contenu et limite du raccourci

Cartographie runtime de la room 8 autour de Lara (`43364,256,51900`) :

- sol walkable : boîtes 14–19 à `y≈1024` (secteurs `f=4`) ;
- le reste de la grille est `NO_HEIGHT` (`-32512`) ;
- objets présents : `CRUMBLING_FLOOR` (obj 105) en damier, `TELEPORTER`
  (387), `EARTHQUAKE` (366), `CAMERA_TARGET` (409), `PUZZLE_HOLE4`
  (245), `ANIMATING15_MIP` (445) à `43520,0,52736` (probablement la
  porte/sortie de droite) ;
- aucun `SWITCH_TYPE*` dans les rooms 8/12 : le « bouton » du walkthrough
  est donc un élément animé/trigger d’une autre room (probablement 25/26).

Le vault depuis la corniche permet d’atteindre la room 8, mais **la
sortie de droite reste fermée** car le bouton du crawlspace n’a pas été
pressé. Le raccourci ne remplace donc pas la séquence
hang → traverse → crawlspace → bouton.

Sauvegarde d’état : `/tmp/opencode/TOMB5.room8.sav`.

### Assignations génériques ANIMATING / PUZZLE_HOLE (16 novembre 2026)

`PortSetupGameplayObjects` n’assignait les contrôles `ANIMATING` que
pour deux objets spéciaux de Trajan’s Markets. Il manquait les boucles
génériques de `setup.cpp` :

- `PUZZLE_HOLE1..8` : `ControlAnimatingSlots` + `PuzzleHoleCollision` ;
- `PUZZLE_DONE1..8` : `ControlAnimatingSlots` + `PuzzleDoneCollision` ;
- `ANIMATING1..12_MIP` : `InitialiseAnimatingSlots`,
  `ControlAnimatingSlots`, `ObjectCollision`, flags de sauvegarde,
  `bones[0] |= 8`, `bones[4] |= 4` ;
- `ANIMATING13..16_MIP` : `InitialiseAnimatingSlots`,
  `ControlAnimatingSlots`, flags, `HitEffect = 0`.

Le cas spécial Trajan’s (ANIMATING3_MIP/ANIMATING4) reste prioritaire,
et les boucles `ANIMATING` sont désactivées pour `LVL5_TITLE` afin de
préserver les animations du plan du titre (raison du contournement
précédent).

Validation : dans la room 8, `objects[445].control` et
`objects[444].control` pointent bien vers `ControlAnimatingSlots`
(ANIMATING15 / ANIMATING15_MIP, le mécanisme de sortie). La porte ne
s’anime toujours pas sans son trigger : le bouton du crawlspace reste
à identifier. Sanity corniche 200 frames OK, 4177 tests PASS.

Build `build-gameplay59` : SHA256
`a1ea77fa9809d94b26f09dd7b02c3d11eb2a9597a798680c9c793518999420fb`.

#### Précision : ANIMATING15 n’est pas la porte de sortie

Vérification runtime : `ANIMATING15` (obj 444, anim 697) et
`ANIMATING15_MIP` (obj 445, anim 698) ont des animations **vides**
(`frame_base = frame_end = 0`). Même activés (`flags |= REVERSE`,
`status = ACTIVE`, `AddActiveItem`), leur frame reste 0. Ce sont donc
des décorations/grilles statiques, pas le mécanisme de sortie de la
room 8. Le bouton/trigger du crawlspace reste à identifier (piste :
scan des données de trigger des cellules des rooms 8/12/25/26/92 pour
un `TO_OBJECT` visant la porte ou un flipmap).

#### Test des flipmaps autour de la room 8

`FlipMap(0..9)` sur la sauvegarde room 8 ne change rien :
`flip_status` reste à 0. La sortie de la room 8 n’est donc probablement
pas un flipmap mais une porte/objet ou un `TO_FLIPEFFECT` déclenché par
le bouton du crawlspace. Le scan des triggers par cellule
(`trigger_index` après `GetHeight`) renvoie des mots qui ressemblent
encore à des données de sol ; il faudra un décodeur de triggers dédié
ou repérer le bouton en jeu.

### `DoProperDetection` porté (16 novembre 2026)

`GAME/LARAFIRE.C` : `DoProperDetection` était un stub. Porté depuis
`TOMB5pc/game/larafire.cpp` — gestion des impacts de projectiles sur
sols, pentes (`BIG_SLOPE`, `DIAGONAL`), plafonds et murs, avec rebonds
(`fallspeed`, `speed`, `y_rot`) et changement de salle via
`ItemNewRoom` (implémentation PSXPC de `COLLIDE_S.C`).

Notes de portage : `ITEM_INFO`/`FLOOR_INFO` qualifiés `struct`,
`ushort` → `unsigned short`, casts `short(...)` → `(short)(...)`,
includes `COLLIDE.H`, `COLLIDE_S.H`, `ITEMS.H`. Aucun changement de
comportement hors PSXPC.

Validation : **4177 tests PASS**, corniche 200 frames sans crash.

Build `build-gameplay59` : SHA256
`e4b074ccea108c072786c93aee96fae3cd251a537042be425e109883aefef98a`.

### `GetTargetOnLOS` porté (16 novembre 2026)

`GAME/CONTROL.C` : `GetTargetOnLOS` était un stub (`return 0`), alors
que `FireWeapon` l’appelle pour le ciblage. Porté depuis
`control.cpp` : LOS + `ObjectOnLOS2`, test de collision, shatter des
meshes destructibles, ricochets, dégâts (`HitTarget`), objets smashables,
switchs explosifs (`SWITCH_TYPE7/8`, `GetSwitchTrigger`,
`ProcessExplodingSwitchType8`), crossbow/laser, et gestion des meshes
statiques (`ShatterObject`, `SmashedMesh*`).

Adaptations : `ITEM_INFO`/`MESH_INFO`/`GAME_VECTOR`/`PHD_VECTOR`
qualifiés `struct`, `phd_atan` → `phd_atan_asm`,
`IFL_SWITCH_ONESHOT` → `IFLAG_UNK40`, `IFL_CODEBITS` →
`IFLAG_ACTIVATION_MASK`, `GF_OFFICE` → `GF_LVOP_TRAIN`, include
`LARAFIRE.H` pour `weapons`/`HitTarget`.

Validation : **4177 tests PASS**, corniche 200 frames sans crash.

Build `build-gameplay59` : SHA256
`2babbc6898792b180ffedff44a88267078175e3348c07d638f8e15627b32a95c`.

### Pistolets réels + correction `ObjectOnLOS2` (16 novembre 2026)

#### `PistolHandler`
`GAME/LARA2GUN.C` : le `PistolHandler` simplifié (recherche d’item +
`HitTarget`) est remplacé par celui de `lara2gun.cpp` :
- `LaraGetNewTarget`, `LaraTargetInfo`, `AimWeapon` des deux bras ;
- gestion torse/tête selon les locks ;
- **`AnimatePistols(weapon_type)`** (donc `FireWeapon` réel) ;
- flash de lumière dynamique aux mains (`GetLaraJointPos`,
  `TriggerDynamic`).

Le pipeline complet `LaraGun → PistolHandler → AnimatePistols →
FireWeapon → GetTargetOnLOS → dégâts` est désormais actif.

#### `ObjectOnLOS2` : boucle infinie
`SPEC_PSXPC_N/GETSTUFF.C` : la boucle sur les items d’une room faisait
`item = &items[r->item_number]; item_num = item->next_item;` à chaque
itération, ce qui la figeait sur le deuxième item
(`while (item->next_item != -1)`). Depuis que `GetTargetOnLOS` l’appelle
réellement, cela bloquait le jeu au premier tir.
Corrigé en `item_num = item->next_item; while (item_num != -1);`.

#### Validation runtime
Statue ROMAN_GOD (`obj 61`, item 79) en room 90, Lara équipée des
pistolets, cible verrouillée (`lara.target = 79`) :
- `AnimatePistols`/`FireWeapon` tirent réellement ;
- **PV de la statue : 300 → 276 → 192 → 90** en quelques rafales ;
- aucun crash/hang.

**4177 tests PASS**, corniche 200 frames OK.

Build `build-gameplay59` : SHA256
`3f4aafa8109a786725285338666ff0b220f1460f45b73dc3a1daf12cebfb35b6`.

### Armes longues : `RifleHandler` et `AnimateShotgun` (16 novembre 2026)

`GAME/LARA1GUN.C` : les deux fonctions étaient des stubs.
- `RifleHandler` est porté depuis `lara1gun.cpp` : `LaraGetNewTarget`
  (sauf crossbow sans laser), `LaraTargetInfo`, `AimWeapon`, torse/tête,
  puis `AnimatePistols(WEAPON_REVOLVER)` ou `AnimateShotgun`, et flash
  dynamique (mains pour revolver, canon pour shotgun/HK).
- `AnimateShotgun` est porté : fumée, états 0/2/6/8, `FireShotgun`,
  `FireHK`, `FireCrossbow`, douilles shotgun, sons HK/silencieux,
  synchronisation des frames de bras.

Adaptations : `W_SILENCER/W_AMMO1/W_AMMO2` → `WTYPE_SILENCER/
WTYPE_AMMO_1/WTYPE_AMMO_2` (énumération existante d’`OBJECTS.H`),
`LMX_HAND_R` → `LJ_RHAND`, `phd_sin/cos` → `SIN/COS`, `GF_MIRROR` →
`GF_LVOP_MIRROR_USED`, `TriggerDynamic_MIRROR` → `TriggerDynamic`,
includes `CAMERA.H`, `PSXINPUT.H`, `LARA2GUN.H`, `GAMEFLOW.H`.

Validation : **4177 tests PASS**, corniche 200 frames OK.
Un test synthétique « revolver » (sans passer par le draw normal) déclenche
l’assertion `DEL_CalcLaraMatrices_Interpolated_ASM` (`CALCLARA.C:1766`)
car les frames de bras/weapon_item ne sont pas initialisées ; à valider
par la séquence réelle de sortie de l’arme.

Build `build-gameplay59` : SHA256
`11db0025e7813856e032182d57a44a0c3bacd8b06ab9e7a0c7fc2ec1badb6f9b`.

### Shotgun : draw/undraw et matrice de bras (16 novembre 2026)

Deux bugs empêchaient la sortie/le tir du shotgun (et des armes
longues) :

1. `draw_shotgun` / `undraw_shotgun` (`GAME/LARA1GUN.C`) étaient des
   décompilations erronées : `anim_index` sans `+1`, états
   `STATE_LARA_RUN_FORWARD` au lieu de 1/3, conditions inversées, et
   `frame_base = anims[item->frame_number].frame_ptr` au lieu de
   `anims[item->anim_number].frame_ptr`. Remplacés par les versions de
   `lara1gun.cpp`.
2. `DEL_CalcLaraMatrices_Interpolated_ASM` (`CALCLARA.C:1792`) :
   `Hardcore_iTranslateXYZ_CL((long*)s1[74], t8)` passait la **valeur**
   `s1[74]` comme pointeur au lieu de son adresse. Corrigé en
   `&s1[74]` (les autres appels utilisaient déjà `&`), ce qui causait
   `a22 = 1` et le SIGSEGV à la première frame de bras dessinée.

Validation runtime : shotgun forcé par la séquence de draw réelle
(`request_gun_type = WEAPON_SHOTGUN`, `gun_status = LG_NO_ARMS`) en
room 90 face à ROMAN_GOD :
- `draw_shotgun` crée l’item 110 et passe en `LG_READY` ;
- tirs réels, munitions 100 → 70, cible = 79 ;
- **PV de la statue : 300 → 210** ;
- aucun crash.

**4177 tests PASS**, corniche 200 frames OK.

Build `build-gameplay59` : SHA256
`fa82913848f1cff77d4c0b1c1e29d2f19acc490306586c66e0870ed1967a9315`.

### HK / crossbow : condition de draw et bolt (16 novembre 2026)

1. **Précédence de condition dans `LaraGun`** (`GAME/LARAFIRE.C`) :
   ```c
   if (state == 0x47 || state == 0x69 || state == 0x6A &&
       request == 4 || request == 6 || request == 5)
   ```
   À cause de la précédence, toute demande de HK/crossbow
   (`request == 5/6`) prenait la branche « accroupi » et **l’arme
   n’était jamais dessinée**. Corrigé en regroupant les états
   accroupis et les trois armes :
   `(state ∈ {crouch idle/roll/turn}) && request ∈ {shotgun, HK, crossbow}`.

2. **`ControlCrossbow` et `CrossbowHitSwitchType78`** (`GAME/LARA1GUN.C`)
   portés depuis `lara1gun.cpp` : déplacement du bolt, changement de
   salle, `GetCollidedObjects`, cible grappling, et activation des
   switchs 7/8 (`GetSwitchTrigger`, `ExplodeItemNode`).
3. **`CROSSBOW_BOLT`** : assignation dans `PortSetupGameplayObjects`
   (`control = ControlCrossbow`, `draw_routine = DrawWeaponMissile`,
   `using_drawanimating_item = FALSE`, flags de sauvegarde).

Validation : le shotgun reste fonctionnel après le correctif
(statue 300 → 228, munitions 100 → 76). Le test HK/crossbow forcé dans
le Colosseum plante dans `mRotSuperPackedYXZ_CL` car ces objets
**(HK/crossbow) ne sont pas chargés dans ce niveau** ; à valider dans un
niveau qui les contient. **4177 tests PASS**.

Build `build-gameplay59` : SHA256
`7ea4b985123b9bf44c28b56a726fa6ed28e71d6bc5dbac7a6094742b99a735ec`.

### `FlipMap` : `flip_status` inversé (16 novembre 2026)

`FlipMap` (`GAME/CONTROL.C`) faisait :

```c
flip_stats[FlipNumber] = flip_stats[FlipNumber] == 0;
flip_status = flip_stats[FlipNumber] == 0;
```

Deux défauts :
- `flip_status` était inversé (`== 0`) ;
- il était affecté à chaque fois, alors qu’il doit refléter l’état du flip
  courant (0/1) — le PC fait `flip_stats[n] = !flip_stats[n]; flip_status = flip_stats[n];`.

Corrigé. Validation runtime : `FlipMap(3)` fait passer
`flip_status` **0 → 1** (`flip_stats[3]` 0 → 1), donc les zones
`ground_zone[..][flip_status]` et les salles échangées (32 ↔ 76,
65 ↔ 82, 68 ↔ 33) sont désormais cohérentes. La corniche n’a pas de
salle appariée pour son `FlipNumber` (2), donc son apparence ne change
pas.

**4177 tests PASS**, corniche 200 frames OK.

Build `build-gameplay59` : SHA256
`1f70101d8941435cc732067fbbb5c747b32d43d5a1621cf9cdc4d28190b1f7b8`.

### Décodeur de niveau hors-ligne + pièges réactivés (16 novembre 2026)

#### 1. `scripts/porting/decode_level_floordata.py`

Le niveau est relogé dans une arène unique au chargement
(`LoadLevel`/`relocate` dans `GAME/SETUP.C`) : tableau `room`, puis pour
chaque salle `data`/`door`/`floor`/`light`/`mesh`, puis `floor_data`. Un dump
gdb de cette arène suffit donc à reconstruire toute la base du niveau hors du
jeu :

```gdb
dump binary memory /tmp/opencode/lv3_arena.bin room (char*)floor_data+65536
dump binary memory /tmp/opencode/lv3_items.bin items items+level_items
```

```sh
python3 scripts/porting/decode_level_floordata.py dump \
  --arena lv3_arena.bin --items lv3_items.bin \
  --room-ptr 0x567a3964 --floor-ptr 0x567c06f8 --rooms 125
```

L'outil décode les items (objet, salle, OCB, position), les `FLOOR_INFO` par
cellule, les chaînes `floor_data` (TILT/SPLIT/TRIGGER + cibles
`TO_OBJECT`/`TO_FLIPMAP`/…), et les portails (`door`) de chaque salle.
`--selftest` construit un niveau synthétique en mémoire et vérifie tout le
décodage sans le jeu ; le test `tests/porting/test_level_floordata.py` le
lance dans la suite.

#### 2. Ce que le décodage a établi pour The Colosseum (niveau 3)

- **125 salles, 110 items.** Les numéros d'objet doivent être lus dans le
  binaire (`p (int)BRIDGE_FLAT`) : les blocs `#if` de `OBJECTS.H` décalent
  les indices après ~366 (`STEAM_LASERS` = 391, `BRIDGE_FLAT` = 448 et non
  387/444).
- **Les salles 8, 12, 14 et 25 sont empilées** sur le même `x/z`
  (`38912,50176`), aux altitudes 0 / 768 / 6144 / -1024 : la corniche
  (room 12, `FlipNumber=2`) surplombe la salle 8, elle-même au-dessus du
  puits 25, relié à la salle 92.
- **Les salles 8 et 25 n'ont aucun trigger de sol** : leur contenu est
  purement mécanique (CRUMBLING_FLOOR en damier avec OCB 1 à 120 =
  temporisation, `EARTHQUAKE`, `PUZZLE_HOLE4`, `TELEPORTER`, `ANIMATING15_MIP`).
  Le « bouton du crawlspace » supposé n'existe pas dans les données : la
  sortie de la salle 8 est le portail ouest vers la salle 25, plus une
  remontée par la salle 92. Les triggers des cellules voisines de la salle 14
  (salle miroir, `FlipNumber=1`) ne ciblent que les dalles qui s'effondrent.
- Les 114 triggers du niveau sont décodés sans ambiguïté (les scans de mots
  bruts précédents confondaient les données de sol et les déclencheurs).

#### 3. Handlers d'objets du niveau 3

Matrice obtenue en lisant `objects[n].control/collision/initialise/floor`
à l'exécution, puis complétée :

| objet | numéro | état |
| --- | --- | --- |
| TRAPDOOR1..3, FLOOR/CEILING_TRAPDOOR1..2 | 106-112 | **assignés** (`InitialiseTrapDoor`, `TrapDoorControl`, `TrapDoor/FloorTrapDoor/CeilingTrapDoorCollision`) |
| FLAME_EMITTER, FLAME_EMITTER2, FLAME_EMITTER3 | 121-123 | **assignés** (`InitialiseFlameEmitter[2]`, `FlameEmitterControl`, `FlameEmitter2Control`, `FlameEmitter3Control`, `FireCollision`) |
| WATERFALLMIST | 368 | **assigné** (`WaterFall`) |
| EARTHQUAKE | 366 | **porté** depuis `objects.cpp` et assigné |
| CRUMBLING_FLOOR / FALLING_BLOCK | 103-105 | déjà assignés |
| PULLEY, SWITCH, DOOR, CLOSED_DOOR, PUZZLE/KEY_HOLE, PICKUP, PUSHABLE, RAISING_BLOCK1 | — | déjà assignés |
| TEETH_SPIKES | 117 | **non assigné** : `ControlScaledSpike` et `DrawScaledSpike` sont encore des stubs `UNIMPLEMENTED` |
| ROLLINGBALL | 114 | **non assigné** : `ControlRollingBall` est un stub |
| STEAM_LASERS | 391 | **non assigné** : `Initialise/Control/DrawSteamLasers` absents du port |
| FISHTANK | 413 | **non assigné** : `Initialise/ControlFishtank` absents |
| TELEPORTER | 387 | **non assigné** : `Initialise/ControlTeleporter` absents (nécessite `TriggerSuperJetFlame`, flashs et `LaraBurn`) |

#### 4. Ports de ce lot

- `GAME/TRAPS.C` : `FlameEmitterControl` complet (jet de flammes OCB
  négatif, `AddFire`, `TriggerSuperJetFlame`, `TriggerDynamic`,
  `LaraBurn`), `InitialiseFlameEmitter`, `InitialiseFlameEmitter2`,
  `InitialiseScaledSpike`.
- `GAME/TOMB4FX.C` : `ItemNearLara` (utilisé par les émetteurs de flammes).
- `GAME/OBJECTS.C` : `EarthQuake` réel (bounce caméra, `SFX_EARTHQUAKE_LOOP`,
  réveil des `FLAME_EMITTER` de la salle à 1 chance sur 64 par frame).
- `GAME/SETUP.C` : assignations ci-dessus dans `PortSetupGameplayObjects`.

Validation runtime (sauvegarde corniche, forçage des items 13/31/67) :

```
T3 handlers: trapdoor init/crtl/coll non nuls
T3 handlers: flame init/crtl/coll non nuls, draw nil
T3 quake f0 oscille 20<->106, camera.bounce -14..-101
T3 flame active=1 ; T3 trapdoor state=1 anim=582
T3 OK (160 frames, aucun SIGSEGV)
```

**4177 tests PASS** (+2 tests du décodeur).

Build `build-gameplay59` : SHA256
`7051f2aca364a21177baabb06068cc07e1a55dac3616591915229dc783259585`.

#### 5. Précision : géométrie exacte de la sortie de la salle 8

Les champs `pit_room`/`sky_room` des `FLOOR_INFO` donnent le lien vertical
réel des cellules de la salle 8 :

```
room 8 (x=38912 z=50176, floor=0)   room 12 (corniche, floor=1024)
  cellules centrales : pit_room=12, sky_room=25
  cellules (0,2) et (0,3) x=39424 : floor 0 / -1024, pit_room=255, sky_room=255
```

Autrement dit la corniche est **sous** la salle 8 et la salle 25 est
**au-dessus** (y croît vers le bas) ; les deux cellules ouest `(0,2)`/`(0,3)`
sont les seules sans lien vertical et portent le portail `door[0] → room 25`
(floor 0 puis -1024). La sortie de la salle 8 est donc un simple **pas vers
l'ouest** avec une chute de 1024 dans la salle 25, puis la salle 92 ; aucun
bouton ni interrupteur n'intervient.

### Entrée déterministe dans la salle 8 et traversée (16 novembre 2026)

#### 1. Piloter Lara sans X : forcer `input` à `LaraControl`

Le pad virtuel (`/tmp/opencode/vpad` + `input_daemon.py`) et les touches
xdotool ne produisaient plus aucune entrée (`inputBusy = 0` alors que
`PadConnected = 1`). Pour tester le gameplay de façon reproductible, on
force `input` juste avant que `LaraControl` ne le lise :

```gdb
break LaraControl
commands
silent
set GLOBAL_playing_cutseq = 0
set cutseq_trig = 0
set globoncuttrig = 0
set bDisableLaraControl = 0
set var input = 1          # IN_FORWARD
continue
end
```

⚠️ `set input = 1` échoue (« syntax error near `= 1` ») : gdb préfixe
`set input…` par la sous-commande `set input-radix`. Il faut `set var input`.
Bits utiles : `IN_FORWARD=0x1`, `IN_BACK=0x2`, `IN_LEFT=0x4`,
`IN_RIGHT=0x8`, `IN_JUMP=0x10`, `IN_ACTION=0x40`, `IN_WALK=0x80`.

#### 2. La sauvegarde « corniche » est posée sur le bord de la grille

La sauvegarde de reprise (`43364,768,52325`, room 12) est **hors de la
grille de cellules de la room 12** (elle s'arrête à `x=43008`) ; la seule
surface possible sous cette position serait le pont `ANIMATING15_MIP`
(item 21, `43520,0,52736`), or `ANIMATING15` n'a **pas** de callback de sol
(ni sur PC ni dans le port). Lara s'y arrête donc au bord du vide : ce
n'était pas un gel de contrôle.

En revanche une sauvegarde patchée en `43520,768,51712` (room 12) fait
apparaître Lara **dans la salle 8 à `y=256`**, debout sur les dalles qui
s'effondrent (`CRUMBLING_FLOOR` item 15, OCB 80), et elle répond
normalement aux entrées forcées :

```
PJ2 n=5   room=8 pos=43520,256,51712   floor=256 state=2   (debout)
PJ2 n=10  room=8 pos=43520,-84,52209   state=3 anim=77 speed=50 fall=-76  (saut)
PJ2 n=20  room=8 pos=43520,256,53659   floor=256 state=2   (atterrissage)
PJ2 n=30  room=8 pos=43520,256,54065   state=1 speed=35    (course)
PJ2 n=35  room=8 pos=43520,256,54171   state=2             (bord de dalle)
```

Conclusion : **la salle 8 est jouable** (déplacements, saut, atterrissage
sur les dalles, arrêt aux bords) ; aucun handler ne manque pour s'y
déplacer. Le chemin d'entrée réel est le saut sur les dalles de la
colonne `cx=4` (`y=256`), pas la position de la sauvegarde actuelle.

#### 3. Démarrage lent à ne pas confondre avec un blocage

Avec beaucoup de périphériques `uinput` résiduels (`/dev/input/event*`),
`[EMU] Initialising Emulator` peut n'apparaître qu'au bout de **110 à
200 s**. Un log qui s'arrête sur `[New Thread …]` n'est pas forcément un
échec : attendre, puis relancer si rien après ~4 min.

#### 4. Suite du parcours

Depuis `43520,256,54171` (room 8), l'étape suivante est le déplacement vers
l'ouest jusqu'aux cellules `(0,2)`/`(0,3)` (`x=39424`, sol 0 puis -1024,
sans `pit_room`/`sky_room`) qui portent le portail vers la salle 25, puis la
salle 92.

### Salle 8 : traversée mesurée et limite ouest (16 novembre 2026)

Parcours rejoué avec `input` forcé (voir section précédente), en partant
d'une sauvegarde patchée en `43520,768,51712` (room 12, `y_rot=0`) qui fait
apparaître Lara dans la salle 8 à `y=256` sur les dalles qui s'effondrent :

| frames | entrée | résultat |
| --- | --- | --- |
| 5–14 | `IN_FORWARD\|IN_JUMP` | saut, `state=3`, `speed=50` |
| 15–100 | `IN_FORWARD` | course vers `+z`, arrêt au bord `43520,256,54171` |
| 101 | `y_rot` forcé à `-16384` | demi-tour vers `-x` |
| 101–145 | `IN_FORWARD` | traversée de la plateforme jusqu'à `40037,256,53811` |
| 146–165 | `IN_FORWARD\|IN_JUMP` | saut vertical sur place (`speed=2`) |

Mesures importantes :

- La plateforme de dalles est **traversable d'est en ouest** : de
  `x=43520` à `x=40037`, `y=256` constant, sans chute ni blocage — donc les
  `CRUMBLING_FLOOR` et le pont `ANIMATING15_MIP` (cellule `(4,2)`) portent
  bien Lara.
- À l'ouest, la marche s'arrête à `x=40037` (bord de la dernière dalle).
  Un **saut vertical** à cet endroit ne progresse pas en `x` (`speed=2`) et
  la fait tomber dans le puits : `room 26` (`y=3141`, `fall=147`) puis
  `room 14` (`y=6144`, `state=8`) — chute d'environ 6000 unités, donc
  mortelle. Le saut simple n'est donc **pas** la sortie.
- La sauvegarde « corniche » contient `room=0` (et non 12) avec
  `43364,768,52325`, `y_rot=-16384` ; c'est `GetFloor` qui rétablit
  `room 12` au chargement.

Piste restante pour la sortie ouest : un **saut avec élan** (garder
`IN_FORWARD` pendant l'appui, pas un saut sur place) depuis `x≈40500` pour
couvrir les ~100 unités qui manquent et retomber sur la cellule `(0,2)`
(`x=38912..39936`, sol 0), ou l'accès par la salle 92 côté est.

### Correctif racine : entrées clavier + manette (`EMULATOR/EMULATOR.C`)

`Emulator_UpdateInput` (et sa variante debug) fusionnait les deux sources
avec un **ET** :

```c
((unsigned short*)padData[i])[1] = kbInputs & controllerInputs;
```

Or `kbInputs` et `controllerInputs` sont des masques **actifs au niveau
bas** (`0xFFFF` = rien appuyé). Un ET exige donc le *même* bouton enfoncé
sur le clavier **et** sur la manette. Dès qu'une manette est présente
(`SDL_NumJoysticks() > 0`, ce qui est le cas avec `vpad`), **aucune** des
deux sources ne produit d'entrée : c'est exactement le symptôme observé
(`inputBusy = 0` alors que `PadConnected = 1`, Lara figée malgré les
touches).

Corrigé en OU, sur les deux chemins :

```c
((unsigned short*)padData[i])[1] = (unsigned short)(kbInputs | controllerInputs);
```

Validation runtime (sauvegarde corniche, clavier via `xdotool`) :
`inputBusy` passe de `0x0` à `0x1` (avant) puis `0x4` (gauche, `state=20`
TURN_FAST) et Lara se déplace (`43364 → 43109`). Le pad virtuel `vpad`
reste, lui, sans effet (`RawPad = 0`) : ce chemin séparé n'est pas résolu,
mais le clavier suffit désormais au debug manuel.

Régression verrouillée par `tests/porting/test_input_merge.py` (le bug ne
se voit ni à la compilation ni dans les tests fonctionnels).

Note de build : les objets de l'émulateur sont dans l'archive statique
`build/.../EMULATOR/libPSX.a` ; après modification de
`EMULATOR/EMULATOR.C` il faut `make -C build/porting/build-gameplay59/build/EMULATOR`
puis relancer `sh CMakeFiles/TombRaiderChronicles_PSXPC_N.dir/link.txt`
(avec `LIBRARY_PATH` 32 bits, sinon `libstdc++.so` 64 bits casse le lien).

Build `build-gameplay59` : SHA256
`9d152a50622831050b5db6a0fb339ff4762db53832f9fdfa300efba435d92a8a`.

### Salle 8 : géométrie vue à l'écran et sauvegardes « room 8 » (16 novembre 2026)

Capture de la fenêtre de jeu (`import -window`) à `40037,256,52736` (room 8) :
Lara se tient sur une dalle carrelée ; devant elle, **une marche montante**
vers un sol plus haut et une niche sombre sur la droite. Aucun gouffre
visible dans l'axe — le vide est **latéral**.

Cela recoupe exactement les cellules décodées :

- `(0,2)` (x `38912..39936`, z `52224..53248`) : sol **0**, soit 256 au-dessus
  de la dalle (marche franchissable) ;
- `(0,3)` (même x, z `53248..54272`) : sol **-1024**, soit 1280 au-dessus
  (mur) ;
- `(0,1)` (z `51200..52224`) : **aucun sol** (-32512).

D'où l'échec des essais précédents : à `z=51712` (ligne `cz=1`) il n'y a
**rien** à l'ouest, la chute mène aux salles 26/14 ; il faut d'abord se
décaler dans la ligne `cz=2` (`z` entre 52224 et 53248) puis monter la
marche de 256 dans `(0,2)`.

#### Sauvegardes dont le champ `room` vaut 8

Une sauvegarde patchée en `40037,256,52736` **room 8** ne démarre pas en
jeu : l'écran se fige sur une **cinématique** (Lara derrière des barreaux),
l'image n'avance plus et aucune ligne de log ne sort (le message
`[SAVE] loaded … level 3 room 8` est bien imprimé juste avant). Ce n'est
pas une boucle de `GetFloor` : un `interrupt` + `bt` montre la pile
normale de rendu (`DrawOTag` → `Emulator_EndScene` → `WaitForTimestep`).
Les sauvegardes en **room 12** démarrent normalement. Conclusion pratique :
garder les points de reprise en room 12 et entrer dans la salle 8 par le
saut sur les dalles.

#### Délais de démarrage

Sous gdb **et** avec `stdbuf`, `[EMU] Initialising Emulator` peut sortir
après 60 à 200 s (init GL/audio), et la sortie standard est bufferisée :
un log muet n'est pas une preuve de blocage. Pour un diagnostic fiable,
lancer sans gdb et capturer la fenêtre avec `import -window`.

### Salle 8 : mécanique des dalles et issue ouest (16 novembre 2026)

#### Les dalles s'effondrent avec un délai par dalle

Les `CRUMBLING_FLOOR` de la salle 8 portent chacune un OCB qui est une
**temporisation** : `1, 5, 10, 20, 30, 40, 50, 70, 80, 100, 120`. Stationner
sur une dalle la fait céder : c'est la cause de **toutes** les chutes
observées jusqu'ici (`room 26` puis `room 14`, `y=6144`, `hp=-1`), et non
un défaut de collision. Exemple mesuré, en restant 100 frames sur la dalle
OCB 120 de la cellule `(1,2)` :

```
PR2 n=150 room=8 pos=40130,256,52659 floor=256   (debout, cz=2)
PR2 n=175 room=8 pos=40107,261,52492 floor=261   (dalle en train de céder)
PR2 n=180 room=12 pos=40083,465,52492 floor=6144 (chute)
PR2 n=190 room=14 pos=40730,6144,52492           (mort, hp=-1)
```

#### Issue ouest : portail bloqué, la salle 8 est un cul-de-sac

En restant mobile (saut d'entrée, marche continue), Lara traverse bien la
plateforme : `43520,256,53731` → `40037,256,53754` (colonne `cx=4` puis
`cx=1`, ligne `cz=3`), puis remonte vers `z=52492` (ligne `cz=2`). Mais à
`x≈40107` **la marche vers l'ouest ne progresse plus** (`state=2`, puis
`state=1 speed=38` sans déplacement) : la cellule `(0,2)` est un **portail**
(`DOOR_TYPE`) vers la salle 25 dont le sol est à `-1024`, soit un mur de
1280 depuis la salle 8 — infranchissable.

Autrement dit : la salle 8 ne mène nulle part à l'ouest. Les dalles qui
s'effondrent ne servent qu'à piéger le joueur, et la sortie de la zone
(corniche + salle 8) est ailleurs — probablement la chute maîtrisée depuis
la corniche vers la salle 26 (`pit_room=26`, 2048 plus bas, survivable)
plutôt que la salle 8.

Test complémentaire : depuis la corniche, `saut+avant` vers l'ouest ne
déclenche aucun saut (`state=14` GRAB_TO_FALL puis `state=2`, position
inchangée à `43109,768,52325`) — Lara est déjà au bord et le moteur refuse
de la faire sortir dans le vide.

### Carte du niveau et graphe de progression (16 novembre 2026)

Deux outils s'ajoutent au décodeur, tous deux utilisables sans le jeu :

```sh
python3 scripts/porting/decode_level_floordata.py --emit-selftest /tmp/synth
python3 scripts/porting/render_level_map.py \
  --arena lv3_arena.bin --items lv3_items.bin \
  --room-ptr 0x... --floor-ptr 0x... --rooms 125 \
  --out map.png [--xmin … --xmax … --zmin … --zmax … --scale 48]
```

`render_level_map.py` peint chaque cellule par altitude (clair = bas,
sombre = haut, gris foncé = pas de sol), étiquette les salles et place les
items. Les deux outils sont couverts par
`tests/porting/test_level_floordata.py` (niveau synthétique).

En construisant le graphe des **portails** (`door`) et des liens verticaux
(`pit_room`/`sky_room`), on obtient le chemin voulu par le niveau depuis la
corniche :

| salle | sol | contenu |
| --- | --- | --- |
| 12 | 1024 | LARA (départ, corniche) |
| 26 | 3072 | puits sous la corniche |
| 27 | 3072 | — |
| 108 | 1024 | 4 triggers (CD 57, objets 29/26) |
| 15 | 1024 | `CLOSED_DOOR1`/`2`, **GLADIATOR**, `KEY_HOLE1` |
| 18 | 1024 | — |
| 100 | 512 | 2 triggers (obj 25) |
| 102 | 512 | `KEY_HOLE2`, `CLOSED_DOOR2`, `ANIMATING1_MIP` |
| 110 | 2816 | — |
| 83 | 4352 | — |
| 111 | 4352 | — |
| 85 | 5888 | 1 trigger (CD 55) |
| 70 | 7936 | **`PICKUP_ITEM1`** → `TO_FINISH` |

Le combat du **ROMAN_GOD** (salle 90) est sur une antenne de la salle 100
(`100 → 90`).

Autrement dit : **la corniche mène vers le bas (salle 26), pas vers la
salle 8**. Les salles 8/14/25/92 (dalles qui s'effondrent, pont
`ANIMATING15_MIP`) sont une branche latérale sans issue nouvelle — ce qui
clôt le blocage « bouton du crawlspace » : il n'y avait rien à trouver.

### Parcours du Colosseum : document de travail dédié

Le chemin de progression, les mécaniques salle par salle et la recette de
test (sauvegardes de reprise valides, latence de démarrage, pilotage
`set var input`) sont regroupés dans
[`colosseum-walkthrough.md`](colosseum-walkthrough.md).

### Salle 12 → 26 : mesure du point de bascule (17 novembre 2026)

`GetFloor` le long de la corniche à `y=1024`, `z=53760`, en partant de la
room 12 :

```
x=43520..39936  room=26   (positions hors grille de la room 12)
x=39424         room=26   height=1151  idx=1089
x=38912         room=26   height=1151  idx=1089
x=38400         room=12   height=-32512 (plus de sol)
```

La bascule vers la salle 26 se fait donc à l'**extrémité ouest** de la
corniche (`x≈39424`), avec une marche de quelques centaines d'unités et
non une chute de 2048 : c'est un pas vers l'ouest, ce qui corrige
l'hypothèse « chute maîtrisée ».

### Sélection de niveau : chemin de code vérifié (17 novembre 2026)

Investigation statique du « choisir Trajan's Markets démarre le niveau 1 » :

1. `TitleOptions()` (`SPEC_PSXPC_N/TITSEQ.C`), branche
   `MENU_LEVEL_SELECT_MENU` : `byte_46` est l'entrée courante (bornée à
   `[0, Gameflow->nLevels - 2]`), et sur `IN_CROSS` :
   ```c
   gfLevelComplete = byte_46 + 1;
   byte_46 = 0;
   ret = 3;
   ```
2. `DoGameflow()` (`GAME/GAMEFLOW.C`), branche `GF_TITLE_LEVEL` : avec
   `gfStatus == 3`, il fait `gfCurrentLevel = gfLevelComplete` **et**
   repositionne le pointeur de script
   `gf = &gfScriptWad[gfScriptOffset[gfCurrentLevel]]` (ligne suivant le
   `else if (gfStatus == 4)`), donc la mécanique de saut de niveau est
   complète.

Le défaut restant est donc en amont, dans **l'entrée de menu** : soit
`byte_46` n'est pas initialisé à l'ouverture de `MENU_LEVEL_SELECT_MENU`
(il est réutilisé par le menu de chargement et remis à 0 à plusieurs
endroits), soit la navigation `IN_DPAD_UP/DOWN` n'incrémente pas pendant la
fenêtre de `RawEdge`. Vérification en jeu tentée : la navigation clavier
fonctionne dans le menu principal (`New Game` → `Special Features` se
déplace), mais sous gdb la cadence tombe à ~0,5 fps et un `x` sur
`Special Features` déclenche le **DEMO MODE** avant que le sous-menu ne
s'affiche ; `watch gfCurrentLevel` n'a enregistré aucune bascule. Le point
demande donc une passe manuelle (menu → Special Features → Level Select)
pour trancher. Aucun correctif spéculatif appliqué.

### `ControlScaledSpike` porté (dents de scie) (17 novembre 2026)

`GAME/TRAPS.C` : `ControlScaledSpike` remplace le stub par la version de
`traps.cpp` — extension/rétraction pilotées par `item_flags[0]/[1]`,
`TestBoundsCollideTeethSpikes`, dégâts (8 PV glissants, mort si chute ou
dents sorties selon `trigger_flags & 7`), gerbes de sang (`TriggerBlood`)
et animation de mort dédiée (`ANIMATION_LARA_SPIKED` +
`STATE_LARA_DEATH`).

`GAME/SETUP.C` : `TEETH_SPIKES` reçoit `InitialiseScaledSpike` (déjà porté)
et `ControlScaledSpike`, avec `save_flags`. Le **rendu** reste le chemin
standard (pas de `DrawScaledSpike`) : assigner le stub actuel imprimerait
un `UNIMPLEMENTED` par frame sans rien dessiner, alors que le rendu
standard affiche au moins le maillage.

Validation runtime (sauvegarde corniche, item 104 forcé actif) :
handlers non nuls (`init`/`ctrl`), item identifié `obj=117 room=124
ocb=36`, 200 frames sans `SIGSEGV`, `lara_hp` inchangé (Lara est à l'autre
bout du niveau). Avec l'OCB 36 (bit 32), les dents restent en position
rentrée (`f2=1`), ce qui est le comportement attendu de cette variante.

Build `build-gameplay59` : SHA256
`fc1576c71a62171a8c168654e0c802d0624530e293fd969453b75974c2e4ade1`.

### `ControlRollingBall` porté (bille de la salle 13) (17 novembre 2026)

`GAME/TRAPS.C` : `ControlRollingBall` remplace le stub par la version de
`traps.cpp` — gravité et `fallspeed`, rebonds amortis, sondage de sol à
±128 et ±512 autour de la bille (`GetFloor`/`GetHeight`), correction de
vitesse (`item_flags[0]`/`[1]`), `camera.bounce` selon la distance,
réorientation progressive (`phd_atan_asm`) et `_TestTriggers` pour les
déclencheurs sous la bille. `GAME/SETUP.C` assigne `ROLLINGBALL`
(`control`, `RollingBallCollision`, `save_position`, `save_flags`).
Includes ajoutés à `TRAPS.C` : `MATHS.H` (`phd_sqrt_asm`/`phd_atan_asm`) et
`COLLIDE_S.H` (`ItemNewRoom`, déclaré sous `PC_VERSION` seulement dans
`ITEMS.H`).

Validation runtime (item 23 forcé actif, OCB 0) :

```
RB item23 obj=114 room=13 ocb=0 pos=7680,-1280,75264
RB n=20  pos=7680,5676,91152  f1=3072  fall=53
RB n=40  pos=7680,6912,92672  f1=21    fall=0
RB n=200 inchangé (bille arrêtée)
```

La bille **tombe, roule et s'arrête** ; 200 frames sans `SIGSEGV`.

Build `build-gameplay59` : SHA256
`513472275916c1390736ebddb6953147d729c3b8d275c51adfe6f8e3c3935a47`.

### Diagnostics des stubs par frame : `UNIMPLEMENTED_ONCE()` (17 novembre 2026)

Plusieurs fonctions encore non portées sont appelées **à chaque frame** :
`UpdateFireSparks`, `UpdateGunShells`, `UpdateRats`, `UpdateBats`,
`KlaxonTremor`, `ProcessClosedDoors`, `WadeSplash` côté jeu, et
`PadSetActAlign`/`PadStartCom` côté émulateur. Leur `UNIMPLEMENTED()`
imprimait une ligne par frame :

- log illisible pendant les tests (9 050 lignes / 320 Ko pour 200 frames),
- un `printf` par frame en pleine boucle de contrôle.

Ajout de `UNIMPLEMENTED_ONCE()` dans `SPEC_PSXPC_N/SPECIFIC.H` et
`EMULATOR/EMULATOR.H` (même message, préfixé `(once)`), utilisé à ces neuf
emplacements. Le comportement (no-op) est **identique**, seule la
diagnostique change.

Mesure sur la sauvegarde corniche, 201 frames : chaque message apparaît
**une seule fois** (`WadeSplash` 1, `UpdateFireSparks` 1,
`ProcessClosedDoors` 1, `UpdateGunShells` 1, `PadSetActAlign` 1) et le log
passe de 9 050 lignes / 320 Ko à **1 617 lignes / 54 Ko** (−83 %).
Corniche 201 frames OK, aucun changement de comportement.

Build `build-gameplay59` : SHA256
`2b2b6dc2ced7f6e9dd4b87d45782583f78a743bf2a079e9fea8496864bf3c85c`.
Régression verrouillée par `tests/porting/test_stub_diagnostics.py`.

### Note de reproductibilité du binaire (17 novembre 2026)

Après nettoyage des sondes temporaires (printf `[LEVEL]`/`CPRET` dans
`CONTROL.C`/`GAMEFLOW.C`, retirés — l'arbre est revenu à `HEAD`), la
recompilation produit un `MAIN` de SHA256
`b59fa0a336cd9653724838bb3f16eab04050863092061ed76ecbeaf958ba7b0f`,
différent du `2b2b6dc2…` enregistré plus haut **à source identique** :
l'archive `EMULATOR/libPSX.a` est réassemblée à la main (`ar r`) et les
métadonnées d'archive ne sont pas reproductibles. Le comportement est
vérifié identique (corniche 201 frames OK, 1 493 lignes de log, soit le
même régime que la mesure « once »). Les SHA enregistrés servent de
traçabilité, pas de garantie de reproductibilité bit-à-bit.

Piste ouverte (documentée section 7 de
[`colosseum-walkthrough.md`](colosseum-walkthrough.md)) : le retour au
titre après chargement n'a pas été reproduit avec les sondes en place —
le niveau 3 se lance et tourne (`[LEVEL] post-initial ControlPhase
status=0 gameMode=0 level=3`) ; les observations « retour au titre »
précédentes correspondent à des échantillonnages trop précoces pendant le
chargement (et à la bufferisation de stdout), pas à une sortie du niveau.

### `KlaxonTremor` porté (17 novembre 2026)

`GAME/CONTROL.C` : `KlaxonTremor` remplace le stub par la version de
`joby.cpp` — klaxon périodique (`SFX_KLAXON` toutes les 512 frames),
tremblement de caméra par impulsions (`camera.bounce`) déclenché
aléatoirement après 450 frames, avec les deux compteurs `static`
(`timer`, `bounce`) du code d'origine. Un stub de moins parmi les
fonctions appelées chaque frame.

Validation : corniche **201 frames OK**, aucun `SIGSEGV`, 4 183 tests
PASS (le test `test_stub_diagnostics.py` a été mis à jour : `KlaxonTremor`
n'est plus un stub).

Build `build-gameplay59` : SHA256
`95bdcc4f207cdf7041837630023d863d65b3dd2c92ab6622faa9bdab214cd423`.

### `FixedCamera` porté (17 novembre 2026)

`GAME/CAMERA.C` : `FixedCamera()` remplace le stub `UNIMPLEMENTED()` par
la version de `camera.cpp` — caméra fixe pilotée par `UseForcedFixedCamera`
ou par `camera.fixed[camera.number]`, suivi de cible, `MoveCamera(&ideal, 1)`
et décrément de `camera.timer`. C'était un **blocage fonctionnel réel** :
`CalculateCamera` appelle `FixedCamera()` dès que
`camera.type != CHASE_CAMERA`, et le stub laissait la caméra figée sur sa
position précédente (vue statique, Lara hors champ / non dessinée). Or la
salle 12 porte justement un trigger `CAMERA(0)`.

Includes ajoutés : `TOMB4FX.H` (FlashFader/DoBloodSplat), `DEBRIS.H`
(ShatterObject), `SPOTCAM.H` (SniperOverlay).

**Limite assumée et documentée** : le sous-bloc « sniper »
(`fixed->flags & 2`) n'est pas porté — il dépend de
`TriggerRicochetSpark`, `DoBloodSplat` et `ShatterObject`, absents du port
PSX (`TriggerRicochetSpark` n'existe que sous `PC_VERSION`, et y est un
stub). Aucun camera item de ce niveau n'utilise le mode sniper ; le
commentaire est laissé dans le code.

Validation : corniche **201 frames OK**, `camtype=0`, caméra mobile,
4 183 tests PASS. Mesure associée : sur la corniche la caméra se résout en
**room 8** (salles empilées) et Lara (`room 12`) n'est pas dans la liste de
rendu — limite de géométrie indépendante de ce port, documentée au § 6 de
[`colosseum-walkthrough.md`](colosseum-walkthrough.md).

Build `build-gameplay59` : SHA256
`b9d8e710fcbc4ba3d9bb09310e809ae92384829cfa0ffb02324dd27688d5771e`.
