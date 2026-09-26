# RE-781 — Hauteur callback : producteur, propagation et consommateur

26 septembre 2026, Europe/Paris. Après RE-780, correction bornée de deux affectations dans GetHeight : initialiser l'output avec la hauteur courante avant callback, puis propager cet output au retour. Le vrai BridgeFlatFloor et le vrai UpdateLaraRoom sont exercés sur la cible et dans les TUs source, avec des préconditions construites explicitement. Ce n'est ni une validation universelle de GetHeight, ni la preuve d'un callback atteint naturellement en jeu.

## Tracker
- [x] Archives de l'exécution interrompue récupérées sans reset ni réécriture ; véritable verrou exclusif conservé pendant la reprise.
- [x] Callback cible authentifié exécuté jusqu'au retour, puis composition avec registration et consommateur.
- [x] RED comportemental actual-TU sur production avant patch ; GREEN avec le même harness après patch.
- [x] Runtime du filtre RE-780 acquis et runtime du relink avec correction callback relus indépendamment ; captures réellement inspectées.
- [x] Échec UBSan conservé et reproduit séparément sur la baseline : défaut préexistant, non réparé ici.
- [x] RED documentaire : deux échecs attendus avant story/dashboard, à 09:59:20 ; tests inchangés pour GREEN.
- [x] Revue indépendante de publication : PASS borné le 26 septembre à 10:07, review-publication-1003/verdict.json ; refus global UBSan antérieur conservé, aucune validation sanitaire globale.
- [ ] Registration native non validée et effet du callback en gameplay non établi ; équivalence complète bloquée.

## Preuve cible
Sous `build/reverse/autonomy-20260926-morning-coordinator/`, `target-flat-02/` conserve **108 cas / 27 callbacks** : GetHeight et BridgeFlatFloor authentifiés, mêmes données reconstruites à chaque cas, sortie initialisée, callback retournant et sortie consommée. Le premier essai `target-flat-01.log` est un échec de setup conservé, pas un RED comportemental.

`target-chain-01/` conserve **144 cas / 144 callbacks** : une tranche authentique de registration remplace les slots préalablement empoisonnés ; GetHeight appelle ensuite les vrais callbacks, avec ordre, valeurs entrantes et stores contrôlés. `target-caller-01/` conserve **144 cas / 144 callbacks**, avec retour complet UpdateLaraRoom → GetFloor → GetHeight → BridgeFlatFloor et écriture discriminante du champ floor. Les trois objets item sont comparés intégralement dans ce probe. Un appel comportant deux objets peut appeler zéro, un ou deux callbacks selon les inhibitions ; le nombre de callbacks n'est pas celui des cas.

La registration s'exécute à une base de relocation synthétique, sans rejouer toute l'initialisation. Les rooms, triggers et items sont construits ; provenance du payload et tranche SETUP contrôlée séparément. La revue confirme que la tranche n'est pas affectée par la relocation, sans replay complet de celle-ci. Unicorn et l'interpréteur indépendant sont un **modèle logiciel**, pas validation matérielle ni parcours naturel de démarrage.

## Preuve source et correction
La première matrice privée a **216 cas**, RED **32 échecs**, puis zéro échec après correction privée. La matrice publique élargie comporte **288 cas** : trois hauteurs de sol, deux hauteurs pour chacun des deux objets, trois hauteurs de requête, quatre masques d'inhibition et deux consommateurs. Le RED production `production-red-02/` du 09:32:43 rapporte **114 échecs**, exit 1, après compilation et liaison réussies. Le GREEN `production-green-02/` du 09:33:06 rapporte **zéro échec**, exit 0, mêmes fixture et options. Deux ajouts seulement dans GETSTUFF.C ; aucune autre correction moteur.

Le runner `tests/reverse/fixtures/re781/run_test.py` compile GETSTUFF.C, COLLIDE_S.C et OBJECTS.C entiers, avec headers normaux, g++ Linux/i386, PSX_VERSION et PSXPC_TEST, puis liaison normale avec élimination des sections inutilisées, sans autorisation de symboles non résolus. Les sorties couvrent appel direct et vrai UpdateLaraRoom ; le champ floor est initialement distinct et le buffer des trois items est comparé intégralement. Le test public n'est pas un build du jeu complet.

Le slot callback utilise int/int*, tandis que BridgeFlatFloor déclare long/long*. La fixture recourt à un **adaptateur typé** explicite sans cast de pointeur incompatible et sans lecture de l'output indéterminé de la baseline : le vrai corps BridgeFlatFloor travaille sur un temporaire long. L'égalité des tailles i386 ne rend pas ces types identiques. **registration native non validée** : cette fixture ne prouve pas le branchement direct du callback dans le moteur. Les valeurs sont bornées ; ni LP64, ni tous backends, ni tous débordements du retour short ne sont certifiés.

La fixture RE-780 conserve son filtre et ses contrôles, mais attend désormais la propagation de la valeur synthétique lorsque son callback est appelé. Son README qualifie l'ancien contrat historiquement ; les résultats RE-780 publiés ne sont pas réécrits.

## Revue indépendante et UBSan
`review-proof-0945/` contient les exécutions du reviewer interrompu avant rédaction finale : actual-TU courant **288 cas, zéro échec**, baseline **288 cas, 114 échecs**, sorties complètes identiques aux archives production. Ce replay a fait GREEN puis RED ; il ne remplace pas la chronologie TDD d'origine. Son interpréteur distinct retrouve stores et callbacks des trois matrices cible. Pour caller, les traces brutes diffèrent d'une visite de hook par cas : **144 visites supplémentaires** dans l'archive, sans divergence de stores/callbacks ; pas d'identité complète de trace revendiquée.

La clôture indépendante `review-proof-closure-0954/REPORT.md` et `verdict.json` refuse un PASS global. **UBSan exit 1** : décalage à gauche d'une valeur négative dans GetFloor, GETSTUFF.C ligne 338, hors delta callback. L'essai auteur et celui du reviewer échouent réellement ; aucun PASS sanitaire. Le coordinateur a ensuite recompilé la baseline égale à HEAD dans `baseline-ubsan-1000/` et reproduit le même diagnostic, exit 1 : **préexistant**, pas une régression créée par les deux affectations. Le défaut demeure, sans patch spéculatif. La décision de publication bornée doit conserver ce refus et ses limites, non le transformer en GREEN global.

## Runtime acquis — filtre et relink corrigé
Deux archives relues : `build/reverse/autonomy-20260926-runtime/run01/` réutilise le relink du 25 septembre ; `runtime-callback/run01/` utilise GETSTUFF recompilé le 26 septembre et un nouveau relink, avec les 122 autres entrées de link historiques identiques. **pas de fullbuild neuf**. La revue `review-runtime-0945/REPORT.md` conserve **2234 assertions indépendantes** sur archives, pas des tests pytest ni un nouveau runtime reviewer.

Pour chacune : **305 draws**, **90 appels / 90 retours** instrumentés, dont 40 GetHeight. Le témoin atteint ignore les dépendances item/object pour le type non-objet ; le payload terminal suivant est consommé. **callback non exercé dans le témoin**, zéro visite de son callsite : le code corrigé est dans le binaire mais son effet n'est pas validé par cette route. Store floor **0→0 non discriminant**. Hors témoin, les callbacks ne sont pas observés exhaustivement.

Les captures finales montrent Lara dans une ruelle texturée, pas un écran noir ; entrée gameplay puis déplacement observé séparément de la réception SDL. Arrêt volontaire debugger-kill, pas sortie naturelle du jeu. Les deux images restent privées et sont livrées en pièces jointes ; aucun asset public, aucun dump/opcode/pseudocode brut versionné.

## Validation publique
Sélection exacte des 75 tests RE-780 reprise du ledger `build/reverse/autonomy-20260925-publication-0928/suite-final.ledger.json`, augmentée du test actual-TU et des deux contrats documentaires RE-781. Résultat exécuté à 10:01 : **78 tests PASS en 1,58 s pytest**, exit 0, dont un actual-TU RE-781 compilant **288 cas sans échec** et l’actual-TU RE-780 compilant **153 cas sans échec** ; ces cas ne sont pas des tests pytest supplémentaires. Revalidation après inscription conservée séparément. Logs, argv, exits, horaires et hashes avant/après sous `build/reverse/autonomy-20260926-morning-coordinator/publication/`. Les **7 échecs historiques** RE-778 et l'ancien **FAIL fade** restent conservés et non résolus : **pas de GREEN global**, aucune suite globale prétendue verte.

## Handoff actif
Overview actif : callback producteur/consommateur réparé sur la matrice bornée, route native visible sur relink mais callback non exercé dans le témoin. Le dashboard est append-only, ses anciens textes demeurent des snapshots datés. Prochain objectif : attribution de la registration native et atteinte naturelle d'un callback avec consommation sensible ; le défaut UBSan de GetFloor reste une piste séparée à prouver avant correction. Pas de correction ABI ni de décalage signé spéculative dans ce lot. Aucun avancement implicite après l'échéance absolue 10:30 du 26 septembre 2026.
