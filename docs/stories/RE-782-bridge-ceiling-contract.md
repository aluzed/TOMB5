# RE-782 — Contrat des trois plafonds de pont

27 septembre 2026, Europe/Paris. Suite de RE-781 : la recherche de registration native découvre un producteur absent, puis trois corps ceiling incorrects. Correction bornée de BridgeFlatCeiling, BridgeTilt1Ceiling et BridgeTilt2Ceiling ; aucune activation des callbacks dans le moteur.

## Tracker
- [x] Verrou exclusif conservé, chaîne RE-781 et règles lues ; rapport utilisateur non suivi préservé sans ouverture.
- [x] Ghidra neuf et vraie TU SETUP : registration absente dans ObjectObjects natif, indépendamment du problème int/long.
- [x] Six corps cible authentifiés exécutés, vraie TU OBJECTS.C comparée : trois floors concordants, trois ceilings divergents.
- [x] Test public actual-TU RED avant modification ; correction privée, mêmes tests GREEN ; Revue indépendante favorable au delta borné.
- [x] Delta examiné intégré à OBJECTS.C, identité octet/hash avec la copie approuvée, compilation et GREEN production exécutés.
- [x] RED documentaire observé avant story/dashboard ; historique du dashboard conservé append-only.
- [ ] Registration, ABI exacte et consommateur GetCeiling non réparés ; aucun effet gameplay validé.

## Producteur natif et ABI
Le dossier privé `build/reverse/autonomy-20260927-midnight/abi-research/` conserve la compilation fraîche de SETUP.C entier, son préprocesseur et son désassemblage. ObjectObjects actif contient un préfixe Lara et un signalement d'incomplétude ; la registration bridge n'est pas compilée. Un harness normalement lié effectue **deux appels**, loaded absent/présent, avec les trois entrées bridge empoisonnées : **six attentes échouent**, exit 1, après compilation et lien réussis. Ce test ne vérifie pas encore les identités précises des six callbacks : ce n'est pas un GREEN suffisant d'une future restauration.

Le test d'affectation directe reproduit l'incompatibilité **int/long** : compilation stricte exit 1, permissive exit 0 avec avertissement. Des tailles i386 égales ne rendent pas les types C++ compatibles. Aucun appel via un type incompatible n'a été effectué.

L'import **Ghidra** neuf du module SETUP authentifié termine avec exit 0 et marqueur de fin. Le préfixe cible ObjectObjects, depuis son entrée jusqu'après la registration des trois bridges, réussit pour les deux états loaded : **148 visites et 46 stores par cas**, RAM complète comparée ; six slots et mip sont installés inconditionnellement. Arrêt avant la suite de la fonction : ni retour complet ObjectObjects ni startup naturel. Placement du module et RAM construits, **modèle logiciel**, pas console matérielle.

`abi-review/` réexécute compilation, cible et Ghidra, reconstruit la relocation depuis les quinze copies du conteneur et produit **45 contrôles sans échec**. Son premier audit **44 contrôles / un échec** est conservé : deux mots du préfixe sont relocalisés ; seule la tranche registration est inchangée. Les trois replays reviewer sont des répétitions des deux cas, pas six cas distincts.

## Six corps et correction attribuée
`bridge-bodies/` extrait fraîchement l'exécutable du disque, vérifie son hash, puis exécute les six routines authentifiées et GetOffset pour les versions inclinées. CPU/RAM frais, instruction et retour bornés, contrôles de stores et comparaison complète de RAM. La vraie TU OBJECTS.C est compilée et liée i386 avec ses headers normaux, sans symbole non résolu autorisé. Appels directs selon la signature long, pas de registration synthétique dissimulée.

La matrice compte **1260 cas** : six callbacks, cinq rotations, sept positions, deux altitudes et trois côtés du seuil. **630 floors concordent ; 630 ceilings divergent.** Ce ne sont pas 1260 tests pytest. La cible écrit la hauteur de surface augmentée de **256** uniquement lorsque la requête est strictement supérieure à la surface : **égalité exclue**. FlatCeiling avait le mauvais prédicat ; les deux TiltCeiling avaient aussi omis l'addition 256. Les floors et GetOffset ne changent pas.

Le test public `tests/reverse/fixtures/re782/bridge_contract.cpp` contrôle sortie, canaris adjacents, item entier et globals. Le premier essai échoue à compiler faute d'un include, conservé comme incident de setup, non RED comportemental. `coordinator/public-red02.json` enregistre ensuite compilation/lien réussis et **1260 cas / 630 échecs**, exit 1, avant patch. `private-green` puis `production-green` recompilent la TU entière avec le **même harness** : **zéro échec**, exit 0. La correction est limitée à **PSX_VERSION && PSXPC_TEST**, testée avec g++ Linux/i386. La branche legacy est conservée, sans validation des autres configurations ni LP64.

## Revue indépendante et limites sanitaires
`bridge-review/verdict.json` accorde un PASS borné, listes de défauts et de préoccupations de sécurité vides. Le reviewer refait RED et GREEN, extrait et décode indépendamment les instructions, puis exécute une seconde implémentation du probe sur les **1260 cas**, avec nouvelles adresses synthétiques et RAM complète. Même logiciel d'émulation, pas oracle matériel indépendant. Il vérifie aussi l'identité des floors/GetOffset et la restitution textuelle exacte de la branche legacy.

**UBSan** sur la copie privée corrigée : 1260 cas, zéro échec, exit 0 et stderr vide dans cette revue. Cela ne résout pas le décalage signé préexistant de **GetFloor** dans RE-781 ; pas de validation générale des overflow/INT_MIN ni du moteur. Les anciens échecs RE-778 et FAIL fade restent historiques : **pas de GREEN global**.

## Validation publique et contrôle coordinateur
La sélection exacte de `publication/suite-final.json` du prédécesseur RE-781 est reprise sans retirer de test, avec les trois nouveaux tests RE-782 : **81 tests PASS en 1,88 s**, exit 0, ledger `coordinator/suite-green.json`. Le coordinateur a comparé les 1260 sorties natives production aux résultats cible archivés et vérifié l'identité des fixtures entre RED et GREEN ; il n'a pas exécuté lui-même un nouveau replay cible. Guards assets/secrets/metadata et diff-check réussis. Le test documentaire a fait deux échecs attendus avant écriture, puis trois tests ciblés PASS avec l'actual-TU. La revue de publication finale `publication-review/verdict.json`, le 27 septembre à 23:33, accorde un PASS borné : 36 contrôles et trois tests RE-782 fraîchement réussis. Elle vérifie les deux suites archivées de 81 tests sans prétendre les réexécuter, maintient le NO-GO registration/gameplay et autorise uniquement l'inscription de ce statut après revue.

## Source, runtime et Handoff actif
Correction source intégrée et test isolé compilé : oui. **pas de runtime jeu**, pas de relink/fullbuild ni de nouvelle capture revendiqués dans cette unité. Le fonctionnement naturel des ponts n'est pas validé.

**Handoff actif : ne pas activer la registration.** Trois obstacles distincts : producteur ObjectObjects manquant, types callback int/long incompatibles, et **GetCeiling** source transmettant **NULL** comme output. Cette dernière observation est fondée ici sur lecture du code, pas une preuve complète de consommation cible. La recherche consommateur séparée et la piste sanitizer ont été interrompues par le fournisseur ; leurs fichiers partiels restent privés et ne valent pas validation. Prochaine unité cohérente : établir puis corriger le contrat output de GetCeiling et composer registration typée, vrais callbacks et consommation sensible avant toute activation. Pas de réactivation globale du grand bloc désactivé ni de patch ABI spéculatif.

Les preuves brutes, exécutables, journaux et échecs restent ignorés sous `build/reverse/autonomy-20260927-midnight/`. La publication ne contient ni assets ni dumps propriétaires. L'autonomie actuelle expire au 28 septembre à minuit Europe/Paris ; aucune activité ultérieure implicitement autorisée.
