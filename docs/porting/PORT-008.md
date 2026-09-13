# PORT-008 — Boucle du premier niveau et passage au suivant

[Tracker](README.md) · [Tableau HTML](index.html#PORT-008)

Status: Blocked

Priorité : P1

Motif : Recette intégrée bloquée tant que PORT-005, PORT-006, PORT-007 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-005, PORT-006, PORT-007

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Jouer un parcours représentatif puis atteindre le niveau suivant, avec mort/reprise et retour au titre utilisables.

## Faits existants — base eac6d930

GAMEFLOW.C traite la fin de niveau ; dans la branche gfStatus==3, une affectation vers le niveau suivant est suivie d’une remise à zéro. C’est une observation source, pas une preuve de la cause d’un échec runtime ni un correctif validé.

## Portée

Un parcours réel avec interaction/pickup, obstacle et sortie normale ; mort/reprise, état persistant et entrée au niveau suivant.

## Exclusions

Campagne entière, tous combats/boss/secrets/cinématiques et niveau de fidélité finale exclus ; décomposer un mécanisme indispensable découvert au lieu de le masquer.

## Tâches — implémentation non commencée

- [ ] Choisir le parcours et les mécanismes réellement requis à partir du niveau chargé.
- [ ] Vérifier triggers et transitions avec témoins fin normale/retour volontaire/mort.
- [ ] Intégrer les dépendances indispensables et rejouer la route avec sauvegarde/reprise.

## Critères d’acceptation futurs

- [ ] Une interaction et un pickup changent leur état attendu sur une route jouée par les entrées normales.
- [ ] La sortie normale charge le bon niveau suivant et son point de départ, sans retour inattendu au titre.
- [ ] Mort/reprise, reprise sauvegardée et retour volontaire au titre restent utilisables ; la route est répétée deux fois.

## Validation et capture attendues

Vidéo privée du parcours avec journal transitions et identités des niveaux ; tests des régressions touchées et scénario de reprise.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Mécanismes du niveau non inventoriés, combat/IA/eau/cinématiques potentiellement bloquants ; ce ticket devra être découpé si nécessaire, sans déclarer le port complet.

## Estimation indicative

10–30 jours-personne exploratoires après dépendances ; forte possibilité de nouveaux tickets. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `GAME/CONTROL.C:3011` — TO_FINISH.
- `GAME/GAMEFLOW.C:231` — Traitement gfStatus.
- `GAME/GAMEFLOW.C:1389` — Sortie DoLevel.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
