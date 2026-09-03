# RE-719 — cohérence du prédécesseur des handoffs terminaux

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-718, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a confirmé que les 14 handoffs terminaux déclarant un champ `predecessor` suivent la séquence attendue, de RE-691 à RE-718.
- [x] Des tests RED couvrent un prédécesseur absent, antérieur, futur et malformé lorsqu'il est déclaré.
- [x] Le générateur refuse fail-closed un champ `predecessor` déclaré qui ne désigne pas le ticket immédiatement précédent, tout en préservant les schémas historiques qui ne le déclarent pas.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Un handoff terminal qui expose un prédécesseur doit désigner le ticket immédiatement antérieur. Cette protection metadata-only ferme une ambiguïté de filiation sans réinterpréter les schémas historiques ni rouvrir RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.