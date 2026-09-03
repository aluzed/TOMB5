# RE-728 — cohérence de la condition d'arrêt du prédécesseur terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-727, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a constaté qu'un successeur terminal pouvait conserver une direction cohérente tout en affaiblissant silencieusement la condition d'arrêt de son prédécesseur.
- [x] Un test RED couvre RE-728 avec une condition d'arrêt différente de celle de RE-727.
- [x] Le générateur exige désormais, pour les nouveaux handoffs à partir de RE-728, que la condition d'arrêt soit identique à celle du prédécesseur immédiatement antérieur.
- [x] RE-727 et RE-728 publient la même condition d'arrêt, sans rouvrir les dossiers de comportement source.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

La condition d'arrêt qui protège l'inventaire terminal ne peut pas être réduite entre deux handoffs successifs. Cette contrainte fail-closed conserve l'exigence d'un contrat comportemental externe attribuable et d'une preuve ABI non brute. Aucun patch de production n'est autorisé sans ces preuves.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.