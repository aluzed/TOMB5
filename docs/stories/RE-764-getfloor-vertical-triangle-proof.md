# RE-764 — GetFloor vertical et helpers triangles : divergence caractérisée

## Tracker

- [x] Carte factuelle et attributions examinées avant le RED documentaire.
- [x] RED documentaire observé : story absente ; un échec attendu et un contrôle historique réussi.
- [x] Preuve privée déjà vérifiée, revue indépendante et clarification PASS lues ; vérification parent attribuée séparément.
- [x] Caractérisation publiée sans changement source ; équivalence réfutée.
- [ ] Nouvelle preuve corrective privée bornée ; aucune intégration production dans cette publication.

## Résultats et portée de la matrice

PASS de caractérisation, équivalence réfutée : 15 niveaux (entrées 2–16), 2704 rooms et 91444 cellules stockées, pas autant de requêtes exécutées. 615 appels de helpers : zéro différence de valeur ou d’événements. Sur 1605 requêtes verticales, 172 cas divergents pour la paire finale (room, offset) et 172 pour les événements ; intersection = union = 172, pas 344 cas distincts. Par niveau : 10 → 32, 12 → 50, 14 → 50, 16 → 40 ; zéro dans les onze autres. Catégories floor sélectionnées : 11 → 80, 12 → 17, 13 → 51, 14 → 24 ; ce classement n’est pas une décomposition causale exhaustive.

Transitions pit cible/natif : 498/476 ; sky : 114/114 ; aucune transition portail. Ces totaux d’événements ne comptent pas les cas divergents. Les 37169 occurrences de catégories éligibles ne sont ni des cellules uniques ni des appels. Un représentant par catégorie, cinq couples de coordonnées locales et des hauteurs voisines des seuils constituent une matrice représentative non exhaustive ; son ordre et sa déduplication intra-niveau ont été reconstruits par le reviewer. Les tests privés n’imposent pas les cardinalités exactes : l’audit indépendant ferme cette lacune pour les artefacts actuels, pas pour toutes les régressions futures.

## Branche attribuée, sans correction

Sur le chemin de helper négatif, cible : y < current-room minfloor ; source/native : y >= room-zero minfloor. Le reviewer recoupe mots cibles authentifiés, branche et delay slot, seconde interprétation et désassemblage natif frais de GetFloor. Le mauvais propriétaire du minimum et le sens opposé du seuil sont un écart concret, pas seulement une assertion du modèle de fixtures. Aucun correctif effectué. GetDoor natif réduit le retour à un octet, tandis que son caller cible normalise sur 16 bits signés ; cette matrice sans portail n’établit aucune équivalence du domaine portail.

Le rejeu reviewer comprend Ghidra frais, compilation de la vraie SPEC_PSXPC_N/GETSTUFF.C et quinze processus natifs. Configuration native 32 bits O0, non-PIE, instrumentation -finstrument-functions : pas un sanitizer. ABI et dépendances projet contrôlées ; lien normal sans suppression des symboles non résolus. La configuration et les décalages signés observés ne prouvent pas la portabilité C++ ni toutes les optimisations/ABI.

## Audits et limites

Le reviewer reconstruit depuis l’ISO les quinze headers, buffers complets, relocations, fixups, images RAM initiales et matrice ordonnée, sans importer l’oracle producteur. Son second interpréteur logiciel reproduit 2220 retours, 199359 pas, 27269 lectures ordonnées avec leurs octets et 612 stores de room, ainsi que les événements/traces. C’est un second modèle logiciel, pas un oracle matériel ; il ne réexécute pas indépendamment le préfixe loader. Les 665499 visites loader et les visites de hooks ne sont pas des instructions matériellement retirées.

Appels directs synthétiques après un suffixe loader borné, corpus authentique mais coordonnées, hauteurs et placements RAM construits ; CPU/RAM réinitialisés par cas. Le producteur contrôle la RAM complète hormis le résultat room permis ; le reviewer reconstruit les images initiales et digests finaux attendus, mais pas de dumps RAM complets par appel archivés. Les lectures cibles bornées et le second interpréteur n’établissent pas une sûreté machine générale, les interruptions, MMIO ou le pipeline load-delay MIPS-I matériel.

Le natif observe les transitions aux frontières de fonctions : pas de trace native exhaustive des écritures, notamment transitoires ou redondantes. Égalité des buffers chargés complets, pas de toutes les allocations ni de la pile. Pas de preuve gameplay, boot complet, rendu, concurrence ou matériel ; pas de validation ASan/UBSan nouvelle. Aucune portée universelle ni exhaustivité du corpus revendiquée.

## Provenance et acteurs

Toutes les pièces privées citées sont sous build/reverse/autonomy-20260909/re764. HANDOFF.md clôt le producteur après timeout : exécution initiale terminée avec trois tests, puis audit de clôture ; ce n’était ni la revue indépendante ni la vérification parent. Le RED privé historique était un manque d’artefact, pas un RED comportemental d’équivalence.

La revue indépendante est documentée par review/report.md : run.py reviewer, 20:54:11.121981–20:54:28.227650 Paris le 9 septembre 2026, exit 0 et 3 tests privés ; puis review/audit.py et review/cpu_audit.py. Le verdict original invalide conservé mélangeait réserves et tableaux bloquants. Le verdict consommé explicitement est review/clarification.json : passed=true, tableaux bloquants vides, limites maintenues. Cette clarification n’a exécuté ni nouveau replay, ni compilation, ni audit comportemental ; son PASS valide la caractérisation, jamais la conformité production.

Selon la commande explicitement transmise par le parent, celui-ci a exécuté python3 -B build/reverse/autonomy-20260909/re764/run.py parent. parent/run-invocation.json mesure le moteur enfant, 21:02:25.753374–21:02:43.708125 Paris, exit 0 ; parent/tests.log confirme 3 tests privés. Ce n’est pas l’intervalle mesuré du wrapper complet. Le parent a lu rapport et clarification puis comparé 151 fichiers comportementaux complets à ceux du reviewer : identité octet par octet, parent-comparison.json, 21:02:57.746442–21:02:57.866615 Paris. Le parent n’a pas relancé l’audit indépendant du reviewer : cette identité de fichiers n’est pas l’exécution de son décodeur ni une reconstruction ISO par le parent.

## Publication publique

Périmètre : aucun rejeu privé pendant cette publication ; source de production inchangée et gardes historiques inchangées. La garde HEAD prépublication et arbre suivi propre pourra légitimement refuser le nouvel arbre : ne pas la contourner. Aucun asset ni preuve privée n’est ouvert par le nouveau test documentaire ; les assertions vérifient la publication, pas la réalité de l’expérience privée. Archives : publication/claims-map.md avant RED, publication/red.log, publication/green.log et publication/suite.log, avec ledgers JSON homologues (commandes, cwd, heures, exits et hashes). Résultats observés le 9 septembre 2026 (Paris) : RED documentaire 21:05:17.675159–21:05:17.940403, exit 1, un échec attendu et un test réussi en 0,07 s ; GREEN 21:06:57.928085–21:06:58.180139, exit 0, 2 tests réussis en 0,06 s. Suite littérale RE763 augmentée du seul test RE764 : 21:06:58.209407–21:07:55.126767, exit 0, 3098 tests réussis en 56,51 s. Test identique entre RED et GREEN. Ces résultats précèdent leur insertion ; la revalidation finale après insertion est consignée séparément dans publication/final.json et publication/final.log, sans prétendre à une nouvelle suite complète.

Le dashboard ajoute une section active RE764 avec son état et son prochain handoff ; les aperçus et transitions RE763 et antérieurs restent historiques, octet pour octet. Cette disposition respecte aussi le contrat documentaire historique de restauration intégrale, sans affaiblir ses tests. Aucun staging, commit, push ou job pendant cette publication ; exactement trois fichiers publics livrés.

## Commande publique exacte

Sélection littérale RE763, ajout du seul nouveau test, cwd /var/www/projects/TOMB5 :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py -q
```

## Handoff

Après RE-764 : prochaine proposition bornée, RED comportemental sur la vraie TU inchangée puis correction privée de cette branche, avec témoins séparant current-room et room-zero, seuils inférieur, égal et supérieur, helper négatif et contrôles des autres branches. Préserver corpus, sorties complètes, événements et provenance ; vérifier la correction par revue indépendante avant toute proposition d’intégration. Limite : pas de passage en production ici ; cette publication ne lance pas la preuve suivante. La largeur GetDoor n’est pas rouverte par une matrice sans portail.
