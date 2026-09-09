# RE-763 — GetDoor : caractérisation sur corpus authentique chargé

## Tracker

- [x] Preuves GREEN, revue indépendante, vérification post-rapport et ledgers parent lus avant toute assertion documentaire ; claim-evidence map privée créée avant tests.
- [x] RED documentaire observé avant cette story : absence attendue, un échec et un contrôle historique réussi.
- [x] Expérience privée déjà vérifiée : PASS de caractérisation bornée, divergence des entiers promus conservée.
- [x] Revue indépendante PASS ; replay parent puis audit reviewer exécuté par le parent établis séparément.
- [x] Validation publique initiale : 2 tests documentaires et suite exacte de 3096 tests réussis ; revalidation après résultats consignée séparément. Revue finale parent de publication distincte, à obtenir avant livraison finale.
- [ ] Traversées verticales GetFloor et helpers triangles sur corpus chargé : prochaine preuve proposée, pas un résultat acquis.

## Résultat et unités de mesure

Le corpus couvre 15 niveaux (entrées 2 à 16), 2704 rooms, 91444 cellules de plancher et 34882 appels distincts GetDoor, un par couple niveau/index représenté. Les résultats par cellule sont une expansion des appels distincts : ni 91444 exécutions cible, ni 91444 tests. Les 2 méthodes unittest privées sont réussies après génération puis audit. Les 15 processus natifs ne sont pas les appels de fonction.

La reconstruction indépendante depuis l’ISO locale compare 8232344 octets de buffers complets chargés, longueurs et contenu intégral compris, y compris les régions non modifiées. Elle reconstruit champs, cellules, portails géométriques, entrées natives et stdout complets, puis vérifie les retours et les séquences ordonnées de lectures GetDoor avec un interpréteur reviewer séparé, sans import du modèle producteur. C’est un second modèle logiciel, pas un oracle matériel ni une certification externe du disque.

16791 cellules donnent un portail explicite ; 74653 donnent une sentinelle/absence. Parmi les portails, 4992 cellules ont une destination supérieure à 127. Destinations explicites observées : 0 à 253 ; zéro destination explicite supérieure à 255, zéro égale à 255 et zéro hors du nombre de rooms de son propre niveau. Les 4992 sont des cellules, pas des valeurs distinctes. 254 et 255 explicites non exercés, de même que les destinations supérieures à 255. La sentinelle 255 n’est pas une destination explicite valide testée. Les 8068 portails géométriques constituent une autre mesure : 2457 au-dessus de 127, aucun hors rooms, bornes 0 à 253.

Il reste 79645 différences cible/entier natif promu : les 74653 sentinelles et les 4992 cellules portail au-dessus de 127. Le retour char de la vraie TU et son extension signée native diffèrent de la valeur cible ; zéro différence après unsigned char. Cette égalité basse n’est pas une équivalence ABI, ni la preuve du registre de retour, du contrat C universel ou des conversions de tous les callers. Le caller cible GetFloor normalise sur 16 bits signés, pas sur 8 bits ; GetFloor inspecté statiquement, non exécuté dans RE763.

## Exécution et portée

Le runner effectue deux imports Ghidra neufs (boot et loader), une compilation fraîche de chaque TU et un lien i386 de la vraie SPEC_PSXPC_N/GETSTUFF.C avec son harness. Le suffixe loader isolé puis GetDoor sont effectivement exécutés sur les données authentifiées, avec placements et registres synthétiques ; pas le loader complet. La décompilation peut dépasser la tranche exécutée et ne constitue pas une extension de preuve. Les 665499 visites loader (arrêt exclu), 1000077 visites GetDoor et 130635 événements de lecture GetDoor sont des compteurs distincts ; les visites de hooks ne sont pas des instructions matériellement retirées.

Les intervalles complets de lecture GetDoor sont vérifiés, pas seulement les lectures commençant dans une zone filtrée. En revanche, les lectures du loader ne disposent pas du même traçage borné. Le runner compare sa RAM Unicorn complète en mémoire ; images RAM complètes non archivées : le reviewer a rejoué/inspecté ces assertions, tandis que sa contre-vérification autonome porte sur les buffers intégralement sauvegardés, pas sur une seconde comparaison indépendante de toute la RAM. Les snapshots finaux n’excluent pas des écritures transitoires restaurées.

Natif : retour normal, aucun symbole non résolu autorisé ; immutabilité de la cellule et du vecteur floor_data, pas de toute la mémoire native. Pas de sanitizers ni trace native exhaustive. Dépendances par TU épinglées séparément ; toolchain, headers système et environnement non hermétiques. Pas de preuve matérielle, pas de preuve gameplay, pas de domaine universel, ni sûreté pour des entrées arbitraires malformées. Aucun correctif de largeur justifié par l’absence de destination supérieure à 255 dans ce corpus.

## Revue, replay parent et audit : attributions séparées

Preuves privées sous build/reverse/autonomy-20260909/re763. GREEN : green/run.json, moteur du 9 septembre 2026, 19:49:47.721778–19:51:06.470743 Paris, exit 0 ; green/tests.log contient 2 méthodes unittest réussies. Revue indépendante : review/report.md, review/verdict.json, review/post-report-verification.json, PASS borné. Le reviewer distinct a lancé run.py reviewer puis son programme indépendant ; 128 fichiers comportementaux reviewer identiques à GREEN, sans normalisation des fichiers. Les ledgers de chemins/horaires ne font pas partie de cette identité.

Le parent a ensuite lancé python3 -B build/reverse/autonomy-20260909/re763/run.py parent, selon la commande explicitement transmise. parent/run.json mesure le moteur enfant : 19:59:04.071333–20:00:21.608102 Paris, exit 0 ; ce n’est pas un intervalle mesuré du wrapper entier. parent/tests.log confirme 2 méthodes unittest réussies.

Puis python3 -B build/reverse/autonomy-20260909/re763/parent_audit.py a exécuté main du reviewer en redirigeant uniquement ses entrées/sorties P/Q vers parent et parent-audit. parent-audit/invocation.json : 20:00:21.642147–20:00:24.017787 Paris, exit 0 ; parent-audit/independent-result.json : PASS, mêmes totaux, buffers complets reconstruits depuis l’ISO et 128 fichiers comportementaux parent identiques à GREEN. C’est l’exécution parent de l’audit déjà écrit par le reviewer, pas un nouvel auteur indépendant. La mention antérieure « aucun replay parent établi » du rapport reste historiquement vraie à sa date, mais précède ces ledgers. Lire le verdict ici ne prétend pas que le parent l’a relu.

## Validation documentaire publique

Aucun rejeu privé pendant cette publication ; gardes historiques inchangées, source de production inchangée. Les tests publics documentaires n’ouvrent aucun asset ni preuve privée. RED documentaire : 20:03:33.058512–20:03:33.331087 Paris, exit 1, 1 échec attendu et 1 réussite en 0,07 s. GREEN documentaire : 20:05:25.586071–20:05:25.839414 Paris, exit 0, 2 tests réussis en 0,06 s. Suite exacte RE762 augmentée du seul nouveau test : 20:05:25.869774–20:06:22.597869 Paris, exit 0, 3096 tests réussis en 56,38 s (56,727739 s monotoniques). Ces résultats précèdent l’insertion de ce paragraphe ; revalidation après insertion : 54 tests réussis en 0,27 s, exit 0, 20:07:03.931559–20:07:04.422335 Paris. Cette clôture documentaire est distincte de la suite complète et sera contrôlée à nouveau après cette mise à jour. Archives réservées à publication/red.log, publication/green.log, publication/suite.log et JSON homologues : commande, cwd, intervalle, exit, durée monotone et hashes avant/après. Le hash du test est conservé entre RED et GREEN ; la revalidation après insertion des résultats est consignée dans publication/final.json et final.log.

## Commande publique exacte

Sélection littérale de la suite RE762, ajout unique du nouveau test, depuis /var/www/projects/TOMB5. Les tests/emulator restent les régressions publiques ordinaires, pas les preuves privées gardées.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py -q
```

## Handoff

Après RE-763 : caractérisation du domaine local GetDoor acquise, sans équivalence des entiers promus. Prochaine preuve proposée : traversées verticales GetFloor et helpers triangles sur corpus chargé ; préciser les chemins, arrêts et comparaisons avant tout patch. Ne pas rouvrir la largeur sur la seule absence de destination supérieure à 255. Cette publication ne lance pas cette unité et n’autorise aucun patch. Le handoff RE762 reste intégralement conservé comme jalon historique.

Autorisation actuelle transmise : recherche jusqu’au 9 septembre 2026 à 23:25 Paris, clôture 23:45 ; la présente livraison reste strictement metadata-only, sans job, staging, commit ou push au moment de la remise. Revue finale parent de publication distincte de la revue privée. Rapport expressément interdit ni ouvert, ni lu, ni hashé, ni modifié. Trois fichiers publics seulement : cette story, le dashboard actif et le test documentaire ; historiques et générateurs préservés.
