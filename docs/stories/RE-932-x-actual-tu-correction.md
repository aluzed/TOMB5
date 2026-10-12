# RE932 — correction X distincte de quatre lignes

## Verdict auteur et progression
**PASS indépendant strict borné** : publication et intégration source des quatre lignes approuvées pour le seul domaine ABI32 ci-dessous. Verdict `build/reverse/autonomy-20261012/re932-independent-review01/verdict.json`, SHA256 `ceb4e4c331c0009231c5db528a2c1b481abf9adf422c18903146cde50c2ec4da` ; `security_concerns=[]`, `logic_errors=[]`. Global/procédure FAIL historiques maintenus. Commit/push sont vérifiés séparément dans le HANDOFF courant, jamais déduits du verdict. Le périmètre cinq lignes précédent reste **FAIL**, sans rétrocertification ni transfert de PASS privé RE900.

- [x] Propriétaire parent 2407067 vivant et contention canonique exit1 avant/après les opérations.
- [x] Test quatre lignes écrit avant patch ; RED réel du source public et pytest RED.
- [x] Candidat dérivé public GREEN : six appels × quatre configurations.
- [x] Quatre rollbacks sensibles : 457/703/716 RAW-only (géométrie inchangée), 711 UBSan exit1.
- [x] Patch production minimal : exactement 457/703/711/716 ; 699 et les six lignes Z inchangées.
- [x] Production/public pytest GREEN ; régressions publiques RE859 X et RE866 Y sans répétition Z.
- [x] Export public neuf sans build ignoré antérieur : inverse exact baseline RED, candidat et production GREEN ; pytest cache désactivé.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après : **DONE**, mesure exacte et inventaire des objets retirés dans `cleanup.json` du root distinct. Aucun historique/firstFAIL/archive froid élagué.
- [x] Revue indépendante stricte des quatre hashes publics, patch source et preuves ; 897 membres scellés authentifiés par le parent.
- [x] Reviewer : compilation neuve repo et export public, baseline RED, candidat/production GREEN, quatre mutants sensibles ; pytest 4 PASS repo et 4 PASS export.
- [x] Nettoyage reviewer : 72 objets dérivés propres retirés, 20839484 octets logiques ; disponible 24059305984 → 24080232448, sans attribution exclusive.

## Contrat fini, causalité et limites
TUs complètes SPEC_PSXPC_N/MATHS.C et EMULATOR/LIBGTE.C, headers publics normaux, table réelle GAME/CAMERA.C, g++ -m32 -std=c++11 -DPSXPC_TEST=1, link --gc-sections,-z,defs. O0/O2 normal et UBSan fail-fast ; sorties compilateur et exécutables réels conservés, wrapper RED exit0 ne signifie pas exécutable GREEN.

Six appels mRotX/iRotX × {0,8192,40960}. Matrices : [1024,0,d,512,0,d/2,256,0,d/4], d=1024 pour 0/8192, -1024 pour 40960. Oracle Python indépendant : géométrie Q12/narrowing signed16, deux stacks complets 2048 octets et CP0 ; scratch full32 VZ0/VZ1 explicitement limité. mRotX VZ0 reste un store low16. Banques complètes comparées entre configurations, non intégralement reconstruites indépendamment ; pas de trace exhaustive des stores.

457/703/716 corrigent des stores full32 publiquement discriminés ; 711 utilise le helper signed existant après shift unsigned. 699 est **inchangée** : packing signed C++11 observablement équivalent dans le domaine fini, retiré du DELTA et du gate, sans nouveaux angles ni domaine artificiellement élargi. Aucune preuve Sony/hardware/gameplay/ABI64/allangles/saturation ni transitive RE900.

## Reproduction
Runner self-locking ; aucun flock externe autour de RE932 :
```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/reverse/test_re932_x_actual_tu.py --phase red --output build/reverse/re932-four-red-new
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/reverse/test_re932_x_actual_tu.py --phase candidate --output build/reverse/re932-four-candidate-new
PYTHONDONTWRITEBYTECODE=1 python3 -B tests/reverse/test_re932_x_actual_tu.py --phase green --output build/reverse/re932-four-production-new
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -p no:cacheprovider -q tests/reverse/test_re932_x_actual_tu.py
```
Sur production corrigée : exits 0/0/0/0 ; RED reconstruit exactement les quatre lignes seulement. RE859/RE866 exigent leur flock mutation externe propre, sans nesting RE932.

## Historique immuable et HANDOFF
Premier root `build/reverse/autonomy-20261012/re932-x-actual-tu/`, ses 650 membres, verdict/cleanup/firstFAIL et dashboard v1 conservés. Premier gate cinq mutants FAIL : 699 strict GREEN ; authoring initial gap/holder expiré restent historiques. Correction de typo documentaire historique : variation 24116330496−24099483648 = **16846848** octets (le texte historique «168****6848» n'était pas une valeur numérique).

Root distinct `build/reverse/autonomy-20261012/re932-four-line-correction01/` : ledgers prospectifs argv/cwd/start/end/exit/timeout, pins, source baseline, candidats/mutants, exécutables, export neuf et nettoyage. Discovery read-only et transport du controller /tmp précèdent le ledger durable, pas de certification exhaustive de ces accès ; chaque écriture repo/compile/output ultérieure est sous mutex canonique avec propriétaire vivant pré/post. Aucun holder expiré/nested lock.

Quatre chemins publics : MATHS.C, test RE932, cette story, dashboard **re932-v2** distinct. Intégration source approuvée dans le domaine fini ; reçu de stage/commit/push séparé dans le HANDOFF courant. Reviewer : annexe RE900 width authentifiée et trois stores natifs décodés, pas de nouvelle exécution cible/CPU ni copie de TU privée. Son premier FAIL de calibration du diagnostic (« negative value » attendu, overflow positif effectivement observé à 711) reste dans early-verdict.json ; retry02 et verdict final strict distincts ne le réécrivent pas. RE930 STRICT reste exclu sans reprise/fallback/provider-change ; suppressions BLOCKED001/002, report/cache/archives historiques préservés, aucun accès/restauration/staging de ces suppressions. Prochaine frontière : décider un nouveau contrat source indépendant, sans répétition des matrices X/Z closes ni élargissement automatique de ce PASS.
