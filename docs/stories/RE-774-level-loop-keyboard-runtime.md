# RE-774 — Boucle du niveau et entrée clavier observées sur ELF32

23 septembre 2026, Europe/Paris. **Après RE-773**, même exécutable source ELF32 précédemment construit et vérifié ; source de production inchangée ; `code_change_readiness=blocked`. Ce jalon intégré suit sélection du titre → chargement → boucle du niveau → touche de contrôle, mais **gameplay complet non validé** : caméra, animation, collision, durée prolongée, sauvegarde et progression restent hors preuve.

## Preuve privée et frontières

- Lancement Xvfb réel sans débogueur, durée bornée à **105 secondes** : touche C envoyée au titre, captures de la fenêtre du jeu `menu-before.png`, `after-8.png`, `after-28.png`, `after-50.png` et `after-60.png`. `run.json` attribue le même hash d'exécutable que RE-773, les injections, captures et **exit 124** de l'application : limite temporelle, pas succès fonctionnel. Les images restent sous `build/reverse/autonomy-20260923-runtime-2021/` ignoré. Les différences de pixels ne prouvent ni déplacement contrôlé ni rendu correct ; `after-50.png` est une capture source après sélection, non une capture PlayStation.
- Lancement GDB distinct (`level.json`, `level-gdb.log`) : entrée `DoLevel` avec sélection du premier niveau, puis `GAME_LOOP_ENTRY` au début de la boucle qui suit `ControlPhase`, avec `gfCurrentLevel=1`, statut de boucle actif et pointeur Lara non nul, chambre initiale et position lisibles. **Niveau chargé et boucle atteinte**, mais cet arrêt GDB ne valide pas le rendu ni un mouvement.
- Autre lancement GDB (`control.json`, `control-gdb.log`) : injection XTest de flèche haut, arrêt conditionnel à `LaraControl` avec `gfCurrentLevel=1`, bit `IN_FORWARD` présent et `GLOBAL_playing_cutseq=0`. Cela établit une **entrée de contrôle observée** par la logique source du niveau, non l'effet visuel ou la jouabilité globale.
- Quatrième lancement GDB (`movement.json`, `movement-gdb.log`) : même précondition de contrôle, puis watchpoint matériel sur les coordonnées de Lara ; position z initiale **31232**, première modification observée à **31255** alors que le bit avant reste présent. Le watchpoint couvre ce champ et ce trajet seulement : il ne démontre pas tous les contrôles, la causalité exclusive du clavier, ni l'absence d'autres écritures transitoires. Les lancements distincts ne doivent pas être présentés comme une exécution continue de toutes les mesures.
- Wrapper de capture et wrappers GDB exit 0 seulement pour leurs dispositifs. Les sondes GDB s'arrêtent volontairement aux points indiqués ; aucun de ces exits ne signifie fin réussie du jeu. Les avertissements de stubs dans les logs n'identifient pas à eux seuls un obstacle fatal ; **aucun asset public** ni capture n'entre dans le dépôt ou le dashboard, le dossier privé est ignoré.

## Vérification documentaire et readiness

Le test documentaire RE-774 a été écrit avant story et dashboard : RED observé, trois échecs attendus, `red.log`, exit 1. C'est un RED de publication manquante, **pas** un RED comportemental du moteur. Sélection RE-770→774 : 12 réussis (`green-final.log`). Suite `tests/reverse/` fraîche : **3335 réussis, 7 échecs** (`suite.log`, exit 1) ; mêmes sept noms de tests que les dérives constatées sur le checkout de référence RE-773. Un CSV historique régénéré incidemment par la suite a été restauré après examen du seul écart de lignes : il n'appartient pas à cette livraison. La suite globale n'est **pas** verte. Ce jalon ne fournit pas la preuve cible/ABI pour patcher GetHeight ; **GetHeight** reste ouvert. `code_change_readiness=blocked`.

## Tracker

- [x] Même ELF32 et nouveau lancement Xvfb de 105 secondes, captures privées et exit applicatif archivés.
- [x] `DoLevel` et boucle de jeu `ControlPhase` atteints après sélection du titre dans un lancement GDB distinct.
- [x] `IN_FORWARD` constaté dans `LaraControl` et modification de z par watchpoint dans un autre lancement borné.
- [x] RED documentaire constaté avant la présente story.
- [ ] Gameplay complet non validé ; pas de correctif source ou de marqueur de reconstruction avancé.

## Handoff

**Après RE-774** : conserver ce jalon limité niveau chargé et contrôle observé. Prochaine preuve intégrée : comparer entrée avant/arrière et contrôles sans entrée sur la même scène, établir une capture réellement interprétable du niveau et vérifier les effets de caméra, collision et progression avant toute correction ; qualifier le premier blocage reproductible si cette continuation échoue. La preuve amont/cible GetHeight demeure indépendante et ouverte. Aucun patch de source sans RED comportemental réel et attribution de la cible.
