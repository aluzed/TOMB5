# RE-754 — Preuve corrective boxes sur vraie TU privée

Publication metadata-only ; résultats privés qualifiés, pas correction de production.

## Tracker

- [x] Revue/handoff et logs parent lus ; attribution séparée.
- [x] RED documentaire observé : story absente, 1 échec en 0,07 s, exit 1.
- [x] Résultats bornés, limites et handoff publiés.
- [x] GREEN documentaire : 1 test en 0,05 s, exit 0. Suite publique RE753 étendue RE754 : 1 208 tests réussis en 50,51 s, exit 0 (publication-suite.log).
- [ ] Intégration du patch minimal au backend prouvé sous TDD : prochaine unité, non exécutée ici.

## Résultat privé et correction

PASS de preuve corrective bornée privée sur copie de la vraie TU GAME/SETUP.C ; aucun patch de production. Seules deux références d’indice deviennent i - 1 ; garde positive, initialisation et décrément inchangés. Harness séparé sans copie de LoadLevel, ABI i386 -m32 -O0 -g. RED archivé : six méthodes, 13 échecs subtests inclus, exit 1 ; pas réexécuté par le reviewer. Ses 247 fichiers sont vérifiés par hashes et reconstruction indépendante : un octet authentique différent à overlap[3], hors limite logique boxes mais dans l’allocation, pas un dépassement d’allocation ni impact gameplay démontré. Le cas zéro est déjà égal en RED ; six cas positifs sensibles divergent. GREEN : 116 salles, buffers entiers de 524 000 octets chacun comparés après 4 774 mots de pointeur normalisés, zéro différence ; frames entières de 329 832 octets identiques. 629 boxes, trois écritures BOX_BLOCKED. Domaine cible ascendant, natif descendant : même ensemble d’effets sur éléments disjoints, pas même ordre des stores.

## Endpoints synthétiques et compteur

Les sept cas synthétiques sont zero, one-clear, one-last, four-0, four-1, four-8, four-9 : 0, 1 et 4 boxes, premier/dernier avec ou sans flag. Différences RED → GREEN respectives : 0 → 0, 1 → 0, 2 → 0, 1 → 0, 2 → 0, 1 → 0, 2 → 0 octets. CPU/RAM cible frais et nouvel inférieur hôte par cas ; injection synthétique après préfixe authentique, fixture de 96 octets, comparaison complète des buffers et frames. Compteur final natif 37 pour zéro injecté, 0 pour positif ; le compteur cible est ensuite réaffecté, pas une égalité registre-variable générale au stop. Aucun hit au watchpoint matériel sur le champ sentinelle ; hooks cible dans les éléments valides. Le watchpoint ne couvre pas tous les stores natifs ni toute la mémoire ; ordre natif inféré du CFG et des buffers.

## Comparaisons, audit et stops

15 événements ordonnés : 7 lectures, 5 allocations, 3 libérations ; sept buffers, tailles et curseurs vérifiés. Triplets avant/après allocations/libérations et final, mais pas aux retours de lecture hôtes non capturés. Les 23 champs pointeurs, 9 scalaires suffixe et textures/SPU sont vérifiés par le runner et son audit, pas tous par le nouveau décodeur reviewer. Audit natif avant exécution : 285 instructions statiques, 10 branches, décodage complet et destinations fermées dans le segment ELF ; pas appel/retour ni branche indirecte. Stop initial SETUP.C:1274, puis arrêt matériel SETUP.C:1429, capture et destruction de l’inférieur. Le contrôle des opérandes absolus nuls ne couvre pas tous les nuls calculés. Boucle cible décodée indépendamment, absence de chevauchement relocation vérifiée localement ; delay slot avançant le pointeur, pas preuve de toute la relocalisation. Stop cible à l’entrée de la huitième lecture objets avant son corps ; appel/delay slot atteints et number_cameras stocké, aucun retour LoadLevel. Lien --unresolved-symbols=ignore-all : ne jamais exécuter ce binaire autonome ni dépasser la borne. 1 608 071 visites du hook, 52 246 overlay, 5 147 suffixe, 64 interceptions et une visite stop : pas des instructions retirées.

## Revue indépendante et parent

Rejeu reviewer inchangé le 9 septembre 2026 de 12:08:45 à 12:08:57 Paris : 12,518391 s, exit 0. 6 tests producteurs/gardes en 11,569 s et 1 test post-audit en 0,154 s, puis audit CLI ; 9 sous-processus directs, pas neuf tests. Python optimisé rejeté, exit 1 attendu. Une exécution cible intégrée authentique et sept tranches synthétiques ; une compilation privée et 8 inférieurs GDB frais. Audit indépendant review_check.py sans import producteur ni listes de normalisation, version finale à 12:12:04, exit 0 : contrôle hors-ligne, pas autre passage CPU. Snapshot 539 fichiers : 521/539 identiques dont buffers/exécutable ; changements dans 18 logs et métadonnées, 47 fichiers historiques inchangés. Vérification parent distincte réellement exécutée avant publication de 12:14:58 à 12:15:11 Paris : run_verified.py puis review_check.py, chacun exit 0. parent-replay.log annonce full-room equivalence et sept cas ; parent-check.log confirme les comptes, zéro différence GREEN et date 12:15:11.378163. Les heures et exits parent sont communiqués par le parent, les résultats sont lus dans ses logs. La mention parent en attente de la revue est antérieure à ce passage ; le rédacteur ne relance aucun probe privé et ne s’attribue aucun rejeu binaire.

## Provenance et limites

HEAD prépublication 6ced334380ef9633953a6689ff64cad4c9d40e0c ; date avant unité : 9 septembre 2026, 12:15:49 Europe/Paris, autorisation jusqu’à 23:25 Paris. 356 dépendances épinglées, fermetures séparées setup 53 et harness 27 ; en-têtes système/toolchain non hermétique. Deux warnings extern-initialized existants, build/GDB exit 0, stderr GDB authentique vide. Gardes HEAD/arbre suivi/index et heure conservées, gardes historiques inchangées ; après publication ne pas rejouer, assouplir ou resealer le runner. Corpus Name=0, doubles allocation/CD/SDK hôtes et frontières matérielles cible doublées, émulateur partagé : pas oracle matériel indépendant. Pas boot/UI, gameplay, chargeur complet, consommateurs overlap/pathfinding, comparaison ROOMLOAD.C, concurrence ou GTE général ; pas de sanitizer, pas de sûreté mémoire générale. Pas de généralisation aux comptes négatifs/extrêmes, charges malformées, autres corpus, ABI ou optimisations. Les 1 155 fixups hors allocation restent inactifs ; un début de pointeur dans le bloc ne valide pas l’objet complet.

## Handoff

Après RE-754 : prochaine unité explicitement prise en charge pour intégrer le patch minimal au backend prouvé sous TDD, avec tests publics de régression et attribution explicite à la preuve bornée. Préserver les cas zéro/premier/dernier/sentinelle et le compteur, obtenir revue avant livraison ; ne pas étendre objets, skins ou autre exploration. La preuve corrective privée est acquise dans sa borne, son intégration production ne l’est pas. Aucun patch de production ni commit/push dans cette publication metadata-only ; aucun reset/clean/job.

## Traces et validation publique

Preuves privées sous `build/reverse/autonomy-20260909/re754/` : `handoff.md`, `review.md`, `parent-replay.log`, `parent-check.log`, `review-replay.json`, `review-check-execution.json`. RED privé et RED documentaire sont distincts. Les tests publics ne lisent ni n’importent ces preuves ; ils gardent la story et sa section courante, les limites, le lien et le handoff. Journaux `publication-red.log`, `publication-green.log`, `publication-suite.log`, `publication-final.log` ; ledger `publication-commands.json` dans ce même répertoire ignoré.

Commandes publiques exactes, cwd `/var/www/projects/TOMB5` :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re754_boxes_correction_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py -q
```

Les invocations privées parent étaient `PYTHONDONTWRITEBYTECODE=1 build/reverse/autonomy-20260908/venv/bin/python build/reverse/autonomy-20260909/re754/run_verified.py` puis le même interpréteur avec `build/reverse/autonomy-20260909/re754/review_check.py`, sorties vers les deux logs parent. Historique cité uniquement : aucun probe après modifications. Rapport interdit jamais ouvert/modifié/stagé ; aucune donnée brute, adresse, opcode ou dump publié.
