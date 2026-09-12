# RE-769 — UpdateLaraRoom : préfixe caller et arguments GetHeight

## Tracker

- [x] Preuve producteur et revue privée lues ; attribution séparée.
- [x] RED documentaire observé avant cette publication metadata-only.
- [x] source de production inchangée ; code_change_readiness=blocked.
- [x] revue finale de publication PASS au 12 septembre 2026 à 18:06 Europe/Paris, distincte du PASS privé.
- [ ] Préconditions du caller et vrai consommateur non établis.

## État et overview actif

Après RE-768, RE769 exécute le caller authentique UpdateLaraRoom depuis son entrée avec GetFloor et ses helpers réels, jusqu’au stop à l’entrée GetHeight. Cet overview actif et le handoff actif sont DANS la seule nouvelle section RE769 ; retrait de cette section restaure le prédécesseur byte-exact, fermetures comprises. Livraison documentaire interne avant 18:04 le 12 septembre 2026 Europe/Paris ; limite utilisateur 18:45, clôture dès 18:30. Au snapshot de publication avant revue, aucun staging, commit, push ou job lancé.

## Résultat borné

PASS privé borné de caractérisation : deux contrôles alias/non-alias de item et lara_item, une divergence x/z des arguments GetHeight dans le contrôle non-alias ; contrôle alias égal. La cible utilise les coordonnées de item, le natif celles de lara_item pour x/z. Zéro différence n’est revendiquée pour le consommateur : zéro divergence GetFloor concerne uniquement arguments, room, record retourné et cinq événements ordonnés par cas, door → portal → door → floor → pit. Ces événements ne sont pas des appels supplémentaires.

Les arguments construits reposent sur le corpus authentifié, mais l’état initial des items est synthétique. Les deux exécutions ont le même état cible pertinent ; seule l’association lara_item varie côté natif : pas deux scénarios cible distincts. Le préfixe caller est réellement exécuté ; ses propres callers et préconditions alias/caller ne le sont pas. non-alias atteignable en jeu non établi ; pas de gameplay, pas de matériel, pas d’équivalence universelle ni justification de patch.

Le record GetFloor est passé comme premier argument GetHeight ; aucune instruction de GetHeight n’est exécutée. Donc pas de lecture du record par ce consommateur, pas de hauteur finale, pas de store item.floor, pas d’ItemNewRoom exécuté et pas de retour complet UpdateLaraRoom. Le wrapper GetHeight capture puis lève une exception, sans retour synthétique exploité comme résultat. ItemNewRoom : appel intra-TU non intercepté par le wrap, situé après le stop ; ne pas prolonger ce harness sans résoudre sa vraie sémantique.

## Preuve consommée et attribution

Producteur : build/reverse/autonomy-20260912/re769-proof/HANDOFF.md ; livraison worker-sealed et son outer ledger. Le producteur a subi un timeout après HANDOFF. final-verification.json absent : lacune historique réelle, clôture producteur non démontrée, pas un échec de la caractérisation. Le producteur non réparé reste historique ; aucune clôture finale producteur n’est attribuée. Les échecs privés de contrat absent et de link initial ne sont pas un RED de correction comportementale ; les répétitions auteur ne sont pas une revue indépendante.

Revue privée : build/reverse/autonomy-20260912/re769-review/rapport.md, build/reverse/autonomy-20260912/re769-review/verdict.json et build/reverse/autonomy-20260912/re769-review/postreport-verification.json. Nouveau passed=true reviewer avec réserves non vides dans security_concerns et logic_errors : limites du préfixe, consommateur non exécuté, non-alias construit, lacune de clôture producteur et divergence caractérisée. Ce PASS repose sur vérifications reviewer fraîches, non sur le fichier absent. Vérification postrapport lue : 17:52:46.128958–17:52:46.285357 +02, passed=true, 275 fichiers vérifiés et 218 originaux proof préservés ; absence producteur toujours constatée.

Selon le rapport, replay reviewer indépendant du runner inchangé : 17:46:45.932840–17:46:51.363318 +02, exit 0. Dix invocations internes, dont Ghidra frais, recompilation des TU entières SPEC_PSXPC_N/COLLIDE_S.C et SPEC_PSXPC_N/GETSTUFF.C avec harness, lien complet, inspection native, deux processus natifs, deux méthodes unittest et audit auteur après génération. Dix invocations ne sont pas dix tests. Les libellés auteur internes aux ledgers restent historiques ; l’acteur de cette invocation est établi par l’outer ledger reviewer. Les 11 fichiers comportementaux sélectionnés sont byte-identiques au worker-sealed, pas seulement égaux en compteurs.

Le contrôle propre utilise un interpréteur reviewer indépendant sans import du producteur ni Unicorn. Il reconstruit la RAM initiale, exécute le suffixe loader et le préfixe caller/helpers avec branches et delay slots ; les valeurs des stores sont recalculées depuis les registres, non copiées du journal auteur. Comparaisons intégrales : rooms 521688 octets, RAM cible avant/après 2097152 octets par cas et deux items totalisant 288 octets, plus traces, lectures, stores calculés, événements et logs natifs parsés. RAM/stack native complète non comparée. L’audit auteur rejoué reste distinct et prenait les valeurs des stores dans le journal. Modèle logiciel borné, pas un oracle matériel ni une émulation PSX complète.

Parent : selon le contexte explicite de la délégation actuelle, lecture via outils du proof/HANDOFF, rapport, verdict et postreport, hashes rapport/verdict/manifest vérifiés à 17:53:23+02 ; aucun replay privé ni audit buffers parent dans ce tick. Rien de plus n’est attribué au parent. Le publisher lit les preuves nommées et exécute seulement les tests publics archivés ; aucun rejeu privé ni audit des buffers privés. La revue finale de publication PASS au 12 septembre 2026 à 18:06 Europe/Paris reste distincte du PASS privé.

## Exécution et limites

Par cas, le journal producteur compte 235 visites authentifiées du préfixe, 36 lectures, six stores inférés et cinq événements, plus la visite du stop non exécuté : pas des instructions retirées ni des watchpoints matériel. Le reviewer reconstruit séparément 235 instructions de son modèle par cas et 59799 pour le suffixe loader. CPU/RAM restaurés entre cas ; pas de preuve d’absence de toutes écritures transitoires natives. La relocation historique est épinglée mais non réexécutée ; le suffixe loader n’est pas un boot ou loader complet. Attribution Ghidra par chaîne d’appels et champs symboliques, non par le seul commentaire source initial non attribuable ; import frais -noanalysis et post-script ciblé, pas analyse automatique globale.

Configuration privée bornée : ELF32, g++ -m32 -O0 ; instrumentation des frontières de fonctions sur GETSTUFF.C, lien sans suppression des symboles non résolus, dépendances séparées par TU. Headers système et compilateur non épinglés, pas de sanitizer, pas de build complet, pas toutes architectures/optimisations, pas de pipeline/load-delay/cache ou concurrence validés. Les petites destinations communes ne prouvent pas la largeur universelle GetDoor ni les conversions caller.

source de production inchangée ; code_change_readiness=blocked. Les gardes historiques inchangées exigent HEAD épinglé, diff HEAD propre, assertions, pins et label neuf ; latest start 18:05, vérification bornée 18:12. La publication modifie l’arbre suivi : ne pas rejouer ni contourner ces gardes. La fenêtre utilisateur ne les renouvelle pas ; toute extension exige autorisation et provenance nouvelles.

## Tests publics et archives

Archives ignorées : build/reverse/autonomy-20260912/re769-publication/ ; red.log, green.log, suite.log et ledgers JSON avec commande exacte, cwd, environnement, début/fin, exit, durée monotone et hashes avant/après immédiatement persistés. Le contrat documentaire ne lit aucune preuve privée : il qualifie la story ET la seule section RE769, et restaure l’historique byte-exact. Les assertions de texte ne démontrent pas elles-mêmes la preuve privée.

RED documentaire constaté : 17:56:01.551968–17:56:01.819152 +02, exit 1, un échec attendu pour story absente et un test historique réussi en 0,08 s pytest. GREEN constaté : 17:57:30.517345–17:57:30.771031 +02, exit 0, 2 tests réussis en 0,06 s pytest. Suite publique exacte RE768 avec le seul test RE769 ajouté : 17:57:40.061224–17:58:39.244517 +02, exit 0, 3761 tests réussis en 58,81 s pytest (59,183314 s processus). Test byte-identique entre RED et GREEN. Résultats inscrits après exécution ; la revalidation documentaire après inscription est distincte, sans seconde suite complète ni nouveau replay privé.

Revalidation documentaire après inscription : postresults.json et postresults.log constatent 85 tests réussis en 1,28 s pytest, exit 0, 17:59:16.442212–17:59:17.962372 +02. Ce résultat précède sa présente inscription et ne constitue pas une revue finale indépendante de publication.

## Commande publique exacte

Depuis /var/www/projects/TOMB5, PYTHONDONTWRITEBYTECODE=1 :

```sh
python3 -B -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py tests/reverse/test_re765_vertical_integration_publication.py tests/reverse/test_re766_multihop_publication.py tests/reverse/test_re767_corpus_composition_publication.py tests/reverse/test_re768_corpus_negative_triangle_publication.py tests/reverse/test_re769_updatelararoom_publication.py -q -p no:cacheprovider --basetemp /var/www/projects/TOMB5/build/reverse/autonomy-20260912/re769-publication/suite-tmp
```

Sélection littérale de la story RE768, seul tests/reverse/test_re769_updatelararoom_publication.py ajouté et basetemp neuf sous re769-publication. La revalidation documentaire utilise cette sélection sans tests/emulator, avec un autre basetemp neuf.

## Handoff

Après RE-769 : caractérisation privée bornée PASS, source inchangée, publication metadata-only ; revue finale de publication PASS au 12 septembre 2026 à 18:06 Europe/Paris, distincte du PASS privé. Prochaine recherche proposée, non commencée : établir les préconditions alias/caller d’UpdateLaraRoom puis poursuivre le vrai GetHeight et l’usage item.floor sur un état cohérent. Ce handoff ne lance ni n’autorise seul cette recherche ; ni gonflement de matrice RE768 ni patch justifié.
