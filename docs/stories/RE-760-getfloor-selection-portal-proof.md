# RE-760 — GetFloor : sélection de cellule et portail, divergence bornée

## Tracker

- [x] HANDOFF privé et revue review/verdict.json lus ; PASS avec réserves non bloquantes, security_concerns et logic_errors vides. Base 5f5b3515 ; contrôle du 9 septembre 2026 à 17:21:04 Europe/Paris.
- [x] Preuve privée existante et attribution parent vérifiées documentairement ; aucune nouvelle recherche.
- [x] TDD documentaire strict : nouveau test avant docs ; RED observé le 9 septembre, 17:22:17.865552–17:22:18.140838 Paris, exit 1, 1 échec attendu (story absente), 1 réussite.
- [x] Publication limitée à story, dashboard actif et nouveau test ; aucun patch.
- [ ] Correction, domain proof des grands IDs, équivalence générale et gameplay non établis.

## Résultat et causes caractérisées

**PASS de caractérisation bornée, PAS équivalence : 3888 cas, 1044 triplets divergents, 972 différences room_number et 555 différences d’indice de cellule.** Décomposition disjointe : **2844 accords, 489 room seule, 483 room et cellule, 72 cellule seule** ; les deux totaux de différences se recouvrent et ne s’additionnent pas. Triplet comparé : room_number, room propriétaire du pointeur, indice de cellule ; pas les adresses absolues entre architectures/processus. Chaque pointeur observé couvre un enregistrement complet de 8 octets dans les 64 cellules synthétiques de sa room ; celle-ci égale room_number.

Matrice ordonnée exacte : 2 formes × 9 décalages X × 9 décalages Z × 3 Y × 8 destinations. Formes initiales 5×6 et 4×3, destinations transposées ; origines initiales X/Z 2048/−3072, autres rooms −1024/1024. Décalages −1025, −1, 0, 1023, 1024, 3071, 4096, 6144, 8192 ; Y −1, 1024, 2048 ; destinations −1, 17, 127, 128, 254, 255, 256, 511, chacune sur 486 cas.

| Destination | Triplets divergents | Room | Cellule |
|---|---:|---:|---:|
| −1 (absence de floor-data) | 36 | 0 | 36 |
| 17/127/128/254, chacune | 0 | 0 | 0 |
| 255 | 36 | 0 | 36 |
| 256 | 486 | 486 | 0 |
| 511 | 486 | 486 | 483 |

Le **clamp haut Z**, lorsque X relatif est non positif, choisit X cellule 1 côté cible contre y_size−2 côté source. La forme où y_size−2 vaut 1 masque le défaut. Les 72 cellule seule restent dans la room initiale ; des cellules intermédiaires différentes contenant le même portail peuvent conduire au même pointeur final : accord final ne prouve pas chaque sélection intermédiaire.

Le retour GetDoor est normalisé sur **16 bits signés** côté cible, mais stocké dans **unsigned char** par GetFloor natif. Destination 256 : room 256 cible contre 0 native ; 511 : room 511 cible contre room initiale 1 native, car l’octet 255 devient sentinelle. **255 explicitement testé comme destination DOOR**, sentinelle dans les deux versions ; aucun short négatif testé comme destination DOOR. −1 est le contrôle sans floor-data, pas une destination négative. Ces fixtures ne prouvent pas la validité des IDs supérieurs à 255 dans un niveau réel.

## Exécution, authenticité et limites

3888 appels cibles GetFloor, 3888 processus natifs, **6804 entrées cibles GetDoor**, **2916 visites de store** de room inférées, **470232 visites de hook**, maximum 145 par cas : pas des instructions retirées. **3 méthodes unittest** privées GREEN après génération, pas 3888 méthodes. Le RED privé archivé comporte trois absences de probe/résultats : **pas un RED comportemental** ; il ne démontre pas une correction test-first.

GetFloor entrée→retour, GetDoor réellement exécuté, aucun service doublé. Cible authentifiée contre le boot extrait de l’ISO locale, header et payload complets vérifiés ; pas de provenance commerciale externe démontrée. CPU/RAM neufs, GP/stack/retour injectés, instructions visitées authentifiées, intervalles complets de lectures contrôlés, retour/SP vérifiés sous borne 400 visites. Pit/sky sentinelles 255, floor=8 et ceiling=0 : branches de hauteur traversées, helpers triangle non exécutés, aucune traversée verticale. Les 3888 séquences ordonnées de lectures ont été reconstruites par le reviewer ; stores inférés des instructions/registres, pas tracés par hook d’écriture.

La vraie TU SPEC_PSXPC_N/GETSTUFF.C inchangée, identique à HEAD, a été fraîchement compilée et exécutée par le reviewer : i386, g++ -m32 -O0, PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DEBUG_VERSION=0, DISC_VERSION=1. Pointeur/long 32 bits, FLOOR_INFO 8 et room_info 80 octets contrôlés. Harness compilé séparément, dépendances par TU contrôlées contre 293 inputs scellés ; lien avec élimination de sections sans ignorer les symboles non résolus. Désassemblage natif frais confirmant la conversion étroite.

RAM cible de 2 Mio comparée en direct sauf room_number attendu ; **images RAM non archivées**. Le reviewer a contrôlé code et exécution de l’assertion, pas refait une comparaison intégrale depuis les JSON seuls. Côté natif, tableaux rooms/cells/words comparés avant/après, pas toute la mémoire du processus ni absence d’écritures transitoires restaurées. Aucune équivalence des traces natives/cibles, ABI générale ou adresses absolues.

Archives Ghidra inspectées, pas de nouveau lancement par le reviewer : import raw MIPS little-endian, script ciblé, projet temporaire supprimé, pas une conservation démontrée d’un projet existant. Ledger historique exit 0 ; avertissement d’overlap GetDoor et échec de reconstruction du retour indirect GetFloor conservés. Décodage indépendant de 202 instructions ; instructions authentiques et exécution fondent le retour, pas la signature décompilée. Aucun nouveau scan de callers.

Fixtures synthétiques et dimensions positives bornées : aucun caller englobant, chargement réel, validité réelle des portails, cycles/chaînes longues ou domaine général des dimensions/IDs démontrés. Pas de preuve gameplay, matérielle PS1, GTE/MMIO, concurrence ou sauvegarde ; autres backends non validés, pas de build jeu complet ni sanitizer. Toolchain/bibliothèques/en-têtes système non scellés, -MMD ne les couvre pas ; pas de preuve de portabilité universelle des décalages signés. Le test producteur dépend d’attentes sérialisées ; l’audit reviewer ferme la matrice exacte pour cette livraison sans modifier le contrat historique.

## Attribution de la vérification

**Revue indépendante PASS**, review/verdict.json et HANDOFF.md (aucun review/review.md présent) : réserves conservées, pas équivalence. Reviewer-01 réellement exécuté, exit 0, 17:13:13.322058–17:14:11.271312 Paris le 9 septembre 2026 ; vraie TU recompilée. Audit indépendant post-producteur **review/audit.py** exécuté par le reviewer, exit 0, 17:16:06.330578–17:16:06.672405 Paris, ledger review/audit-run.json. Initial et worker-replay sont des archives inspectées par ce reviewer ; worker-replay exit 0 malgré le timeout de remise signalé. Ce PASS porte sur la preuve privée, pas sur une revue indépendante de cette publication.

Selon les vérifications explicitement transmises par le parent, il a réellement exécuté replay.py parent-01, exit 0, puis relu le verdict et comparé les fichiers result.json complets : initial/worker-replay/reviewer-01/parent-01 **byte-identiques**, SHA256 2c34ee2aeb2f6aa8ac30fb0ae59b5d9297a822a5c7b01cd0d5ec36cca028760b. Ledger parent-01-run.json lu ici : intervalle du processus enfant probe **17:19:20.619538–17:20:17.882597** Paris, exit 0 ; ce n’est pas un intervalle mesuré séparément du wrapper extérieur. Le **parent n’a pas exécuté l’audit indépendant** ; cet audit reste attribué au reviewer. Le HANDOFF antérieur ne revendiquait pas encore les actions parent ultérieures. Aucune de ces exécutions privées n’est celle du worker de publication.

## Validation publique

Aucun rejeu privé pendant cette publication ; gardes historiques inchangées. Aucun générateur historique exécuté ni brut propriétaire publié. Journaux sous build/reverse/autonomy-20260909/re760/publication : red.log, green.log, suite.log, ledgers homologues et commands.json avec commandes exactes, cwd, intervalles, exit et hashes avant/après. Test documentaire inchangé entre RED et GREEN ; limites vérifiées séparément dans story et section RE-760. Les sections historiques du dashboard sont comparées byte-for-byte à la base Git, hors aperçu/handoff actifs.

GREEN documentaire : 2 tests réussis en 0,06 s, exit 0, 17:24:42.373298–17:24:42.640575 Paris. Suite exacte RE-759 augmentée du nouveau test : 1 357 tests réussis en 51,79 s, exit 0, 17:24:42.672010–17:25:34.745937 Paris. Revalidation après insertion de ces résultats enregistrée séparément dans publication/final.json et final.log. Ces tests publics du worker de publication ne sont pas les 3 méthodes privées ni un rejeu parent/reviewer.

Commande exacte depuis /var/www/projects/TOMB5, sélection littérale RE-759 avec le nouveau test ajouté :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py tests/reverse/test_re756_smash_publication.py tests/reverse/test_re757_smash_correction_publication.py tests/reverse/test_re758_smash_integration_publication.py tests/reverse/test_re759_getdoor_publication.py tests/reverse/test_re760_getfloor_publication.py -q
```

## Handoff

Après RE-760 : caractérisation sélection/portail clôturée sans correction. Proposition cohérente suivante seulement : correction privée du clamp haut Z sur vraie TU, **TDD comportemental RED avant correction**, formes sensibles et contrôles masquants, bords X/Z et portails. Séparer les room IDs supérieurs à 255, qui exigent une **domain proof** avant toute correction de largeur. Aucun patch ni nouvelle unité exécutés dans cette publication.

Les gardes historiques HEAD/arbre propre/date peuvent intentionnellement refuser le rejeu après publication ; ne pas les modifier, désactiver ou resealer. Toute reproduction future exige une nouvelle unité de provenance autorisée. Recherche jusqu’à 23:25 Paris et clôture jusqu’à 23:45 Paris le 9 septembre 2026, aucun nouveau job. Au moment de cette remise : aucun staging, commit ou push ; nouveaux story/test non suivis. Rapport explicitement interdit jamais ouvert ni modifié.
