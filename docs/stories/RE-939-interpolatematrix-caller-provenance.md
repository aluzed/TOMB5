# RE939 — provenance SOURCE des appelants d’InterpolateMatrix

Statut : **PASS_SOURCE_SELECTION_ONLY** indépendant ; `integration=false`. Recherche de provenance achevée, préfixe dynamique encore **BLOCKED**. Publication documentaire seulement : aucune modification de production, aucune exécution cible fraîche, aucun gameplay validé, procédure globale non approuvée.

## Progression
- [x] Inventaire SOURCE et préprocesseur de la configuration native ABI32 courante.
- [x] Revue indépendante fraîche des faits et du choix de préfixe.
- [x] Nettoyage, conservation de l’essentiel et mesure espace avant/après — DONE.
- [ ] État appelant naturellement produit avec fraction non nulle et témoin sensible.
- [ ] Exécution actual-TU du préfixe complet puis comparaison attribuée et revue indépendante ; pas d’activation transitive.

## Nouveauté exécutée
L’audit a prétraité **15 TU**, produit **37 lignes** de métadonnées et authentifié **302 pins**. **3 tests** GREEN ; **302 mutations** de pin et un retrait rejetés. Les arguments du compile database historique sont authentifiés, mais le prétraitement utilise les sources actuelles. Configuration ABI32 little-endian, c++ -m32, DISC_VERSION/PSX_VERSION/PSXPC_TEST/NTSC/USE32BIT actifs, BETA/DEBUG/RELOC inactifs. Aucun objet compilé ni exécutable de gameplay n’est revendiqué.

Dans ce périmètre backend/database, un seul appel direct effectif à InterpolateMatrix : `GetJointAbsPosition`, `SPEC_PSXPC_N/SPHERES.C:151`. **8 appels amont** : CreatureEffectT, CreatureEffect, ConfirmCameraTargetPos, deux sites CutsceneRopeControl, ControlBlinker, GunHit et ProcessExplodingSwitchType8. Les variantes InterpolateMatrix_AI et InterpolateMatrix_CL sont distinctes. Inventaire lexical direct : pas de complétude indirecte ni toutes plateformes.

Revue indépendante : nouvel audit identique, puis huit TU et contrôle des macros indépendamment prétraités ; trois tests et mutations/retrait fraîchement exécutés. Les 30 invocations enfants finales producteur et les 30 de replay reviewer ont des noms UUID distincts. Producteur : **267 membres** authentifiés ; reviewer : **140 membres** authentifiés. PASS limité aux faits SOURCE, pas à une sensibilité exécutée du futur préfixe.

## Unique préfixe sélectionné et frontière
Sélection : entrée de `ProcessExplodingSwitchType8` jusqu’au retour d’InterpolateMatrix, arrêt interne **avant SPHERES.C:154**. L’appelant fournit pos=(0,0,0) et joint=0. Un arrêt extérieur après restauration des matrices pourrait masquer le témoin brut R33 ; cette proposition initiale est conservée mais superseded.

La chaîne SOURCE identifie GetFrames, InitInterpolation, les rotations/translations et les piles de matrices. Il faudra conserver ces producteurs réels, observer les 96 mots bruts avant restauration, vérifier stacks/canaris et un contrôle fraction zéro, sans injecter directement matrices ou paramètres d’interpolation. LIBGTE commun reste un algorithme logiciel partagé, pas un oracle hardware.

**Blocage de provenance naturelle :** InitialiseItem initialise une frame donnant fraction zéro sous taux valide ; `AnimateItem` effectif est un stub. Aucune progression naturelle vers une **fraction non nulle** n’est établie. Deux frames authentiques compatibles sélectionnées artificiellement ne suffiraient pas à prouver l’atteinte gameplay. Critère de réouverture : état cohérent produit par un vrai appelant/animateur, branche interpolée atteinte, témoin observablement sensible avant restauration et dépendances/ABI bornées. À défaut, rester BLOCKED sans patch.

## Preuves et réserves
Racines privées ignorées :
- `build/reverse/autonomy-20261013/selection-939/` : audit_final.py, tests, pins, provenance, résultats, premiers échecs et ledgers.
- `build/reverse/autonomy-20261013/selection-939-review/` : verdict, replay frais, contrôles indépendants, nettoyage et clôture.

Verdict reviewer SHA256 : `bccf3f76294ec9840c14a2d85878cc854757313e77c4f7bda8ea9034ae5568fc`.
Manifest producteur SHA256 : `d9ad6766cec52990848f5d4b78645d0fc2787e07d341527c4cecaa646d7bd07f`.
Manifest reviewer SHA256 : `696918a31187970db2106acaaa1c1397f49d11494bcdb4f96893909287cfd3a6`.

Bootstrap hors ledger prospectif et premiers noms d’invocation réutilisés : réserves conservées, pas de rétrocertification. Échec d’inventaire producteur et expectation reviewer sur expansion macro conservés ; replays corrigés distincts. Aucun PASS global/procédural. RE938 reste la dernière correction source livrée ; matrices closes non rejouées. **RE930/BLOCKED007 strictement exclus**, refus fournisseur non résolu.

## Nettoyage et livraison
Sous-tâche **Nettoyage, conservation de l’essentiel et mesure espace avant/après — DONE**, producteur et reviewer : zéro suppression, scripts/inputs/FAILs/ledgers/seals essentiels conservés, mesures df/statvfs archivées, aucun gain net revendiqué. Suppressions personnelles BLOCKED001/002, rapport, cache, tests RE937 non suivis, dashboard RE932 et archives froides préservés.

Publication : story et [dashboard RE939](../reverse/tomb5-progress-dashboard-re939-v1.html) autonomes ; le contrat documentaire possède son propre RED d’absence puis GREEN, distinct d’un RED comportemental. Revue des hashes exacts et livraison Git relèvent de la clôture coordinateur, sans altérer les preuves scellées. Prochaine frontière : débloquer la provenance naturelle, pas répéter les matrices déjà closes.
