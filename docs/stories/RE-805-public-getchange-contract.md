# RE-805 — Régression publique GetChange actual-TU, production inchangée

Auteur : AlexP

## Tracker
- [x] Contrat synthétique autonome public : 1440 cas distincts par mode, sans assets ni build privé en entrée.
- [x] Vraies unités compilées intégralement : SPEC_PSXPC_N/CONTROL_S.C et GAME/ITEMS.C; GetChange est défini dans la première, pas dans ITEMS.C. Aucun appelant ITEMS validé par cette compilation.
- [x] Baseline comportemental RED avant écriture du candidat : 48 divergences de buffers dans chacun des modes normal et strict ASan+UBSan, build réussi; stderr runtime vide.
- [x] Candidat privé minimal : une remise à zéro du compteur j à chaque changement admissible, aucune autre modification; GREEN1440/1440 dans les deux modes.
- [x] Oracle indépendant : ensemble de couples changement/range admissibles et choix lexicographique minimal, pas copie du helper ni réponses cible importées.
- [x] Preuve indépendante RE804 existante consommée, aucune nouvelle matrice cible RE804.
- [ ] Revue exacte indépendante de ces fichiers, des hashes, logs et transformation privée.
- [ ] Intégration production autorisée séparément après revue; aucun GO implicite.

## Domaine vérifié
Trois changements admissibles, premier sans match puis deuxième avec match au premier/deuxième/troisième range, et troisième de repli avec sortie distincte : discrimine le compteur partagé même si le helper retourne encore un succès. Comptes premier/deuxième de zéro à trois, cinq frames below/start/inside/end/above, états normal/égaux/goal incorrect, deux offsets de changement. Les 48 différences sont toutes sensibles au reset; elles ne représentent pas 48 défauts indépendants. Ordre de sélection et bornes inclusives vérifiés. Item complet et tables animation/change/range complets inchangés sauf les deux champs attendus de l’item; invariance des trois pointeurs globaux. Tests publics volontairement RED sur la production actuelle, pas xfail ni attendu du défaut.

## Attribution et limites
Le PASS privé RE804 reste preuve cible distincte; le contrat public utilise exclusivement données synthétiques et logique indépendante. Aucun raw cible publié. i386 C++11 O0, pas LP64/NDEBUG. Prérequis publics installés : multilib C++, SDL2/GLEW, ASan/UBSan; absence explicite des prérequis peut produire SKIP, erreur build actual-TU jamais masquée. ASan sans leaks, UBSan fail-fast et stderr contrôlé; pas sûreté globale. Nombre de changements fixé à trois, domaine non universel; pas trace exhaustive des stores. Ni activation AnimateItem, commandes, gravité, fullbuild, registration naturelle, runtime ni gameplay : pas de GREEN global.

## Préservation et handoff
Sources production inchangées. RE801/802/803/804 et leurs métadonnées historiques inchangées; dashboard append RE805 seulement, exclusion explicitement nommée dans la garde historique RE803 et nouvelle garde exact-byte du dashboard antérieur. Suppressions BLOCKED001/002 et report-tech non suivi intacts. Aucun stage/commit/push. Métadonnées sûres : `docs/reverse/generated/re805-public-getchange-contract.json`. Test public : `tests/reverse/test_re805_getchange.py`; fixture : `tests/reverse/fixtures/re805/getchange.cpp`. Prochaine action : revue exacte indépendante du manifeste privé puis décision parent; pas patch production par cette story.

## Calendrier
Arrêt exploration impératif 02:50 Paris le 3 octobre 2026; revue parent avant 02:56, owner avant 02:57, aucune extension implicite au-delà de 03:00.
