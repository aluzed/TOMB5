# Linux32 / PSXPC_N — recette reproductible (PORT-001)

Cadrage de travail **provisoire**, pas une décision définitive de plateforme. Cette
recette construit les sources du checkout ; elle ne télécharge aucun jeu. Un
build réussi ou une sortie zéro ne valide ni menu ni gameplay.

**État au 29 octobre 2026** : le backend Linux32 (rendu, entrées, sauvegarde
rapide, audio SDL) est stable et testé, mais la campagne réelle est bloquée par
un manque **hérité de la décompilation** : `ObjectObjects`/`TrapObjects`
n'installent pas les gestionnaires des objets et les handlers pickup/collision/
switch/door sont des stubs. Aucun pickup ni interaction n'est possible. Détail
et preuve GDB : section « Cause racine héritée : objets runtime non initialisés »
plus bas.

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
- **Pause/reprise** : `Entrée` ouvre le menu pause, `Resume` rend le contrôle ;
  la scène reprend au même endroit.

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
compris).
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
(`build/porting/pal-chain-20261029/`). Soak PAL de 10 minutes avec la manette
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
- Conséquence visible sur les armes : `CombatCamera`
  (`GAME/CAMERA.C:1638`) a son corps sous `#if 0 || PC_VERSION` et tombe sur
  `UNIMPLEMENTED`. Dès que Lara sort les armes (`Y` sur la manette), la vue 3D
  devient entièrement noire (HUD encore dessiné) ; rengainer (`Y` à nouveau)
  restaure la scène. Reproduit sur NTSC : moyennes 0,1018 → 0 → 0,1025, 63
  appels `CombatCamera` (`build/porting/vpad-draw-20261029/`). Le combat aux
  armes est donc lui aussi inutilisable en l'état.

Conséquence : aucun pickup, keyhole, puzzle, levier, porte à clé/crowbar ou
ennemi ne peut réagir à Lara. Le déplacement, les déclencheurs de plancher et
la boucle de niveau fonctionnent, mais les interactions nécessaires à la
résolution de Rome (et de tous les niveaux) sont absentes. Ce n'est **pas** une
régression Linux32 : le même état existe en amont de la décompilation ; c'est
un travail de reconstruction gameplay (RE), soumis aux gates
`docs/stories/BLOCKED-004*` et aux tickets reverse, pas un correctif de port.

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
