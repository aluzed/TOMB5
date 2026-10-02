# BLOCKED-004 — Prérequis de production door non fermés

## État actuel — frontière RE-801
RE-800 : **OpenThatDoor intégré** sous gate PSX_VERSION/PSXPC_TEST/i386, 3328/3328 normal et ASan+UBSan; ShutThatDoor intégré 144/144. RE-801 apporte une **preuve privée** exécutée de la branche lift DoorControl trigger_flags==1 : 16 séquences, 96 appels, baseline RED 96 échecs par mode puis candidat privé GREEN; revue finale archivale PASS seulement sur ce périmètre. Premier reviewer frais interrompu sans verdict; artifacts finaux distingués des timeout/provider. **DoorControl reste stub et ProcessClosedDoors non implémenté en production**, registration non activée, callback bridge naturel bloqué : **pas de GREEN global**.

InitialiseDoor RE-798 reste privé non intégré, domaines élargis/non-head/différés/spécialisés non fermés. RE-794 à RE-800, BLOCKED-003 et sections historiques dashboard gelés; BLOCKED-001/002 supprimés non recréés. Aucun historique stub OpenThatDoor ne décrit la frontière courante.

## Critères de reprise
1. **RE-802** planifiée/non prouvée : une nouvelle branche générique **non-lift** predicate/state de DoorControl, dépendances réelles authentifiées et transitions; actual-TU RED comportemental avant candidat privé, état/trace, GREEN borné et revue indépendante. Ne pas répéter anciennes matrices helpers. Chemin spécial timer séparé; aucun GO supplémentaire.
2. Dépendance absente = blocker explicite, pas retour simulé. La branche lift RE-801 ne ferme ni autres branches/callers ni intégration. ProcessClosedDoors exige preuve propre.
3. Fermer initializer élargi, buffers/origines asymétriques, portails/listes et producteurs spécialisés séparément.
4. Revue exacte d'intégration et normal/sanitizers avant source; registration seulement après contrat cohérent.
5. Callback naturel, fullbuild, runtime/gameplay distincts. Autorisation parent jusqu'à 03:00; recherche 02:20, revue 02:40, owner 02:50; aucune extension implicite.

## Tracker
- [x] ShutThatDoor et OpenThatDoor intégrés sous gate i386 borné.
- [x] RE-801 lift preuve privée, pas intégration DoorControl.
- [x] RED, erreurs copies/ABI/provider et verdict archivage distingués.
- [ ] RE-802 non-lift, DoorControl complet, ProcessClosedDoors et initializer élargi.
- [ ] Registration cohérente, callback bridge naturel et gameplay global.

## Preuves publiques sûres
Voir RE-794 à RE-801 et `docs/reverse/generated/re801-private-door-control.json`. Comptes/readiness/hashes seulement; aucun dump/adresse/opcode/asset. Prochaine histoire **RE-802**, planifiée et non prouvée.
