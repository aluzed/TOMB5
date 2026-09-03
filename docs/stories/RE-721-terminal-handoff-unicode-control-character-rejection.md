# RE-721 — rejet des caractères de contrôle Unicode dans les handoffs terminaux

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-720, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a constaté que la protection RE-720 couvrait C0 et DEL, mais ne formulait pas explicitement l'ensemble Unicode des caractères de contrôle.
- [x] Un test RED injecte le contrôle C1 `U+0085` dans une condition d'arrêt terminale.
- [x] Le générateur utilise désormais la catégorie Unicode `Cc` et refuse fail-closed les contrôles C0, C1 et DEL avant toute projection HTML.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Les champs terminaux projetés sont des métadonnées textuelles Unicode. Le rejet de toute catégorie `Cc` ferme l'écart C1 sans interpréter d'artefact de jeu, sans réinterpréter l'historique et sans rouvrir RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.