# RE-811 — RemoveActiveItem : intégration bornée et régression publique
AlexP — autorisation directe jusqu’à18h; recherche17:20, revue17:45, livraison17:55. Revue publique indépendante pending.

## Tracker
- [x] RE-810 : preuve privée corrective revue indépendamment, scope technique RemoveActiveItem seulement.
- [x] Régression publique synthetic actual-TU complète, sans assets ni archive privée en entrée.
- [x] RED74/106 dans chaque mode normal et strict-ASan-UBSan avant changement production; candidat GREEN106/106.
- [x] Delta source gardé i386, deux expressions seulement; branches legacy byte-exact. Hash exact indépendant authentifié avant intégration.
- [x] Gardes historiques : exclusion du seul successeur nommé et hash de TOUS les octets précédents; inversion exacte du delta vers le hash historique original inchangé.
- [x] Build incrémental réel CMake i386 : ITEMS.C recompilé, jeu relinké, ELF32 Intel80386; pas de runtime/gameplay.
- [x] Revue indépendante de ce livrable public, des fingerprints et des gardes (18 hashes auteur exacts; statut courant ci-dessous).
- [ ] AnimateItem, DoorControl et reachability naturelle des producteurs : frontier bloquée.

## Périmètre et acceptation
96 permutations/removals sur quatre nœuds, dix contrôles zero/head/middle/tail/absent/inactive. Oracle autonome filtre la séquence logique et compare les six structures complètes (buffers866 octets avec head). Les contrôles inactive-present ne démontrent pas un producteur naturel. Strict fail-fast ASan+UBSan propre sur ces seules fixtures, sans skip; pas de GREEN global ni production-ready. La preuve privée RE810 inclut les events cible ordonnés; son fingerprint est seulement une attestation héritée à authentifier par la revue publique. Aucun rejeu de matrice cible.

## Provenance et incidents
Premier essai public : référence items non définie au link; fixture corrigée pour définir le global, diagnostic initial observé; ses logs de compilation ont été écrasés au retry (non utilisés comme RED comportemental). Ensuite RED comportemental réel normal/strict. Le dashboard antérieur et les hashes historiques restent intacts; BLOCKED-005 original conservé, fermeture bornée append-only. Suite ciblée : 52 tests + 2 subtests passent, zéro skip; premier essai7 fails pour import runpy manquant dans le garde RE803, corrigé sans changement d’assertion, journal conservé. Aucun staging/commit/push, aucune restauration BLOCKED001/002, aucun changement de skill.

## Acceptation fullbuild
Build incrémental sur configuration RE806 existante (-m32, PSXPC_TEST/PSX_VERSION/USE_32_BIT_ADDR ON), source attribuable recompilée et exécutable MAIN relinké. Pas de nouvelle configuration ni clean fullbuild revendiqués. Native ≠ gameplay. Logs et hash binaire sous build/reverse/autonomy-20261003/re811-integration.

## CURRENT — revue finale de publication indépendante
PASS_scoped pour les 18 hashes auteur exacts : verdict `build/reverse/autonomy-20261003/re811-publication-review/verdict.json`, SHA256 `76e0814267b9f6e6a037c644b317443809ee808992b732677de2549fc0e8f5d8`; preuve `build/reverse/autonomy-20261003/re811-publication-review/proof-verdict.json`, SHA256 `f336e7336e0abb942ed7434c1598e50c9b4d874df3c486d543a670067e01ad77`.
Les mentions pending, aucun rejeu cible et 52 tests + 2 subtests ci-dessus décrivent la phase auteur historique et restent conservées. Le reviewer a rejoué fraîchement les 106 cas de matrice publique : 212 events ordonnés, comparaison des 866 octets avec head et des 2 MiB complets à l’oracle indépendant; Unicorn/software ISA, pas matériel. Actual-TU i386 normal/strict : baseline RED74/106 et production GREEN106/106; suite indépendante historique 52 tests + 2 subtests.
Validation build : ledger incrémental archivé et hash du binaire ELF32 courant, pas de nouveau build de revue. Premier diagnostic de link non conservé : false. Aucune extension runtime/gameplay, architecture alternative, GREEN global, production-ready ou reachability naturelle; AnimateItem/DoorControl restent bloqués. Les quatre changements de réconciliation attendent leur propre revue finale indépendante; le verdict immuable n’approuve pas ces nouveaux hashes.
