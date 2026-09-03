# RE-725 — présence du prédécesseur de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-724, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L’audit a constaté que la cohérence du prédécesseur n’était vérifiée que lorsqu’un champ `predecessor` existait ; son omission cassait silencieusement la chaîne de traçabilité terminale.
- [x] Un test RED couvre un prédécesseur vide et un prédécesseur composé d’espaces.
- [x] Le générateur exige désormais un prédécesseur non vide avant de vérifier sa cohérence pour les nouveaux handoffs à partir de RE-725, sans invalider l'historique publié.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n’a été trouvé dans les artefacts autorisés ; aucun patch de production n’est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Tout nouveau handoff terminal à partir de RE-725 doit déclarer explicitement son prédécesseur. Cette contrainte fail-closed protège la continuité des métadonnées de suivi sans réécrire l'historique publié et ne réinterprète aucun artefact de jeu. Aucun patch de production n’est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d’un contrat comportemental source-backed attribuable et d’une preuve ABI non brute ; aucun patch de production n’est autorisé avant cette preuve.
