# RE-709 — unicité du ticket de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal autoritaire RE-702 et les protections RE-703 à RE-708 ont été relus avant modification.
- [x] L'audit du tracker a identifié un risque : deux fichiers terminalement admissibles peuvent porter le même ticket, laissant l'ordre du glob décider silencieusement de l'état projeté.
- [x] Un test RED couvre deux handoffs `RE-709` correctement formés mais concurrents.
- [x] Le générateur refuse désormais fail-closed tout ticket du tracker terminal (RE-420+) présent plus d'une fois, tout en laissant l'archive pré-RE-420 inchangée.
- [x] Le dashboard RE-702 est régénéré de manière déterministe; aucun code de jeu, actif, binaire, dump ni donnée propriétaire n'est modifié.

## Décision

Cette protection metadata-only empêche un handoff concurrent d'altérer implicitement l'état terminal. RE-702 demeure terminal : aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.