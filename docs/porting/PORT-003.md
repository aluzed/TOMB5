# PORT-003 — Nouvelle partie et première scène jouable

[Tracker](README.md) · [Tableau HTML](index.html#PORT-003)

Status: Blocked

Priorité : P0

Motif : Recette intégrée bloquée tant que PORT-002 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-002

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Démarrer une nouvelle partie depuis le menu et voir Lara dans le premier niveau des données de référence.

## Faits existants — base eac6d930

S_LoadLevelFile appelle le chargement du niveau ; LoadLevel reconstruit les rooms ; DoLevel relie chargement, caméra, contrôle et dessin. Ces sources présentes ne prouvent pas un niveau jouable. RE-772 n’a pas validé cette transition.

## Portée

Premier niveau des données choisies (Rome attendu, à confirmer par le gameflow), chargement complet et boucle graphique active.

## Exclusions

Campagne entière, fidélité de chaque effet et parcours complet exclus ; pas de succès fondé sur un loader isolé.

## Tâches — implémentation non commencée

- [ ] Fixer jeu de données légal, niveau attendu et recette menu vers nouvelle partie.
- [ ] Identifier le premier obstacle intégré et ses dépendances réelles sans neutraliser silencieusement les services.
- [ ] Corriger seulement après preuve/recette sensible, puis répéter depuis un processus neuf.

## Critères d’acceptation futurs

- [ ] Depuis Nouvelle partie, Lara et une géométrie de niveau identifiable sont visibles sans appel direct de test au loader.
- [ ] Animation et caméra évoluent pendant au moins 60 secondes ; les journaux distinguent crash, timeout et fermeture demandée.
- [ ] Trois relancements reproduisent la même arrivée, avec identité du niveau et configuration archivées.

## Validation et capture attendues

Capture privée de la transition et de la scène, trace de chargement, hash binaire ; absence de crash sur cette fenêtre seulement.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Identité effective du premier niveau, intégrité des données, overlays, animations, dépendances rendu/audio encore à vérifier en intégration.

## Estimation indicative

5–15 jours-personne exploratoires ; aucune garantie tant que PORT-002 n’est pas franchi. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/ROOMLOAD.C:62` — S_LoadLevelFile.
- `GAME/SETUP.C:1208` — LoadLevel.
- `GAME/GAMEFLOW.C:1209` — DoLevel.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
