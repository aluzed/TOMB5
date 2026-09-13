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
