## Progression vérifiée du 2026-10-28

PORT-007 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Constat de blocage : aucun backend de sortie audio hôte (ni SDL_Audio, ni ALSA/Pulse/OpenAL) et aucun mixage SPU/CD dans PSXPC_N ; l'audibilité demandée par PORT-007 ne peut pas être validée sur cet hôte. Correctifs d'arrêt propre intégrés : SPU_StopAll libère toutes les voix et reconstruit les canaux, S_SoundStopSample/S_SoundStopAllSamples/S_SetReverbType implémentés, test SpuSetKey(SPU_OFF, SPU_ALLCH) ajouté, smoke titre exit 0 sans ligne Unimplemented. Aucune écoute, aucun réglage de volume, aucune musique XA validés. Ticket non Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

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
