# RE-791 — Corpus authentique : trouver un niveau utile

2 octobre2026, parent RE790. **Décodage concret exécuté : pivot BASE trouvé**, aucun changement moteur.

## Tracker
- [x] Quinze entrées réelles décodées : titre et quatorze niveaux retail ; 2084 items.
- [x] Buffers room-loaded archivés RE763 reconstruits/recontrôlés intégralement ; layout source et inspection cible antérieure utilisés.
- [x] 151 items Rome comparés aux observations natives RE790, objets/rooms/positions/rotations ordonnés conformes.
- [x] Six tests privés PASS, rejoués indépendamment ; échec dépendance Unicorn initial conservé puis venv existant réutilisé.
- [x] Route title New Game + L1 candidate testée réellement ensuite dans RE792.
- [ ] Pas de suffixe cible items exécuté neuf, ni callback/gameplay corpus validé ; RE-794.

## Résultat utile
35 BRIDGE_FLAT, zéro BRIDGE_TILT1 et31 BRIDGE_TILT2, soit66 items bridge ; tous possèdent une référence action-object dans ce décodage. Niveaux positifs : BASE8, LABYRINTH27, OLD_MILL9, THIRTEENTH_FLOOR13, ESCAPE_WITH_THE_IRIS3, RED_ALERT6. Aucun input arbitraire ni portée universelle revendiqués.

BASE : premier pivot,177items/169rooms et huit FLAT. Le libellé LVL5_BASE contient le préfixe du titre, pas son index natif : BASE est entrée conteneur cinq et niveau moteur quatre, distinction établie par RE792.

Archives `build/reverse/autonomy-20261002/re791-corpus/`. Décodage frais != exécution loader complète. Les buffers room-loaded proviennent d’un suffixe cible authentifié **archivé** ; seul leur contrôle est neuf ici. Comparaison native BASE ultérieure complète et revue bornée dans RE792. **pas de GREEN global** sanitaire/gameplay ; aucun asset/raw versionné.

## Handoff
RE-794 : utiliser BASE et les observations natives, pas une nouvelle matrice synthétique ; capter état rooms/doors/flip live pour navigation/callback sensible. Deadline2octobre23h demeure l’autorisation, sans GO intermédiaire.
