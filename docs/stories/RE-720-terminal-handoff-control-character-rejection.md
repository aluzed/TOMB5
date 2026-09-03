# RE-720 — rejet des caractères de contrôle dans les handoffs terminaux

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-719, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit des champs terminaux a confirmé que les handoffs actuels ne contiennent aucun caractère de contrôle dans les champs projetés.
- [x] Des tests RED couvrent une tabulation, DEL et des retours à la ligne dans chacun des champs terminaux projetés.
- [x] Le générateur refuse fail-closed ces caractères avant la validation de direction et avant toute projection HTML.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Les caractères de contrôle peuvent altérer la lisibilité ou la structure d'un handoff projeté. Leur rejet est une protection metadata-only : il ne réinterprète aucun artefact historique et ne rouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.
