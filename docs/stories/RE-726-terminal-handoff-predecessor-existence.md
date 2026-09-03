# RE-726 — existence du prédécesseur de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-725, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L’audit a constaté que le prédécesseur déclaré était contrôlé textuellement, sans confirmer que son handoff publié existait ; une chaîne terminale pouvait donc être orpheline.
- [x] Un test RED couvre un handoff RE-726 dont le prédécesseur cohérent RE-725 n’est pas publié.
- [x] Le générateur exige désormais, pour les nouveaux handoffs à partir de RE-726, que le ticket prédécesseur soit présent parmi les handoffs terminaux publiés, sans invalider l’historique antérieur.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n’a été trouvé dans les artefacts autorisés ; aucun patch de production n’est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Tout nouveau handoff terminal à partir de RE-726 doit référencer un prédécesseur immédiatement antérieur effectivement publié. Cette contrainte fail-closed complète le contrôle de présence et de cohérence de RE-725, protège la traçabilité des métadonnées sans réécrire l’historique et ne réinterprète aucun artefact de jeu. Aucun patch de production n’est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Successeur publié

RE-727 vérifie que le prédécesseur publié désigne explicitement son successeur ; l’intake d’un contrat comportemental source-backed attribuable et d’une preuve ABI non brute reste requis avant tout patch de production.