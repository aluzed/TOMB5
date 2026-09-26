# Test public synthétique — filtre des actions de hauteur

Ces fichiers publics ont reçu une revue indépendante PASS bornée du filtre ; ils accompagnent la correction intégrée. Ils ne contiennent ni données d'archive, ni instructions extraites, ni adresses historiques, ni fixtures de jeu authentiques. Les valeurs de test sont synthétiques.

## Exécution

Depuis la racine du dépôt, avec g++, support C++ 32 bits et les dépendances des headers normaux disponibles :

```sh
python3 tests/reverse/fixtures/re780/run_test.py --root . --source SPEC_PSXPC_N/GETSTUFF.C --output build/reverse/re780-trigger-filter-new-run
```

Le dossier output doit être absent. Pour tester une correction privée, passer son chemin à `--source`. Le runner compile la TU entière séparément du harnais. Les headers du dépôt sont utilisés sans substitutions. La liaison élimine les sections non atteintes ; elle ne supprime pas les erreurs de symboles non résolus. Ce n'est pas un build du jeu entier.

## Contrat borné

- Tous les types d'action représentables par quatre bits, callback présent/absent, inhibition présente/absente, bit auxiliaire présent/absent.
- Seul le type objet appelle le callback, en préservant arguments et ordre.
- Les types avec payload supplémentaire le consomment et terminent selon le payload, pas selon le mot d'action précédent.
- Terminaison des actions simples ; suites mixtes, répétitions et inhibition mixte.
- Pointeur items protégé pour chacun des types non-objet ; exécution isolée par processus enfant.
- Hauteur plane positive, globals réinitialisés, données/items/descripteurs inchangés. Le callback synthétique écrit son paramètre hauteur sans lire sa valeur entrante.

La sortie se termine par un compteur d'assertions agrégées ; le code de retour vaut zéro uniquement si tous les cas passent. Chaque cas comporte plusieurs assertions regroupées. Les crashes enfants sont des échecs de cas, distincts des erreurs de compilation ou de liaison.

Historique RE-780 : « callbacks non nuls non réparés » décrivait le snapshot avant RE-781, et non la correction actuelle.

Évolution RE-781 : le callback écrit toujours la même valeur synthétique, mais le test attend désormais sa propagation au retour GetHeight quand il est appelé. Le filtre, les arguments, l'ordre et les cas protégés restent inchangés. Les anciens résultats RE-780 restent historiques ; ils décrivaient le retour non propagé avant cette correction.

Limites : fixtures minimales, Linux/i386, pas de sanitizer, pas de preuve universelle d'absence d'UB, pas de callback de jeu réel dans cette fixture, pas de géométrie complexe ni de couverture gameplay. La fixture RE-781 séparée compose le vrai BridgeFlatFloor via un adaptateur de types explicite et le vrai consommateur UpdateLaraRoom.
