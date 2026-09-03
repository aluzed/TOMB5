# RE-715 — complétude de la condition d'arrêt du handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-702 et les protections RE-703 à RE-714 ont été relus avant modification.
- [x] Un test RED fournit un handoff terminal dépourvu de `stop_condition`; l'ancien générateur le présentait comme un état incomplet au lieu de bloquer l'entrée ambiguë.
- [x] Le générateur exige désormais une condition d'arrêt non vide pour tout handoff terminal, avant toute projection du dashboard.
- [x] Le dashboard RE-702 reste déterministe, terminal et sans backlog actif.

## Décision

Cette protection metadata-only ne réouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.