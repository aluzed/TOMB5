# RE938 — InterpolateMatrix : correction finie du mot complet R33

Statut courant : **PASS indépendant fini**, `integration_finite_approved=true`, livraison en cours. Revue fraîche du delta public exact : `build/reverse/autonomy-20261013/re938-independent-review/verdict.json`, SHA256 `7412704e507b386ad3c75abb2dccc1ba9528b67239db4594cf4e5a68459f8c48` ; concerns et logic_errors vides. Verdict et 476 membres authentifiés par le coordinateur, cinq hashes publics identiques avant cette actualisation documentaire. Aucun PASS global, hardware ou gameplay.

Historique producteur conservé : PENDING_REVIEW ; integration_approved=false avant cette revue. Le FAIL procédural RE937 historique reste distinct et immuable.

## Progression et contrat

HEAD de départ : `1a153faf14ecab2ee8ed1ff608c5fd3382741dd8`. Les deux tests RE937 originaux restent non suivis et byte-identiques. Régression RE938 nouvelle et collectable par pytest, sans import RE937 ni entrée privée : compilation de la TU complète `SPEC_PSXPC_N/MATHS.C`, TU complète `EMULATOR/LIBGTE.C`, headers normaux, liaison résolue avec gc-sections. Aucun corps privé archivé n'est publié.

Fresh TDD avant source : les quatre configurations O0/O2 normal et ASan+UBSan failfast produisent un programme exit0 mais une assertion raw96 exit1 ; le contrat documentaire absent échoue aussi avant publication. Les différences observées sont le mot de contrôle C4 : low16 architectural égal, upper16 brut conservé à tort. Ce résultat ne démontre pas un défaut de gameplay.

Delta unique : remplacer le store étroit `R33 = m.m22;` par copie des quatre octets d'un `const int` signé local vers `gteRegs.CP2C.p[4].d` via pointeurs unsigned char, sans violation d'aliasing. L'interpolation et les autres stores sont inchangés.

Contrat GREEN : 4 configurations production, puis export public frais ; mutants inverse, zéro-extension et zéro constant à O0/O2 normal, chacun dynamiquement discriminé. Les résultats exécutés et codes de sortie sont consignés sous `build/reverse/autonomy-20261013/re938-integration/`, notamment `production-green.stdout`, `public-export-green.stdout`, `public-export-baseline-red.stdout`, `RED.json`, `verdict.json`. Les assertions ont un oracle indépendant pour chacun des 96 mots bruts, sans lecture normalisante des registres. Stacks complets 2048 octets, entrées inactives et padding canaris, pointeurs/indices/paramètres/ambiants vérifiés à retour. Cela ne prouve ni les écritures transitoires ni leur ordre.

## Domaine et limites

Exactement 12 appels construits : quatre paires non orthonormales, taux4, fractions1/2/3, R33 positif/négatif et poisons upper16 distincts. ABI32 little-endian (ABI32LE), int/long4, matrice32, banque384 ; décalage arithmétique signé du compilateur. Les opérandes bornés évitent overflow et narrowing hors plage dans ces appels uniquement. Pas de preuve allangles, saturation, hardware GTE, exécution cible fraîche, LP64, callers naturels ou gameplay. RE895 : attribution ARCHIVAL via revue déjà scellée uniquement ; aucune matrice fermée relancée. RE930 et BLOCKED007 strictement exclus.

Export sans .git, build ni entrées privées au premier appel ; seules TU complètes publiques, headers et nouveaux tests/docs sélectionnés. Override absolu `RE938_MUTATION_LOCK` vers `build/reverse/autonomy-mutation.lock` canonique du dépôt parent ; pas de verrou imbriqué. Le runner crée le parent du mutex pour un checkout vierge avant flock (bootstrap concurrent sûr). Le ledger conserve argv/cwd/start/end/exit/timeout des commandes producteur. Découverte initiale read-only/bootstrap explicitement dans transcript ; aucune rétrocertification.

## Nettoyage, conservation de l’essentiel et mesure espace avant/après

Sous-tâche exacte : **Nettoyage, conservation de l’essentiel et mesure espace avant/après — DONE producteur et reviewer**. Seulement les objets compilés neufs reproductibles ont été retirés ; exactpaths/hash/octets et mesures avant/après dans leurs cleanup.json. Reviewer : 48 objets, 8 333 756 octets logiques, absence vérifiée. Conserver sources d'entrée, exécutables, sorties RED et mutants, premiers échecs, résultats GREEN et ledgers. Mesurer footprint et df/statvfs avant/après sans attribuer toute variation d'un filesystem partagé au nettoyage. Préserver .pytest_cache, rapport utilisateur, dashboards historiques dont re932-v1, archives froides et RE893partial ; ne jamais recréer BLOCKED001002 supprimés par utilisateur. Aucun stage/commit/push.

## Objectif suivant

Revue indépendante réalisée sur l'exact allowlist ; dernière vérification de publication/documentation puis commit/push requis avant déclaration de livraison. Ensuite : sélectionner une provenance appelante utile ou un chantier distinct admissible, sans répétition des matrices closes ni activation transitive. Allowlist : `SPEC_PSXPC_N/MATHS.C`, `tests/reverse/re938_r33_actual_tu.cpp`, `tests/reverse/test_re938_r33_actual_tu.py`, cette story et `docs/reverse/tomb5-progress-dashboard-re938-v1.html`. Vérifier les hashes de publication, l'inventaire exact et le sceau producteur, puis rejouer depuis export frais. Inventaire et GREEN producteur ne constituent jamais une approbation d'intégration.

## Résultats fraîchement exécutés

Production : pytest exit0, **11 passed**. Export public vierge : pytest exit0, **11 passed**. RED avant patch et baseline export : chacun quatre échecs comportementaux / exit1, programmes exit0, 9/12 divergences exclusivement C4 upper16 dans chaque configuration ; contrat documentaire RED exit1. Mutants : six rejets observables à O0/O2 normal (pas revendiqués sous sanitizers). Les quatre builds de source sont O0/O2 normal et ASanUBSan failfast. Détails structurés : checks.json et comparaison de chaque exécutable.
