# Linux32 / PSXPC_N — recette reproductible (PORT-001)

Cadrage de travail **provisoire**, pas une décision définitive de plateforme. Cette
recette construit les sources du checkout ; elle ne télécharge aucun jeu. Un
build réussi ou une sortie zéro ne valide ni menu ni gameplay.

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
  interactions dans la fenêtre 30–50 s, ou relancer. Les runs où `Cross` a été
  envoyé trop tard ont fini en `DEMO MODE`, pas dans une partie.
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
`build/porting/ui-evidence-20261028/gameplay-ui.png`, `gameplay-resumed.png`. Aucune manette physique
testée ; pas de hot reload. Tickets :
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
  efface l'état clavier (touche relâchée hors fenêtre) pour éviter une action
  bloquée. Non testé sur un vrai changement de bureau ; le cas « Shift resté
  enfoncé dans le serveur X » a été rencontré pendant la recette et nettoyé
  avec `xdotool keyup`, pas par le jeu.
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

La sauvegarde mémoire PSX (`MemCard*`) n'est pas implémentée pour PSXPC_N et
`RestoreLevelData` reste un stub. Le port fournit donc une **sauvegarde rapide
de port** : `F5` en jeu écrit `TOMB5.SAV` (ou `TOMB5_SAVE_PATH`), `F6` au titre
recharge la sauvegarde et reprend au même endroit.

- **Format** : en-tête magique `T5P2`, version 2, `savegame_info` complet
  (inventaire, santé, stats, niveau), position/rotation/salle/état d'animation
  de Lara, checksum FNV-1a. Fichier de 466 octets.
- **Écriture** : `SaveLaraData()` rafraîchit `savegame.Lara` ; `F5` est capté
  avant le keymap (touche réservée) et consommé une seule fois par frame.
- **Lecture** : `F6` au titre appelle `PortSave_Read`, puis `TitleOptions`
  retourne 2 ; le gameflow recharge `savegame.CurrentLevel` en mode 4,
  `sgRestoreGame()` restaure l'état de Lara, puis `PortSave_ApplyPending()`
  replace Lara (position, salle, animation), met à jour la salle et réinitialise
  la caméra.
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

### Limites PORT-006

- `RestoreLevelData` n'est pas implémenté : les objets, portes, pickups et
  interrupteurs du niveau repartent de l'état initial ; seuls Lara et son
  inventaire/santé sont restaurés. Ce n'est pas une reprise d'état complet.
- Pas de sauvegarde via carte mémoire PSX ni via le menu d'inventaire ; `F5`/`F6`
  sont des touches réservées non remappables. Pas de chargement en jeu (le
  chargement n'est traité qu'au titre), pas de slots multiples, pas de
  sauvegarde pendant une FMV/menu.
- Un fichier absent/corrompu est refusé avec un log et le titre continue.
  L'écriture n'est pas atomique (pas de fichier temporaire + rename).

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
