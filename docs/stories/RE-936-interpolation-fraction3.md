# RE936 — InterpolateMatrix fraction3

## Progression
- [x] Nouveau RED public actual-TU avant patch, quatre configurations ABI32.
- [x] Candidat et production GREEN, 24 rollbacks individuels sensibles.
- [x] Export public frais, sans ancien input ignored, reproduit RED/candidat/GREEN.
- [x] Revue indépendante fraîche : SCOPEDPASS_FINITE_SOURCE_INTEGRATION, erreurs/concerns vides.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après : DONE, objets neufs régénérables seuls ; preuves essentielles conservées.
- [ ] Revue finale de publication et commit/push : clôture parent après validation des cinq hashes finaux.

## Correction et preuve
Douze expressions seulement dans `InterpolateMatrix` : pour fraction3/rate4, secondaire moins différence secondaire-primaire décalée arithmétiquement, soit `secondaire - ((secondaire-primaire) >> 2)`. Baseline byte-identique au HEAD initial `a81f7e3258e98423f367837058229ced2c4744fa`. Aucun autre helper ni corps privé intégral transféré.

Domaine fini : deux paires construites non orthonormales, six appels, rate4 fractions1/2/3 ; ABI32 little-endian C++11 avec décalage arithmétique signé. R33 positif, upper16 initial zéro. Sommes/différences dans int32, résultats géométriques dans int16. Quatre configurations : O0/O2 normales et ASan/UBSan fail-fast, TUs complètes MATHS.C/LIBGTE.C avec headers normaux ; linking gc-sections, seule fonction testée appelée.

Revue indépendante `re936-independent-review01/verdict.json`, SHA256 `608a7ea07bf02d46391ff4a2351fa8bf0be4ba39a1243f7313efd76f690a3946` : 36 exécutions fraîches actual-TU, baseline4 RED, candidat4 GREEN, production4 GREEN, 24 rollbacks individuels sensibles (12 expressions × O0/O2 normal). Oracle distinct sur les 96 mots raw ; quatre configurations privées supplémentaires GREEN vérifient MatrixSP=7 inchangé et les 2048 octets des deux stacks, pointeurs/paramètres. Le harness public vérifie les stacks mais ne pose pas lui-même le sentinel MatrixSP ; qualification supplémentaire privée explicite.

Attribution RE895 : 261 membres authentifiés, décodage statique indépendant du payload pour les douze expressions et leurs largeurs. Aucun CPU cible frais, aucune propagation de PASS privé ni preuve matérielle. Parent a authentifié les inventaires gate359/public981/reviewer389, tailles/SHA/exactsets/seals. Source et tests restent identiques à la revue numérique ; seuls ces docs sont finalisés pour publication distincte.

## Reproduction publique
`python3 -B tests/reverse/test_re936_interpolation_actual_tu.py --mode all --output /chemin/neuf`

G++ multilib et headers SDL2 requis. `RE936_MUTATION_LOCK` absolu route le mutex canonical lors de l’export ; ne pas ajouter de flock externe autour du runner lock-aware. Test de bootstrap : création du parent avant ouverture, contention et libération vérifiées exit0. Les wrappers distinguent executable exit0 des assertions oracle RED exit1 ; GREEN assertions exit0. Export public frais reproduit toutes les phases sans inputs ignored historiques.

## Nettoyage et limites
Gate : 7 448 568 octets d’objets neufs retirés ; promotion publique : 13 051 720 ; reviewer : 7 585 328. Exactpaths/mesures statvfs/df dans les ledgers privés. Scripts, inputs, exécutables et FAIL/seals conservés. Pas de prune historique, assets/coldarchives/RE893partial/maintenance quotidienne inchangés. La variation de capacité du filesystem partagé n’est pas attribuée exclusivement à ces suppressions.

Intégration approuvée uniquement pour ce contrat fini. Aucune preuve allangles, saturation, LP64, appel naturel, gameplay, matériel, CPU cible frais ou écritures transitoires. RE930/BLOCKED007 strictement exclu sans reprise/fallback/équivalent. Procédure/global FAIL historiques et lacunes discovery/bootstrap conservés ; bootstrap EOF auxiliaire reviewer exit1 conservé avec correction distincte, aucune rétrocertification. Temps outil : gate267.16s/267.22s task/outer (exécution locale219.72s) ; promotion368.50s/368.54s ; revue437.96s/438.00s. Autorisation et scopes distincts, pas de succès inféré depuis wrapperexit0.

[Dashboard versionné distinct](../reverse/tomb5-progress-dashboard-re936-v1.html).
