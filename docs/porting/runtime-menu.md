# Runtime Linux32 — premier crash de navigation corrigé

18 septembre 2026 ; base `7ac47a84`. Linux32/PSXPC_N reste une cible **provisoire**.
PORT-001 et PORT-002 restent **In progress**. Aucun ticket accepté Done.

## Résultat concret

Le titre n'était pas seulement bloqué sur un splash. Les preuves interrompues
retrouvées et un lancement neuf du binaire antérieur montrent l'arrivée dans
`TitleOptions`, puis **SIGILL au premier Down**, dans `S_SoundPlaySample`, appelée
par `SoundEffect` depuis le menu. La branche active de cette fonction ne retournait
pas de valeur ; le compilateur utilisé émettait une instruction de trap après
l'appel. Le paramètre transmis comme pitch provenait aussi du mauvais argument.

La correction est limitée à `SPEC_PSXPC_N/SFX.C::S_SoundPlaySample` : transmettre
le pitch d'entrée et retourner le résultat de `PlaySample`, comme le contrat cible
attribué. Aucun changement des autres backends, du loader ou de `PlaySample`.
Le correctif n'est **pas** une reconstruction audio complète : le callee source
reste incomplet, notamment les volumes et son résultat propre.

## Progression / recette réellement exécutée

- [x] Crash initial reproduit par entrée clavier XTest réelle, sans écriture des
  variables du jeu ni saut artificiel du titre.
- [x] Test actual-TU i386 avant correction : **30 échecs SIGILL, 60 PASS** ; après
  correction, **90 PASS**, test inchangé. Le double `PlaySample` est explicitement
  substitué au lien via un symbole faible sur l'objet privé compilé ; wrapper et
  wrapper looped de contrôle restent les vraies fonctions de la TU.
- [x] Nouveau build jeu corrigé, exit 0. GLEW du build antérieur réutilisé ; ceci
  n'est pas présenté comme un quatrième rejeu complet de la recette GLEW.
- [x] Trois processus neufs du binaire corrigé atteignent `TitleOptions` vers
  26 secondes, avec captures privées à 29 secondes. Options New Game et Special
  Features réellement lisibles ; inspection des pixels, pas seulement OCR.
- [x] Premier parcours : Down change l'index 0→1, Up le ramène 1→0 ; `c` valide
  New Game par le chemin normal, puis entrée observée dans `DoLevel(1)`.
- [x] Deux parcours suivants : Down, `c` ouvre Special Features ; `z` (Triangle)
  revient au titre. Captures du sous-menu et du retour inspectées. Relâchements
  des touches observés (`RawPad=0`), aucun état forcé dans le debugger.
- [x] Trois fermetures WM_DELETE_WINDOW : **application exit 0** observé par GDB.
- [ ] Acceptation complète du menu (dont lisibilité de la sélection à travers son
  animation), manette physique, variantes de données et audio.
- [ ] Scène jouable, commandes Lara et gameplay validés.
- [x] Revue indépendante précommit PASS le 18 septembre à 09:47 Paris :
  126 tests publics neufs réussis, contrôle renderer réussi et preuves archivées
  auditées sans régénération. Rapport privé `review01/review.md` ; cela ne valide
  ni le gameplay ni le matériel audio.

À 60 secondes du premier parcours, l'image montre Lara derrière des barreaux et
un indicateur circulaire : **écran illustré de chargement, pas une scène jouable**.
La sélection change dans l'état observé ; une seule différence de couleur entre
captures ne suffit pas, car le texte sélectionné est animé.

## Attribution et limites de la preuve cible

Nouvelle unité privée : `build/reverse/autonomy-20260918-1030-recovery/proof-audio/`.
L'exécutable cible est authentifié par empreinte, en-tête et payload ; GP établi
à partir du startup et non des pseudo-globales du décompilateur. Ghidra frais
avec commandes/exit et marqueur de fin ; wrapper exécuté sur **126 cas**, callee
réel sur **216 cas**. Comparaison avec un interpréteur entier séparé : RAM
complète, registres, traces de visites et événements. Chaque cas réinitialise CPU
et RAM ; les visites incluent entrées interceptées et arrêt, pas des instructions
retirées. Les matrices utilisent des états construits, non un boot cible complet.

Le double du wrapper est distinct des cas exécutant réellement `PlaySample`,
`CalcVolumes`, `SPU_Play` et l'allocateur cible. Ces derniers conservent deux
frontières SDK synthétiques : aucune validation du matériel SPU ou du son audible.
Le worker de preuve a atteint sa limite de temps sans HANDOFF ; ses commandes
terminées et résultats existent, mais cela ne constitue pas une revue finale du
patch. Les fichiers historiques et leurs gardes de date sont conservés.

## Rejouer les tests publics sans assets

```sh
ulimit -c 0
python3 -B -m pytest -p no:cacheprovider -q tests/porting \
  --basetemp=build/porting/menu-public-tests
python3 scripts/porting/render_backlog.py --check
```

Le test requiert un compilateur C++ i386/multilib et GNU objcopy. Il n'exécute pas
le callee audio réel et ne prouve pas le gameplay. Les sorties temporaires doivent
rester ignorées ; aucun exécutable, image du jeu ou opcode n'est versionné.

## Provenance privée et codes de sortie

Bundle `build/reverse/autonomy-20260918-1030-recovery/` :

- `wrapper-red.json/.log`, `wrapper-green.json/.log` : commandes, dates, exits,
  hashes source/test et logs ; le RED porte sur le comportement natif.
- `configure.json`, `build.json`, `runtime-build/` : compilation corrigée.
- `baseline-runtime/` : ancien binaire hashé séparément, SIGILL frais.
- `fixed-runtime/`, `menu-back2/`, `menu-back3/` : identité binaire/données/fenêtre,
  événements XTest et fermeture, captures hashées et logs GDB.
- `proof-audio/*-invocation.json` : authentification, Ghidra, deux exécutions
  cibles concordantes, audit sémantique supplémentaire et cinq tests finaux.

**Build exit, recorder exit, GDB exit et application exit sont différents.** Le
premier script GDB fait `bt` après fermeture normale : GDB exit 1 (« No stack »),
mais `APPLICATION_EXIT 0` et « exited normally » sont enregistrés. Les deux
parcours suivants évitent ce `bt` sans inférieur et terminent aussi GDB exit 0.
Le baseline GDB peut sortir 0 après SIGILL : ce n'est pas un succès du jeu.

Les anciens blocs de PORT-001/backlog sont conservés intégralement comme
historique. La progression runtime courante les précède ; leurs anciennes
échéances/réserves ne sont pas réécrites rétrospectivement.
