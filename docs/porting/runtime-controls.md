# Linux32 — commandes, première transition et réarmement du regard

19 septembre 2026. PSXPC_N/i386 reste **provisoire**. PORT-003/004/005 :
**In progress**, pas Done ; acceptation intégrée encore bloquée par le regard
incomplet et les autres critères non exercés. Cette unité prolonge
[runtime-level.md](runtime-level.md), sans modifier son historique.

## Observations réelles avant correctif

Deux processus neufs, binaire antérieur authentifié, parcours titre → New Game,
entrées clavier XTest, pause → Quit/Yes → titre, fermeture de fenêtre normale.
Aucun saut de niveau, écriture GDB d'état du jeu ou remplacement runtime de service.

- Premier parcours : `x` déclenche un saut ; position verticale négative dans les
  traces, retour au sol, poses de saut et réception visibles. `Up` avance puis
  s'arrête contre un obstacle. Appuyer sur `c` sans objet n'établit pas une interaction.
- Deuxième parcours : `Up` maintenu traverse naturellement **room 0 → room 2**,
  d'un couloir vers une zone plus ouverte, avant arrêt contre un obstacle.
  Il ne s'agit pas d'une validation générale des collisions ou des salles.
- Défaut reproductible : `Shift_L` + `Right` conserve `lara.look=0`, ne tourne pas
  la tête et fait tourner le corps. `Shift_L` seul atteint réellement le stub
  `LookCamera` ; une capture du deuxième parcours montre une vue noire.
- Les deux parcours reviennent au titre et terminent avec **application exit 0**
  et **wrapper GDB exit 0**.

## Cause locale attribuée et correctif minimal

Une inspection Ghidra neuve du boot SLUS authentifié, en lecture seule, démontre
que `LaraAboveWater` réarme le bit `look` **après** Look/Reset et **avant** le
contrôleur d'état. Le contrôleur peut ensuite l'effacer : cette inhibition doit
être consommée au frame suivant, puis réarmée. La source omettait ce réarmement.
Le producteur inhibiteur `lara_as_splat` et sa table de dispatch ont été attribués.
L'initialisation cible complète n'a pas été prouvée dans cette unité.

`GAME/LARA.C` ajoute seulement ce réarmement sous `PSX_VERSION && PSXPC_TEST`.
La validation native porte sur **i386** : cette conjonction n'est pas, à elle seule,
une preuve pour toutes les architectures possibles. Le bit `look` correspond entre
cible et en-têtes natifs ; les champs suivants de `lara_info` ne sont **pas** tous
aux mêmes offsets. Aucun transfert aveugle de structure cible vers l'hôte.

Ce correctif ne reconstruit **pas** `LookCamera`. L'attribution de ce dernier révèle
plusieurs dépendances de géométrie, sol/plafond et un dispatch indirect conditionnel.
La preuve locale du réarmement ne vaut pas preuve de ces dépendances.

## Tests comportementaux et limites

- **RED avant patch : 60 failed / 56 passed** ; compilation et linkage réussis.
- **GREEN : 116 passed**, après nouvelle compilation du TU intégral `GAME/LARA.C`.
- Vrais `LaraAboveWater`, `LookLeftRight`, `ResetLook`, vrais en-têtes et ABI i386.
- Matrice : look initial, entrées directionnelles, contrôleur inhibiteur/non
  inhibiteur, motifs de flags voisins ; séquences de trois frames de récupération.
- Doubles explicitement bornés aux tables de dispatch et services d'animation,
  physique, armes et triggers. Ces tests ne prouvent ni monde physique ni gameplay.
- Affaiblissement de symboles sur un objet privé uniquement ; aucune suppression
  de symboles non résolus. Sections machine des fonctions testées inchangées.
- Attribution cible **statique**, pas nouvelle émulation cible ni équivalence totale.

```sh
python3 -m pytest -q tests/porting/test_lara_look_rearm.py
python3 -m pytest -q -p no:cacheprovider tests/porting
python3 scripts/porting/render_backlog.py --check
```

Le dernier ensemble comprend aussi des tests documentaires et de préflight :
leur succès n'est pas une validation additionnelle du jeu.

## Rejeu après correctif — binaire fraîchement construit

Le driver `scripts/porting/linux32.py build` a recompilé **GLEW et le jeu** dans
un nouveau dossier. Un troisième processus a rejoué les mêmes entrées que le
second parcours, sans intervention sur les états du jeu.

- [x] Titre → New Game → transition room 0 → room 2 conservés.
- [x] Pendant `Shift_L` + `Right`, `lara.look=1`, rotation de tête non nulle,
  rotation corporelle stable ; avant patch, tête nulle et corps en rotation.
- [x] Relâchement : tête revenue au neutre et rendu de scène revenu.
- [x] Pause → Quit/Yes → titre ; fermeture normale, application et GDB exit 0.
- [ ] **Vue noire toujours présente pendant le regard**, avec interface visible :
  `LookCamera` reste un stub. Ne pas appeler ce correctif « caméra réparée ».

Les trois planches contact ont été inspectées : 15, 13 et 13 captures originales.
`runtime-audit.json` recoupe les hashes, fenêtres d'entrée, états et exits ; il
vérifie des archives, sans ajouter de lancement. Les contrôles ont produit
**251 tests publics PASS** sur `tests/porting`, dont les 116 cas du nouveau harness.

## Tracker

- [x] Saut et réception observés sur le chemin réel avant correction.
- [x] Première transition entre deux salles observée, sans état forcé.
- [x] Défaut du regard reproduit ; divergence locale attribuée dans Ghidra.
- [x] Réarmement corrigé après RED réel ; GREEN sur TU intégral.
- [ ] Regard caméra complet : `LookCamera` reste un stub.
- [ ] Interactions avec objets, collisions étendues, perte de focus et manette.
- [ ] Sauvegarde/reprise, audio et premier niveau complet.

## Preuves privées

`build/reverse/autonomy-20260919-1000/unit02-controls-0824/` :

- `run01/`, `run02/` : chronologies, entrées, captures hashées et traces avant patch.
- `look-attribution/`, `look-rearm/` : exports Ghidra authentifiés, ledgers,
  vérifications de payload complet et projet inchangé ; aucune donnée brute versionnée.
- `rearm-fix/` : RED/GREEN, attribution relue, audit objets et commandes exactes.
- `fresh-build/` : build neuf du jeu et de GLEW, ELF32/i386 et bibliothèques vérifiés.

Les captures, exécutables, exports et données de jeu restent ignorés. Le rapport
utilisateur préexistant est laissé intact et n'a pas été consulté.
