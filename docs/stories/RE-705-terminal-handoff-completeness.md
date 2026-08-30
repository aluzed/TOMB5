# RE-705 — complétude du handoff terminal du dashboard

Status: `Done`

## Progress tracker

- [x] Le handoff autoritaire RE-702 et le dashboard terminal RE-704 ont été relus avant modification.
- [x] Un test RED a démontré qu'un handoff `TBD` dépourvu de condition d'arrêt était présenté à tort comme un historique avec reste à faire.
- [x] Le générateur distingue déterministiquement une clôture prouvée d'un état terminal incomplet qui exige validation.
- [x] Le dashboard issu de RE-702 conserve le statut de clôture prouvée; aucun inventaire, code de jeu, actif ou donnée binaire n'est modifié.
- [x] Les tests ciblés, garde metadata-only et contrôle des fichiers protégés sont exécutés avant livraison.

## Décision

Cette protection de traçabilité est metadata-only. Une valeur `next_ticket=TBD` sans condition d'arrêt ne peut pas être interprétée comme un backlog actif ni comme une clôture fiable. RE-702 reste complet et terminal: sa condition d'arrêt exige un contrat comportemental externe attribuable et une preuve ABI non brute avant toute réouverture ou tout patch de production.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.
