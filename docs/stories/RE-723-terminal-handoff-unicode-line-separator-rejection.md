# RE-723 — rejet des séparateurs de ligne Unicode dans les handoffs terminaux

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-722, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a constaté que RE-722 refusait les contrôles et formats Unicode, mais pas les séparateurs de ligne et de paragraphe Unicode (`Zl`, `Zp`).
- [x] Un test RED injecte `U+2028` dans une condition d'arrêt terminale.
- [x] Le générateur refuse désormais fail-closed les catégories Unicode `Cc`, `Cf`, `Zl` et `Zp` dans tous les champs terminaux projetés.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Les séparateurs Unicode de ligne et de paragraphe peuvent fragmenter visuellement un champ de métadonnées projeté sans apporter de preuve de comportement. Leur rejet ferme cette ambiguïté de présentation sans interpréter d'artefact de jeu, sans réinterpréter l'historique et sans rouvrir RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.