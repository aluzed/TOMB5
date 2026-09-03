# RE-708 — présence obligatoire de l'identifiant de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff autoritaire RE-702 et les protections RE-705 à RE-707 ont été relus avant modification.
- [x] Un test RED démontre qu'un handoff sans `story_id` pouvait être accepté et devenir le dernier état du dashboard.
- [x] Le générateur exige désormais un `story_id` présent et identique à l'identifiant dérivé du nom de fichier pour chaque handoff du tracker terminal (RE-420+), sans réécrire les archives antérieures.
- [x] Le dashboard RE-702 est régénéré de façon déterministe; aucun code de jeu, inventaire, actif ou donnée binaire n'est modifié.
- [x] Les tests ciblés, les gardes metadata-only et le contrôle des fichiers protégés sont exécutés avant livraison.

## Décision

Cette protection de traçabilité est metadata-only et fail-closed. Un identifiant absent ne peut plus contourner la vérification de cohérence fichier/enregistrement ni masquer une reprise non autorisée. RE-702 reste terminal : aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.