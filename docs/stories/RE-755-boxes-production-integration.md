# RE-755 — Intégration production de la correction boxes

## Tracker

- [x] Date avant unité : 9 septembre 2026, 12:45:39 Europe/Paris ; borne autorisée 23:25 Paris. HEAD de départ fc14df38617ab66173a7777ca030645b32e42b40.
- [x] Preuve RE-754 et revue privées lues ; aucun rejeu cible ni modification de leurs fichiers.
- [x] RED public comportemental observé avant source : 6 échecs, cas zéro réussi, exit 1 en 0,74 s.
- [x] Patch minimal et GREEN : 7 tests réussis, exit 0 en 0,70 s.
- [x] RED documentaire : story absente, 1 échec, exit 1 en 0,06 s.
- [x] GREEN ciblé après raffinement : 8 tests en 0,74 s, exit 0 ; suite prédécesseur exacte étendue RE-755 : 1 216 tests en 51,41 s, exit 0, 12:52:20–12:53:11 Paris.
- [x] Revue indépendante : revue PASS, 10 tests frais en 0,84 s, exit 0 ; audit reviewer séparé.
- [x] Vérification parent : 1 216 tests en 51,07 s, exit 0 ; sept buffers frais et identité source vérifiés (parent-audit.json).
- [ ] Chargeur complet, consommateurs et autres backends : hors preuve, non clos.

## Correction et attribution

Deux références d’indice dans GAME/SETUP.C deviennent i - 1, sans autre modification de production. La garde positive, l’initialisation du compteur dans la boucle et son décrément restent inchangés. Le compteur conserve 37 sur zéro injecté et vaut zéro après les cas positifs. number_boxes est également vérifié. Le premier et le dernier élément sont couverts avec et sans BOX_LAST ; BOX_BLOCKED est ajouté uniquement au champ attendu, les autres octets restent identiques. La sentinelle immédiatement adjacente porte BOX_LAST sans BOX_BLOCKED et ne doit pas être modifiée.

Attribution : preuve corrective bornée RE-754, sa story et sa revue, non nouveau résultat cible de RE-755. Configuration réellement compilée : PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DISC_VERSION=1, DEBUG_VERSION=0 ; i386 -m32 -O0 -g, en-têtes ordinaires. C’est une source partagée : autres backends non validés par cette unité, ni autres optimisations/ABI. La boucle corrigée demeure descendante ; équivalence des effets disjoints prouvée antérieurement, pas identité de l’ordre des stores avec la cible ascendante.

## Tests publics sur vraie TU

`tests/emulator/test_setup_boxes.py` compile directement la vraie TU GAME/SETUP.C, sans extraction ni copie de LoadLevel. Un harness séparé fournit uniquement les globales boxes/number_boxes et des tables synthétiques ; pointeur/long 32 bits, box_info 8 et Level 228 octets sont contrôlés à la compilation. Sept cas : zéro, un sans/avec flag, quatre sans flag/premier/dernier/premier et dernier. Chaque cas démarre un nouvel inférieur GDB. Les 48 octets de la table synthétique complète sont comparés, y compris champs non modifiés et records adjacents. Cela contrôle des effets finaux, pas tous les accès mémoire ; aucun watchpoint d’accès n’est revendiqué ici.

Le prologue LoadLevel est exécuté jusqu’à la première initialisation locale ; aucun corps de chargement ni service CD/SDK n’est exécuté. Le debugger injecte level, boxes, le compte et i, puis positionne le PC au début de number_boxes. Audit CFG avant exécution : décodage complet de la plage, jeu d’instructions restreint, aucun appel/retour ni saut indirect, destinations de branches sur frontières internes ou sortie. Exécution instruction par instruction, PC contrôlé à chaque pas et budget borné. Arrêt avant camera.fixed, puis destruction de l’inférieur : pas de retour LoadLevel. Le lien --unresolved-symbols=ignore-all reste volontairement incomplet hors tranche : ne jamais exécuter ce binaire autonome ni continuer au-delà de la borne. Ce test ne traverse pas le préfixe authentique de RE-754 et ne remplace pas sa preuve cible.

Deux préflights du nouveau harness ont échoué avant le RED comportemental : borne inclusive de désassemblage GDB, puis instruction de décalage absente de la liste autorisée. Ils ont été corrigés sans toucher à la source. Le RED retenu comporte bien six différences comportementales, pas des erreurs de compilation/debugger. Le GREEN a recompilé la TU modifiée. Le raffinement ultérieur du test remplace la ligne d’entrée fixe par sa recherche symbolique, vérifie la taille Level et utilise les constantes du header pour la sentinelle ; aucune assertion comportementale affaiblie.

## Provenance et limites

Nouvelle unité publique RE-755 ; gardes historiques inchangées, aucun runner historique appelé, resealé ou assoupli. Les anciens HEAD-pinned probes restent volontairement incompatibles avec l’arbre publié. Les tests publics n’importent ni ne lisent leurs preuves, ne nécessitent aucun asset et restent rejouables hors échéance : ils ne sont pas un runner d’exploration autonome. Journaux et exécutables de cette unité uniquement dans les répertoires temporaires pytest et `build/reverse/autonomy-20260909/re755/` ignoré. Les commandes et empreintes de livraison identifient cette exécution ; système/toolchain non hermétiques.

Pas de preuve gameplay, boot/UI, consommateurs overlap/pathfinding, chargeur entier, console, GTE ou entrée malformée. Comptes négatifs/extrêmes non couverts. Pas de sanitizer ; pas de sûreté mémoire générale. Aucune extension loaders/objets/skins, aucun changement aux preuves historiques. La revue indépendante historique RE-754 n’est pas une revue de ce patch. Nouvelle revue PASS dans review.md : dix tests ciblés frais et audit des buffers. Vérification parent distincte : suite de 1 216 tests en 51,07 s, exit 0, lancée à 12:59:38 Paris ; parent-execution.json consigne la fin et la commande avec --basetemp=build/reverse/autonomy-20260909/re755/parent-pytest. Après cette génération, le parent a reconstruit les sept buffers complets, vérifié compte/compteur et identité avec la TU corrective privée : parent-audit.json. Aucun rejeu cible. Le ledger RED initial est rétrospectif ; le transcript outil confirme le RED avant le patch, sans attribuer son observation au reviewer. Aucun commit au moment de cette revue ; livraison après les contrôles finaux. Aucun reset/clean/job. Rapport interdit ni ouvert, ni modifié, ni stagé.

## Validation et traces

Cwd `/var/www/projects/TOMB5`. Logs privés `red.log`, `green.log`, `publication-red.log`, `publication-green.log` (premier passage documentaire, casse des mots corrigée), `targeted-green.log`, `suite.log`, `final.log` et ledger `commands.json` sous `build/reverse/autonomy-20260909/re755/`. RED/GREEN publics distincts des RED/GREEN privés historiques. Commandes :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator/test_setup_boxes.py -q --tb=short
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re755_boxes_integration_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py tests/reverse/test_re753_boxes_publication.py tests/reverse/test_re754_boxes_correction_publication.py tests/reverse/test_re755_boxes_integration_publication.py -q
```

La troisième commande est exactement la suite publique de RE-754 avec le nouveau test documentaire ajouté ; le nouveau test comportemental est découvert via tests/emulator. Aucun générateur historique lancé volontairement.

## Handoff

Après RE-755 : intégration minimale approuvée par revue indépendante et vérification parent ; prête à la livraison après contrôles finaux. Préserver garde, compteur, cas zéro, premier/dernier et sentinelle ; ne pas étendre objets ou autre chargeur dans cette unité. Unité corrective close dans cette borne. Prochaine hypothèse pour une unité distincte : preuve des consommateurs boxes/overlap avant toute conclusion gameplay ; non exécutée ici. RED de clôture documentaire : 1 échec attendu sur revue PASS en 0,07 s, exit 1 (closure-red.log).
