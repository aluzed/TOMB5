# RE-751 — Boucle productrice complète des salles, preuve différentielle bornée

## Statut

**PASS borné pour publication metadata-only ; aucun correctif de production justifié.** Extension de RE-750 aux 116 salles du cas normal Name=0. Aucun écart comportemental dans le cas exécuté ; aucune certification des mots transformés comme pointeurs utiles.

## Tracker

- [x] Preuve privée et revue indépendante fraîche avant toute publication suivie.
- [x] Producteur cible jusqu’à la fin des 116 salles, comparaison avec la vraie GAME/SETUP.C recompilée.
- [x] Buffers complets, champs, qualifications et descripteurs audités indépendamment.
- [x] Audit parent des artefacts et reconstitution indépendante avant publication.
- [x] RED documentaire observé : story absente, une assertion attendue.
- [x] GREEN documentaire : 1 test réussi ; suite publique RE750 étendue à RE751 : 1 205 tests réussis.
- [ ] Dépendances post-room résolues et nouvelle borne prouvée avant toute extension.
- [ ] Trajet réel du consommateur, corps GTE, retour complet du chargeur et matériel.

## Exécution et borne

S_LoadLevelFile → dispatch → LoadLevel conserve CPU/RAM/curseur, depuis un état initial synthétique, Name=0. Boot et en-tête authentifiés, module extrait hashé et comparé à la copie historique, image entière de la relocation réelle comparée à l’interpréteur indépendant. Chaque visite d’instruction cible est authentifiée contre le boot ou le module relocalisé ; aucune instruction cible patchée.

La cible termine les **116 salles**, effets du dernier **delay slot** du backedge inclus, puis s’arrête **avant la remise à zéro** suivante et avant les opérations post-room. Compteur final et curseur vérifiés, aucune visite du suffixe post-room observée. **1 584 596 visites** du hook comprennent **64 interceptions** et **une visite d’arrêt** : **pas un compte d’instructions retirées**.

Compilation fraîche de la vraie **GAME/SETUP.C**, harness séparé, i386 O0 **32 bits**, en-têtes normaux ; DISC_VERSION=1, DEBUG_VERSION=0, PSX_VERSION=1, PSXPC_TEST=1. Pointeur et long 32 bits, Level 228 octets et room_info 80 octets vérifiés. Breakpoint matériel GDB à **SETUP.C:1274**, **i=116**, **j=24**. Capture et désassemblage neuf situent l’arrêt avant le chargement local immédiatement suivi d’une **écriture absolue nulle** non résolue. L’inférieur est détruit, sans retour LoadLevel. Bornes comparables sur l’état observé, pas sur tous les registres.

**Le lien conserve `--unresolved-symbols=ignore-all` : exécutable dangereux hors de cette borne.** Il faut résoudre les dépendances avant toute extension ou exécution hors de cette protection. Deux avertissements extern-initialized historiques, -Wno-narrowing ; pas de sanitizer.

## Comparaisons et qualification

| Observation | Résultat et limite |
|---|---|
| Lectures | 7 buffers utiles complets comparés, 680 secteurs ; GPU/SPU et table audio vérifiés selon leurs contrats |
| Frames | 329 832 octets inchangés |
| RoomInfo | 524 000 octets intégralement comparés ; normalisation limitée aux 3 364 mots réellement transformés |
| Transformations | 580 champs data/door/floor/light/mesh et 2 784 additions |
| Audit reviewer additionnel face à RE750 | Exactement 3 335 mots nouveaux différents, aucun autre octet ; frames identiques |
| Allocation | 5 allocations, 3 libérations ; descripteurs complets normalisés [curseur relatif, utilisé, libre] avant/après chaque événement, ordre et état final concordants |
| Lectures et allocateur | Invariants cible aux lectures, mais pas aux retours de lecture host : descripteurs non capturés ; allocateur double host, descripteur reconstruit depuis used, pas la TU MALLOC réelle |
| Champs audités par le reviewer | 580 intervalles : 461 non vides entièrement dans l’allocation, 119 de longueur nulle |
| Curseur final relatif | 205 856 ; 318 144 octets restants, ni dépassement ni preuve du contenu post-room |

**161 entrées actives** selon les comptes bruts ont toutes leur **valeur de départ** dans leur bloc data. **1 155 valeurs** transformées hors allocation sont toutes inactives selon ces comptes ; chacune des 116 salles contient au moins une valeur hors allocation. Le reviewer a indépendamment vérifié les comptes dans **[0,24]** ; le probe principal les classe sans cette assertion explicite.

Une valeur de départ dans le bloc ne prouve ni la taille de l’objet accessible, ni sa validité sémantique, ni son innocuité universelle. Le producteur additionne ces valeurs sans les utiliser comme adresses de déréférencement ; **consommateur roomlet non exécuté** dans RE751. **GTE non exécuté**. La normalisation ne masque pas les autres octets du buffer ; elle ne transforme pas chaque mot en pointeur valide.

## Revue indépendante, audit parent et provenance

Revue indépendante commencée le 9 septembre 2026 à 09:37:22 Europe/Paris, sur **HEAD prépublication 8265c8c08d017a79bddb734eb1f23a9f12da4d4f**. Le timeout précédent était un handoff incomplet, pas un échec de preuve.

Le reviewer a sauvegardé **67 fichiers** avant rejeu puis exécuté **6 tests en 17,011 s**, démarrés à 09:38:15 Paris : **deux exécutions** nouvelles du producteur cible, **une véritable recompilation** de GAME/SETUP.C avec harness séparé et exécution du nouvel ELF sous GDB. Son mtime est renouvelé et ses octets reproductibles. **44 fichiers** JSON/CSV/bin identiques à la sauvegarde, comprenant des métadonnées conservées : pas 44 nouvelles exécutions. Seul host-output.log diffère parmi les 67 fichiers (bannière debuginfod, adresse argv et PID), sans différence de résultat.

Le reviewer a aussi exécuté review_check.py, exit 0 : décodage indépendant sans plan_rooms, reconstitution du buffer entier, validation de chaque ligne fixups/room-fields/qualification, champs capturés, descripteurs et ordre, traces de fin de boucle et différences RE750. Python optimisé réellement essayé et rejeté. Aucune suite publique exécutée dans cette revue privée.

**Vérification par audit parent à 09:43 Paris**, avant publication : review_check.py, exit 0, 44 fichiers identiques, 116 salles, 3 364 transformations, 3 335 différences nouvelles, 161 valeurs actives dans data et 1 155 hors allocation toutes inactives ; borne vérifiée. **pas de rejeu cible ni de compilation par le parent** pour RE751 : cet audit ne doit pas être confondu avec les six tests frais du reviewer. La présente publication ne relance aucun probe privé gardé et n’ouvre aucune recherche.

La garde propre RE751 vérifie HEAD, git diff HEAD (index inclus), ignorance du probe, fenêtre du 9 septembre 2026 jusqu’à **23:25 Paris** et **182 dépendances** par manifeste lui-même hashé. Contrôles à l’import/début, **non continus** ; **code RE751 non auto-épinglé** dans ce manifeste, mais sauvegardé et vérifié inchangé par la revue. Les **en-têtes système** et exécutables outils ne sont pas couverts par ces hashes. Le complément reviewer a prétraité séparément les deux TU : toutes les dépendances non système couvertes après normalisation, hors host.cpp lui-même sauvegardé. Premier essai sur chemins non canonicalisés corrigé sans modifier probe ou manifeste ; versions courantes cohérentes avec toolchain.json.

Les **gardes historiques** ne sont ni appelées, ni désactivées, ni modifiées. La publication change volontairement l’état accepté par la garde prépublication. Futur rejeu uniquement dans une **nouvelle unité explicitement autorisée** avec provenance propre, sans affaiblir RE751 ni ses prédécesseurs ; aucune promesse de rejeu inconditionnel après publication.

Preuves privées conservées dans `build/reverse/autonomy-20260909/re751/` : `review.md` fait autorité ; `review-fresh-tests.log`, `review-check.log`, `review-audit.json`, `review-run.json`, `review-baseline-manifest.json`, `review-dependency-audit.json`, `review-optimized-rejection.log`, `review-provenance.diff`, `host-command.json`, `debug-command.json`, `host-build.log`, `host-output.log` et `host-boundary.json`. Aucun artefact brut publié ou suivi.

## Validation publique

Le test public vérifie uniquement la documentation, pas la preuve binaire. RED : **1 échec attendu en 0,06 s**, story absente ; journal privé `publication-red.log`. GREEN : **1 test réussi en 0,05 s**, `publication-green.log`. Suite RE750 inchangée plus le nouveau test RE751 : **1 205 tests réussis en 50,81 s**, `publication-suite.log`. Journaux dans le dossier privé RE751 ; aucun probe gardé exécuté.

```sh
python3 -m pytest tests/reverse/test_re751_rooms_publication.py -q
python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

## Limites

Allocation/CD/GPU/SPU host sont des doubles ; frontières SDK/CD cible explicites. Pas de matériel, timing, concurrence, boot complet, autres niveaux ou erreurs, renderer/GTE, boucle consommateur, retour du chargeur ou comparaison native ROOMLOAD/ROOMLET. **pas de sûreté mémoire générale**, ni hooks généraux de contrôle mémoire, ni preuve sur la RAM adjacente ou tous les accès. Les tests synthétiques de corruption/bornes restent étroits, pas un moteur général de mutation ; la conclusion repose aussi sur les assertions réelles de buffers et l’audit indépendant.

## Handoff

**Après RE-751 : résoudre les dépendances** natives dangereuses au-delà de la boucle des salles, notamment les globales liées à des adresses nulles, avant de déplacer l’arrêt. La prochaine unité cohérente doit prouver ces dépendances et une borne post-room explicitement attribuée ; le trajet réel du consommateur et le GTE restent ouverts, pas implicitement validés par le producteur complet. Reconstruction seulement si un écart observable est prouvé. Historique, générateurs et sources de production inchangés ; aucun commit dans cette publication.
