# PORT-007 — Audio essentiel et arrêt propre des sons

[Tracker](README.md) · [Tableau HTML](index.html#PORT-007)

Status: Blocked

Priorité : P1

Motif : Recette intégrée bloquée tant que PORT-004 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-004

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Entendre les sons utiles et l’ambiance, avec réglage du volume et sans son persistant hors contexte.

## Faits existants — base eac6d930

SFX.C contient SPU_Play/PlaySample et le pont de samples ; CD.C contient S_CDPlay/S_CDStop. Présence d’appels et fonctions partielles ne prouve pas une sortie audible fonctionnelle.

## Portée

Sons menu/action, ambiance du premier niveau, volumes, arrêt au titre et reprise après pause selon le contrat retenu.

## Exclusions

Fidélité matérielle SPU, toutes voix/langues, mixage de la campagne entière et redistribution audio exclus.

## Tâches — implémentation non commencée

- [ ] Fixer périphérique de sortie et sources sonores représentatives avec contrôle silence.
- [ ] Tracer chemin sample/CD et durée de vie des voix ; traiter seulement les manques attribués.
- [ ] Vérifier changements volume, pause/retour titre et absence de boucle persistante.

## Critères d’acceptation futurs

- [ ] Au moins un son menu, deux actions distinctes et une ambiance sont audibles aux moments attendus.
- [ ] Volume nul coupe la catégorie concernée et le rétablissement la rend audible sans modifier une autre catégorie.
- [ ] Retour au titre arrête les sons du niveau ; trois cycles n’accumulent pas de sons persistants.

## Validation et capture attendues

Capture audio privée et journal événements, écoute humaine sur sortie choisie ; appels de services seuls insuffisants.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Backend actif, couverture des samples, musique/cinématiques et partage des voix à caractériser.

## Estimation indicative

3–10 jours-personne exploratoires pour ce socle audio. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/SFX.C:164` — PlaySample.
- `SPEC_PSXPC_N/CD.C:267` — S_CDPlay.
- `GAME/GAMEFLOW.C:1308` — Ambiance du niveau.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
