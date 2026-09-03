# RE-714 — unicité des en-têtes de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-702 et les protections RE-703 à RE-713 ont été relus avant modification.
- [x] Un test RED fournit un handoff terminal dont l'en-tête `next_ticket` est dupliqué, ce qui permettrait à un parseur CSV de choisir silencieusement une colonne.
- [x] Le générateur refuse maintenant tout handoff à en-tête dupliqué avant de construire le dashboard.
- [x] Le dashboard RE-702 reste déterministe et terminal.

## Décision

Cette protection metadata-only ne réouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.