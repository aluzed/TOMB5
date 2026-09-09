# RE-759 — GetDoor : preuve bornée du décodage floor-data

## Tracker

- [x] Handoff privé, review/verdict.json et review/review.md lus ; publication le 9 septembre 2026 après contrôle à 16:30:51 Europe/Paris, HEAD b1987997.
- [x] Preuve privée existante : 674 cas, vraie TU, parent et Revue indépendante PASS ; aucune nouvelle recherche.
- [x] Test documentaire écrit avant création de cette story et modification du dashboard ; RED observé : 1 échec attendu (story absente), 1 réussite, exit 1, 16:32:08.140654–16:32:08.401904 Paris.
- [x] Publication limitée à cette story, dashboard actif et test documentaire ; aucun patch de production.
- [ ] Équivalence ABI, callers complets, autres backends et gameplay non prouvés.

## Résultat mesuré et hypothèse

PASS de caractérisation bornée : **674 cas = 576 cas de matrice + 98 chaînes**, **642 différences de valeurs promues MAIS 0 différence d’octet**. Les **2 méthodes unittest** privées ne sont pas 674 méthodes de test. **17129 visites de hook**, pas des instructions retirées ; maximum observé 43 visites et 6 lectures par cas.

GetDoor saute au plus un descripteur floor puis un ceiling, respecte END sur les descripteurs sautables, et retourne la destination seulement pour DOOR ; END sur DOOR n’annule pas son ID. Index zéro produit la sentinelle. Matrice : indices 0/1/3, 32 fonctions basses, END absent/présent, destinations 17/128/254 ; chaînes combinant sept types floor et sept ceiling, END ceiling absent/présent. Les contrôles index zéro redondants sont intentionnels.

Cible authentifiée contre le boot extrait indépendamment de l’ISO ; CPU/RAM synthétiques neufs par cas, GP injecté, contrôle des instructions visitées, entrée/retour et SP bornés, aucun callee ou service doublé. Hook interdit toute écriture et vérifie les intervalles de lecture entiers. Comparaison des 2 Mio RAM en direct ; images RAM non archivées : les booléens ne permettent pas de refaire cette comparaison après coup.

La vraie TU SPEC_PSXPC_N/GETSTUFF.C inchangée est fraîchement compilée et exécutée en i386, g++ -m32 -O0, PSX_VERSION=1 et PSXPC_TEST=1, en-têtes normaux, sections inutilisées éliminées sans ignorer les symboles non résolus. Pointeur/long 32 bits et FLOOR_INFO 8 octets vérifiés. Un processus natif traite les 674 appels avec storage et FLOOR_INFO réinitialisés et intégralement contrôlés par appel ; pas de reset CPU natif par ligne ni de comparaison de toute sa mémoire.

## ABI, consumers et limites impératives

La valeur native publiée est la promotion C du char signé retourné, pas EAX brut. Les retours cibles se répartissent en 529 sentinelles 255, 32 valeurs 17, 32 valeurs 128 et 81 valeurs 254 ; les promotions natives correspondantes sont −1, 17, −128 et −2. **Aucune équivalence ABI**, aucune équivalence des traces mémoire, aucun caller complet exécuté, aucune joignabilité complète établie et aucun patch justifié par cette observation.

GetFloor source récupère le retour dans unsigned char ; la slice cible normalise sur 16 bits signés, pas sur 8 bits. Les trois sites d’appel directs inspectés ne sont pas des callers exécutés. Destinations 17/128/254 seulement : **255 est observé comme sentinelle, pas testé comme destination DOOR**. Destinations supérieures à 255 et shorts négatifs exclus ; aucune conclusion sur l’ensemble des room IDs. Autres bits supérieurs des headers, chaînes longues/malformées, indices hors limites, validité réelle des portails et chargement du niveau exclus.

Pas de build jeu complet, pas de sanitizer, autres backends non validés, toolchain/en-têtes système non scellés. Pas de preuve gameplay, sauvegarde, concurrence ou matériel ; snapshots finaux natifs ne prouvent pas l’absence d’écritures transitoires restaurées.

## Attribution et revue indépendante

Archives privées uniquement sous build/reverse/autonomy-20260909/re759. Initial : exit 0, 16:20:48.218694–16:20:52.080114 Paris ; worker-replay : exit 0, 16:22:00.143950–16:22:03.909957. Deux méthodes privées GREEN par passage.

Parent réel parent-01 : **exit 0, 16:24:29.527416–16:24:33.431566 Paris**, ledger parent-01-run.json lu pendant cette publication. Selon les vérifications explicitement transmises par le parent, celui-ci a comparé les résultats complets, byte-identiques à initial, puis relu le verdict indépendant. Ce ne sont pas des exécutions de ce worker de publication ; le handoff producteur antérieur ne revendiquait pas encore ces contrôles ultérieurs.

**Revue indépendante PASS** : review/verdict.json (passed true, security_concerns et logic_errors vides) et review/review.md. Le reviewer a exécuté reviewer-01, exit 0, 16:25:38.035110–16:25:41.818824 Paris : compilation fraîche de la vraie TU, processus natif et 674 appels cibles. Son audit indépendant post-producteur (review/audit-run.json et review/audit-result.json, exit 0) reconstruit la matrice exacte, les retours/promotions et les 674 séquences de lectures sans importer le probe. Fichiers result.json complets byte-identiques entre initial, worker-replay, parent-01 et reviewer-01 ; 344 fichiers préexistants vérifiés sans modification. Ce PASS concerne la preuve privée, pas une revue indépendante de cette nouvelle publication.

Le reviewer a inspecté les archives Ghidra corrigées et décodé indépendamment le binaire, sans relancer Ghidra. La première attribution d’adresse était erronée ; l’inspection corrigée est corroborée par le corps symbolique et l’exécution authentifiée. L’avertissement de chevauchement de delay-slot est conservé, pas masqué. L’inspection native fraîche confirme la promotion signée. Le test producteur ne verrouillait pas à lui seul les 674 lignes exactes : l’audit reviewer les a recomptées pour cette livraison, sans modifier ce test historique.

## Validation publique

Aucun rejeu privé pendant cette publication ; gardes historiques inchangées. Aucun générateur historique exécuté, aucune trace brute ni octet propriétaire publié. RED documentaire et commandes/intervalle/exit/hashes conservés sous publication/red.log, red.json et commands.json ; GREEN sous green.log/green.json, suite publique sous suite.log/suite.json. La sélection est exactement celle de RE-758 augmentée du nouveau test documentaire. Les assertions de limites portent séparément sur cette story et la seule section RE-759 du dashboard.

GREEN documentaire : 2 tests réussis en 0,05 s, exit 0, 16:33:33.399315–16:33:33.646370 Paris. Suite exacte RE-758 augmentée : 1 355 tests réussis en 51,67 s, exit 0, 16:33:33.677576–16:34:25.628956 Paris. Ces passages sont ceux du worker de publication, distincts des 2 méthodes privées et du replay parent/reviewer. Revalidation après insertion de ces résultats enregistrée séparément dans publication/final.json et final.log.

Commande exacte de suite, depuis /var/www/projects/TOMB5 (invocations RED/GREEN/finale également dans publication/commands.json) :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py -q
```

## Handoff

Après RE-759 : caractérisation GetDoor clôturée sans correction ; prochaine hypothèse proposée seulement : **GetFloor, sélection de cellule aux bords et traversée d’un portail**, comparaison du pointeur sélectionné et room_number sur vraie TU/cible, avec floor/ceiling/pit désactivés dans la première borne puis vrais helpers seulement sur extension autorisée. Aucun travail GetFloor effectué ici. L’accord d’octet GetDoor ne prouve pas ce consumer.

La garde privée épingle HEAD/arbre propre/date prépublication : une publication peut intentionnellement empêcher son rejeu. Ne pas modifier, désactiver ou resealer les probes/gardes ; toute future reproduction exige une nouvelle unité de provenance autorisée. Recherche autorisée jusqu’à 23:25 Paris, clôture jusqu’à 23:45 Paris le 9 septembre 2026 ; aucun nouveau job. Au moment de ce handoff de publication : aucun staging, commit ou push ; story et test nouveaux non suivis, livraison au parent. Rapport interdit jamais ouvert ni modifié.
