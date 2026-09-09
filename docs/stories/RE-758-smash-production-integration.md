# RE-758 — SmashObjectControl : intégration production minimale

## Tracker

- [x] Date avant unité : 9 septembre 2026, 15:28:17 Europe/Paris ; HEAD ef2d4603344b28410ffc95861af7b79117ac9569, arbre suivi/index propre.
- [x] Story RE-757, HANDOFF privé, revue finale technique, clarification de verdict et ledger parent lus ; aucun rejeu privé.
- [x] Tests publics écrits avant patch ; RED comportemental et garde observés, buffers et commandes conservés.
- [x] Évaluation de la source partagée et garde de préprocesseur ; intégration minimale puis GREEN sur compilation fraîche.
- [x] RED documentaire avant story/dashboard ; publication sous tests.
- [x] Suite exacte RE-757 augmentée : 1 353 tests réussis ; audit worker post-production PASS.
- [x] Vérification parent effectuée puis revue indépendante PASS ; résultats distincts du worker.
- [ ] Autres backends et gameplay non validés ; hors portée de cette intégration.

## Résultat et portée des backends

La vraie TU GAME/OBJECTS.C conserve SmashObject inchangé. SmashObjectControl transmet directement item_number, déjà short, uniquement sous PSX_VERSION && PSXPC_TEST. La branche alternative conserve exactement l’expression historique. Une garde de préprocesseur évite de généraliser la correction privée RE-757 à tous les consommateurs de cette source partagée. Le consumer et ses services ne sont pas réécrits dans la production.

CMakeLists.txt collecte GAME pour plusieurs plateformes ; SPEC_PSXPC_N/CMakeLists.txt active PSX_VERSION et PSXPC_TEST par défaut, tandis que SPEC_PSX n’active pas ce dernier. La preuve privée et la compilation publique utilisent ce couple de macros, g++ i386 -O0, ABI pointeur/long 32 bits. Le garde porte sur la configuration, pas sur le nom commercial de plateforme ni l’architecture du compilateur : autres backends non validés, architectures/configurations alternatives de cette même famille non validées. Quatre combinaisons booléennes du garde sont vérifiées par prétraitement du wrapper isolé ; ceci n’est pas la compilation des quatre backends. Les macros absentes ont leur sens usuel faux dans cette expression.

Le patch n’est pas byte-identique à la copie privée corrigée : il ajoute cette isolation de backend et conserve l’ancienne expression hors attribution. La preuve historique attribue le forwarding signé au delay slot complet ; elle n’autorise pas une suppression globale des décalages ailleurs.

## Tests synthétiques publics

128 cas : entrée directe/wrapper × indices 0–3 × BOX_LAST absent/présent × BOX_BLOCKED absent/présent × états 0–3 ; dimensions indépendantes. 64 appels directs et 16 wrappers index zéro sont des contrôles qui passent déjà en RED. 48 échecs comportementaux concernent les wrappers indices 1–3 ; 1 échec de garde correspond à la configuration corrigée encore absente. RED total : 49 échecs et 84 réussites. GREEN : 133 tests réussis, dont 128 cas, quatre sélections du préprocesseur et une couverture cartésienne.

Le harness synthétique compile la TU entière avec les en-têtes normaux ; linker avec élimination des sections inutilisées, sans autorisation de symboles non résolus. Le binaire appelle réellement wrapper et consumer. Une compilation fraîche et 128 processus natifs par passage comportemental. L’oracle Python construit indépendamment les buffers I=576, B=32, F=64 octets et événements ordonnés, sans utiliser les résultats natifs ni les probes privés. Les items/boxes non sélectionnés sont comparés aussi ; room=80 octets comparée avant/après sans normaliser son pointeur. Les coordonnées, flags et valeurs sentinelles sont synthétiques et distincts du corpus privé ; aucun octet propriétaire public.

SoundEffect, ExplodingDeath2, RemoveActiveItem : trois doubles ABI sans effets mémoire, enregistrant les arguments et l’ordre des appels. Leurs corps authentiques ne sont pas exécutés ; le service RemoveActiveItem n’apparaît que pour l’état actif. États/flags uniformes entre items dans chaque cas : états hétérogènes simultanés, indices négatifs/extrêmes, coordonnées complètes et validité générale des pointeurs exclus. Pas de build complet, pas de sanitizer, pas de sûreté mémoire générale, pas de preuve gameplay, de caller runtime réel, de sauvegarde, de concurrence ou de matériel. Toolchain et en-têtes système non hermétiques. Les snapshots finaux des buffers ne détectent pas les écritures transitoires restaurées.

## Chronologie et validation

RED actual-TU : 15:31:17.173881–15:31:17.949837 Paris, exit 1, 49 échecs dont 48 comportementaux ; compilation réussie. GREEN avec tests inchangés : 15:31:46.203536–15:31:46.801563, exit 0, 133 tests en 0,38 s. Source baseline et test RED archivés avant patch, source/test hashes consignés avant et après chaque lancement. Ce ledger local n’est pas un horodatage tiers infalsifiable.

RED documentaire : 15:32:29.242319–15:32:29.515404, exit 1, story absente ; un échec et un contrôle réussi. GREEN documentaire : 2 tests réussis en 0,06 s, exit 0, 15:34:08.615355–15:34:08.878157 Paris. Suite exacte RE-757 augmentée : 1 353 tests réussis en 51,48 s, exit 0, 15:34:17.278479–15:35:09.059720 Paris (durée processus 51,780910 s). Audit worker post-production : exit 0, 15:36:00.360549–15:36:00.410579 ; stdout natif complet RED/GREEN vérifié, 576 octets items et 24 octets boxes différents en RED, zéro secteur différent. Ce contrôle ne constitue pas une revue indépendante ; logs audit-command et worker-audit.json. Revalidation finale après insertion de ces résultats archivée séparément dans final.log.

Preuves nouvelles exclusivement sous build/reverse/autonomy-20260909/re758 : red.log, green.log, publication-red.log, suite.log et commands.json ; sous-répertoires dédiés conservent compilation, binaire, stdout complet et commandes de chaque cas. Aucun rejeu cible, aucun ancien probe exécuté ou modifié, gardes historiques inchangées. Les résultats parent/reviewer RE-757 sont lus comme preuves historiques, pas attribués à ce worker. Les tests documentaires contrôlent cette story et la seule nouvelle section du dashboard ; aucun générateur historique relancé pour publier ces textes.

## Vérification parent et revue indépendante

Vérification parent effectuée : 1 353 tests réussis en 51,66 s, exit 0, du 9 septembre 2026 à 15:39:06.755439 au 15:39:58.702926 Paris ; commande exacte et hashes dans parent-suite.json/log. Audit du producteur exécuté par le parent après la suite, 15:40:05.520907–15:40:05.570264, exit 0 : parent-audit-command.json/log et parent-audit.json. Comparaison complète des stdout/buffers RED archivés et GREEN parent frais ; 48 wrappers divergents en RED, 576 octets items et 24 boxes différents, zéro secteur. Ce contrôle parent n’est pas un nouvel oracle indépendant.

Revue indépendante PASS : review/review.json, listes security_concerns et logic_errors vides, 188 tests frais en 0,70 s, exit 0, 15:41:18.317701–15:41:19.222071 Paris. Le reviewer recompile la TU, exécute 128 processus natifs et reconstruit séparément RED archivé et GREEN frais, y compris room complète via le symbole ELF. Il vérifie le sceau historique RE-757 sans le rejouer ; aucun rejeu privé. Le parent a relu le verdict strict et vérifié les cinq hashes des livrables avant synchronisation documentaire. Revue initiale valable pour ce snapshot ; la clôture documentaire reçoit une revue delta séparée.

Le script worker verify.py a échoué sur une assertion de whitespace couvrant toute la TU historique. Aucun nettoyage de la source ancienne : git diff --check et l’audit indépendant des seuls ajouts passent. L’échec est conservé, pas présenté comme une vérification réussie. RED de synchronisation documentaire observé par le parent : un échec attendu et un contrôle réussi, exit 1, closure-red.json/log ; aucun changement de production ou de test comportemental après la revue initiale.

GREEN de clôture documentaire parent : 55 tests réussis en 0,34 s, exit 0, 15:47:23.915461–15:47:24.467531 Paris ; commandes et hashes dans closure-green.json/log. Ce passage suit la synchronisation de la story, du handoff courant et de la section RE-758 ; la production et le test comportemental restent identiques au snapshot de revue.

## Handoff

Après RE-758 : intégration production bornée validée par le parent puis par une revue indépendante fraîche. Dans le handoff initial, ces deux contrôles étaient notés non exécutés par ce worker ; leur réalisation ultérieure est attribuée ci-dessous. Clôture technique de cette intégration ; aucun rejeu privé. Une prochaine unité de recherche devra sélectionner un comportement cohérent encore non prouvé dans les consumers du niveau, sans répéter cette matrice ni élargir implicitement la validation aux autres backends ou au gameplay. Les probes privés gardés restent intacts.

Commandes depuis /var/www/projects/TOMB5 :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator/test_smash_object_control.py tests/reverse/test_re758_smash_integration_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py -q
```

La seconde commande est exactement la sélection RE-757 augmentée du test documentaire nouveau ; tests/emulator inclut automatiquement les 133 nouveaux tests. Utiliser un nouveau nom de ledger et un répertoire temporaire exclusif pour chaque rejeu parent/reviewer. Ne pas rejouer RED contre la production corrigée : inspecter son archive et son hash ; une nouvelle expérience comparative exige une provenance distincte sans modifier la production ou les probes historiques.

Autorisation du 9 septembre : recherche jusqu’à 23:25 Paris, clôture jusqu’à 23:45 Paris. Au moment de ce handoff worker : aucun staging, commit, push ou job ; rapport interdit jamais ouvert ni modifié. Historiques préservés ; tests et story nouveaux non suivis jusqu’à décision de livraison du parent.
