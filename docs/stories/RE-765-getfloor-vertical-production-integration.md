# RE-765 — GetFloor : preuve privée et intégration verticale bornée

## Tracker

- [x] Contrôle initial le 11 septembre 2026 à 20:15:35 Europe/Paris : HEAD be7b08c218b12a8fe57d748b197f5d3fff5cb818, arbre suivi et index propres. RE765 sans conflit de story.
- [x] Preuve revalidée et revue privée lues ; aucun rejeu privé dans cette intégration, gardes historiques inchangées.
- [x] Test public synthétique sur TU entière écrit avant patch ; RED comportemental archivé avant correction, GREEN recompilé avec test identique.
- [x] Correction production minimale gardée ; alternative historique conservée.
- [x] RED documentaire observé avant cette publication ; suite publique et validation finale consignées dans les ledgers de livraison.
- [x] revue indépendante production PASS attribuée aux artefacts de revue production ci-dessous ; aucun replay parent revendiqué.
- [ ] Généralisation à tous callers, architectures, chaînes verticales et gameplay non établie.

## Preuve privée consommée, non réexécutée ici

La preuve est attribuée à build/reverse/autonomy-20260911/re765-revalidation/HANDOFF.md. Le PASS indépendant est celui des artefacts build/reverse/autonomy-20260911/re765-independent-review/rapport.md et re765-independent-review/verdict.json (passed=true, listes bloquantes vides), pas d’un message supposé du reviewer. Leur replay rapporte 442 cas divergents en baseline (172 corpus et 270 synthétiques), zéro après correction ; valeurs et événements portent sur les mêmes cas, pas 884. Chaque phase comprend 15 niveaux et 9 fixtures, 8070 appels cible. Les 91444 cellules inventoriées ne sont pas toutes exécutées verticalement. Le reviewer rapporte deux compilations de TU par phase, un lien ELF32 i386 et un import Ghidra frais par phase. Ce sont ses exécutions historiques du 11 septembre, pas des commandes exécutées dans cette intégration.

La preuve distingue propriétaire courant et room zéro ainsi que polarité, y compris égalité. Les 450 contrôles privés floor négatifs couvraient neuf paires de minima : 180 dessous, 90 égaux, 180 dessus. La revue recommande la correction gardée, mais son PASS privé ne remplace pas la revue du delta production.

## Delta production et portée

Dans SPEC_PSXPC_N/GETSTUFF.C, uniquement le test après floor-helper négatif : sous PSX_VERSION && PSXPC_TEST, y < r->minfloor décide le retour ; dans l’alternative, y >= room->minfloor reste inchangé. Aucun autre changement : clamp RE762, GetDoor réel et sa largeur char/normalisation unsigned char, helper ceiling et corps des helpers restent intacts. Aucun patch de la TU privée non gardée n’est copié en bloc.

Le gate est une configuration, pas une architecture. Compilation réellement testée : ELF32 i386, g++ -m32 -O0, frame pointer conservé, PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Cette dernière option est celle du probe, pas la valeur CMake par défaut. Les quatre combinaisons booléennes sont vérifiées par prétraitement de la branche seulement : pas quatre builds de backends. Autres backends et autres architectures non validées, y compris au sein de la configuration sélectionnée.

## Régression publique synthétique

648 cas indépendants : deux rooms courantes (1 et 2) × trois minima courants × trois minima room zéro × trois relations au seuil courant (dessous/égal/dessus) × trois retours helper (-1/0/+1) × lien absent/actif × floor/ceiling. La construction séparée de la matrice vérifie l’ensemble exact. 54 contrôles floor négatifs avec lien actif, 18 pour chaque relation, discriminent indépendamment propriétaire et polarité ; égalité exclut une comparaison non stricte. Les minima zéro parcourent leur propre axe : pas un alias du minimum courant. Contrôles ceiling et helpers nuls/positifs conservés. Les seuils ceiling sont ceux de r->y, sans modification de leur contrat. Lien absent signifie sentinelle 255, pas destination valide vers 255. Destination verticale ordinaire 3 ; pas de chaîne multi-saut ni portail dans cette nouvelle matrice.

tests/emulator/test_getfloor_vertical.py compile la TU entière réelle avec ses en-têtes ordinaires et un harness séparé : GetFloor, GetDoor réel et les deux helpers réels, aucun double ni symbole non résolu autorisé. Deux compilations, un lien frais et 648 processus natifs par passage. Appel helper direct contrôlé dans chaque processus puis GetFloor réel ; tous reviennent normalement sous timeout. Le lien élimine les sections inutilisées : pas un build complet du jeu.

Oracle Python distinct du harness : reconstruction intégrale des rooms (320 octets), cells (512 octets) et floor data (8 octets), pointeurs obtenus depuis le symbole cells de l’ELF frais. Tous les octets sont comparés avant/après, y compris records non sélectionnés et mots sentinelles adjacents. Comparaison du résultat room/pointeur et des événements ordonnés entrée/sortie de GetFloor, GetDoor et du helper appelé, avec cellule intermédiaire et room observée. Instrumentation aux frontières de fonctions, pas de trace native exhaustive des écritures transitoires. Les retours helpers sont contrôlés par appel direct, pas par interception du registre retour à chaque sortie instrumentée.

## Résultats publics et archives

Sous build/reverse/autonomy-20260911/re765-integration/ :

- red.log : premier lancement incomplet, 652 erreurs de fixture et un test réussi, parent du répertoire pytest absent ; ce n’est pas un RED comportemental. Correction du seul recorder, aucun changement du test ou de production pour résoudre ce problème.
- red-behavior.log/json : 20:18:47.638143–20:18:49.779849 Paris, exit 1, 37 échecs et 616 réussites : 36 divergences comportementales et une sélection de gate. Compilation/link et 648 sorties natives réussis. red-archive.json a figé baseline, test, logs et 666 fichiers à 20:19:04.876735, avant patch.
- green.log/json : 20:19:14.857451–20:19:16.866117 Paris, exit 0, 653 tests réussis : 648 cas, quatre gates et un contrat de matrice. Compilation fraîche, test byte-identique au RED.
- publication-red.log/json : 20:19:54.919645–20:19:55.201954 Paris, exit 1, story absente et contrôle append-only réussi.
- suite.log/json et final.log/json : suite exacte RE764 augmentée du seul fichier documentaire RE765 ; tests/emulator découvre automatiquement la nouvelle régression. Les ledgers donnent argv, cwd, début/fin, exit et hashes avant/après. Résultats de suite insérés après exécution, puis revalidés.

Le recorder neuf refuse les labels existants, vérifie HEAD/index, emplacement ignoré et échéance locale de livraison 20:40. Il ne lance aucun producteur privé. La fenêtre du recorder est historique, pas une nouvelle autorisation. Cette clôture documentaire reste bornée par la délégation actuelle ; au moment de cette étape, staging et commit en attente. Les tests publics ordinaires restent rejouables sans dépendance à cette fenêtre.

Suite complète réellement exécutée : 3753 tests réussis en 58,63 s pytest, exit 0, 20:22:17.771061–20:23:16.773943 Paris (59,002265 s monotoniques). Audit auteur post-production : exit 0, 20:23:29.506648–20:23:29.728638, audit-invocation.json, audit.log et audit-result.json. Sans import du test/oracle public, reconstruction séparée des buffers complets et événements RED/GREEN/suite, 648 cas par passage ; 36 divergences finales et 36 événements divergents en RED, intersection = union = 36, zéro en GREEN/suite. Hypothèses incomplètes : propriétaire seul 54 désaccords, polarité seule 18 sur les 54 témoins négatifs. Les 666 fichiers RED archivés sont inchangés et le delta source exact est contrôlé. Cet audit du même auteur n’est pas une revue indépendante production.

Validation finale worker : 3753 tests réussis en 58,55 s pytest, exit 0, 20:24:04.726878–20:25:03.646070 Paris, attestés par re765-integration/final.json et final.log. Le timeout de transmission n’est pas un échec de cette commande. Revue indépendante production PASS attribuée à build/reverse/autonomy-20260911/re765-production-review/rapport.md, re765-production-review/verdict.json (passed=true, listes bloquantes vides) et re765-production-review/final-verification.json (unchanged=true, verdict_valid=true). Exécution distincte du reviewer : 3753 tests réussis en 58,66 s pytest, exit 0, 20:26:33.751829–20:27:32.798585 Paris, tests-invocation.json et tests.log dans ce répertoire de revue. Ces résultats worker et reviewer sont lus dans leurs artefacts, pas réexécutés par cette clôture ; aucun replay parent revendiqué. Le PASS couvre le snapshot antérieur à ces changements documentaires ; il ne prétend pas être une revue indépendante du présent delta documentaire.

## Limites et progression

Correction étroite intégrée et testée sur le backend/configuration attribué ; pas de preuve gameplay, matériel, boot complet, concurrence ou sûreté C++ universelle. Pas de sanitizer dans cette unité ; ABI, optimisations, coordonnées et domaines restent bornés. Les snapshots ne sont pas toute la mémoire du processus ; pas de preuve d’absence de stores transitoires. En privé, stores inférés et interpréteur logiciel ne valent pas oracle matériel, et images RAM finales complètes par appel non archivées. Dépendances -MMD par TU, sans environnement hermétique ni headers système épinglés.

Historique documentaire et gates conservés ; dashboard strictement append-only avec une section active RE765. Les anciennes recommandations restent des jalons, pas le handoff actif. Aucun asset, dump cible, opcode ou pseudocode cible dans les fichiers publics. Rapport technique laissé volontairement non ouvert conformément à la consigne actuelle de préservation, sans inventer d’interdiction historique.

## Commande publique exacte

Depuis /var/www/projects/TOMB5, sélection RE764 inchangée plus documentaire RE765 :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py tests/reverse/test_re761_getfloor_correction_publication.py tests/reverse/test_re762_getfloor_integration_publication.py tests/reverse/test_re763_getdoor_corpus_publication.py tests/reverse/test_re764_getfloor_vertical_publication.py tests/reverse/test_re765_vertical_integration_publication.py -q
```

Le ledger suite.json conserve aussi les options de cache et basetemp effectivement exécutées.

## Handoff

Après RE-765 : unité close, revue indépendante production PASS sur le snapshot examiné, puis synchronisation documentaire. Au moment de cette clôture documentaire, staging et commit en attente ; publication par commit autorisée au parent par la délégation actuelle, sans staging ni commit effectué ici. Aucun replay parent revendiqué ; ne pas affaiblir les guards privés pour accepter l’arbre modifié. Prochaine recherche proposée, non effectuée dans cette unité : délimiter une preuve des chaînes verticales multi-sauts avant toute nouvelle correction. Aucun nouveau ticket ouvert. La largeur des IDs GetDoor, les autres chemins et la preuve générale GetFloor restent hors périmètre.
