# RE-795 — Producteur générique door natif absent

## Résultat testé
ObjectObjects réel, TU SETUP.C i386 et vrais headers: quatre cas loaded/non-loaded et slots nuls/empoisonnés, 46 records door par cas, aucune installation native. Le test comportemental d’installation reste RED (exit1); caractérisation de l’absence PASS (exit0). Cette caractérisation n’est pas un GREEN correctif. Les autres modifications Lara/bridge et voisins sont comparées sur la table complète.

La boucle authentique générique est exécutée sous état synthétique: 14 slots non-MIP pour chacune des deux conditions loaded, RAM entière comparée pour ce segment. Le préfixe authentique vérifie les registres entrants. Boot et 15 copies module réauthentifiés, relocation exécutée; provenance des descripteurs d’extraction héritée. Ni ObjectObjects cible complet, ni startup ni corps installés exécutés ici.

## Blocage concret
Le setup désactivé est du staging source incomplet, pas une preuve que les doors authentiques doivent être sans registration. InitialiseDoor natif manque; enregistrer un symbole inexistant ou activer tout le bloc désactivé ne reconstruit rien. Les 14 slots cible, 46 records fixture et 28 noms door live sont des périmètres distincts. Familles spécialisées non prouvées.

## Tracker
- [x] Absence du producteur natif prouvée par actual-TU RED.
- [x] Contrat générique cible revu indépendamment et borné.
- [ ] Reconstruire l’initialiseur et les dépendances avant activation.
- [ ] Activer une registration cohérente sous nouvelle preuve actual-TU.

## Suite et limites
RE-796 prouve 32 appels initializer cible; RE-797 intègre seulement ShutThatDoor sous backend borné. Registration toujours non activée, pas de GREEN global. RE-798 doit poursuivre la reconstruction privée et sa fermeture; voir BLOCKED-004-door-production-prerequisites et le manifeste metadata-only.
