# RE-767 — GetFloor : composition portail puis pit sur corpus authentifié

## Tracker

- [x] Preuve et revue indépendante privée lues avant RED documentaire ; attribution consignée dans claims-map.md.
- [x] RED documentaire observé avant création de la story et modification du dashboard.
- [x] Publication metadata-only ; source de production inchangée, readiness inchangée, gardes historiques inchangées.
- [x] Réserve levée : revue finale de publication PASS au 11 septembre 2026 à 21:49 Europe/Paris, sur le snapshot relu ; verdict documentaire distinct du PASS privé.
- [ ] Caller réel et triangle négatif dans cette composition non prouvés.

## État et overview actif

État actif au 11 septembre 2026, Europe/Paris. Après RE-766, la matrice multi-sauts synthétique reste un jalon historique ; RE767 ajoute un échantillon de composition sur corpus authentifié, sans correction. Cet overview actif et le handoff actif sont placés dans la seule nouvelle section RE767 du dashboard. Sections antérieures, transitions et fermeture HTML restent octet pour octet inchangées. Livraison bornée à 21:47 dans la délégation actuelle ; aucun staging, commit, push ou job effectué pendant cette publication.

## Résultat borné

PASS privé borné : huit appels directs GetFloor sur corpus authentifié, zéro divergence de la paire finale (room, cellule) et zéro divergence des événements ordonnés entre cible et production actuelle. Les ensembles divergents ont intersection et union nulles, sans addition de compteurs recouvrants. Chaque appel suit exactement door, portal, door, floor, pit : huit événements portal et huit événements pit, pas seize cas indépendants.

L’échantillon provient de l’entrée 10 : 243 rooms, 5824 cellules stockées et un buffer chargé de 521688 octets ; ces cellules ne sont pas autant de requêtes GetFloor. La découverte avait examiné 3065 requêtes de modèle, pas des appels cible, dans les entrées 2 à 10 avant de s’arrêter sur huit candidats. Deux cellules de la room 57, quatre hauteurs dérivées par cellule, composent les routes 57 → 222 → 119 et 57 → 223 → 123. Ce sont des arguments construits depuis les données authentiques, avec état de départ synthétique : aucun caller réel du jeu ni accessibilité gameplay établis. Échantillon non exhaustif.

Limite décisive : arrivée portail avec index floor-data nul, helper floor retournant zéro ; aucun triangle négatif exercé et aucune nouvelle validation du correctif owner/polarité RE765. Destinations portail 222/223, supérieures à 127 et inférieures à 255 ; pas de destination explicite 255 ni supérieure à 255. Pas de couverture universelle de la largeur GetDoor ou des conversions caller. Dans cet échantillon, pas de sky, cycle, multi-pit, clamp extérieur ni contrôle négatif de non-traversée.

## Preuve consommée et attribution

Preuve auteur : build/reverse/autonomy-20260911/re767-corpus/HANDOFF.md et build/reverse/autonomy-20260911/re767-corpus/COMMANDS.md. Le worker a exécuté le runner et cinq méthodes unittest après génération, puis ses audits structurel et complémentaire. Aucun RED comportemental revendiqué : aucune correction dans cette unité. Le présent RED est uniquement documentaire.

Revue indépendante privée : build/reverse/autonomy-20260911/re767-review/rapport.md, build/reverse/autonomy-20260911/re767-review/verdict.json et build/reverse/autonomy-20260911/re767-review/final-verification.json. Verdict lu : passed=true, security_concerns et logic_errors vides. Vérification finale de revue datée du 11 septembre 2026 à 21:38:50.306261 +02. Le reviewer distinct a rejoué le runner inchangé avant expiration : intervalle du subprocess runner 21:34:09.752624–21:34:17.335102 +02, exit 0. Il a exécuté Ghidra frais, compilé le harness et la TU entière SPEC_PSXPC_N/GETSTUFF.C, lié complètement, puis cinq méthodes unittest et l’audit auteur après génération. Les chaînes auteur hardcodées des ledgers restent historiques et ne désignent pas l’acteur reviewer.

Le reviewer a écrit un décodeur indépendant, sans import des modèles/producteurs : reconstruction intégrale des buffers loader/natif de 521688 octets et de la baseline RAM de 2097152 octets, ordre exact des requêtes, routes, record final complet dans sa table propriétaire, stdout natif, résultats et événements. Selon sa revue, 12 fichiers comportementaux worker/reviewer sont identiques intégralement. Il a authentifié traces et lectures, contrôlé les stores inférés et les empreintes RAM reconstruites. Les images RAM post-appel ne sont pas archivées ; leur égalité a été assertée par le moteur frais. Ce décodeur n’est pas une deuxième émulation CPU, ni un oracle matériel.

Parent : selon le contexte explicite de la délégation actuelle, lecture par outils du HANDOFF, du rapport, du verdict et de final-verification ; aucun replay ni audit buffers parent effectué dans ce tick. Cette attribution ne décrit pas des actions futures et ne fournit aucun intervalle ou exit parent inventé. Publisher : lecture des documents nommés et seuls tests publics consignés ici, aucun rejeu privé ni reconstruction des buffers privés. La revue finale de publication PASS au 11 septembre 2026 à 21:49 Europe/Paris porte sur le snapshot relu : build/reverse/autonomy-20260911/re767-final-review/rapport.md et build/reverse/autonomy-20260911/re767-final-review/verdict.json ; elle reste distincte du PASS privé. Selon la délégation de clôture, le parent a lu ce rapport et ce verdict via outils à 21:50, sans replay privé ; aucune réussite future n’est présumée.

## Exécution et limites

La preuve privée comprend un suffixe loader cible authentifié, pas un loader complet ; 59799 visites de hook pour ce suffixe. La relocation logicielle n’est pas une nouvelle exécution du relocateur cible. Les huit appels cible vont de l’entrée au retour avec GetDoor et helper floor réels, sans retour de fonction doublé ; CPU/RAM restaurés par appel. Pour ces appels : 1444 visites de hook, 224 lectures et 16 stores inférés, pas des instructions matériellement retirées ni une trace dynamique exhaustive des stores. Les helpers inclus ne constituent pas des requêtes supplémentaires de l’échantillon.

Configuration privée testée : ELF32, g++ -m32 -O0, PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Deux compilations fraîches, dépendances séparées par TU, assertions ABI, link sans tolérance aux symboles non résolus ; un processus natif pour huit requêtes, retour normal exit 0. Buffer vérifié après chaque appel, seul buffer natif final archivé. Instrumentation aux frontières de fonctions, pas de trace exhaustive des écritures transitoires ; états finaux ne prouvent pas leur absence. Configuration bornée, pas toutes architectures ou optimisations, pas de sanitizer, pas de build complet, hardware/cache/MMIO/concurrence ou preuve gameplay. Les avertissements Ghidra ne sont pas une preuve de décompilation intégrale correcte.

Garde privée propre : fenêtre 21:23–21:39 et interdiction de lancement après 21:35, HEAD épinglé et diff HEAD propre, assertions et pins. Désormais garde expirée : aucun replay ici, aucun contournement. Toute nouvelle exécution nécessiterait autorisation et provenance nouvelles sans modifier les anciennes gardes. La borne actuelle de publication 21:47 ne renouvelle pas la fenêtre privée. Source de production inchangée et readiness inchangée : pas de nouvelle autorisation de patch ou de généralisation GetFloor.

## Tests publics et archives

Archives : build/reverse/autonomy-20260911/re767-publication/ ; red.log/json, green.log/json, suite.log/json enregistrent commandes exactes, cwd, environnement, début/fin, exit, durée monotone et hashes avant/après. Le test ne lit ni assets ni preuves privées, n’importe aucun producteur et ne lance aucun probe. Il vérifie les qualifications de cette story et de la seule section RE767 ainsi que la restauration exacte du dashboard au HEAD prédécesseur. Ses assertions documentaires ne démontrent pas à elles seules l’expérience privée.

RED documentaire observé le 11 septembre 2026 : 21:41:53.032318–21:41:53.303608 +02, exit 1, un échec attendu (story absente) et un test réussi en 0,07 s pytest. GREEN : 21:43:26.784684–21:43:27.042329 +02, exit 0, 2 tests réussis en 0,06 s pytest. Suite exacte RE766 augmentée du seul fichier de test RE767 : 21:43:27.073968–21:44:26.154104 +02, exit 0, 3757 tests réussis en 58,71 s pytest (59,079687 s processus). Test identique entre RED et GREEN. Ces résultats précèdent leur inscription ; la revalidation documentaire après inscription est une exécution distincte, à constater dans final.json et final.log, sans revendiquer une seconde suite complète.

## Commande publique exacte

Depuis /var/www/projects/TOMB5, avec PYTHONDONTWRITEBYTECODE=1 :

```sh
python3 -B -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py tests/reverse/test_re765_vertical_integration_publication.py tests/reverse/test_re766_multihop_publication.py tests/reverse/test_re767_corpus_composition_publication.py -q -p no:cacheprovider --basetemp /var/www/projects/TOMB5/build/reverse/autonomy-20260911/re767-publication/suite-tmp
```

Sélection littérale de RE766 avec uniquement tests/reverse/test_re767_corpus_composition_publication.py ajouté ; basetemp neuf sous les archives RE767 et cache pytest désactivé.

## Handoff

Après RE-767 : preuve privée bornée PASS, publication metadata-only ; revue finale de publication PASS au 11 septembre 2026 à 21:49 Europe/Paris, sur le snapshot relu, réserve initiale levée. Prochaine recherche proposée, non commencée dans cette unité : attribuer un caller réel GetFloor avec arguments, room entrante et usage du retour, ou un portail authentique arrivant sur triangle négatif. Aucun de ces objectifs n’est commencé ni autorisé par ce handoff seul. Pas de gonflement de matrice ni de validation du triangle négatif déduite de l’index nul ; production et readiness restent inchangées.
