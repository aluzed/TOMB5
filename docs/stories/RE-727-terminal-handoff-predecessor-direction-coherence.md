# RE-727 — cohérence de direction du prédécesseur de handoff terminal

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-726, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L’audit a constaté qu’un prédécesseur publié pouvait déclarer une clôture (`TBD`/`none`) tout en étant référencé par un nouveau handoff ; la chaîne était alors contradictoire.
- [x] Un test RED couvre RE-727 dont le prédécesseur RE-726 existe mais ferme encore la chaîne.
- [x] Le générateur exige désormais, pour les nouveaux handoffs à partir de RE-727, que le prédécesseur immédiatement antérieur désigne explicitement le ticket courant.
- [x] RE-726 désigne RE-727, ce qui rend la transition publiée cohérente sans rouvrir les dossiers de comportement source.
- [x] RE-727 désigne RE-728 afin de poursuivre l'audit fail-closed de la condition d'arrêt publiée.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n’a été trouvé dans les artefacts autorisés ; aucun patch de production n’est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Tout nouveau handoff terminal à partir de RE-727 doit avoir un prédécesseur publié, immédiatement antérieur, dont `next_ticket` désigne ce ticket. Cette contrainte fail-closed complète les contrôles d’existence et de cohérence du prédécesseur, protège la traçabilité des métadonnées et ne réinterprète aucun artefact de jeu. Aucun patch de production n’est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d’un contrat comportemental source-backed attribuable et d’une preuve ABI non brute ; aucun patch de production n’est autorisé avant cette preuve.
