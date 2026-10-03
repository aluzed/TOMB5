# RE820 — orientations non nulles, sans portail ni flip

**Private producer findings pending independent review**. Publication metadata-only
PENDING_REVIEW; private_review=PENDING_INDEPENDENT_REVIEW; intégration BLOCKED.
Ces résultats sont ceux du producteur privé, non une certification indépendante.

## Domaine nouveau et frontière réelle
Cinq fixtures construites objet284: angles 0, -32768, 16384, -16384, 1;
cellules discriminantes 11,13,7,17,17. Portail absent, tous flips absents.
Angle1 est une branche logicielle finie non cardinale; aucune provenance naturelle.
Registration SETUP privée partielle exécutée, slot adjacent préservé, puis appel
**direct de l'initialiseur privé**: pas une nouvelle composition InitialiseItem,
pas de nouveau caller prouvé, pas de natural startup. ITEMS/COLLIDE liés ne
signifie pas navigation exécutée: ItemNewRoom appelé zéro fois.

## Résultats privés déclarés et sensibilité
Dix exécutions natives fraîches (cinq normales, cinq ASan+UBSan strictes), exit0,
stderr vide. MALLOC.C réel natif et init_game_malloc employés. Buffers complets
1088324 octets égaux à l'oracle déclaratif et projection cible, zéro différence.
Cinq replays logiciels directs de l'initialiseur cible authentique; projection
2980 octets, descripteur contrôlé séparément. RAM archivée n'est pas un oracle
exhaustif de toute RAM. Ordre: allocation, GetDoor, GetDoor, ShutThatDoor,
ShutThatDoor; les positions flip nulles sont incluses. Native82 demandés/84
consommés contre cible92: rebasing explicite, tails préservés, pas identité ABI.

Le refus initial SIGILL exit-4 normal/strict est un RED de domaine, **pas un RED
comportemental**. Mutant calcul anglezéro sans refus: exécution exit0 sans stderr,
cellule11 au lieu7; contrat exit1 normal/strict, 11 octets différents dans chaque
mode après rebasing. Ceci est le vrai RED comportemental, pas une corruption
artificielle des observations. Leakchecking ASan explicitement désactivé.

## Progression / acceptation restante
- [x] Producteur privé: domaine fini discriminant nonzero/sansportail exécuté.
- [x] Publication metadata-only sous contrat TDD, production inchangée.
- [ ] Revue indépendante de cette livraison privée et publication exacte.
- [ ] Provenance caller/orientations naturellement atteints et compatibilité ABI.
- [ ] Portail/flip, domaine général et intégration séparément autorisée.

Aucun gameplay, matériel/SDK/GTE, startup naturel, ObjectObjects complet,
controller/AnimateItem, absence générale d'UB ou GREEN global certifié.
BLOCKED-006 reste ouvert; pas d'activation ni de nouveau caller/naturalstartup.
La revue concurrente n'est pas consommée et ne peut promouvoir ces métadonnées.
Ne pas répéter la matrice allocateur RE819; frontière suivante: revue puis
provenance naturelle/caller ou domaine portail/flip distinct.
