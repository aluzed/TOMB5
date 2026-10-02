# BLOCKED-003 — Témoin naturel bridge non atteint

Statut : OPEN / preuve de consommation manquante. Parent RE793, prochain RE-794.

## Tracker
- [x] BASE naturel, huit bridges et six slots enregistrés vérifiés.
- [x] Corpus et graphe de navigation extraits/testés ; aucune injection.
- [ ] Callback naturel sensible et son effet consommé.

## Preuves
RE792/793 et manifeste public `docs/reverse/generated/re790-re793-native-bridge-progress.json`. Revue étroite RE792 PASS, zéro callback,1904paires consommateurs retenues. Route observée n’atteint pas les rooms bridge. Graphe13/14rooms candidat != preuve de traversée. Preuves brutes et scripts privés ignorés sous `build/reverse/autonomy-20261002/`.

## Critères de reprise
1. Capturer rooms/cells/doors/flip vivants lors d’un démarrage BASE frais ou relink explicitement attribué, sans remplacer leurs valeurs.
2. Attribuer premier portail discriminant et état de collision ; piloter uniquement via inputs réels, sans calls injectés/téléportation.
3. Observer callback enregistré effectivement appelé, hauteur d’entrée/sortie, préconditions flags/sector et effet ensuite consommé ; distinguer appel sans modification et effet sensible.
4. Capturer/inspecter/livrer PNG de chaque runtime, nettoyer processus/display ; revue indépendante et tests réels avant source si correction prouvée.

Pas de sûreté/globale ni équivalence hardware implicite. Deadline actuelle autorise la reprise avant2octobre23h, sans nouveau GO intermédiaire ; après échéance pas d’exploration. Les suppressions utilisateur antérieures restent préservées.
