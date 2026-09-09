# RE-761 — GetFloor : preuve corrective PRIVÉE du clamp haut Z

## Tracker

- [x] Lecture de recovery/HANDOFF.md, review/rapport.md et review/verdict.json ; Revue indépendante PASS bornée, sans problème de sécurité ni erreur logique bloquante.
- [x] Parent ultérieur distingué du récupérateur et du reviewer ; publication commencée le 9 septembre 2026 à 18:23:03 Europe/Paris, HEAD e07466ef.
- [x] TDD documentaire : test écrit avant les documents, RED observé à 18:24:32.068910–18:24:32.357139 Paris, exit 1, 1 échec attendu story absente et 1 réussite ; aucun changement du test pour obtenir GREEN.
- [x] Exactement une nouvelle story, une section dashboard avec aperçu/handoff actifs, un nouveau fichier de test documentaire ; source de production inchangée.
- [ ] Intégration au backend attribué et régression TU publique non réalisées ; largeur des IDs exclue sans domain proof préalable.

## Résultat correctif privé

**Preuve corrective PRIVÉE, pas intégration production ni équivalence générale.** Le RED comportemental archivé porte sur la baseline byte-identique à SPEC_PSXPC_N/GETSTUFF.C : **1944 cas, 3 méthodes unittest, 216 échecs de sous-tests**. Décompte indépendant : **72 divergences finales, 144 divergences intermédiaires, 144 cas distincts, intersection 72**. Les sous-tests en échec ne sont donc pas 216 cas distincts.

Une seule substitution dans la copie privée de la vraie TU : **dx = 1** remplace dx = r->y_size - 2 dans la branche haut-Z/dx<=0. Aucun changement GetDoor ni de type unsigned char. Le GREEN récupéré, son replay, reviewer-01 et parent-01 portent chacun sur 1944 cas et 3 méthodes unittest, zéro divergence finale et intermédiaire. Ce sont les sélections finales et celles observées aux entrées GetDoor, pas une équivalence universelle de GetFloor. Le RED reste archivé, ni relancé ni remplacé ; tentative historique de substitution échouée et timeout de remise du producteur conservés, puis récupération réussie avant revue.

Matrice ordonnée : deux géométries synthétiques, neuf positions X × neuf positions Z, trois hauteurs, quatre destinations (-1, 17, 254, 255), 486 cas par destination. 17 et 254 traversent réellement le portail et sélectionnent dans la seconde géométrie ; -1 et 255 sont contrôles, pas preuve d’un portail valide vers 255. Formes sensibles et masquantes, bords et sélections intermédiaires sont couverts dans cette matrice seulement. Par corpus : **2916 entrées GetDoor, 206640 visites de hook, 28836 événements de lecture cible** ; les visites ne sont pas des cycles matériels ni un compte d’instructions retirées.

## Authenticité, ABI et observations

Vraie TU privée complète fraîchement compilée avec harness séparé, g++ -m32 -O0, i386 / ELF32. Assertions de tailles pointeur/long/FLOOR_INFO/room_info et offsets ABI ; dépendances fraîches des deux TU contrôlées (9 entrées harness, 20 TU) contre 301 entrées scellées. Inspection indépendante du GetFloor réellement lié : branche corrective et véritable appel GetDoor, stockage en octet et promotion non signée inchangés. Chaque producteur réussi lance 1944 processus natifs et 1944 émulations cible ; les audits ne sont pas des compilations ni des émulations supplémentaires.

Payload authentifié, instructions visitées contrôlées ; branche et delay slot corroborés par décodage indépendant et archive Ghidra RE760 inspectée. Aucun nouveau lancement Ghidra. L’audit indépendant reconstruit les images initiales complètes de 2 Mio, sans importer engine, expected ou audit recovery, puis vérifie RED + GREEN frais : **3888 paires RAM complètes, 3888 paires de buffers natifs**. Seul room number attendu change en RAM cible ; rooms/cells/words natifs immuables, pointeurs floor normalisés. Résultats cible tous champs et stdout natif entier contrôlés ; les buffers natifs ne représentent pas toute la mémoire du processus.

Limites : pas de traçage exhaustif des accès transitoires natifs, pas de sanitizers ; stores cible inférés du décodage et complétés par RAM entière. Plages de lectures autorisées contrôlées, pas preuve universelle de validité sémantique ni reconstruction indépendante de toute la séquence attendue de lectures. Toolchain non hermétique, -MMD exclut les headers système. Coordonnées, dimensions et arithmétique bornées ; aucune portabilité universelle des décalages signés ou ABI générale prouvée. Pit/sky sentinelles : chaînes verticales, triangles, callers englobants, validité réelle des portails et grands IDs non établis. Pas de preuve gameplay, matérielle, de concurrence ou d’autres backends. La signedness et la largeur du retour GetDoor ne sont pas corrigées : unsigned char demeure ; largeur des IDs exclue, domain proof nécessaire.

## Attribution et relectures

**Revue indépendante PASS** : review/rapport.md, review/verdict.json et **review/independent_audit.py**. Reviewer a réellement exécuté le runner scellé reviewer-01, exit 0, 18:14:37.892907–18:16:30.850378 Paris, 112.957476 s monotoniques, et son audit indépendant (exécuté en chevauchement avec la fin du runner), exit 0, 18:16:14.620174–18:17:08.429173, 53.809013 s. Ce PASS qualifie la preuve privée, pas une revue indépendante de cette publication.

Selon les actions explicitement transmises par le parent, il a réellement exécuté PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python -B build/reverse/autonomy-20260909/re761/recovery/replay.py parent-01 depuis /var/www/projects/TOMB5. Le ledger recovery/parent-01/replay-result.json lu ici confirme le wrapper **18:20:28.640767–18:22:12.885740** Paris, exit 0, **104.244974 s** monotoniques. Le runner comprend producteur + tests + audit RECOVERY : le **parent n’a pas exécuté l’audit indépendant** du reviewer. Le parent a transmis avoir relu le verdict et comparé les result.json complets recovery-green/recovery-replay/reviewer-01/parent-01 : byte-identiques, SHA256 8604cbc481a3e0dfcece954fe7cdf11cd890cc3273e0b96a23b0d7413981f50b.

L’attribution historique codée en dur du runner et de l’audit recovery dit « aucune revue indépendante » : elle décrit leur origine et ne décrit correctement ni le reviewer ni le parent actuels. Chaînes scellées conservées, qualification externe ici. Les mentions « pas revue indépendante ni vérification parent » du handoff de récupération et l’absence d’attribution parent dans le rapport reviewer précèdent ces actions ultérieures ; elles ne les nient pas. Le worker de publication lit ces archives, mais ne s’attribue ni replay privé ni audit indépendant.

## Validation publique

Aucun rejeu privé pendant cette publication ; gardes historiques inchangées, aucun générateur historique exécuté. Données brutes, RAM, désassemblage, binaires et ledgers restent uniquement sous build ignoré. Journaux : build/reverse/autonomy-20260909/re761/publication/red.log, green.log, suite.log, final.log ; JSON homologues et commands.json enregistrent commande exacte, cwd, environnement, début/fin, exit, durée monotone et hashes avant/après. Le nouveau test ne lit/import aucun artefact privé et ne lance aucune preuve privée. Les sections et transitions historiques sont préservées byte pour byte, hors aperçu et premier paragraphe handoff actifs.

GREEN documentaire : 2 tests réussis en 0,06 s, exit 0, 18:26:50.069846–18:26:50.332016 Paris (0,262091 s monotoniques). Suite exacte RE-760 augmentée uniquement du nouveau fichier de test : 1359 tests réussis en 51,95 s, exit 0, 18:26:50.363187–18:27:42.591971 Paris (52,228699 s monotoniques). Revalidation intégrale après insertion de ces résultats archivée dans final.json et final.log ; aucune assimilation aux 3 méthodes privées.

Commande exacte depuis /var/www/projects/TOMB5, sélection littérale de publication/suite.json RE-760 avec ajout unique du nouveau test :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py -q
```

## Handoff

Après RE-761 : preuve corrective privée clôturée, source de production inchangée. Prochaine proposition cohérente seulement : intégration au backend attribué du clamp minimal avec régression TU publique en TDD comportemental, configuration explicitement bornée, autres backends intacts. Largeur des IDs exclue ; domain proof nécessaire avant toute correction du type. Cette publication n’exécute ni n’autorise implicitement cette intégration.

Recherche autorisée jusqu’à 23:25 Paris, clôture jusqu’à 23:45 Paris le 9 septembre 2026 ; aucun nouveau job. Les gardes historiques HEAD/arbre propre/index/date peuvent refuser les replays après publication : ne pas les contourner ni resealer. Aucun staging, commit ou push ; rapport expressément interdit ni ouvert, ni hashé, ni modifié. Aucun patch production.
