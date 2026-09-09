# RE-757 — SmashObjectControl : preuve de correction privée

## Tracker

- [x] Date avant unité : 9 septembre 2026, 14:51:31 Europe/Paris ; arbre suivi/index propre, HEAD prépublication 8ef424639bb887dea85e167d3b3cc85b7d55c999.
- [x] HANDOFF privé, preuves parent, revue indépendante et clarification de verdict lus ; aucun rejeu privé.
- [x] RED documentaire avant docs : story absente, 1 échec en 0,07 s, exit 1 ; 14:53:09.687741–14:53:09.950476 Paris.
- [x] Correction privée et limites publiées ; production inchangée.
- [x] GREEN documentaire et suite exacte RE-756 augmentée : 1 218 tests réussis.
- [x] Revue finale indépendante de publication PASS ; 52 tests documentaires frais réussis.
- [ ] Intégration PRODUCTION non implémentée ici.

## Résultat et matrice

PASS de correction privée bornée sur la vraie TU GAME/OBJECTS.C. La baseline privée est byte-identique à la production ; la copie corrigée ne change que la transmission directe de item_number dans SmashObjectControl, sans décalage préalable avant conversion en short. La cible normalise l’indice signé avec le delay slot de l’appel ; le wrapper natif fautif transmettait zéro. Le consumer SmashObject n’est pas réécrit dans le harness. Aucun patch suivi : production inchangée.

128 cas par passage : deux entrées directe/wrapper × quatre indices 0–3 × BOX_LAST absent/présent × BOX_BLOCKED absent/présent × quatre états 0–3 ; dimensions indépendantes. RED : 64 appels directs égaux, 16 wrappers index zéro égaux, 48 divergences wrappers indices 1–3. GREEN : 128 cas égaux, zéro divergence. Comparaison complète I=576, B=32, F=64 octets et événements ordonnés ; room=80 octets inchangée. Différences cumulées RED : 576 octets items, 24 octets boxes, zéro secteur. Les items non sélectionnés sont également contrôlés.

Chaque passage a trois méthodes unittest : couverture cartésienne, oracle cible complet, égalité stdout native/cible complète. Ce ne sont pas 128 méthodes : une compilation fraîche i386, 128 processus natifs et 128 exécutions cible par passage. 11296 visites de hooks dont 288 entrées de doubles par passage, pas des instructions retirées. Un rejeu RED/GREEN représente deux compilations et 256 processus natifs/exécutions cible. L’oracle Python construit les octets attendus sans employer les résultats natifs.

## Chronologie et attribution

Worker original : RED comportemental, 48 sous-cas FAIL, exit 1, 14:33:52.708586–14:34:25.052901 ; copie corrigée absente selon prepatch.json à 14:34:46.291330 ; GREEN fraîchement compilé, trois méthodes PASS, exit 0, 14:35:04.629709–14:35:36.969700. Suite/moteur/harness inchangés entre RED/GREEN. Le rejeu worker reproduit 256 lignes intégralement identiques ; son audit post-production ne constitue pas une revue indépendante. La déclaration prépatch n’est pas une observation rétrospective du reviewer.

Parent réellement exécuté avant publication, depuis /var/www/projects/TOMB5 : PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python -B build/reverse/autonomy-20260909/re757/replay.py parent. parent-replay.json consigne RED 14:40:50.514055–14:41:23.059676, exit 1 attendu ; GREEN 14:41:23.059938–14:41:55.706767, exit 0 ; audit 14:41:55.707040–14:41:58.778758, exit 0. parent-audit.log confirme 128 cas, 48 divergences RED, zéro GREEN, 512 images RAM. Exit global 0 et 256 lignes identiques explicitement communiqués par le parent ; aucun intervalle global parent inventé.

La revue indépendante review/review.md et review/review.json rapporte un rejeu personnel d’une copie byte-identique du driver sous review/, gardes conservées : 14:43:07.803942–14:44:16.984190 Paris, exit 0 ; RED exit 1 puis GREEN et audit exit 0. Deux compilations fraîches ; 256 lignes identiques aux originales. Son independent_check.py, sans import du moteur, de la suite ou de l’audit producteur, reconstruit séparément les effets depuis la RAM initiale : exit 0, résultat à 14:46:07.499990. Il compare également les 256 lignes parent : 512 comparaisons de lignes au total, pas 512 cas distincts. Le rédacteur lit ces archives, aucun rejeu privé dans cette publication metadata-only.

review/review.json historique porte PASS mais classait deux limites dans security_concerns : incohérence de schéma conservée, non occultée. review/verdict-clarification.json fournit PASS, security_concerns=[] et logic_errors=[] ; clarification documentaire seulement, sans nouveau rejeu ni nouvel audit comportemental. Les limites restent applicables. Le HANDOFF initial « parent/reviewer en attente » précède ces preuves ; aucune archive ancienne n’est réécrite.

## Observation, provenance et exclusions

512 images initiales/finales de 2 Mio sont archivées compressées par paire RED/GREEN ; le reviewer les décompresse et vérifie leurs hashes. Audit indépendant des buffers, stdout, événements et RAM hors effet attendu, stack autorisée exclue. Observation : stores inférés par décodage préexécution, pas trace exhaustive des stores retirés ; RAM finale seule insuffisante pour détecter les écritures transitoires restaurées ; pas de contrôle général des lectures ni de sûreté mémoire globale.

SoundEffect, ExplodingDeath2, RemoveActiveItem : trois doubles ABI à retour normal sans effets mémoire, corps authentiques non exécutés. Retour, stack et liens vérifiés dans la borne ; aucune valeur de retour ne sert d’oracle matériel. Fixtures synthétiques de quatre items, huit secteurs, quatre boxes et une room ; flags/état uniformes entre items d’un cas. Les dimensions indépendantes ne couvrent pas les états hétérogènes simultanés ; indices négatifs/extrêmes et domaine complet de coordonnées exclus.

Compilation de la TU privée entière g++ i386 O0 avec PSXPC_TEST/PSX_VERSION et élimination des sections inutilisées ; ABI 32 bits, pas de build complet du jeu, pas de sanitizer. 314 entrées projet épinglées ; en-têtes système/toolchain non scellés, environnement non hermétique. Boot et copie disque authentifiés par le moteur et contrôles reviewer ; pas de nouveau Ghidra ni d’exit headless revendiqué. La revue vérifie la conservation de 4687 fichiers préexistants RE757, 1567 entrées du sceau et 106 entrées historiques RE756 : pas empreinte exhaustive de tous les binaires historiques. Les liens de lecture ne sont pas une barrière OS. Gardes git sur diff HEAD, index inclus mais non tous les non-suivis ; ledgers locaux, pas horodatages tiers infalsifiables. Pas de caller runtime réel, sauvegarde, boot complet, matériel ou concurrence ; pas de preuve gameplay.

## Validation publique

GREEN documentaire : 1 test réussi en 0,06 s, exit 0, 14:55:11.836090–14:55:12.119978 Paris. Suite exacte de la story RE-756 avec le nouveau test ajouté : 1 218 tests réussis en 50,92 s, exit 0, 14:55:26.306524–14:56:17.492861 Paris ; durée processus 51,186050 s.

Revalidation après insertion des résultats : publication RE-757, prédécesseur RE-756 et dashboard, 52 tests réussis en 0,25 s, exit 0, 14:56:44.252016–14:56:44.722071 Paris (publication/final.log). Le passage final-text recontrôle ensuite le texte figé ; son résultat reste dans les logs ignorés.

Test documentaire limité à cette story et à la nouvelle section RE-757 ; handoff courant contrôlé séparément. Aucune lecture/importation privée dans le test ; adresses, dumps, opcodes et code cible brut interdits dans les nouveaux textes. Sections/ancres/contrats historiques préservés ; aucun générateur historique lancé pour écrire les documents versionnés. Les tests préexistants de génération emploient leurs répertoires temporaires.

Commandes publiques, cwd /var/www/projects/TOMB5 :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re757_smash_correction_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

Journaux immédiats sous build/reverse/autonomy-20260909/re757/ : publication/red.log, publication/green.log, publication/suite.log, publication/final.log et publication/commands.json. Chaque lancement public est enveloppé par publication/record.py : commande/cwd/environnement/start et hashes d’entrée écrits avant lancement ; end/exit/durée processus/hash de sortie écrits immédiatement après. Les durées pytest restent distinctes des durées processus. Ces tests vérifient la publication, pas une nouvelle équivalence cible.

## Handoff

Après RE-757 : correction privée vérifiée par worker, parent et revue indépendante ; prochaine unité bornée PRODUCTION, non implémentée ici. Exiger RED/GREEN public sur la vraie TU avant/après patch minimal de transmission, évaluation des backends affectés par la source partagée, tests de régression sur matrice indépendante et buffers complets/événements, puis revue indépendante avant livraison. Ne pas assimiler preuve i386 privée à validation de tous les backends ; ne pas élargir services, objets ou gameplay dans cette intégration.

Autorisation courante du 9 septembre 2026 : recherche jusqu’à 23:25 Paris, clôture jusqu’à 23:45 Paris. Cette publication n’exécute ni n’autorise implicitement une nouvelle intégration ; gardes historiques inchangées ; après publication ne pas relancer, assouplir ou resealer les scripts privés. Au moment de la rédaction prérevue, aucun staging ni commit/push effectué. Aucun job créé ni changement de production. Livraison limitée aux trois fichiers publics autorisés ; preuves brutes exclusivement ignorées. Rapport interdit jamais ouvert ni modifié. Revue finale indépendante de publication PASS (final-review/review.json) ; 52 tests frais réussis. Suite publique rejouée par le parent : 1 218 tests réussis en 51,38 s, exit 0 ; parent-public-suite.json/log. Aucun rejeu privé supplémentaire.
