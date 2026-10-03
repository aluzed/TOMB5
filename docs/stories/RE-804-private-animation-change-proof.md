# RE-804 — GetChange authentique et changement d’animation : checkpoint privé

## Tracker
- [x] 24 cas distincts authentiques nouveaux : 12 GetChange directs et 12 compositions AnimateItem→GetChange; 11 appels helper composés, 23 entrées par répétition, 2090 visites. Deux rejeux frais reviewer, pas 48 cas distincts.
- [x] actual-TU baseline RED avant candidat : 13 échecs par mode, un défaut GetChange direct et 12 AnimateItem stub, pas treize preuves du reset.
- [x] Candidat privé GREEN 24/24 normal et strict ASan+UBSan; quatre mutants CODE normaux : 2/8/12/6.
- [x] Revue indépendante PASS privé borné, aucune préoccupation restante; 10 builds/runs actual-TU frais et un contrôle ABI supplémentaire. 313 entrées manifeste, 314 fichiers originaux inchangés et 643 prédécesseurs vérifiés.
- [ ] RE-805 : régression publique actual-TU du reset GetChange minimal et revue exacte avant patch production.
- [ ] Domaines élargis, registration, callback naturel, fullbuild et gameplay.

## Contrat et attribution
Fixtures synthétiques stationnaires : changements nuls, état égal, goal incorrect, bornes inclusives, deuxième range et deuxième changement. Premier changement manqué puis deuxième admissible expose le compteur non remis à zéro. Le candidat helper privé remet ce compteur à zéro pour chaque changement sélectionné; aucune correction production ici. AnimateItem avance puis appelle réellement GetChange, recharge l’animation/current_state après match et efface required seulement si égal. Douze retours directs et douze retours composés, buffers complets de 268 octets; aucun retour/service simulé. Six matches et six no-matches par mode d’appel. Les visites ne sont pas un compte d’instructions retirées.

Le commentaire source de localisation erroné a été résolu par l’appelant authentique; l’inspection initiale reste archivée. Compteur de sensibilité 10→8 corrigé puis recompilé et rejoué : premier échec conservé. Le mutant sans reset discrimine deux cas, pas toutes les compositions. Revue cible/native fraîche et oracle de buffers indépendant; même moteur Unicorn et mêmes fixtures, pas CPU indépendant. Les événements natifs d’entrée/sortie ne capturent pas une ABI portable exhaustive.

## Limites et statut
- Fixtures synthétiques stationnaires seulement; pas domaine universel ou routine complète.
- Pas nouvelle validation frame_end héritée de RE803.
- Commandes, son, effets, déplacement et gravité exclus.
- Aucun DoorControl élargi ni ProcessClosedDoors validé.
- Unicorn logiciel, pas hardware ou jeu.
- Même moteur CPU et fixtures, oracle buffers indépendant seulement.
- RAM finale hors pile autorisée; écritures transitoires non prouvées.
- i386 C++11 O0 assertions actives, ni LP64 ni NDEBUG.
- ASan sans leaks, UBSan fail-fast, pas sûreté globale du dépôt.
- Instrumentation native entrée/sortie non capture ABI portable ni trace exhaustive.
- Loader, registration, callback naturel, fullbuild/runtime/gameplay exclus; pas de GREEN global.
- Reset GetChange privé prouvé, non production-ready avant régression publique actual-TU et revue exacte.

DoorControl et AnimateItem restent stub, ProcessClosedDoors non implémenté; GetChange garde le défaut de reset production. Candidat privé prouvé n’est pas production-ready. Pas de GREEN global. RE801/RE802/RE803, leurs métadonnées et dashboard historiques gelés; suppressions BLOCKED001/002 et report-tech non suivi préservés.

## Prochaine frontière et calendrier
RE-805 planifiée/non prouvée : régression publique actual-TU GetChange du reset minimal, contrôle normal/strict et revue exacte d’intégration avant tout patch production; aucun GO implicite. Élargir mouvement/commandes/gravité séparément, ne pas rejouer les matrices closes comme nouvelle preuve. Autorisation jusqu’à 03:00 Paris le 3 octobre 2026; stop recherche 02:20, revue 02:40, owner 02:50, aucune extension implicite.

## Preuves publiques sûres
Métadonnées : `docs/reverse/generated/re804-private-animation-change.json`. Comptes, hashes et symboles seulement; aucun contenu cible brut. Revue indépendante SHA256 : 9d2e382e77c4fcd14bcc2e9b94b6debe3458343fa6be90779780c8a669b6c3c1. Publication soumise à sa revue propre, distincte du PASS privé.
