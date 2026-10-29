## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Débordement SqrtTable trouvé par ASan pendant un soak PAL + manette : global-buffer-overflow dans mSqrt (MATHS.C:152), appelé par sub_2CL1 (LARA1.C:1555) avec un argument négatif. Correctif : clamp des entrées négatives à 0 dans mSqrt/mSqrt_2/phd_sqrt_asm/phd_sqrt_asm_CH/mSqrt_L et accès borné PortSqrtLookup() (0..209) dans MATHS.C/MATHS.H/LIGHT.C/CALCHAIR.C. Vérification GDB/ASan : toutes les variantes retournent 0 pour -1, mSqrt(INT_MAX)=46152, aucun rapport ASan ; soak ASan PAL + manette 571 s sans erreur (pal-asan-soak3-20261029/), crash initial documenté dans pal-asan-soak-20261029/. Smoke normal build-guard2 : scène de Rome rendue (guard-smoke2-20261029/). tests 4174 PASS. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

ASan PAL + manette virtuelle : avec ASAN_OPTIONS=detect_leaks=0, New Game (cutseq name: 1, 2153 occurrences), gamepad détecté et déplacement au stick, exit 0, aucune erreur AddressSanitizer (pal-asan2-20261029/). Avec LeakSanitizer actif, 189290 octets signalés dans libnvidia-glcore.so avec piles driver (aucune frame du port), donc bruit GL et non fuite du jeu (pal-asan-20261029/). Build ASan SHA256 ee0e15dca0cb3cdb8cd53e11932d1c51cbbe0a93ebde3a80caee9d9f3936cb2a. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-001 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Soak RSS de 15 minutes sur build-cm avec entrées aléatoires et audio dummy : 47 échantillons VmRSS, 75112 → 75560 Ko (+448 Ko, plateau dès 150 s jusqu'à 871 s), états R/S, aucune erreur fatale, exit 0 ; captures à 300 s (inventaire) et 600 s (allée de Rome). Preuve build/porting/soak-rss-20261029/. Tests complets relancés : 4174 PASS avec CPLUS_INCLUDE_PATH/LIBRARY_PATH 32 bits ; sans ces variables les harnais C++ échouent sur bits/c++config.h (prérequis d'environnement). Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-27

PORT-001, PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-10-27T23:59:00+01:00. Linux32 provisoire.

Clone neuf de b5411b6b sans preuves privées. Environnement remis en état sans sudo (pytest, en-têtes C++ 32 bits, GLU et GLEW via un sysroot local). tests/porting 496 PASS, tests/emulator 3676 PASS. Deux builds ELF32 i386 neufs avec GLEW recompilé séparément. Images PAL SLES_033.31 et NTSC SLUS_013.11 converties en TOMB5.CUE/BIN ; l'image NTSC n'est pas la révision exacte du baseline (MD5 3530… au lieu de 4EF5…). Trois lancements PORT-002 : menu à ~35 s, Down/Up changent la sélection, Special Features puis retour, New Game atteint la cinématique. PORT-003 : la scène de Rome est atteinte vers 140 s, Lara et la géométrie sont rendues, déplacement observé, fermeture WM_DELETE_WINDOW et exit 0. Aucune revue indépendante ; le HUD Camera X/Y/Z était encore présent. Preuves privées : build/porting/port002-20261027c, launch-newgame2..4.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression runtime du 2026-09-18

PORT-002 — **In progress** ; PORT-001 reste en cours. Autorisation jusqu’au 2026-09-18T10:30:00+02:00. Linux32 provisoire.

Premier crash de navigation corrigé : SIGILL au retour manquant de S_SoundPlaySample, avec argument pitch rétabli selon preuve cible. RED 30 échecs/60 PASS puis GREEN 90 PASS sur vraie TU i386 et double PlaySample explicite. Trois lancements neufs du binaire corrigé : titre atteint vers 26 secondes, menu capturé à 29 secondes, entrées réelles Down/Up/c/z observées selon parcours ; ouverture Special Features et retour, Nouvelle partie atteint DoLevel(1). Fermetures WM_DELETE_WINDOW : application exit 0. Capture de chargement illustrée, gameplay non validé ; audio complet non reconstruit. Preuves privées : build/reverse/autonomy-20260918-1030-recovery/. Revue indépendante précommit PASS à 09:47 Paris : 126 tests publics réussis, preuves archivées auditées sans régénération ; pas de validation audio matérielle ni gameplay.

Détails : [preuve runtime](runtime-menu.md).

Les blocs antérieurs ci-dessous sont historiques, y compris leur ancienne échéance et leurs réserves visuelles. Aucun Done attribué.

## Progression active du 2026-09-18

PORT-001 — **In progress**. Autorisation technique bornée jusqu’au 2026-09-18T08:30:00+02:00 ; elle ne valide pas définitivement la cible.

Recette build/launch industrialisée : scripts/porting/linux32.py, deux builds ELF32 neufs avec GLEW recompilé séparément, sans chemin runtime-1058. Lancement frais avec données privées ; fermeture WM_DELETE_WINDOW, application exit 0 avant limite. Captures privées non vides (pixels décodés), pas de validation visuelle complète ; menu et gameplay non validés. Rejeu indépendant : troisième build ELF32 réussi ; correction préflight 125/126 caractères après revue. Acceptation visuelle complète non établie. Preuves : build/reverse/autonomy-20260918-0830/.

Recette : [Linux32](linux32.md).

Les statuts, compteurs et restrictions du lot initial ci-dessous restent un historique du 13 septembre, pas une nouvelle demande de GO. Aucun ticket accepté Done.

Status: In progress

## Fiche initiale historique

# PORT-001 — Build Linux32 reproductible

[Tracker](README.md) · [Tableau HTML](index.html#PORT-001)

Status: Todo

Priorité : P0

Motif : Prêt à planifier ; aucune implémentation autorisée par ce lot.

Dépendances : Aucune

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Pouvoir construire et lancer la même application depuis un environnement documenté, sans dépendre du répertoire privé d’un précédent essai.

## Faits existants — base eac6d930

RE-772 rapporte un build ELF32 réussi avec GLEW privé ; le build ELF64 a crashé dans LoadLevel. Linux.cmake recherche SDL2/OpenGL/GLEW mais ne fixe pas à lui seul l’ABI 32-bit.

## Portée

Toolchain, options effectives, dépendances i386, chemins de données fournis légalement, lancement et fermeture.

## Exclusions

Reconstruction menu, correctifs gameplay, port natif64 et redistribution des données exclus.

## Tâches — implémentation non commencée

- [ ] Documenter une recette neuve avec versions et architecture de chaque dépendance ; adapter seulement après autorisation d’implémentation.
- [ ] Reproduire dans un nouveau build tree et archiver flags, ELF, résolution des bibliothèques et hash avant lancement.
- [ ] Documenter le placement des données utilisateur et tester absence de données avec diagnostic exploitable.

## Critères d’acceptation futurs

- [ ] Deux builds neufs à partir du même commit aboutissent sans dépendance cachée à runtime-1058 ; identité bit-à-bit du binaire non exigée.
- [ ] Le binaire est ELF32, ses bibliothèques sont compatibles, le splash est capturé depuis ce binaire et une fermeture normale est observée.
- [ ] Une dépendance ou donnée absente produit une erreur attribuable et une procédure de résolution.

## Validation et capture attendues

Logs configure/build/ldd et application distincts, capture privée avec hash du binaire ; recette rejouée indépendamment. Un timeout ne remplace pas une fermeture normale.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Disponibilité des dépendances sur une autre machine, variantes de données et nécessité d’un conteneur à décider.

## Estimation indicative

1–3 jours-personne pour industrialiser la recette existante ; hors résolution de défauts runtime nouveaux. Confiance : Medium. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `docs/stories/RE-772-build-runtime-observable.md:15` — Build32 et limites.
- `SPEC_PSXPC_N/PLATFORM/Linux.cmake:3` — Dépendances Linux.
- `SPEC_PSXPC_N/CMakeLists.txt:11` — Options indépendantes du build type.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
