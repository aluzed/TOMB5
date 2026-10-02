# RE-796 — 32 appels authentiques initializer, reconstruction native absente

## Résultat testé
32 appels complets de l’initialiseur générique authentique, entrée jusqu’au vrai retour: quatre orientations × flip absent/présent × navbox blockable absent/présent × portail absent/présent. Allocateur, copie, GetDoor, ShutThatDoor et ItemNewRoom dans les cas portail s’exécutent continûment: aucun retour simulé ni helper sauté. Authentification fraîche et revue indépendante PASS de cette preuve bornée.

Comparaison complète des régions sélectionnées door/item/rooms/floors/boxes/cinq LOT, canary et comptabilité allocateur. Ce n’est ni égalité whole-RAM ni preuve mémoire-sûre. Allocation door cible 92 bytes; projection native explicite 82 bytes d’après les vrais headers i386. La projection enlève les paddings mais conserve des entiers pointeurs: ce n’est ni un adapter de rebasing/déréférence ni une exécution native initializer.

## Dépendances à reconstruire
Respecter snapshots floor avant fermeture, sélection orientation/flip/portail, navbox et LOT, allocation non zéro et tail poison, alias item/room et listes ItemNewRoom. Cas non-head/deferred, échec allocation, géométrie asymétrique et branches spécialisées restent à couvrir. Audit CFG linéaire, pas preuve exhaustive de reachability.

## Tracker
- [x] Matrice authentique 32 appels complets et oracle indépendant revus.
- [x] Projection ABI caractérisée avec headers réels.
- [ ] Implémenter et tester l’initialiseur actual-TU natif avec pointeurs réels.
- [ ] Fermer les dépendances et couvrir les branches spécialisées.

## Suite et limites
RE-797 fournit le seul helper de fermeture désormais intégré; cela ne corrige pas l’initialiseur absent. RE-798: TDD privé actual-TU initializer et fermeture des dépendances; OpenThatDoor peut être une étape de preuve bornée si nécessaire. Control/open/process et registration restent bloqués, pas de GREEN global. Voir BLOCKED-004-door-production-prerequisites et le manifeste metadata-only.
