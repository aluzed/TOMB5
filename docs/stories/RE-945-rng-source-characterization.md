# RE-945 — DRAFT SOURCE-only RNG characterization

**SOURCE_UNCHANGED — no target oracle — independent public review pending.**

Publication brouillon de tests réutilisables, pas une correction RE ni une intégration approuvée. La revue privée indépendante caractérise la source seulement ; une revue publique indépendante ultérieure est obligatoire avant toute promotion de ce brouillon.

## Contrat fini

La TU complète versionnée `SPEC_PSXPC_N/MISC.C` est compilée avec ses headers normaux : GCC i386, C++11, `-O0`, `-m32`, defines `PSX_VERSION`, `PSXPC_TEST`, `USE_32_BIT_ADDR`. Le harness fournit les vrais globals `long rand_1/rand_2`; `GAME/CONTROL.C` n'est pas liée. Sections fonctions/données séparées, lien `--gc-sections,-z,defs`, aucun unresolved ignoré. Dépendances : Python3/pytest, g++ multilib, headers SDL2. Portabilité signifie reproduction sur cet environnement ABI, pas validité LP64 ou contrat universel C++.

Six seeds construits : `0`, `1`, `2`, `65536`, `0xD371F947`, `0xffffffff`; un pas Control puis un pas Draw, pas des seeds naturels ni une longue séquence. Le modèle Python modulo32 et shift arithmétique décrit cette exécution GCC, **pas un oracle cible**. Overflow signé indéfini ; conversions unsigned vers signed et shift négatif dépendants de cette implémentation C++11.

La source actuelle retourne un masque pour Control et une multiplication pour Draw. Le test conserve exactement cette différence sans décider ce que le jeu cible devrait faire. L'isolation des deux états est contrôlée après chaque appel, puis avec seeds distincts et reseeding dans les deux directions. Les arguments du harness sont validés (argc, chiffres, conversion, plage uint32).

## Dette conservée et sensibilité

**UBSan : 3/6 diagnostics connus conservés**, nonzero sur `2`, `65536`, `0xD371F947`, overflow signé à `MISC.C:518` dans Control. UBSan strict stoppe avant Draw dans ces trois cas : aucune couverture strict Draw n'est revendiquée pour eux. Les trois autres cas stricts doivent finir sans diagnostic. Le passage des assertions de dette attendue ne signifie **pas sanitizer clean** ; aucun `-fwrapv` ni correction de production.

Sensibilité : copie privée de la TU complète, seule expression Draw `* 0x7FFF` remplacée par `& 0x7FFF`; comparaison observable avec le modèle source et préservation des états. Ce mutant n'est ni candidat de correction ni preuve cible. Le seed zéro peut être insensible ; la gate exige des différences observées. Aucun RED comportemental de la source existante n'est inventé. RED/GREEN concerne séparément le contrat documentaire absent puis publié.

## Reproduction

```sh
python3 -B -m pytest -p no:cacheprovider tests/reverse/test_re945_rng_actual_tu.py
python3 -B tests/reverse/test_re945_rng_actual_tu.py --output /tmp/re945-fresh-ABSENT
```

Chaque compilation/output est protégée par `build/reverse/autonomy-mutation.lock` existant en canonical. Une copie publique sans `.git` ni `build` utilise explicitement un mutex par export `.re945-export-mutation.lock` : mécanisme de portabilité distinct, pas possession du repository. `RE945_MUTATION_LOCK` accepte un chemin absolu existant pour verrou canonical explicite. Journaux prospectifs UUID/argv/cwd/start/timeout/exit/durée et origines ; résultats frais, sans cache preuve privé.

Export public autorisé : seulement cette story, le dashboard RE945, le harness, le test Python, `SPEC_PSXPC_N/MISC.C` versionné et la fermeture explicite des headers versionnés nécessaires. Inventaire SHA256 exact dans la preuve privée de publication. Aucun `.git`, build historique, assets, binaire cible ou oracle privé exporté. Les outputs générés par le test sont distincts des inputs exportés.

## Limites et STOP

SOURCE-only ; aucun replay cible frais, hardware, gameplay, attribution de contrat cible/caller, candidat, correction source, stage/commit/push. Exclusions absolues : RE930 BIU/kernel/SPU et unités historiquement refusées ; RE944 cmd1/TranslateItem/LoadLevel et équivalents refusés ; aucune réexécution des gates AnimateItem/movement/cmd4/GetChange/interpolation/turn180 closes. Refusal ⇒ STOP, aucun contournement.

Le producteur doit livrer ses résultats canonical/export frais et sa sensibilité dans HANDOFF privé scellé ; cette story ne remplace pas une revue indépendante. **independent public review pending** demeure le statut public.
