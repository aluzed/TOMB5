# BLOCKED-004 — Prérequis de production door non fermés

## État actuel — frontière RE-800
RE-800 : **OpenThatDoor intégré** sous gate PSX_VERSION/PSXPC_TEST/i386 après acceptation indépendante du patch exact. Actual-TU publique 3328/3328 normal et ASan+UBSan; baseline RED 2944/3328 conservée; cinq mutants code rejetés. ShutThatDoor reste intégré et vérifié 144/144 dans les deux modes. Ces helpers ne ferment pas la chaîne door : registration non activée et callback bridge naturel toujours bloqué, **pas de GREEN global**.

InitialiseDoor reste non intégré : RE-798 est un prototype privé borné, les domaines élargis non-head/différés/spécialisés ne sont pas fermés. **DoorControl et ProcessClosedDoors restent non implémentés en production**, chacun exige reconstruction et preuve propre. La preuve initializer cible RE-796 n'est pas une intégration native. RE-794/795/796/797 et les stories RE-798/799, BLOCKED-003 et les sections dashboard historiques restent gelés. BLOCKED-001/002 supprimés ne sont pas recréés. Le constat OpenThatDoor stub dans l'historique ne décrit plus la frontière courante.

## Critères de reprise
1. **RE-801 / DoorControl** : une branche atteignable minimale sur objet valide, entrée/retour cible authentifiés et dépendance réellement exercée; test privé actual-TU d'abord, RED comportemental puis candidat borné. Comparer état sélectionné et trace d'appels; ne pas répéter les anciennes matrices helpers.
2. Si dépendance requise absente, garder un blocker explicite et RED, sans retour simulé revendiqué comme équivalence. ProcessClosedDoors exige ensuite sa propre reconstruction, pas une conclusion tirée de OpenThatDoor.
3. Fermer les domaines initializer allocation/listes non-head et différées, origines/dimensions asymétriques, portails flip distincts et branches spécialisées; RE-798 reste une preuve privée étroite, pas validation de tous les producteurs.
4. Revue indépendante, normal/sanitizers sans diagnostic et gate du backend prouvé avant toute nouvelle intégration. Registration seulement après contrat cohérent; ne pas activer un producer incomplet.
5. Callback naturel, fullbuild et gameplay restent obligations distinctes. Aucun runtime ni élargissement d'autorisation accordé par ce document.

## Tracker
- [x] Producteur absent et ancien RED préservés comme historique.
- [x] Initializer privé borné distingué de l'intégration native.
- [x] ShutThatDoor et OpenThatDoor intégrés sous gate i386 borné.
- [x] Ancien FAILED et claim sanitizer invalide conservés dans l'historique gelé.
- [ ] Initializer élargi, DoorControl et ProcessClosedDoors natifs prouvés.
- [ ] Registration cohérente, callback bridge naturel et gameplay global.

## Preuves publiques sûres
Voir RE-794 à RE-800; métadonnées historiques `docs/reverse/generated/re794-re797-door-progress.json` non réécrites et nouveau `docs/reverse/generated/re800-openthatdoor-integration.json`. Comptes/readiness/hashes seulement, sans dumps/adresses/opcodes/assets. Prochaine histoire **RE-801**, planifiée et non prouvée, dans l'autorisation renouvelée uniquement.
