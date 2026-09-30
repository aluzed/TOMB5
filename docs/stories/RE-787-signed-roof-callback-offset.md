# RE-787 — GetCeiling : offset signé transmis au callback réel

30 septembre 2026. Baseline `243c16ac`. Correction bornée sous **PSX_VERSION && PSXPC_TEST** : conserver l'**offset signé** de cinq bits dans l'accumulateur int de GetCeiling, multiplication définie par 256. Branche legacy conservée ; aucun marqueur d'équivalence promu. Deux champs offset distincts discriminent leur sélection, puis un consommateur réel discrimine l'accumulateur avant son retour short.

## Tracker
- [x] Probe cible authentifié : GetCeiling, helper arithmétique, TwoBlockPlatformCeiling et OnTwoBlockPlatform exécutés continûment, **7680** appels synthétiques.
- [x] RED actual-TU normal et **UBSan** strict avant correction : **2304** entrées callback divergentes et **309** retours observables divergents, inclus dans les 2304 cas.
- [x] GREEN : 18 tests ciblés frais, dont quatre matrices current/baseline × normal/UBSan et régressions RE784/RE786.
- [x] RED documentaire : deux absences attendues avant inscription ; historique dashboard protégé par digest.
- [x] Revue combinée indépendante source/publication PASS borné (`re787-review-combined/verdict.json`) : replay target indépendant existant inspecté, 12 tests frais. CLI source initial et tentative seal interrompus timeout124 avant verdict ; cette reprise de clôture ne leur attribue aucun succès.
- [x] Revue documentaire : deux tests RE787 PASS, trois guards historiques RED après append ; digests inchangés, seul successor RE787 nommé exclu et protégé par son propre guard.
- [x] Sélection étendue issue du ledger RE786 augmentée des six tests RE787 : **115 tests PASS en 14,32 s**, exit 0 (`re787-suite-green01.ledger.json`). Pas suite globale.
- [x] Revue finale combinée de publication PASS borné ; inscription minimale autorisée, livraison Git à vérifier séparément.
- [ ] Registration native réelle, traversées, gameplay et autres architectures non validés.

## Contrat et preuve causale
La cohorte : six types roof 9, 10, 15, 16, 17, 18 × 32 valeurs du premier champ offset, second champ décalé de 17 modulo 32 × huit coordonnées asymétriques × cinq modes de consommation. Deux diagonales, témoins de frontière et d'égalité, offsets positifs et négatifs. Cinq modes : callback absent, seuil y égal, seuil y dépassé, mesh désactivé, item inhibé. Les objets/registration et l'état appelant sont construits ; pas de preuve d'une route réelle de gameplay.

L'accumulateur cible reçoit l'extension signée du champ sélectionné. La baseline stockait cette valeur dans unsigned short avant multiplication implicite par déplacement : les offsets négatifs ajoutaient 65536 de trop au t7 int transmis au callback. Le retour short final masque ce surplus si le consommateur ne change pas le résultat. Le vrai TwoBlockPlatformCeiling compare toutefois l'entrée au y de l'item : certains résultats négatifs devraient être remplacés par la hauteur de plateforme, mais la baseline présentait une valeur positive artificielle. Cela établit **309** retours divergents dans cette cohorte, sans extrapolation à la collision/gameplay.

Probe privé `build/reverse/autonomy-20260930-15h/re787-target/` : extraction neuve du boot depuis le disque authentifiée, instructions visitées vérifiées, CPU/RAM restaurés par appel, SP/RA et registres sauvegardés restaurés, comparaison de 2 MiB de RAM hors 96 octets de pile autorisés. Cette égalité finale n'exclut pas des écritures transitoires ; pas de trace dynamique complète de stores. Unicorn logiciel, pas oracle matériel. Le coordinateur a inspecté l'archive existante ; son replay neuf n'est pas revendiqué.

La fixture publique compile les TUs GETSTUFF et TRAPS entières avec headers normaux, g++ i386/C++17, lien normal et élimination des sections inutilisées. Un **adaptateur** exactement typé observe int* et transmet une copie long* au corps réel TwoBlockPlatformCeiling ; sur i386 les deux sont 32 bits. Cet adaptateur n'établit pas l'ABI de registration native. Il ne substitue pas une formule au corps du callback. Cellule, floor-data, item, object, room et cinq globals comparés avant/après ; pas de sûreté globale.

## RED/GREEN et limites
Première exécution publique : deux FAIL current comportementaux et deux échecs du checker baseline car le total de retours avait été saisi 516 au lieu des **309** effectivement produits. Échec conservé, total corrigé selon les observations, puis RED inchangé contre la source baseline : deux FAIL current et deux PASS baseline. Seulement ensuite, correction minimale production. GREEN : **18 tests PASS en 5,00 s**, exit 0 (`re787-green01.log`). Quatre matrices natives de 7680 appels chacune ne sont pas 7680 tests pytest ; les assertions indépendantes Python contrôlent ordre exact, sélection de champ, entrée callback, retours, événements et invariance.

**pas de runtime** jeu, pas de fullbuild/relink, pas de nouvelle capture ; **pas de GREEN global** sanitaire ou gameplay. Pas tous couples offset, rotations ni branches traversées ; pas garantie de registration réelle. Aucun asset/dump/opcode/pseudocode original versionné. Suppressions blocked utilisateur et rapport interdit préservés, aucun ancien ticket/dossier recréé.

## Handoff
Obstacle restant : la preuve utilise un adaptateur typé et une registration construite, pas une installation réellement atteinte dans l'application. Critères de reprise : établir producteurs et ABI effectifs du callback sur le backend, puis appels réels sensibles avec les préconditions du consommateur ; un succès de matrice ne suffit pas à rendre le gameplay GREEN. Prochaine cible proposée seulement après nouvelle autorisation : composition registration native et consommateur roof sur une route réelle, ou audit d'une autre divergence de GetCeiling si cette composition bloque. Aucun nouveau secteur après14:35 ; tests/revue/livraison/clôture dès14:40, arrêt absolu15h.
