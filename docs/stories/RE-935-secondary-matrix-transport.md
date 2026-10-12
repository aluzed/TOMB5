# RE935 — transport secondaire cohérent iPushMatrix / iLoadMatrix

## Progression
- [x] RED comportemental public avant patch, TU complètes et vrais headers ABI32.
- [x] Candidat GREEN puis proposition source minimale, deux unités cohérentes.
- [x] Export public neuf sans build initial, reproduction et régression primaire.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après : DONE matériellement, lacune documentaire conservée.
- [x] Revue indépendante numérique et attribution archivale : SCOPED PASS, erreurs/concerns vides.
- [x] Intégration source approuvée uniquement pour le contrat fini ABI32LE raw.
- [ ] Revue finale de publication et livraison commit : clôture parent après vérification des hashes.

## Preuve et contrat borné
HEAD initial 6bd84ff9c468f2b1ba11b8d985bad91cce21ce2b. 96 cas / 192 snapshots par configuration : high16 {0,0x1234,0x8000,0xffff}, low16 {0,0x1000,0x8000,0xffff}, indices initiaux couplés {0,29}, modes push direct / load direct / push→perturb→load secondaire→push→perturb→iPop réel. Indices maximaux31, retour30. Comparaison exacte GTE384 (trois banques), stacks1024 chacune, entrée64/canaries16+16, deux pointeurs relatifs et MatrixSP23. Canaries externes stacks NON établies ; ASan couvre allocations. Primaire et secondaire initialement différents, aucune projection géométrique ne remplace le contrat raw.

TUs MATHS.C/LIBGTE.C complètes : g++ -m32 -std=c++11, PSXPC_TEST=1, O0/O2 normaux et ASan/UBSan fail-fast. Baseline normale : executable0, assertion1, wrapper RED0 ; baseline sanitizer : executable1, diagnostic shift négatif. Le message stdout historique du wrapper RED disant stderr empty ne concerne que le normal, PAS ces arrêts sanitizer. Candidat et proposition finale : executable0 et stderr vide. Rollback indépendant producer120/192 snapshots divergents, consumer96/192 à O0 ET O2. Deux lignes de copie numérique modifiées : producer32octets, consumer4octets ; rollback producteur restaure le corps entier original, pas mutants séparés de chaque ancien store.

RE881 reviewer2887 et producer3125 membres authentifiés tailles/SHA/exactsets/seals ; 72 sorties target archivées reconstruites indépendamment, sans importer les oracles privés. Payload authentifié et attribution CFC2 C8..C15→SW32 / LW32→CTC2 C8..C15 contrôlée statiquement. ARCHIVE_BACKED, aucun CPU cible frais ni PASS transitif ni TU privée copiée.

## Audit largeur, signedness, aliasing
ABI little-endian vérifiée au runtime ; long4, short2, MATRIX3D32, m22@16, pad explicite@18, tx@20, banqueCP2C128@256. L33 est alias signed16 du mot C12 ; R33 alias signed16 C4 primaire, transport primaire déjà corrigé au HEAD, inchangé. iLoad transfère m22+pad quatre octets vers C12. iPush transfère C8..C15 depuis la représentation du BANK ENTIER (offset32), pas depuis un sous-objet de4octets. Accès unsigned char aux représentations : pas cast int/uint32 sur MATRIX3D, pas shift signed négatif, pas conversion arithmétique du mot. Fixture typée réelle entourée de canaries ; bounds stacks garantis dans les seuls indices déclarés. Conventions union du modèle GTE conservées, pas preuve universelle C++/ABI64/hardware.

## Reproduction publique
```sh
python3 -B tests/reverse/test_re935_secondary_transport.py --phase red --output build/reverse/re935-red
python3 -B tests/reverse/test_re935_secondary_transport.py --phase candidate --output build/reverse/re935-candidate
python3 -B tests/reverse/test_re935_secondary_transport.py --phase green --output build/reverse/re935-green
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider tests/reverse/test_re935_secondary_transport.py tests/reverse/test_re934_matrix_transport.py
```
Les phases inversent exactement les deux unités et refusent mixed/drift. Exports doivent fournir RE935_MUTATION_LOCK vers le mutex canonical du propriétaire, jamais un mutex local concurrent. Final public-export02 : phases RED/candidate/GREEN exits0, pytest propre1PASS exit0 ; repo3PASS exit0 (RE934 régression uniquement). git diff --check exit0. Pas commit/stage/push.

## Limites et procédure
Source finie SCOPED_PASS_INDEPENDENT_REVIEW_COMPLETE : revue `re935-independent-review01/verdict.json`, SHA256 `b61aacb82bff5dc623cd84c4bfcc9dc4f75f5ca4d6f344e99a6a997958a9ce0b`, 490 membres authentifiés par le parent. Le reviewer a fraîchement compilé les quatre configurations et reconstruit l'oracle indépendant de 629 colonnes : baseline144 snapshots divergents, mutants push120/load96, candidat et source GREEN. Son export propre RE935+RE934 donne 3PASS exit0 ; phases red/candidate/green exits0. Les 72 observations target sont archivales, reconstruites depuis leurs inputs ; aucune nouvelle exécution target. Source et tests restent byte-identiques à la revue ; seules story/dashboard sont finalisées pour une revue de publication distincte. Revue375.80s task/375.92s outer ; producteur540.71s task/540.77s outer dépasse demande540s, plafond600s respecté : dépassement conservé.

Callers naturels/dualstack provenance, gameplay, hardware, stores transitoires, allangles et LP64 NON prouvés. RE930/BLOCKED007 strictement non repris ni équivalent/fallback ; X/Z clos non réouverts. Global/procedure FAIL historiques maintenus. Nouveau ledger prospectif des compilations/opérations internes, mais discovery initiale et orchestration externe pas exhaustives ; premier cleanup.json et stdout driver écrasés lors seconde passe, tailles du premier cleanup perdues et chemins récupérés explicitement sans rétrocertification. Le ledger complet demandé nest donc PAS certifié : FAIL_PROCEDURE_LEDGER_GAPS. Objets uniquement neufs inutilisés supprimés, inputs/scripts/exécutables/RED/UBSanFAIL/seals conservés ; aucune prune historique ni maintenance modifiée. Mesures df/statvfs dans preuve privée, pas revendication récupération nette du filesystem partagé.

[Dashboard versionné distinct](../reverse/tomb5-progress-dashboard-re935-v1.html).
