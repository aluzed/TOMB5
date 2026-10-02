# BLOCKED-004 — Prérequis de production door non fermés

## État actuel
RE-794 observe un premier portail naturel natif; RE-795 conserve RED pour le producteur générique absent; RE-796 prouve 32 initializer authentiques, pas une reconstruction native; RE-797 intègre seulement ShutThatDoor i386 et vérifie 144 cas normal/sanitizer. Registration non activée et callback bridge naturel toujours bloqué, pas de GREEN global.

Défauts source encore présents: InitialiseDoor absent; DoorControl, OpenThatDoor et ProcessClosedDoors non implémentés. Ils ne deviennent pas de simples limites parce qu’un helper est GREEN. Les histoires et BLOCKED-003 antérieurs sont gelés; BLOCKED-001/002 supprimés ne sont pas recréés.

## Critères de reprise
1. RE-798: écrire d’abord des tests privés actual-TU initializer RED sur structures réelles et buffers complets; implémenter ensuite allocation, pointeurs réels, floor/flip/portal/navbox et listes ItemNewRoom.
2. Fermer et prouver les dépendances requises: OpenThatDoor peut recevoir une preuve bornée séparée; Control/ProcessClosedDoors exigent leur propre reconstruction. Ne pas activer un producer incomplet.
3. Comparer aux cas authentifiés indépendants; étendre origines/dimensions asymétriques, portails flip distincts, non-head/deferred, échecs allocation et branches spécialisées. Aucun élargissement implicite aux familles non prouvées.
4. Exiger revue indépendante, normal/sanitizer sans diagnostic et gate du backend effectivement testé avant toute nouvelle intégration. Activation registration seulement après contrat cohérent prouvé.
5. Établir ensuite une route runtime naturelle et callbacks consommés; fullbuild/gameplay restent des obligations distinctes. Aucune nouvelle autorisation de runtime ou de prolongation accordée par ce document.

## Tracker
- [x] Producteur absent documenté et RED préservé.
- [x] Initializer cible borné et helper ShutThatDoor intégré distingués.
- [x] Ancien FAILED et claim sanitizer invalide explicitement conservés.
- [ ] Initializer/control/open/process natifs et registration cohérente.
- [ ] Callback bridge naturel et gameplay global.

## Preuves publiques sûres
Voir RE-794 à RE-797 et docs/reverse/generated/re794-re797-door-progress.json: métadonnées, comptes, hashes de verdict et readiness seulement. Aucun dump, adresse, opcode, coordonnées, état brut ou asset publié. Prochaine histoire RE-798, dans l’autorisation existante seulement.
