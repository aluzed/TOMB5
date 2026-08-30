# RE-703 — projection dashboard de la clôture terminale

Status: `Done`

## Progress tracker

- [x] Le handoff autoritaire RE-702 a été relu : `next_ticket=TBD`, `next_topic=none` et le stop condition interdit toute reprise sans contrat comportemental source-backed et preuve ABI.
- [x] Le générateur du dashboard projette désormais ce stop condition, après échappement HTML, au lieu de laisser le lecteur déduire l'état depuis un backlog historique.
- [x] Un test ciblé couvre le modèle, la projection déterministe et le dashboard régénéré.
- [x] Aucun code de jeu, actif protégé ou donnée binaire n'est modifié.

## Décision

Ce ticket est une amélioration de traçabilité metadata-only, pas une réouverture du sous-backlog RE-702. L'objectif de reconstruction immédiatement sûr reste bloqué jusqu'à la disponibilité d'un contrat comportemental externe attribuable et d'une preuve ABI.
