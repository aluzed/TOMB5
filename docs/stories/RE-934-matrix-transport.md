# RE-934 — transport cohérent full32 mPushMatrix / mLoadMatrix

**Statut : PASS indépendant strict limité ; intégration des deux lignes source approuvée pour le domaine fini ABI32 little-endian.** Verdict `build/reverse/autonomy-20261012/re934-independent-review02/verdict.json`, SHA256 `376c3e1f2b4c774f894c769c3ec3b3216a3d9487a28b3d6a1c36ac543cd2956f` : `passed=true`, `security_concerns=[]`, `logic_errors=[]`. Global/procédure FAIL maintenus. Commit/push font l'objet d'une vérification séparée dans le HANDOFF courant. Le PASS privé RE880 n'est pas transféré au public : les TUs actuelles complètes sont recompilées.

## Progression

- [x] RED comportemental public avant patch ; inverse exact identique au HEAD précédent.
- [x] Delta cohérent producteur/consommateur de deux lignes, sans copie de TU privée.
- [x] GREEN actual-TU ABI32 O0/O2 normal et ASan/UBSan fail-fast ; rollbacks individuels sensibles.
- [x] Export public neuf initialement sans build ; pytest 2 PASS, phases RED/candidat/GREEN vérifiées.
- [x] Revue indépendante : oracle propre, banques/stacks/entrée complets, cinq hashes publics.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après : DONE pour producteur et reviewers ; seuls objets nouveaux inutilisés retirés, exactpaths et mesures dans leurs cleanup.json.
- [x] Premier FAIL reviewer conservé ; correction distincte de schéma archival, sans recompter les exécutions.

## Contrat et résultats

Backing logiciel brut C4, pas sign-extension hardware. ABI i386 little-endian, `long=4`, MATRIX3D=32, m22@16, pad explicite@18, tx@20. Delta cohérent : deux copies de quatre octets via unsigned char, sans pointeur uint32_t aliasant MATRIX3D. Aucune activation GetSpheres, caméra, boot ou gameplay.

96 cas construits : high16/low16 chacun 0000/1234-ou-1000/8000/ffff, profondeurs initiales0/29, trois modes push direct, load direct, push→load→push→pop réel. 192 snapshots : les compositions perturbent la banque entre transferts. Oracle déclaratif indépendant : CP0/CP2D/CP2C complets384 octets, deux stacks1024 chacun, entrée32 et deux canaries16, indices Matrix/iMatrix et MatrixSP. Stacks complets contrôlés, sans canaries externes explicites ; ASan couvre les dépassements instrumentés. Snapshots finaux ne prouvent ni stores transitoires ni ordre des stores.

Baseline publique RED avant patch, assertions exit1, exécutables exit0/stderr vide. Candidat GREEN O0/O2 normal et ASan/UBSan fail-fast ; deux rollbacks individuels sensibles O0/O2 normal. Pas d'arithmétique GTE appelée. MATHS.C/LIBGTE.C complètes, headers normaux, linking gc-sections/zdefs. Domaine fini, pas validation ABI64, architecture hardware ou autres producteurs iPush/iLoad/inventaire.

## Attribution historique séparée

Archive indépendante RE880-review :1776 membres authentifiés,48 sorties reconstruites indépendamment. Verdict e34b91f4e66df6f3c7081088fec501a66a3cc974e1c84d5108eb6b1ed66e4f07 ; seal53855a37246f08a93399040f0449d0d367b8c52879127ec3fa568a9517e1be3d. Payload privé SHA30542142759ad7d7a0b8d7bdb3aafc2d6ad3bd2db6c853421775c5e4b792e032. Décodage indépendant attribue LW32→CTC2 C4 et CFC2 C4→SW32. Archive≠rejeu CPU cible frais ; aucun claim targetfresh. Le runner public n'utilise aucune source privée, table privée ou binaire cible.

## Reproduction publique

`python3 -B tests/reverse/test_re934_matrix_transport.py --phase red --output build/reverse/re934-red`

`python3 -B tests/reverse/test_re934_matrix_transport.py --phase candidate --output build/reverse/re934-candidate`

`python3 -B tests/reverse/test_re934_matrix_transport.py --phase green --output build/reverse/re934-green`

`PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider tests/reverse/test_re934_matrix_transport.py -q`

Runner self-locking canonical build/reverse/autonomy-mutation.lock : ne pas envelopper dans flock externe. Bootstrap testé sans build préalable. Baseline inverse accepte unité entièrement ancienne/corrigée, rejette mixed/drift. Outputs ignorés uniquement sous build ; journal argv/cwd/start/end/exit/timeout prospectif pour compilations/exécutions.

## Limites procédurales

Transports découverte et premières écritures tools non exhaustivement ledgerés prospectivement ; protection mutation par holder explicite live contrôlé avant/après, pas rétrocertification de ledger. Preuves exécutables et publication indépendantes ; revue parent limitée acceptée après compilation fraîche. Premier reviewer FAIL scellé (`d29` attendu au lieu du schéma historique `d30`) préservé ; audit corrigé distinct RE934-independent-review02, aucune exécution recomptée. Baseline reviewer : 160 snapshots divergents dans chaque configuration ; rollbacks : 160 et 96. Global et procédure restent FAIL, notamment bootstrap export initial sous mutex local avant routage canonique. Sources utilisateur supprimées, caches/report/dashboard antérieurs et archives protégées préservés. Nettoyage limité aux objets nouveaux reproductibles, avec mesures exactes dans HANDOFF privé.

Preuves et export frais : `build/reverse/autonomy-20261012/re934-matrix-transport/`. Prochaine frontière : transport secondaire iPushMatrix/iLoadMatrix ou provenance d'un appelant, après sélection et preuve publique distinctes ; aucun PASS transitif ni activation de consommateur déduite. Matrices X/Z closes et unité RE930 refusée restent strictement exclues.
