# RE-717 — rejet des conditions d'arrêt terminales génériques

Status: `Done`

## Progress tracker

- [x] Le handoff RE-702, le dashboard terminal et les protections RE-703 à RE-716 ont été relus avant modification.
- [x] Des tests RED couvrent les valeurs génériques `none`, `TBD`, `unknown`, `n/a` et `?` dans une condition d'arrêt terminale.
- [x] Le générateur refuse fail-closed ces placeholders, même entourés d'espaces ou avec une casse différente.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Une condition d'arrêt doit décrire un blocage vérifiable ; un placeholder ne constitue pas une clôture audit-able. Cette protection metadata-only ne réouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.