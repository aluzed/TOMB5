# RE-768 — GetFloor : portail puis triangle négatif sur corpus authentifié

## Tracker

- [x] Preuve et revue privée lues, attribution explicitée avant RED documentaire.
- [x] RED documentaire observé : story absente ; restauration historique déjà réussie.
- [x] Publication metadata-only, source de production inchangée ; code_change_readiness=blocked.
- [x] revue finale de publication PASS au 12 septembre 2026 à 17:26 Europe/Paris, distincte du PASS privé.
- [ ] Aucun caller réel ni portée gameplay démontrés par cette unité.

## État et overview actif

État actif au 12 septembre 2026, Europe/Paris. Après RE-767, dont l'arrivée portail avait un index nul et ne couvrait aucun triangle négatif, RE768 apporte une preuve nouvelle du prédicat négatif après portail. Cet overview actif et le handoff actif sont DANS la nouvelle section RE768 du dashboard ; toutes les sections antérieures et les fermetures HTML restent identiques. La limite utilisateur 18:45 et la livraison interne avant 17:24 sont fournies dans la délégation actuelle ; elles ne modifient pas la garde privée 17:40. Aucun staging, commit, push ou job effectué pendant cette publication.

## Résultat borné et nouveauté

PASS privé borné : six appels directs GetFloor depuis l'entrée corpus 10, zéro divergence de la paire finale (room, cellule) et zéro divergence des événements ordonnés entre cible et vraie production actuelle. Deux coordonnées et trois hauteurs below/equal/above du seuil de room 15 : trois négatifs et trois positifs. Chaque appel franchit le portail 7 → 15 et atteint l'index floor-data 891, type 11 non nul. Pour le négatif : arrêt sous le seuil, deux transitions pit vers room 19 à égalité et au-dessus ; aucun pit dans les contrôles positifs. Six événements portail et deux événements pit ne sont pas huit appels supplémentaires. Les ensembles divergents de résultats et événements ont intersection et union nulles.

Le corpus comporte 243 rooms, 5824 cellules stockées et un buffer complet de 521688 octets. Les entrées et l'état CPU/RAM sont des arguments construits sur données authentiques, pas des entrées d'un caller exécuté : aucun caller réel, pas de gameplay, pas de matériel PSX ni d'atteignabilité en jeu établis. Échantillon non exhaustif. La recherche antérieure de 62560 requêtes géométriques, 251 coordonnées négatives et 1004 requêtes du modèle floor n'est pas rejouée ici ; ce ne sont pas des appels cible. Les autres types triangle, sky, cycles, multi-pit et destinations hors domaine commun restent exclus.

Les IDs room 7/15/19 sont dans le domaine commun des conversions ; GetDoor fournit 255 comme sentinelle d'absence, pas une destination explicite 255 ni supérieure à 255. Le natif convertit par unsigned char ; la cible normalise en signé 16 bits. Aucune équivalence universelle des conversions ou de l'ABI étroite n'en découle. Le seuil appartient à la room courante d'arrivée, non à room zéro ; les cas négatifs couvrent l'égalité et les deux côtés sans justifier un nouveau patch sur la source déjà corrigée.

## Preuve consommée et attribution

Preuve auteur/récupérateur : build/reverse/autonomy-20260912/re768-proof/HANDOFF.md et build/reverse/autonomy-20260912/re768-proof/COMMANDS.md. La récupération a clos audit et runner scellé sans correction de TU ; ses RED historiques portaient sur contrats/API ou audit manquant, pas sur une nouvelle correction comportementale. L'ancien contrôle optimisé défaillant reste archivé ; seul run768sealed.py est le runner final, avec refus explicite des assertions désactivées et labels réutilisés. Ces faits sont lus, non rejoués par le publisher.

Revue privée : build/reverse/autonomy-20260912/re768-review/rapport.md, build/reverse/autonomy-20260912/re768-review/verdict.json et build/reverse/autonomy-20260912/re768-review/post-report-verification.json. Verdict privé lu : passed=true, security_concerns et logic_errors vides ; vérification postrapport datée du 12 septembre 2026, 17:12:44.211914–17:12:46.180360 +02. Selon le rapport, le reviewer distinct a rejoué le runner final de 17:05:28.896516 à 17:05:37.133126 +02, exit 0, puis ses contrôles propres. Les libellés worker dans les ledgers scellés ne certifient pas l'acteur actuel.

Le reviewer rapporte Ghidra frais et recompilation de la TU entière SPEC_PSXPC_N/GETSTUFF.C et du harness, puis 12 méthodes unittest après génération : sept proof, trois discovery API sans nouvelle recherche et deux audit. L'audit du récupérateur a ensuite été exécuté explicitement ; il reste distinct du nouvel interpréteur indépendant du reviewer. Les 18 fichiers comportementaux comparés avec l'initial sont intégralement identiques, pas seulement égaux en compteurs.

Le nouveau décodeur/interpréteur indépendant reconstruit séparément relocation, buffer loader/natif de 521688 octets, baseline de 2097152 octets et six images RAM finales de 2097152 octets chacune ; comparaison complète avec longueurs, entrées/stdout natifs complets, records retournés contenus dans leurs tables propriétaires. Sans import du modèle/producteur et sans Unicorn, il reconstruit l'ordre des lectures, événements, stores et visites de la petite tranche cible. Trois contrôles de corruption RAM/stdout/ordre des lectures sont rejetés, séparément des 12 méthodes unittest. C'est une indépendance méthodologique logicielle, pas une émulation PSX complète ni un oracle matériel ; les instructions du suffixe loader ne sont pas toutes réinterprétées indépendamment.

Parent : selon le contexte explicite de la délégation actuelle, lecture via outils du HANDOFF, rapport, verdict et postreport, vérification des hashes rapport/verdict/delivery-hashes et du JSON verdict à 17:13:41, avec parent-review-read.json ; aucun replay privé ni audit buffers parent dans ce tick à ce stade. Cette attribution vient du message de délégation, pas d'une inférence à partir du rapport privé ; aucun intervalle ou exit parent supplémentaire n'est inventé. Le publisher lit les preuves citées et exécute seulement les tests publics archivés : aucun rejeu privé ni comparaison des buffers privés. La revue finale de publication PASS au 12 septembre 2026 à 17:26 Europe/Paris porte sur le snapshot relu ; réserve publique levée, distincte de la revue privée PASS. Rapports : build/reverse/autonomy-20260912/re768-final-review/rapport.md et verdict.json.

## Exécution et limites

Le suffixe loader cible authentifié comporte 59799 visites de hooks, pas un boot/loader complet. Les six appels GetFloor/helpers : 1193 visites de hooks, 153 lectures, huit stores inférés ; pas des instructions retirées ni des watchpoints hardware. CPU et RAM synthétiques restaurés par appel. Le reviewer reconstruit indépendamment les stores ; le journal worker reste qualifié inféré. Les états finaux exacts ne prouvent pas l'absence de toute écriture transitoire ni la validité de tous les pointeurs transformés du corpus.

Configuration native bornée : ELF32, g++ -m32 -O0, PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Dépendances séparées par TU, headers système et compilateur non reconstruits indépendamment ; link complet sans tolérance aux symboles non résolus. Un processus natif pour six requêtes, retour normal. Instrumentation des frontières de fonctions : pas de trace exhaustive des stores natifs, pas de sanitizer, pas toutes architectures/optimisations, pas de build complet ni pipeline matériel. Ghidra frais avec -noanalysis et post-script ciblé, pas analyse automatique globale.

Source de production inchangée, code_change_readiness=blocked ; gardes historiques inchangées, HEAD épinglé et arbre suivi propre requis par la preuve privée. La publication modifie cet arbre : ne pas rejouer les anciens probes ni contourner leurs gardes. Après expiration de 17:40 ou changement de provenance, toute nouvelle exécution demande une unité autorisée distincte ; la limite utilisateur 18:45 n'est pas un renouvellement de cette garde. Aucun patch justifié par cette cohorte concordante.

## Tests publics et archives

Archives : build/reverse/autonomy-20260912/re768-publication/ ; red.log, green.log, suite.log et ledgers JSON enregistrent commande exacte, cwd, environnement, début/fin, exit, durée monotone et hashes avant/après. Contrat purement documentaire : aucune importation ni exécution privée. Les assertions de présence ne prouvent pas à elles seules les expériences attribuées. Le test exige la qualification dans cette story ET la seule section RE768, puis la restauration byte-exact du dashboard prédécesseur, fermetures comprises.

RED documentaire réellement observé le 12 septembre 2026 : 17:16:05.078716–17:16:05.361651 +02, exit 1, un échec attendu (story absente), un test réussi en 0,07 s pytest. GREEN observé : 17:17:28.534846–17:17:28.797056 +02, exit 0, 2 tests réussis en 0,06 s pytest. Suite publique exacte RE767 avec le seul test RE768 ajouté : 17:17:28.916902–17:18:28.044732 +02, exit 0, 3759 tests réussis en 58,75 s pytest (59,127362 s processus). Test byte-identique entre RED et GREEN. Ces résultats précèdent leur inscription ; revalidation après résultats distincte à consulter dans final.json et final.log, sans anticiper son succès ni prétendre à une seconde suite complète.

## Commande publique exacte

Depuis /var/www/projects/TOMB5, avec PYTHONDONTWRITEBYTECODE=1 :

```sh
python3 -B -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py tests/reverse/test_re765_vertical_integration_publication.py tests/reverse/test_re766_multihop_publication.py tests/reverse/test_re767_corpus_composition_publication.py tests/reverse/test_re768_corpus_negative_triangle_publication.py -q -p no:cacheprovider --basetemp /var/www/projects/TOMB5/build/reverse/autonomy-20260912/re768-publication/suite-tmp
```

Sélection littérale reprise de la commande RE767, seul tests/reverse/test_re768_corpus_negative_triangle_publication.py ajouté ; basetemp unique sous re768-publication. Les tests documentaires/dashboard affectés seront revalidés après inscription, sans relancer tests/emulator ni une preuve privée.

## Handoff

Après RE-768 : nouvelle preuve privée portail → triangle négatif PASS, publication metadata-only ; revue finale de publication PASS au 12 septembre 2026 à 17:26 Europe/Paris. Prochaine recherche proposée, non commencée dans cette unité : attribuer un caller réel GetFloor, ses arguments et sa room entrante, puis l'usage du record retourné. Ce handoff ne lance ni n'autorise seul une extension. Aucun gonflement de matrice et aucun patch : la nouveauté est le prédicat non nul après portail, pas une répétition du cas index nul RE767.
