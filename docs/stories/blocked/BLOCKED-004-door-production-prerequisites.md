# BLOCKED-004 — Prérequis de production door non fermés

## État actuel — frontière RE-802
RE-800 : **OpenThatDoor intégré** sous gate PSX_VERSION/PSXPC_TEST/i386, 3328/3328 normal et ASan+UBSan; ShutThatDoor intégré 144/144. La frontière RE-801 lift reste une preuve privée non intégrée, revue finale archivale; historique gelé. **RE-802** ferme seulement le préfixe générique **non-lift** privé : TriggerActive réel, 40 cas (20 actifs/20 inactifs), 2408 visites hooks, 120 événements; baseline RED événements 40/état 26 puis candidat GREEN 40/40 normal/strict, cinq code mutants normaux discriminants. Revue indépendante fraîche cible/native PASS borné, pas approbation d'intégration/publication.

Arrêt AVANT première instruction AnimateItem; natif observe entrée puis exception sans retour, aucun retour simulé. **DoorControl et AnimateItem restent stub**, ProcessClosedDoors non implémenté production, registration non activée, callback bridge naturel bloqué : **pas de GREEN global**. Aucun runtime/fullbuild/gameplay.
InitialiseDoor RE-798 reste privé non intégré, domaines élargis/non-head/différés/spécialisés non fermés. RE-794 à RE-801, BLOCKED-003 et sections historiques dashboard gelés; BLOCKED-001/002 supprimés non recréés. Aucun historique stub OpenThatDoor ne décrit la frontière courante.

## Critères de reprise
1. **RE-803** planifiée/non prouvée : minimum réel de corps/prérequis AnimateItem; authentifier entrée/retour cible et dépendances effectivement exercées, actual-TU RED comportemental avant candidat privé, état/trace et GREEN borné normal/strict, revue indépendante. Ne pas répéter matrices du préfixe RE-802 fermé ni anciennes matrices helpers.
2. Dépendance absente = blocker explicite, pas retour simulé. Préfixe ne ferme ni AnimateItem, retour DoorControl, autres branches/callers ni intégration. ProcessClosedDoors exige preuve propre.
3. Fermer initializer élargi, buffers/origines asymétriques, portails/listes et producteurs spécialisés séparément.
4. Revue exacte d'intégration et normal/sanitizers avant source; registration seulement après contrat cohérent.
5. Callback naturel, fullbuild, runtime/gameplay distincts. Autorisation parent jusqu'à 03:00 Paris le 3 octobre 2026; recherche 02:20, revue 02:40, owner 02:50; children au plus 900 s bornés au temps restant, aucune extension implicite.

## Tracker
- [x] ShutThatDoor et OpenThatDoor intégrés sous gate i386 borné.
- [x] RE-801 lift preuve privée, pas intégration DoorControl.
- [x] RE-802 non-lift préfixe privé revu frais, RED/GREEN et code mutants.
- [x] Timeout, setup/link/checker RED et HANDOFF 00:59 obsolète conservés séparément.
- [ ] RE-803 AnimateItem réel, DoorControl complet, ProcessClosedDoors et initializer élargi.
- [ ] Registration cohérente, callback bridge naturel et gameplay global.

## Preuves publiques sûres
Voir RE-794 à RE-802 et `docs/reverse/generated/re802-private-door-prefix.json`. Comptes/readiness/hashes/symboles seulement; aucun dump/adresse/opcode/asset. Prochaine histoire **RE-803**, planifiée et non prouvée.
