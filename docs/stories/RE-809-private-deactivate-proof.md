# RE-809 — Constat privé désactivation et blocage prédécesseur
Auteur : AlexP — statut blocked; revue finale publication pending.

## Tracker
READINESS : blocked
- [x] Clarification indépendante acceptée pour caractérisation privée seulement; verdict original rejeté et préservé, jamais PASS réutilisable.
- [x] 271 fichiers authentifiés; 12 retours réels, 1098 visites hooks, 17150 octets buffers complets par cas archivés.
- [x] actual-TU RemoveActiveItem : 6 fixtures, RED2 par mode normal/strict, uniquement nonhead-middle/nonhead-tail; actual-TU AnimateItem stub : 6 fixtures, RED6.
- [x] Publication FIRST RED et exclusion nominative RE809; dashboard antérieur entier protégé.
- [ ] BLOCKED-005-removeactiveitem-predecessor-link : prérequis correctif privé.
- [ ] RE-810 : delta privé predecessor-link RED sensible, buffers/events complets normal/strict; revue indépendante avant intégration.
- [ ] Revue finale indépendante publication : pending.
- [ ] Intégration, activation et readiness production : non autorisées.

## Constat et portée
Le lien du prédécesseur n’est pas mis à jour par le helper public dans les deux cas non-head middle/tail. Les contrôles head, active-absent, inactive-present et active-empty concordent dans ce seul jeu. inactive-present viole l’invariant producteur et reste un contrôle synthétique explicite. AddActiveItem est attribué statiquement seulement, aucune reachability naturelle ou gameplay. Chaînes construites acycliques, quatre items; pas corpus authentique.
Opcode3 est ignoré sur les chemins dispatch exécutés par les six fixtures, liaison et retour observés; aucune absence universelle, aucun CFG complet/callees/image général certifié. Aucun candidat cmd3 inventé, aucune activation. RED du stub entier AnimateItem ne démontre pas une causalité spécifique cmd3.
Comparaisons RAM/buffers finaux et events ordonnés archivés, pas accès transitoires ni mémoire processus entière. Stack archivée comparée sans oracle indépendante. Strict RED comportemental sans diagnostic sur ces fixtures, pas preuve universelle d’absence UB. Aucun replay cible ni nouvelle recherche par publication.

## Clarification et incidents
Le passed=true original avec concerns/errors est rejeté; ses octets restent intacts. La nouvelle clarification distingue défaut production bloquant, absence universelle rejetée, déviation verrou canonique et scratch non sandbox OS. Pas conformité rétroactive. stderr original syntaxe manquant : source fautive et exit1 conservés, diagnostic frais séparé, aucune prétention tous logs conservés.

## Vérification séparée et limites
GetChange public courant : actual-TU 1440 cas normal/strict vérifiés dans livraison publication, aucun skip autorisé; pas matrice cible. Aucun sourcepatch, fullbuild/runtime/gameplay; pas de GREEN global. Histoires/métadonnées précédentes, sources, index, report utilisateur et suppressions BLOCKED001/002 intacts. mutation.lock bref; aucun stage/commit/push. Recherche STOP11:25, revue11:45, livraison owner11:55, deadline12:00 Paris. Ce checkpoint publie un constat bloqué, pas clôture source.
