# RE-706 — complétude du prochain sujet du handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff autoritaire RE-702, le dashboard terminal et la protection RE-705 ont été relus avant modification.
- [x] Un test RED a démontré qu'un handoff `next_ticket=TBD` avec une condition d'arrêt, mais un `next_topic` concret, était présenté à tort comme une clôture.
- [x] Le générateur exige maintenant `next_topic=none`, en plus de `next_ticket=TBD` et de la condition d'arrêt, avant d'afficher une clôture prouvée.
- [x] Le dashboard RE-702 est régénéré de façon déterministe; aucun code de jeu, inventaire, actif ou donnée binaire n'est modifié.
- [x] Les tests ciblés, les gardes metadata-only et le contrôle des fichiers protégés sont exécutés avant livraison.

## Décision

Cette protection est metadata-only. Un sujet suivant non nul constitue une ambiguïté de reprise: il ne peut pas être masqué par un ticket `TBD` et une condition d'arrêt. RE-702 reste terminal car il porte explicitement `next_topic=none`; toute reconstruction demeure bloquée jusqu'à l'intake d'un contrat comportemental externe attribuable et d'une preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.