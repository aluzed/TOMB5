# RE-773 — Titre interactif observé sur ELF32 frais

23 septembre 2026, Europe/Paris. **Après RE-772**, un nouveau build source ELF32 de `TombRaiderChronicles_PSXPC_N` atteint un menu visible et accepte une sélection par clavier. C'est un jalon intégré build → fenêtre → rendu → entrée → branche du menu, pas une validation du niveau jouable ni une équivalence avec la cible PlayStation ; source de production inchangée ; code_change_readiness=blocked.

## Résultat et provenance

- Même HEAD initial que la présente unité, configuration CMake Debug, `DISC_VERSION=ON`, compilation et liaison `-m32`, bibliothèque GLEW privée déjà disponible sous `build/` ignoré. Configuration exit 0 et **build exit 0** ; `file` identifie ELF32. Aucun asset, binaire ou capture n'est ajouté au dépôt public.
- Premier lancement Xvfb réel : fenêtre du jeu et captures à plusieurs instants, durée bornée à **45 secondes** ; application **exit 124**, limite temporelle, pas réussite fonctionnelle. Aux premières captures : splash/logo ; plus tard, image rendue différente. Les changements de pixels seuls ne prouvent pas le menu.
- Deuxième lancement Xvfb réel : actions **XTest** horodatées (flèche bas, flèche haut, touche C), captures brutes avant et après sous le même répertoire privé. À la capture `after-up.png`, OCR local reconnaît **New Game** et **Special Features** : menu visible. Les captures après touche C montrent une autre scène, sans preuve que le niveau soit jouable ; les comparaisons de pixels sont confondues par l'animation de fond. Ce lancement de **80 secondes** s'achève aussi en **exit 124**, limite temporelle, sans crash observé dans cette fenêtre.
- Une exécution distincte du même binaire sous GDB s'arrête à la branche de sélection de `TitleOptions` après injection XTest de C. Le log privé `select-gdb.log` constate l'entrée correspondante, **ret=3**, **gfLevelComplete=1**, indicateur logique `PadConnected=1` et option PlayAnyLevel inactive. Le diagnostic d'initialisation signale pourtant l'absence de manette physique : cet indicateur n'en démontre pas une. Le bouton a atteint la logique native du menu et sélectionné le premier niveau ; GDB arrête l'exécution à cette frontière et ne prouve pas le chargement, l'affichage ou les contrôles du niveau.
- Deux diagnostics GDB plus courts se sont terminés par timeout avant leur point d'arrêt (non présentés comme preuve négative). Les reprises plus longues constatent l'entrée du flux titre puis `TitleOptions`, avec état de menu initial et clavier logique connecté. Aucune correction de source n'a été dérivée des avertissements « Unimplemented ».

Preuves privées : `build/reverse/autonomy-20260923-runtime-1945/` (ignoré), notamment `configure.log`, `build.log`, `runtime.json`, `runtime.log`, `interactive.json`, `interactive.log`, `select.json`, `select-gdb.log`, `after-up.png`, `after-cross.png`, scripts privés de capture et journaux GDB. Le wrapper exit 0 indique seulement la fin du dispositif ; les sorties application sont explicitement consignées. Captures directement livrables au demandeur, mais **aucun asset public** dans les documents, le Git ou le HTML.

## Contrat et limites

La preuve de titre interactif est source/runtime sur ce build, non un test matériel, ni une attribution cible Ghidra, ni un test exhaustif de toutes les options. L'OCR d'une image ne suffit pas seul : l'arrêt GDB sur le chemin de sélection constitue le contrôle d'entrée distinct. **Gameplay non validé** ; la capture après sélection n'est pas une validation du rendu/contrôle d'un niveau. La collision cible GetHeight reste ouverte, hors de cette unité. Aucun patch sans test comportemental RED et preuve de comportement/ABI de la cible.

## Vérification documentaire

Test RE-773 écrit avant les documents : RED documentaire observé, trois échecs attendus (story et deux dashboards non avancés), exit 1, `red.log`. Ce RED ne constate pas un défaut comportemental du jeu. GREEN final : 53 tests réussis (`green-final.log`). Suite `tests/reverse/` : **3332 réussis, 7 échecs** (`suite.log`) ; les sept échecs des familles RE-165, RE-340, RE-699/700/701 sont également reproduits sur le checkout de référence `315216e2` (`baseline-tests.log`, `baseline-ignored-tests.log`). Ce n'est pas une suite globale verte, ni une justification pour masquer ces dérives préexistantes. Revue indépendante : vérification documentaire en lecture seule, sans nouveau runtime ni validation de gameplay. Le test documentaire vérifie le contrat écrit et la conservation des dashboards, pas l'authenticité autonome des sondes privées.

## Tracker

- [x] Nouveau build ELF32, captures d'un vrai processus source et entrée XTest observée.
- [x] Menu visible et branche de sélection `TitleOptions` atteinte dans un lancement GDB séparé.
- [x] Test documentaire écrit et RED observé avant story/dashboard.
- [ ] Gameplay, chargement complet de niveau et cible GetHeight non validés ; code_change_readiness=blocked.

## Handoff

**Après RE-773** : menu observable et sélection du premier niveau établis dans les limites ci-dessus ; gameplay non validé. Prochaine unité intégrée utile : prolonger le même chemin au-delà du retour de `TitleOptions`, qualifier le premier niveau effectivement chargé, sa capture et l'effet des entrées de contrôle ; si échec, arrêter au premier obstacle reproductible et attribuer ce blocage avant tout correctif. Maintenir en parallèle la preuve amont/cible GetHeight ouverte. Ce handoff ne présume ni autorisation de patch ni succès de gameplay.
