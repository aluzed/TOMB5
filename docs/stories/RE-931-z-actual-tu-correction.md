# RE931 — correction Z actual-TU publique, domaine fini

## Verdict
**SCOPED_PASS_CORRECTED_INDEPENDENT_RE931**. Revue corrigée distincte : `build/reverse/autonomy-20261012/re931-corrected-independent-review01/verdict.json`, SHA256 `5e24ec4f19744e239e2bc29b909f1c967c0e0358a5b08f0d17dbf30cc57f65d0` ; erreurs/concerns vides, publication et intégration du seul delta six lignes dans le domaine ABI32 fini approuvées. Global/procedure FAIL historiques maintenus. Premier verdict indépendant **FAIL PUBLIC_LOCK_BOOTSTRAP** conservé immuable. Correction minimale du runner : création concurrente sûre (`exist_ok=True`) de `build/reverse` avant l'ouverture du verrou ; ce bootstrap précède nécessairement l'acquisition et n'est pas prétendu protégé. Test de régression écrit et exécuté RED (FileNotFoundError, exit1) avant cette ligne, puis GREEN ; il vérifie aussi l'exclusion d'un second détenteur et la libération du verrou. Export public neuf sans build/entrée ignorée : RED attendu, GREEN O0/O2 normal/UBSan, candidat et six mutants sensibles, pytest **2 passed**. Preuves nouvelles : `build/reverse/autonomy-20261012/re931-lock-bootstrap-correction01/`. Les six lignes de MATHS.C restent inchangées, SHA256 `c6e502e74496a003c28cd1f1f39890d12ff3aa4aa153508b29169adffcd115b6`. Revue corrigée et ensemble de livraison **approuvés dans ce périmètre fini** ; stage/commit/push vérifiés séparément dans le HANDOFF courant, jamais déduits du verdict ; aucune revendication globale, hardware, cible fraîche ou gameplay.

## Progression
- [x] HEAD initial `70e7b363e8b0fea29f55913b43063afe98860a1c` vérifié.
- [x] RED public réel **avant** édition de MATHS.C : RAW full32 divergent ; géométrie scalaire correcte ; UBSan fail-fast à la ligne 767.
- [x] Candidat neuf dérivé exclusivement du MATHS.C public courant, exactement six lignes ; aucun candidat privé copié.
- [x] GREEN candidat et production : ABI32, O0/O2 normal et UBSan fail-fast, link normal sans symboles non résolus.
- [x] Six rollbacks individuels sensibles : quatre RAW-only sans divergence géométrique ; deux arrêts UBSan (packing et valeur négative).
- [x] Replay public par inverse des six lignes, sans entrée privée/ignorée préexistante.
- [x] Pytest RE931 : 1 passed ; régression RE866 : 36 cas × 8 configurations, PASS.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après.
- [x] Revue indépendante exacte corrigée, export neuf et source six lignes approuvés dans le domaine fini.
- [x] Ensemble autorisé pour livraison sous gate hashes/stage/remote ; reçu de commit/push dans le HANDOFF courant, distinct du verdict.

## Configuration et domaine exacts
TUs complets `SPEC_PSXPC_N/MATHS.C` et `EMULATOR/LIBGTE.C`, headers normaux, `g++ -m32 -std=c++11 -DPSXPC_TEST=1`, `--gc-sections,-z,defs`. Harness public avec stacks/globals synthétiques, table versionnée de GAME/CAMERA.C. Aucun stub GTE/rotation, aucun replay cible inventé. ABI32 exigée par static_assert ; pas de revendication ABI64 ici.

Huit appels : mRotZ/iRotZ × angles {0,8192} × matrices { [4096,0,0,2048,2048,0,1024,1024,0], [2048,0,1,1024,1024,0,512,512,1] }. Domaine déclaré avant RED, nonsaturant et délibérément borné pour éviter la dette signée indépendante : les champs L21/L23 et les autres packings exécutés sont non négatifs/représentables dans ces fixtures. Ce choix ne démontre pas leur sûreté générale. Les autres shifts de iRotZ restent non prouvés globalement ; aucun élargissement de domaine ni activation.

Oracle géométrique indépendant en Python : produits entiers exacts, division plancher Q12, narrowing signé16. Comparaison des deux stacks complets (2048 octets), de CP0, des pointeurs de stack et SP ; capture des trois banques CP2D/CP2C/CP0 complètes et égalité inter-configurations. Le contrat RAW indépendant porte sur les deux mots scratch Z CP2D[1]/[3], empoisonnés avec hauts/bas non nuls : zero-angle conserve les mots, angle actif efface les 32 bits. Les autres mots CP2 sont capturés, **pas** tous reconstruits par un oracle indépendant. Snapshots de retour, pas trace exhaustive des stores.

## Delta et causalité
mRotZ : **deux** clears full32. iRotZ : **deux** clears full32 plus **deux** packings unsigned via le helper mRotX_signed32 existant. Total exact : six lignes, sans modification X/Y. RAW-only n'est pas une divergence de géométrie, ni preuve d'un effet visible en jeu. UBSan baseline rapporte un débordement shift positif ligne 767 ; le rollback 808 rapporte le shift de -2896.

## Reproduction publique
Ne pas ajouter de flock externe : le runner prend explicitement le verrou canonique pour chaque compilation/écriture/opération enregistrée.

```sh
python3 tests/reverse/test_re931_z_actual_tu.py --phase red --output build/reverse/re931-fresh-red
python3 tests/reverse/test_re931_z_actual_tu.py --phase candidate --output build/reverse/re931-fresh-candidate
python3 tests/reverse/test_re931_z_actual_tu.py --phase green --output build/reverse/re931-fresh-green
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -p no:cacheprovider -q tests/reverse/test_re931_z_actual_tu.py
```

`red` construit le baseline public inchangé, ou l'inverse exact du delta si le source est déjà corrigé. Son exit0 désigne la vérification d'un RED attendu : les exécutables baseline/rollback UBSan ont réellement exit1 ; voir leurs stderr et invocation JSON. Les producer subprocess ne sont jamais remplacés par un wrapperexit0 présenté comme GREEN.

## Conservation et limites
Preuves sous `build/reverse/autonomy-20261012/re931-z-actual-tu/`, dont RED avant patch, premier candidat, puis replay raffiné et production. Commandes compilateur/exécution enregistrées prospectivement avec argv/cwd/start/end/exit/timeout75. Le replay raffiné possède aussi les journaux d'opérations d'écriture et les pins d'entrées. Les premiers fichiers d'entrée avaient des ledgers moins détaillés : ils restent conservés, sans certification rétroactive de procédure complète. Aucun seal historique réparé ; ce producer ne délivre pas de seal d'approbation.

BLOCKED-001/002 restent supprimés, sans lecture/restauration ; rapport technique et .pytest_cache préservés. Aucun stage/commit/push ; RE929 historique inchangé, dashboard RE931 indépendant. Mesures et empreinte réelle dans cleanup.json ; objets/exécutables conservés pour revue, seuls bytecodes RE931 nouveaux supprimés.

## Nettoyage correctif
Nettoyage, conservation de l’essentiel et mesure espace avant/après : mesures réelles statvfs et chemins exacts dans `re931-lock-bootstrap-correction01/cleanup.json`. Conservation des sources publiques exportées, sorties et exécutables utiles à la revue ; aucun cache utilisateur, archive froide, FAIL initial ou dépendance courante supprimé.

## HANDOFF
Revue corrigée obtenue : bootstrap/exclusion/libération GREEN, baseline authentifié RED, production et candidat huit appels × quatre configurations GREEN, six mutants sensibles et pytest frais 2 PASS. Le premier FAIL reste FAIL. Parent : authentifier le reçu de livraison dans le HANDOFF courant ; la prochaine frontière est une correction source indépendante avec ses propres TDD/ABI/domain bounds, sans élargir ce PASS aux angles négatifs, saturation, LP64 ou gameplay. Ne pas répéter les matrices closes. Startup/BIOS/RE930 restent hors périmètre.
