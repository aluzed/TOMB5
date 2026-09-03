# RE-716 — condition d'arrêt terminal significative

Status: `Done`

## Progress tracker

- [x] Le handoff RE-702, le dashboard terminal et les protections RE-703 à RE-715 ont été relus avant modification.
- [x] Un test RED fournit une condition d'arrêt composée uniquement d'espaces ; l'ancien générateur l'acceptait comme non vide.
- [x] Le générateur refuse désormais tout champ terminal obligatoire vide ou réduit à des espaces, avant toute projection du dashboard.
- [x] Le dashboard RE-702 reste déterministe, terminal et sans backlog actif.

## Décision

Cette protection metadata-only et fail-closed ne réouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.