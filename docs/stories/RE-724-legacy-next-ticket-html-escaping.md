# RE-724 — échappement HTML du prochain ticket hérité

Status: `Done`

## Progress tracker

- [x] Le handoff terminal RE-723, le handoff parent autoritaire RE-702 et le dashboard ont été relus avant modification.
- [x] L'audit a constaté que `next_ticket` était échappé par les règles terminales actuelles, mais pouvait être projeté sans échappement si le générateur rendait un dernier handoff historique antérieur au seuil terminal.
- [x] Un test RED fournit un `next_ticket` hérité contenant une balise HTML et vérifie que la projection reste textuelle.
- [x] Le générateur échappe désormais aussi `next_ticket` au point de projection HTML, quel que soit l'âge du handoff.
- [x] Aucun contrat comportemental externe attribuable ni preuve ABI non brute n'a été trouvé dans les artefacts autorisés ; aucun patch de production n'est tenté.
- [x] Le dashboard reste déterministe, terminal et sans backlog actif.

## Décision

Le dashboard doit traiter tout champ de métadonnées comme du texte à sa frontière HTML, y compris lorsqu'une compatibilité avec un handoff historique est conservée. Cet échappement fail-closed de présentation ne réinterprète aucun artefact de jeu et ne rouvre pas RE-702. Aucun patch de production n'est autorisé sans contrat comportemental externe attribuable et preuve ABI non brute.

## Next safe objective

`TBD` — intake d'un contrat comportemental source-backed attribuable et d'une preuve ABI non brute ; aucun patch de production n'est autorisé avant cette preuve.
