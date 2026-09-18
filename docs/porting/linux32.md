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
