## Progression vérifiée du 2026-10-27

PORT-001, PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-10-27T23:59:00+01:00. Linux32 provisoire.

Clone neuf de b5411b6b sans preuves privées. Environnement remis en état sans sudo (pytest, en-têtes C++ 32 bits, GLU et GLEW via un sysroot local). tests/porting 496 PASS, tests/emulator 3676 PASS. Deux builds ELF32 i386 neufs avec GLEW recompilé séparément. Images PAL SLES_033.31 et NTSC SLUS_013.11 converties en TOMB5.CUE/BIN ; l'image NTSC n'est pas la révision exacte du baseline (MD5 3530… au lieu de 4EF5…). Trois lancements PORT-002 : menu à ~35 s, Down/Up changent la sélection, Special Features puis retour, New Game atteint la cinématique. PORT-003 : la scène de Rome est atteinte vers 140 s, Lara et la géométrie sont rendues, déplacement observé, fermeture WM_DELETE_WINDOW et exit 0. Aucune revue indépendante ; le HUD Camera X/Y/Z était encore présent. Preuves privées : build/porting/port002-20261027c, launch-newgame2..4.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Lancement frais : New Game termine LoadLevel vers 71 s, scène avec Lara et locomotion minimale vérifiées par entrées réelles et captures inspectées ; pause, Quit/Yes, retour titre puis fermeture normale (application et GDB exit 0). Aucun patch loader : observation précédente trop courte. Sept tests des archives du 18 septembre réussis, sans nouveaux runtimes pour ces archives. Source jeu inchangée depuis 73faba47 ; binaire existant authentifié, pas de rebuild dans cette unité. PORT-001 reste en cours, PORT-004 et suivants bloqués pour recette intégrée ; campagne, collisions étendues, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit01-0757/.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression runtime du 2026-09-18

PORT-002 — **In progress** ; PORT-001 reste en cours. Autorisation jusqu’au 2026-09-18T10:30:00+02:00. Linux32 provisoire.

Premier crash de navigation corrigé : SIGILL au retour manquant de S_SoundPlaySample, avec argument pitch rétabli selon preuve cible. RED 30 échecs/60 PASS puis GREEN 90 PASS sur vraie TU i386 et double PlaySample explicite. Trois lancements neufs du binaire corrigé : titre atteint vers 26 secondes, menu capturé à 29 secondes, entrées réelles Down/Up/c/z observées selon parcours ; ouverture Special Features et retour, Nouvelle partie atteint DoLevel(1). Fermetures WM_DELETE_WINDOW : application exit 0. Capture de chargement illustrée, gameplay non validé ; audio complet non reconstruit. Preuves privées : build/reverse/autonomy-20260918-1030-recovery/. Revue indépendante précommit PASS à 09:47 Paris : 126 tests publics réussis, preuves archivées auditées sans régénération ; pas de validation audio matérielle ni gameplay.

Détails : [preuve runtime](runtime-menu.md).

Les blocs antérieurs ci-dessous sont historiques, y compris leur ancienne échéance et leurs réserves visuelles. Aucun Done attribué.

# PORT-002 — Du splash au menu interactif

[Tracker](README.md) · [Tableau HTML](index.html#PORT-002)

Status: Blocked

Priorité : P0

Motif : Recette intégrée bloquée tant que PORT-001 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-001

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Atteindre un menu lisible et pouvoir choisir Nouvelle partie avec une entrée réelle.

## Faits existants — base eac6d930

RE-772 ne montre qu’un splash pendant 30 secondes, sans menu ni gameplay validés. DoTitle pilote le titre ; TitleOptions contient des branches liées à la connexion et à la cinématique. Cause de l’absence de menu non établie.

## Portée

Chemin normal de démarrage, rendu du menu, clavier ou manette de référence, navigation/validation/retour ; entrées minimales incluses.

## Exclusions

Pas de saut artificiel du titre, pas de lancement direct du niveau présenté comme navigation validée ; commandes en jeu réservées à PORT-004.

## Tâches — implémentation non commencée

- [ ] Reproduire et isoler l’étape splash/titre/menu avec chronologie des événements.
- [ ] Vérifier conditions de fondu/cinématique et réception des entrées sans présumer la cause.
- [ ] Implémenter uniquement une correction attribuée si nécessaire et faire une recette de navigation.

## Critères d’acceptation futurs

- [ ] Sur trois lancements neufs, un menu avec options lisibles apparaît dans une borne convenue et consignée.
- [ ] Les actions haut/bas/valider/retour modifient visiblement la sélection sans touche bloquée.
- [ ] Nouvelle partie quitte le menu par le chemin normal ; atteindre une scène jouable relève de PORT-003.

## Validation et capture attendues

Vidéo ou série de captures privées horodatées, entrées enregistrées, logs et sortie application ; distinguer menu visible et menu réactif.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Interaction clavier/PadConnected, séquence titre, rendu ou synchronisation : hypothèses à départager, pas causes établies.

## Estimation indicative

3–10 jours-personne exploratoires ; à rechiffrer dès le premier obstacle reproduit. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `docs/stories/RE-772-build-runtime-observable.md:19` — Splash et absence de menu.
- `GAME/GAMEFLOW.C:931` — DoTitle.
- `SPEC_PSXPC_N/TITSEQ.C:140` — TitleOptions.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
