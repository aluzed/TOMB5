# BLOCKED-004 — Prérequis de production door non fermés

## État actuel — frontière RE-804
RE-804 : preuve privée GetChange authentique, 24 cas nouveaux (12 directs/12 AnimateItem composés, 11 appels helper composés), 2090 visites par répétition, deux rejeux frais; baseline actual-TU RED13 (un helper, 12 stub), candidat GREEN24 normal/strict; mutants CODE 2/8/12/6. Revue indépendante PASS borné. Reset GetChange privé prouvé, non production-ready; sources inchangées, DoorControl/AnimateItem stub, ProcessClosedDoors absent, registration bloquée, pas de GREEN global.
**RE-805** planifiée/non prouvée : régression publique actual-TU du reset minimal GetChange et revue exacte avant tout patch production; aucune répétition de matrices closes ni GO implicite.

## Checkpoint historique — frontière RE-803
RE-803 : 16 AnimateItem stationnaires privés, 1716 visites; quatre compositions synthétiques DoorControl→TriggerActive→AnimateItem, 642 visites, retour réel. Baseline RED16/4 puis candidat GREEN16/4 normal, ASan, UBSan et combiné; revue distincte fraîche19 builds/runs,271 hashes inchangés, CODE mutants16/8/16. Acceptation de fixtures seulement, aucun self-loop/mouvement/commandes/gravité ni GetChange authentique. Production stub inchangée, pas de GREEN global.

## Checkpoint historique — frontière RE-802
RE-800 : **OpenThatDoor intégré** sous gate PSX_VERSION/PSXPC_TEST/i386, 3328/3328 normal et ASan+UBSan; ShutThatDoor intégré 144/144. La frontière RE-801 lift reste une preuve privée non intégrée, revue finale archivale; historique gelé. **RE-802** ferme seulement le préfixe générique **non-lift** privé : TriggerActive réel, 40 cas (20 actifs/20 inactifs), 2408 visites hooks, 120 événements; baseline RED événements 40/état 26 puis candidat GREEN 40/40 normal/strict, cinq code mutants normaux discriminants. Revue indépendante fraîche cible/native PASS borné, pas approbation d'intégration/publication.

Arrêt AVANT première instruction AnimateItem; natif observe entrée puis exception sans retour, aucun retour simulé. **DoorControl et AnimateItem restent stub**, ProcessClosedDoors non implémenté production, registration non activée, callback bridge naturel bloqué : **pas de GREEN global**. Aucun runtime/fullbuild/gameplay.
InitialiseDoor RE-798 reste privé non intégré, domaines élargis/non-head/différés/spécialisés non fermés. RE-794 à RE-801, BLOCKED-003 et sections historiques dashboard gelés; BLOCKED-001/002 supprimés non recréés. Aucun historique stub OpenThatDoor ne décrit la frontière courante.

## Critères de reprise
1. **RE-805** planifiée/non prouvée : régression publique actual-TU du reset minimal GetChange, RED production puis candidat normal/strict et revue exacte avant correction production. RE-804 ferme uniquement les fixtures privées; ne pas répéter les matrices closes.
2. Dépendance absente = blocker explicite, pas retour simulé. Préfixe ne ferme ni AnimateItem, retour DoorControl, autres branches/callers ni intégration. ProcessClosedDoors exige preuve propre.
3. Fermer initializer élargi, buffers/origines asymétriques, portails/listes et producteurs spécialisés séparément.
4. Revue exacte d'intégration et normal/sanitizers avant source; registration seulement après contrat cohérent.
5. Callback naturel, fullbuild, runtime/gameplay distincts. Autorisation parent jusqu'à 03:00 Paris le 3 octobre 2026; recherche 02:20, revue 02:40, owner 02:50; children au plus 900 s bornés au temps restant, aucune extension implicite.

## Tracker
- [x] ShutThatDoor et OpenThatDoor intégrés sous gate i386 borné.
- [x] RE-801 lift preuve privée, pas intégration DoorControl.
- [x] RE-802 non-lift préfixe privé revu frais, RED/GREEN et code mutants.
- [x] Timeout, setup/link/checker RED et HANDOFF 00:59 obsolète conservés séparément.
- [x] RE-803 AnimateItem stationnaire et composition synthétique bornés, privés seulement.
- [x] RE-804 GetChange authentique privé borné, sans patch production.
- [ ] RE-805 régression publique actual-TU et revue exacte du reset; DoorControl élargi, ProcessClosedDoors et initializer élargi.
- [ ] Registration cohérente, callback bridge naturel et gameplay global.

## Preuves publiques sûres
Voir RE-794 à RE-804 et `docs/reverse/generated/re802-private-door-prefix.json`. Comptes/readiness/hashes/symboles seulement; aucun dump/adresse/opcode/asset. Prochaine histoire **RE-805**, planifiée et non prouvée.

## Checkpoint courant RE817 — evidence acceptance, non GO production

RE815/816 livrés restent historiques gelés. RE817 récupération indépendante privée
PRIVATE_ONLY_PASS distincte du timeout original NON CERTIFIÉ et de attempt01 rejetée.
Initializer direct privé actual-TU normal/strict : baseline RED1 candidat GREEN0,
cible994 visites/2992 octets, oracle projeté2980 et ledger11 discriminants par mode,
deux mutants code rejetés. Allocation native82 vs cible92; allocateur double déclaré.
Une fixture generic284 angle0 rooms0..3 portal2/sentinelle255 seulement.
Voir [RE817](../RE-817-native-initializer-prerequisite.md), verdict et manifest épinglés.

Acceptance : preuve privée du prerequisite initializer, pas registration ou InitialiseItem
natifs, pas composition caller, allocateur réel ou domaine général. Publication finale
pending revue parent séparée; aucune approbation intégration/activation/production.
BLOCKED-003/004/006 restent ouverts; BLOCKED-001/002 ne sont pas recréés.
Prochaine frontière RE818 non effectuée : composition conditionnelle producer/caller
actual-native, callback et retours réels, oracle indépendant borné, baseline RED/candidat
GREEN normal/strict, provenance exacte puis revue indépendante. Preuve domaine élargi
et allocateur réel restent distinctes; ne pas rejouer les matrices closes.

- [x] RE817 preuve privée récupération indépendante acceptée scoped.
- [ ] Revue publication RE817 finale parent.
- [ ] RE818 composition conditionnelle actual-native, domaine général et allocateur réel.
