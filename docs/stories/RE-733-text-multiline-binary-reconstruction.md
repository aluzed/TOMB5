# RE-733 — PrintString : transitions multiligne prouvées

## Statut et périmètre

Terminé — implémentation, tests, guards et revue indépendante validés.
Autorisation : autonomie jusqu’au 8 septembre 2026 à 23:45 Europe/Paris.
Suite de RE-732, sans réouverture des anciens inventaires terminaux.

Unité cohérente : réancrage horizontal et état vertical lors des changements
de ligne dans `SPEC_PSXPC_N/TEXT_S.C::PrintString`.

## Progression

- [x] Contrôler état live, identité Git, version et disponibilité du projet.
- [x] Exécuter Ghidra headless en lecture seule sur le programme cible.
- [x] Recouper appelant, ABI, GP, helper partagé et delay slots.
- [x] Écrire les tests puis observer RED : 8 échecs, 7 cas conformes.
- [x] Corriger les deux transitions prouvées uniquement.
- [x] GREEN : 36 tests de rendu et mesure réussis.
- [x] Régression emulator/reverse : 3383 tests réussis.
- [x] Revue indépendante de livraison et guards : approuvés, aucun défaut bloquant.
- [x] Livraison préparée : quatre fichiers sûrs explicitement indexés.

## Preuve cible et décision

Cible : boot PSX NTSC v1.0 `SLUS_013.11`, MD5
`4ef523e708d7a7d6571f39c6e47784f9`, conforme à `CONTRIBUTING.md`.
Le payload a été comparé au boot privé de son en-tête. Le bloc mémoire importé
correspond à cet en-tête ; le champ global imageBase de Ghidra n'est pas
l'adresse de début de ce bloc. Les alias KSEG du boot restent délibérés.

Deux nouvelles exécutions headless en lecture seule ont inspecté le rendu,
la mesure, les dimensions, leur appelant Requester, le boot et le helper
partagé d’alignement. Attribution recoupée par arguments, graphe et sorties :
chaîne, coordonnées, couleur, drapeaux et émission des sommets GPU.
La globale d’échelle est recoupée par opérande relatif au GP initialisé au boot,
non par les globals automatiques incohérentes du décompilateur.

| Comportement | Preuve | Modification |
|---|---|---|
| Ligne suivante alignée à droite | Le helper partagé soustrait la largeur à l’ancre, comme pour la première ligne | Remplacer l’addition par la soustraction |
| Sauts de ligne consécutifs | Effacement explicite du bas précédent avant avance verticale fixe | Activer l’affectation auparavant laissée en commentaire |
| Centrage, gauche, échelle, couleurs et fin de chaîne | Chemins conservés et couverts par les tests | Aucune modification |

Le retour du helper initial est ajusté par un delay slot. La décompilation
seule ne décrit donc pas fidèlement le parcours : les instructions et leurs
slots ont été lus directement, notamment pour les deux décisions ci-dessus.
Aucune instruction, adresse cible, table extraite ou décompilation n’est publiée.

## Vérification et limites

`tests/emulator/test_text_layout.py` compile le vrai fichier avec ses en-têtes,
exécute `PrintString`, `GetStringLength` et `DrawChar`, puis vérifie les polygones
émis. Les métriques et couleurs sont synthétiques. Les deux stockages legacy
reçoivent les mêmes métriques pour isoler la mise en page de la sélection de
police encore incomplètement reconstruite. Aucun remplacement de `DrawChar`.

Couverture : ancrages gauche/droite/centre, priorité centre, réduction,
lignes blanches répétées ou initiales, couleurs et espaces, fins de chaîne,
absence de dessin et conservation du drapeau lors du clignotement.

- RED réellement observé avant correction : 8 échecs / 7 réussites.
- GREEN ciblé : 36 réussites, dont 15 nouveaux cas de rendu.
- Régression complète emulator/reverse : 3383 réussites.
- Recoupement parent : instructions décisives relues et 36 tests réexécutés.

Ce sont des tests hôte du port, pas une exécution du binaire cible dans un
émulateur. Aucun marqueur de reconstruction complète n’est ajouté.
Accents, octets hauts, bornes et mapping des tables restent hors périmètre.
Les coordonnées 16 bits ne justifient pas de correctif de signe supplémentaire
sans différence observable.

## Handoff — recherche toujours autorisée

Prochaine unité : établir la sélection des glyphes entre mesure et rendu,
ainsi que les domaines de caractères admis ; si les accès hors tableau ne
peuvent pas être représentés sûrement, changer de cluster. Ne pas multiplier
les variantes de validation de cette transition désormais corrigée.
Le domaine accentué reste bloqué pour modification, pas pour recherche.

Preuves et journaux privés dans le répertoire ignoré
`build/reverse/autonomy-20260908/` : `print-layout-proof.md`,
`print-inspection.txt`, `print-layout-helper.txt`, `print-headless.log`,
`print-layout-headless.log`, `print-layout-red.log`, `print-layout-green.log`,
`print-layout-regression.log`. Ne jamais indexer ces fichiers.
