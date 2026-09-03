# RE-718 — rejet des sujets terminaux génériques

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-717, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] Des tests RED couvrent les valeurs génériques `none`, `TBD`, `unknown`, `n/a` et `?` dans le sujet d'un handoff terminal.
- [x] Le générateur refuse fail-closed ces placeholders, même entourés d'espaces ou avec une casse différente.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Un sujet terminal doit identifier un audit et ne peut pas être un placeholder. Cette protection metadata-only renforce la traçabilité sans rouvrir RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.