# RE-766 — GetFloor : preuve multi-sauts bornée, publication metadata-only

## Tracker

- [x] Evidence et attribution examinées avant écriture du test documentaire ; carte privée claims-map.md.
- [x] RED documentaire observé : story absente, contrôle historique déjà réussi.
- [x] Preuve auteur et revue indépendante privée consommées sans nouvelle exécution privée.
- [x] Publication uniquement documentaire ; source de production inchangée, gardes historiques inchangées.
- [x] Revue finale séparée PASS ; réserve initiale levée par authority-closure. Décision de livraison du parent distincte.
- [ ] Preuve sur corpus/consommateur réel et généralisation GetFloor non établies.

## État et overview actif

Après RE-765, la correction verticale intégrée constitue le prédécesseur de cette caractérisation multi-sauts. RE766 ajoute une preuve bornée sur cette production, pas une nouvelle correction. Cet overview actif et le handoff actif se trouvent DANS la nouvelle section RE766 du dashboard ; tous les anciens aperçus, transitions et gates restent des jalons historiques octet pour octet. Au moment de cette clôture documentaire, aucun staging, commit, push ou job effectué ici ; staging et commit restent à effectuer.

## Résultat borné et matrice

PASS privé de caractérisation : 22680 appels cible et autant d’appels natifs, dont 15876 GetFloor et 6804 helpers, sur 36 fixtures ; 22140 entrées distinctes (fixture, mode, input). Zéro n’est pas une extrapolation : zéro divergence de valeurs et zéro divergence d’événements ordonnés sur ce domaine. Les ensembles divergents ont intersection et union nulles, sans addition de compteurs recouvrants.

Géométrie et RAM synthétiques : floor/ceiling, propriétaires ascending/descending/equal, contrôles room-zero 256/1792, portails none/prefix/landing-decoy. Chaque fixture contient 189 contrôles helpers et 441 requêtes GetFloor. Les hauteurs sont liées au scénario, pas un produit cartésien uniforme de toutes les hauteurs. Sauts verticaux observés 0/1/2/3 : floor 2394/1404/1422/2718, ceiling 3276/1350/1332/1980. Les portails préfixes réalisent deux transitions ; le leurre à l’atterrissage vertical n’est pas reconsommé. Le propriétaire courant est discriminé après les premier et deuxième sauts ; les mutants owner/polarity sont des formules, pas des TU mutantes compilées.

## Evidence et attribution

Auteur/producteur puis closer : build/reverse/autonomy-20260911/re766-multihop/HANDOFF.md. Le producteur avait terminé ; le timeout concernait sa clôture CPU. Le closer a complété l’audit CPU et six tests privés, sans relancer le producteur. Le RED privé historique correspondait à six artefacts absents, pas à un contre-exemple comportemental ni à la causalité d’une correction.

Reviewer indépendant délégué : build/reverse/autonomy-20260911/re766-independent-review/review.md, re766-independent-review/verdict.json et re766-independent-review/delivery-verification.json. Verdict lu : passed=true, tableaux bloquants vides. Son replay frais a exécuté la cible authentifiée sous Unicorn, compilé la TU entière SPEC_PSXPC_N/GETSTUFF.C, relancé Ghidra frais, puis six tests privés et les audits auteur après génération. Le reviewer a également écrit reviewer_check.py sans importer l’oracle/producteur : reconstruction des requêtes, décodeur sémantique des buffers, stdout complet, target rows, transitions, appartenance complète du record au propriétaire et baselines. Ce check ne reconstruit pas à lui seul toute la géométrie : l’audit buffers auteur fraîchement rejoué apporte cette étape. Les chaînes d’attribution auteur hardcodées dans ces outils restent historiques ; leur exécution reviewer n’en fait pas du code reviewer.

Le reviewer rapporte 253 fichiers comportementaux producteur/reviewer identiques octet pour octet, 301944 octets de buffers natifs et 75497472 octets de baselines RAM contrôlés. Il compte 3219072 visites de hook, 469008 lectures et 32940 stores cible inférés ; les visites ne sont pas des instructions matériellement retirées. La revue privée n’est pas la revue finale de cette publication. La revue finale initiale re766-final-review a été suspendue à 21:09 pour une réserve d’autorité ; réserve initiale levée après preuve du message parent portant la borne 21:09. Verdict final PASS : build/reverse/autonomy-20260911/re766-final-review/authority-closure/verdict.json ; intégrité : authority-closure/hash-verification.json. Les 79 tests reviewer initiaux et les 2 tests de clôture sont des exécutions reviewer historiques, pas des exécutions parent. Selon la délégation actuelle, le parent a lu ce verdict et hash-verification, sans replay privé ni audit buffers. La suite de 3755 tests reste attribuée à l’auteur. La revalidation documentaire de cette synchronisation est consignée séparément sous re766-publication/closing/final.json et final.log.

Parent : selon le contexte explicite de la délégation actuelle, lecture du HANDOFF, du rapport et du verdict par outils ; pas de replay ni audit parent, aucune comparaison de buffers parent. Aucun intervalle, argv ou exit parent n’est inventé. Publisher : lecture des artefacts ci-dessus et exécution des seuls tests publics consignés ici ; aucun rejeu privé ni reconstruction des buffers privés pendant cette publication.

## Configuration et limites

Configuration exécutée par la preuve privée : g++ -m32 -O0, ELF32, PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Assertions ABI, dépendances séparées par TU, link sans suppression de symboles non résolus et retour natif normal dans le harness ; pas un build complet du jeu. Ce gate est une configuration, pas une architecture validée universellement. GetDoor reste unsigned char côté natif contre normalisation 16 bits cible : les petites destinations de cette matrice masquent cette question générale. Sentinelle de lien absent n’est pas destination valide couverte.

Limites : pas de corpus chargé par le loader dans RE766, aucun caller réel, pas de gameplay, matériel, cache/MMIO/pipeline ou concurrence. Le CPU supplémentaire est un modèle logiciel, pas un oracle matériel. Pas de cycles, grandes destinations ou preuve de toutes les branches de clamp. Côté natif, comparaison mémoire après chaque appel, mais seul le buffer final est archivé ; pas de trace exhaustive des écritures transitoires. Stores cible inférés au hook et validés par RAM finale/interpréteur. Instrumentation aux frontières de fonctions. Il n’y a pas de sanitizer ni de variantes d’optimisation ; les décalages signés ne fondent pas une preuve portable du langage. Toolchain et headers système non intégralement scellés.

Les gardes historiques inchangées incluent HEAD épinglé et git diff HEAD propre, assertions, pins et fenêtre privée 20:38–21:10 le 11 septembre 2026 Europe/Paris. La publication peut légitimement faire refuser cet arbre : ne pas affaiblir la garde et ne pas promettre de replay après 21:10. La délégation initiale de publication était bornée à 21:09 : borne désormais historique, sans renouveler la garde privée. La présente clôture documentaire est autorisée par la nouvelle délégation, dans la fenêtre utilisateur jusqu’à 22h.

## Tests publics et archives

Archives ignorées : build/reverse/autonomy-20260911/re766-publication/ ; red.log/json, green.log/json, suite.log/json et final.log/json enregistrent argv, cwd, environnement, début/fin, durée monotone, exit et hashes avant/après. Le nouveau test ne lit aucune preuve privée, n’importe aucun producteur et ne lance aucun probe. Il teste les qualifications de la story ET de la seule section RE766, ainsi que la restauration exacte du dashboard au HEAD prédécesseur.

RED documentaire observé le 11 septembre 2026 : 21:03:01.661413–21:03:02.023033 +02, exit 1, un échec attendu (story absente) et un test réussi en 0,07 s pytest ; durée processus 0,361093 s. GREEN documentaire : 2 tests réussis en 0,06 s pytest, exit 0, 21:04:17.470472–21:04:17.726955 +02 (0,256047 s processus). Suite publique exacte de la story RE765 augmentée du seul test RE766 : 3755 tests réussis en 58,73 s pytest, exit 0, 21:04:21.932092–21:05:21.030774 +02 (59,098231 s processus). Test identique entre RED et GREEN. Ces résultats sont insérés après leur exécution ; la revalidation documentaire finale du texte est enregistrée séparément dans final.json et final.log, sans prétendre à une seconde suite complète.

## Commande publique exacte

Depuis /var/www/projects/TOMB5, avec PYTHONDONTWRITEBYTECODE=1 :

```sh
python3 -B -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py tests/reverse/test_re765_vertical_integration_publication.py tests/reverse/test_re766_multihop_publication.py -q -p no:cacheprovider --basetemp /var/www/projects/TOMB5/build/reverse/autonomy-20260911/re766-publication/suite-tmp
```

La sélection est celle de RE765, avec uniquement tests/reverse/test_re766_multihop_publication.py ajouté ; cache pytest désactivé et basetemp neuf sous les archives de publication.

## Handoff

Après RE-766 : preuve multi-sauts synthétique close et publication metadata-only ; revue finale séparée PASS, réserve initiale levée ; parent ayant lu verdict et hash-verification selon la délégation de clôture. Au moment de cette clôture, staging et commit non effectués. Prochaine recherche proposée, non commencée : délimiter une preuve sur un corpus authentifié et un consommateur réel GetFloor, avec entrée du caller, propriétaire/cellule retournés, événements et frontière de retour explicitement bornés. Cela relie la matrice multi-sauts aux données ou appels réels au lieu de répéter une matrice synthétique ; aucune reachability n’est présumée. Aucun nouveau ticket ouvert, aucune correction ni nouvelle recherche lancée ici. La largeur générale GetDoor et GetFloor universel restent hors preuve.
