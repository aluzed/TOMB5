# RE-707 — intégrité des enregistrements de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff autoritaire RE-702 et le dashboard terminal ont été relus avant modification.
- [x] Un test RED démontre qu'un fichier de handoff à plusieurs lignes ne peut pas être réduit silencieusement à sa première ligne.
- [x] Le générateur exige maintenant exactement un enregistrement et un identifiant `RE-n` valide pour chaque handoff découvert.
- [x] Le dashboard RE-702 est régénéré de façon déterministe; aucun code de jeu, inventaire, actif ou donnée binaire n'est modifié.
- [x] Les tests ciblés, les gardes metadata-only et le contrôle des fichiers protégés sont exécutés avant livraison.

## Décision

Cette protection de traçabilité est metadata-only et fail-closed. Une seconde ligne ou un identifiant invalide peut masquer une reprise non autorisée; le dashboard échoue donc au lieu de sélectionner implicitement une ligne. RE-702 reste terminal: aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute; aucun patch de production n'est autorisé avant cette preuve.
