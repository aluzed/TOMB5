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
