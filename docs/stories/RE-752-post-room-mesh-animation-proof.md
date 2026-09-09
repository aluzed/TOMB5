# RE-752 — Préfixe post-salles : mesh et animation

## Statut

**PASS borné — publication metadata-only, sans patch de production.** Extension mesurée de RE-751, sans nouvelle recherche.

## Tracker

- [x] Revue indépendante et vérification parent fraîches avant publication suivie.
- [x] Onze globales résolues dans le harness privé, CFG audité et borne protégée.
- [x] Comparaison intégrale des buffers et qualifications conservées.
- [x] RED documentaire observé : story absente, 1 échec attendu en 0,06 s.
- [x] GREEN documentaire : 1 test réussi en 0,05 s ; suite publique RE751 étendue RE752 : 1 206 tests réussis en 50,85 s.
- [x] Revue indépendante de publication approuvée ; suite publique réexécutée par le parent avant livraison.
- [ ] Dépendance AnimTextureRanges, consommateurs/GTE et retour du chargeur non prouvés.

## Résultat mesuré

PASS borné : 116 salles, 11 globales post-room résolues dans le harness privé ; 834 fixups mesh et 576 fixups animation, soit 1 410 mots nouveaux et 4 774 mots normalisés au total. Buffer salle intégral de 524 000 octets égal après normalisation limitée aux positions reconstruites ; frames de 329 832 octets identiques et inchangées. Face à RE751, 4 230 octets différents, tous et seulement dans les mots attendus. Curseur de disposition 422 760, suffixe de 216 904 octets, 101 240 octets restants non consommés. 7 lectures, 5 allocations, 3 libérations ; ordre intercalé des 15 événements et sept buffers vérifiés. Zéro divergence hôte mesurée ; aucun correctif de production justifié.

## Borne native et cible

Vraie GAME/SETUP.C recompilée, harness séparé sans copie de LoadLevel, i386 32 bits -O0 -g, g++ 13.3.0, en-têtes normaux ; PSX_VERSION=1, PSXPC_TEST=1, NTSC_VERSION=1, USE_32_BIT_ADDR=1, DISC_VERSION=1, DEBUG_VERSION=0. Arrêt matériel GDB à SETUP.C:1274, onze symboles non nuls distincts et audit CFG avant de continuer : 111 instructions statiques complètement décodées, sans appel/retour ni branche indirecte, branches sur frontières internes ou sortie protégée. Arrêt matériel à SETUP.C:1332 avant AnimTextureRanges, globale suivante encore nulle ; écriture non exécutée puis inférieur détruit. Cible arrêtée après le delay slot final animation, suffixe suivant non exécuté. Le contrôle null-free vise les opérandes mémoire absolus nuls de cette plage, pas tous les nuls calculés. Le lien conserve --unresolved-symbols=ignore-all : ne jamais exécuter ce binaire autonome ni dépasser la borne ; aucun retour LoadLevel prouvé.

## Authenticité et compteurs

Boot extrait authentifié par empreinte, module comparé à son empreinte et à la copie historique, relocation calculée et image installée comparée au dispatch ; octets authentifiés à chaque visite. Même CPU/RAM/curseur depuis S_LoadLevelFile, sans redémarrage au module. Classes historiques CPU/ISO utilisées, pas leurs anciennes fonctions de garde ou preuve. 1 602 924 visites du hook, 47 100 visites overlay, 64 interceptions et une visite d’arrêt : pas des instructions retirées. 18 328 visites post-room, aucun helper dans ce suffixe ; les 111 instructions statiques ne sont pas un compte d’itérations.

## Arithmétique et mémoire

Source actif OLD_CODE=1 : addition directe de l’offset ; cible : arrondi signé vers zéro. Corpus mesh : offsets pairs et non négatifs, aucune divergence observée ; tests impairs/négatifs du modèle, pas l’équivalence de la vraie TU sur ces entrées. Grands comptes signés/non signés non couverts. Les 834 débuts mesh et 576 débuts animation tombent dans leurs blocs, sans preuve des objets complets ni de leurs consommateurs. Les 161 roomlets actifs ont leur début dans l’allocation ; 1 155 fixups hors allocation sont inactifs. Aucun consommateur exécuté : pas de sûreté mémoire générale. Triplets normalisés avant/après allocations et libérations et descripteur final comparés, mais pas aux retours de lecture hôtes ; descripteurs internes intermédiaires non tous observés, donc full_normalized_descriptors ne signifie pas exhaustivité universelle.

## Revue et vérification parent

Revue indépendante fraîche PASS borné, 9 septembre 2026 : 9 tests en 17,656 s, deux exécutions cible, vraie recompilation et exécution i386 sous GDB, puis contrôle indépendant sans importer le probe ou ses modèles. Vérification parent distincte réellement exécutée avant publication de 10:29:45 à 10:30:03 Paris : 9 tests en 17,392 s, deux exécutions cible, nouvelle recompilation et exécution de la vraie TU sous GDB ; run_verified.py et review_check.py exit 0. Le runner réexécute independent_audit.py après la suite : le premier test seul lit les artefacts précédents. Le contrôle supplémentaire review_check.py n’est pas un dixième test. Les neuf sous-processus du runner ne sont pas les neuf tests.

## Provenance et limites

HEAD prépublication 7900232dba4279fe3868d2eb3f0ba3bf10562aa2 ; fenêtre du 9 septembre 2026 jusqu’à 23:25 Paris. 198 dépendances authentifiées ; 11 fichiers de code sauvegardés et vérifiés inchangés. Dépendances canonicalisées séparément : 53 setup et 19 harness ; host.d multi-TU seul insuffisant. Les en-têtes système exclus par -MM, bibliothèques/outils système et paquets Python ne sont pas épinglés cryptographiquement : environnement non hermétique malgré les versions archivées. Python optimisé effectivement rejeté, exit 1 (optimized Python prohibited) ; assertions indispensables, audits isolés pas tous protégés de même. Garde propre RE752 sur heure, HEAD et git diff HEAD index inclus, pas tous les fichiers non suivis. gardes historiques inchangées ; après publication, leur rejet légitime exige une nouvelle unité explicitement autorisée avec provenance propre, jamais un affaiblissement. Corpus unique Name=0, état initial synthétique, doubles allocation/CD/SDK hôtes ; helpers cible réels aux frontières SDK interceptées, pas de preuve matérielle, boot complet, concurrence, rendu/audio effectifs, comparaison ROOMLOAD.C ou consommateurs/GTE. pas de sanitizer ni validation toutes optimisations/ABI ; preuve du binaire i386 -O0 construit, pas de comportement C défini universel.

## Traces et attribution

Preuves privées dans `build/reverse/autonomy-20260909/re752/` : `review.md` fait autorité pour les qualifications ; `parent-replay.log`, `parent-check.log`, `green.log`, `execution-commands.json`, `host-command.json`, `debug-command.json`, `host-build.log`, `host-output.log`, `native-audit.log` et `host-stderr.log`. Le présent rédacteur lit ces traces et ne relance aucun probe privé. Les résultats parent sont postérieurs à la revue, qui ne les revendiquait pas.

Comparaison à la sauvegarde reviewer : 90/93 fichiers identiques, incluant sorties binaires, exécutable recompilé et métadonnées statiques/historiques : pas 90 preuves réexécutées. Trois différences conservées et qualifiées : PID dans host-output.log, horodatages dans execution-commands.json, durée dans green.log. Aucun écart comportemental masqué. Le reviewer a reconstruit le buffer entier depuis l’en-tête et le buffer `read-6.bin`, sans fonctions de modèle ni offsets sérialisés du producteur. Aucun raw, adresse, listing, source propriétaire ou asset publié ; seules conclusions symboliques et métadonnées.

## Validation publique

TDD documentaire réel, sans preuve binaire revendiquée : RED attendu enregistré dans `publication-red.log`, GREEN dans `publication-green.log`, suite dans `publication-suite.log` (dossier privé RE752). GREEN : 1 test réussi en 0,05 s ; suite : 1 206 tests réussis en 50,85 s. Premier passage de suite : 1 échec documentaire RE750 et 1 205 réussites en 50,90 s (publication-suite-first.log) ; le handoff avait perdu le repère historique « Après RE-750 ». Repère rétabli sans modifier les tests historiques, puis suite intégralement verte. Commandes publiques :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/reverse/test_re752_postroom_publication.py -q
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/emulator tests/reverse/test_re747_transaction_publication.py tests/reverse/test_re748_loadlevel_publication.py tests/reverse/test_re749_frames_publication.py tests/reverse/test_re750_room_publication.py tests/reverse/test_re751_rooms_publication.py tests/reverse/test_re752_postroom_publication.py tests/reverse/test_generate_tomb5_progress_dashboard.py -q
```

## Handoff

**Après RE-752 :** arrêt maintenu avant AnimTextureRanges et sa dépendance nulle. Toute extension devra résoudre les dépendances suivantes et auditer une nouvelle borne cohérente avant exécution, dans une nouvelle unité explicitement autorisée. Consommateurs réels, GTE et retour complet restent ouverts ; reconstruire seulement sur écart observable prouvé. Aucun nouveau job, aucun rejeu privé après édition, aucun commit au moment de la rédaction initiale ; revue indépendante de publication ensuite approuvée. Historique, générateurs et sources de production inchangés.
