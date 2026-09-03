# RE-710 — complétude des champs requis du handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal autoritaire RE-702 et les protections RE-703 à RE-709 ont été relus avant modification.
- [x] Un test RED couvre un handoff terminal dont `next_ticket` est vide : il pouvait être projeté comme un backlog implicite au lieu d'être rejeté.
- [x] Le générateur exige maintenant un `story_id`, sujet, prochain ticket et prochain sujet non vides pour chaque handoff RE-420+, sans toucher aux archives antérieures; la condition d'arrêt vide reste explicitement projetée comme état terminal incomplet.
- [x] Le dashboard RE-702 est régénéré de manière déterministe; aucun code de jeu, actif, binaire, dump ni donnée propriétaire n'est modifié.

## Décision

Cette protection metadata-only et fail-closed interdit qu'une direction terminale absente soit interprétée comme une reprise autorisée. RE-702 demeure terminal : aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.