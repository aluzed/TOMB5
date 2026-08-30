# RE-704 — libellé du backlog du dashboard terminal

Status: `Done`

## Progress tracker

- [x] Les entrées autoritaires RE-702 et le dashboard RE-703 ont été relus avant toute modification.
- [x] Un test RED a établi qu'un handoff terminal ne doit pas présenter l'historique comme du travail restant.
- [x] Le générateur choisit déterministiquement le libellé `Historique clôturé — aucun backlog actif` lorsque `next_ticket=TBD` et qu'une condition d'arrêt existe.
- [x] Le dashboard régénéré reflète ce libellé sans rouvrir d'inventaire ni modifier de code de jeu.
- [x] La suite ciblée, le contrôle metadata-only et le contrôle d'assets/staging sont prévus avant livraison.

## Décision

Ce correctif de traçabilité est metadata-only. RE-702 demeure le dernier handoff autoritaire : aucun backlog de reconstruction actif n'est déduit de l'historique. Toute nouvelle reconstruction reste bloquée jusqu'à un contrat comportemental externe attribuable et à une preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.
