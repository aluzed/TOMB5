# PORT-005 — Déplacement solide et passages entre salles

[Tracker](README.md) · [Tableau HTML](index.html#PORT-005)

Status: Blocked

Priorité : P0

Motif : Recette intégrée bloquée tant que PORT-004 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-004

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Parcourir un petit trajet avec pentes, murs et changement de salle sans traversée ni chute incohérente.

## Faits existants — base eac6d930

UpdateLaraRoom et GetCollisionInfo existent côté PSXPC_N. RE-770/771 caractérisent GetHeight/callback côté SOURCE seulement : pas une correction ni une équivalence cible. Préconditions ItemPushLara et preuve cible restent ouvertes.

## Portée

Sol/pente/marche, saut/chute, mur, obstacle statique et portail sur une route de référence ; position/salle/item.floor.

## Exclusions

Pas de correction spéculative du callback ; pas de certification de toutes les géométries, ennemis ou eau.

## Tâches — implémentation non commencée

- [ ] Choisir une route avec témoins géométriques et identifier le consommateur réel de hauteur.
- [ ] Établir les préconditions d’alias/appel et la preuve cible manquante avant toute correction qui s’en réclame.
- [ ] Comparer cas sensibles et trajet intégré, conserver explicitement les divergences non corrigées.

## Critères d’acceptation futurs

- [ ] La route enregistrée franchit le portail attendu et maintient position, salle et hauteur de sol cohérentes.
- [ ] Mur et obstacle empêchent le passage ; saut/chute atterrit sur le sol prévu sans téléportation inexpliquée.
- [ ] Cas limites pente/seuil/absence de collision ont des témoins sensibles ; une caractérisation PASS avec divergence ne clôt pas le ticket.

## Validation et capture attendues

Recette privée en jeu et tests réels des TUs touchées ; attribution binaire requise pour une prétention d’équivalence, sans publier dumps.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

GetHeight cible, appelants ItemPushLara, alias et triangles non couverts par les preuves disponibles ; coût potentiellement supérieur après découverte.

## Estimation indicative

10–30 jours-personne exploratoires sur route bornée ; campagne complète exclue. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/COLLIDE_S.C:53` — UpdateLaraRoom.
- `GAME/CONTROL.C:3428` — GetHeight.
- `docs/stories/RE-771-getheight-callback-source.md:1` — Caractérisation SOURCE.
- `GAME/COLLIDE.C:413` — Collision objets.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
