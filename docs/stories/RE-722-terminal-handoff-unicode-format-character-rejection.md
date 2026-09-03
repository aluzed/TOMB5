# RE-722 — rejet des caractères de format Unicode dans les handoffs terminaux

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-721, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a constaté que RE-721 refusait la catégorie Unicode `Cc`, mais pas les caractères de format invisibles de catégorie `Cf`.
- [x] Un test RED injecte `U+200B` dans une condition d'arrêt terminale.
- [x] Le générateur refuse désormais fail-closed les catégories Unicode `Cc` et `Cf` dans tous les champs terminaux projetés.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Les caractères de format Unicode invisibles peuvent modifier la lisibilité des métadonnées projetées sans apporter de preuve de comportement. Leur rejet ferme cette ambiguïté de présentation sans interpréter d'artefact de jeu, sans réinterpréter l'historique et sans rouvrir RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.