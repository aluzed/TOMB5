# RE-785 — GetCeiling : fin du record sol avant géométrie plafond

30 septembre 2026. Baseline source `4316167e`, après livraison RE-784. Correction minimale de **GetCeiling** sous **PSX_VERSION && PSXPC_TEST** : quand le premier record sol est terminal, rejoindre la phase suivante sans décoder le suffixe comme géométrie plafond. Parcours pit et scan des callbacks conservés, pas de retour anticipé ajouté. Branche legacy inchangée.

## Tracker
- [x] Probe cible authentifié préexistant de cette mission : 56 appels synthétiques, sept types sol, deux états terminal et quatre suffixes pente.
- [x] RED actual-TU normal et UBSan strict, compilations/liens réussis : 21 divergences sensibles par matrice.
- [x] Correction minimale puis GREEN actual-TU et régressions ciblées.
- [x] RED documentaire avant inscription story/dashboard.
- [x] Revue indépendante PASS borné, replay frais56 ; livraison à vérifier séparément (`review-re785-seal/verdict.json`).
- [ ] Gameplay, corpus réel, traversées pit/sky et callbacks réels non validés par cette unité.

## Contrat observable
Le record sol est de type 2, 7, 8, 11, 12, 13 ou 14. Avec son bit terminal présent, la cible conserve la hauteur plafond de base sur les quatre suffixes construits. Sans ce bit, le record plafond suivant modifie la hauteur selon ses deux composantes pente. Contrôle suffixe nul et trois suffixes sensibles : 28 cas terminaux dont 21 distinguent la baseline ; 28 contrôles non terminaux. Les 56 retours target archivés concordent avec le modèle arithmétique natif sur la cohorte après correction. Appels directs, cellules sans pit/sky, hauteur positive ; modèle logiciel, pas oracle matériel.

La fixture compile GETSTUFF entière, headers normaux, g++ i386/C++17, lien normal avec élimination des sections inutilisées, sans ignorer les symboles non résolus. Elle compare retour short promu, record cellule complet, buffer floor-data complet et cinq globals scalaires/pointeur. Baseline publique byte-exact `73f994f0`, prédécesseur avant RE-784 : la hauteur positive isole le défaut terminal de la correction signée. Normal et UBSan strict, 56 cas chaque ; baseline reste volontairement RED avec 21 divergences de retour et invariance des buffers/globals. Aucun changement de compilation unsigned-char ; cette cohorte emploie le mode signé normal.

## Validation et limites
Archives privées `build/reverse/autonomy-20260930-13h/` : ledgers terminal-native-red, terminal-native-red-ubsan, terminal-pytest-red (deux échecs current attendus, deux contrôles baseline PASS), terminal-target03 exit0 et 56 résultats. GREEN courant archivé dans `re785-green.log`. Le probe cible initial définit un collecteur reads mais ne l'installe pas : ses listes vides **ne prouvent aucune absence de lecture**. Aucun constat d'allocation overflow, corruption ou RAM complète indépendante tiré de ce probe. Instruction authentication et retour exécuté sont distincts du contrôle de toutes les lectures.

La correction saute seulement la géométrie roof initiale ; le label précède le code pit et callback existant. Les régressions bridge maintiennent le consommateur GetCeiling et la registration déjà intégrés ; elles ne rendent pas exhaustive cette nouvelle cohorte. Revue indépendante PASS borné, replay frais56 ; livraison à vérifier séparément (`review-re785-seal/verdict.json`).

**pas de runtime** jeu, pas de fullbuild/relink ni nouvelle capture. **pas de GREEN global** : ni tous floor-data, ni triangles plafond, coordonnées extrêmes, architectures autres ou effets gameplay établis. Aucun raw opcode/dump/asset versionné ; suppressions blocked utilisateur et rapport protégé laissés hors commit.

## Handoff
Prochaine preuve utile : authenticité et comportement du premier roof triangle avec offsets négatifs, avant toute correction de son calcul. Le décalage d'un offset signé reste une hypothèse à attribuer et tester, pas une correction autorisée par ce GREEN. Pas de nouveau secteur après 12:40 ; clôture dès 12:45, arrêt absolu à 13:00. Aucun ancien ticket blocked recréé.
