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
