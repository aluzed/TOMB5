# RE-731 — sûreté de format de l'identifiant de story terminal

Status: `Done`

## Progress tracker

- [x] Le handoff RE-730, le parent autoritaire RE-702, le dashboard et les derniers commits ont été relus avant modification.
- [x] Le parent RE-702 reste terminal : `source_behavior_proof_count=0`, `source_patch_authorized_count=0`, domaine et pivot `none`.
- [x] Un test RED reproduit un champ `story_id` contenant un caractère de format Unicode invisible.
- [x] Le générateur refuse ce caractère avant la comparaison de l'identifiant avec le nom du handoff.
- [x] RE-730 annonce explicitement RE-731 et le sujet annoncé correspond au sujet publié.
- [x] RE-731 préserve la condition d'arrêt du parent ; aucun contrat comportemental attribuable ni preuve ABI non brute n'est apparue.
- [x] Aucun patch de production, asset, binaire, dump brut, donnée d'instruction, position interne ou texte propriétaire de désassemblage n'est produit.
- [x] Le dashboard est régénéré de manière déterministe et demeure terminal, sans backlog actif.

## Décision

Un caractère de format Unicode invisible dans `story_id` est désormais rejeté explicitement avant tout contrôle d'identité. Cette défense fail-closed rend l'erreur de format déterministe et préserve l'intégrité de la chaîne terminale, sans rouvrir l'inventaire RE-702. La réouverture reste conditionnée à un contrat comportemental source-backed attribuable et à une preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.