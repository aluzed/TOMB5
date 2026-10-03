# BLOCKED-005 — RemoveActiveItem : lien du prédécesseur
Statut : blocked — AlexP. Constat RE-809, aucun correctif source intégré.

## Evidence bornée
Clarification privée indépendante acceptée; verdict original rejeté et préservé. Archives producteur et revue authentifiées par 271 hashes. Six fixtures helper actual-TU : RED2 normal et strict, nonhead-middle et nonhead-tail; quatre contrôles concordants. Douze retours réels au total, 1098 visites, buffers17150 octets; six autres fixtures AnimateItem stub RED6 ne justifient aucun candidat cmd3. Opcode3 ignoré sur dispatchs exécutés seulement; pas absence universelle.
Le helper public réécrit le lien de l’item retiré au lieu du prédécesseur; ce constat bloque la correction production/intégration. Références privées : build/reverse/autonomy-20261003/re809-review/fresh-native-deltas.json, normal-run.stdout, strict-run.stdout et re809-review-clarification/verdict.json. Pas reproduction cible supplémentaire lors de publication.

## Acceptation RE-810 proposée, NON exécutée
- [ ] Delta PRIVATE predecessor-link seulement; conserver actual-TU baseline RED sensible et démontrer mutants/omission qui échouent.
- [ ] Cas zero/head/middle/tail/absent, chaînes et sentinelle explicites; inactive-present identifié comme contrôle hors invariant, pas reachability naturelle.
- [ ] Comparer tous buffers complets et events ordonnés, pas seulement lien final; modes normal et strict sans skip, journaux complets et fingerprints.
- [ ] Revue indépendante du delta privé avant intégration; aucune intégration, activation, cmd3 inventée, runtime ou GREEN global par ce ticket.
- [ ] Autorisation distincte nécessaire pour tout changement production après preuve et revue.

Incidents/limites : verrou canonique dévié historiquement, scratch non sandbox; stderr original syntaxe absent, diagnostic frais distinct. Ce nouveau BLOCKED-005 ne restaure ni BLOCKED001 ni BLOCKED002 supprimés par utilisateur.
