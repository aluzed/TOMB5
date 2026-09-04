# RE-729 — cohérence du sujet annoncé par le prédécesseur terminal

Status: `Done`

## Progress tracker

- [x] Les handoffs terminaux RE-728 et RE-702, le dashboard et les derniers commits ont été relus avant modification.
- [x] Le parent autoritaire RE-702 reste terminal : `source_behavior_proof_count=0`, `source_patch_authorized_count=0`, domaine et pivot `none`.
- [x] Un test RED reproduit un prédécesseur qui annonce `RE-729` mais un `next_topic` différent du sujet réel de RE-729.
- [x] Le générateur exige désormais, à partir de RE-729, que `predecessor.next_topic` soit identique à `topic` du handoff successeur.
- [x] RE-728 annonce explicitement RE-729 et son sujet publié est identique au sujet de RE-729.
- [x] RE-729 conserve la condition d'arrêt du parent ; aucun contrat comportemental attribuable ni preuve ABI non brute n'est apparu.
- [x] Aucun patch de production, asset, binaire, dump brut, opcode, offset ou pseudocode propriétaire n'est produit.
- [x] Le dashboard est régénéré de manière déterministe et demeure terminal, sans backlog actif.

## Décision

Une référence de ticket ne suffit pas à assurer la continuité de la chaîne : le sujet annoncé par le prédécesseur doit désigner le sujet réellement publié par son successeur. Cette vérification fail-closed protège la traçabilité des handoffs sans rouvrir l'inventaire RE-702. La réouverture reste conditionnée à un contrat comportemental source-backed attribuable et à une preuve ABI non brute.

## Next safe objective

Remplacé par `RE-730` — sûreté de format du prédécesseur terminal ; le blocage de fond reste l'intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute.
