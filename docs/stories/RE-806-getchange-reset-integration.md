# RE-806 — Intégration revue du reset minimal GetChange

Auteur : AlexP

## Tracker
- [x] Revue indépendante : integration_approved explicite, intégration parent limitée au reset du compteur de range à chaque changement correspondant.
- [x] Source exacte vérifiée sans aucune édition production par le worker publication.
- [x] Nouvelle baseline parent RED : 48 divergences sur 1440 cas par mode; candidat intégré GREEN 1440/1440 normal et strict ASan+UBSan, stderr vide.
- [x] unittest public GetChange actual-TU frais GREEN; vraies unités CONTROL_S.C et ITEMS.C, aucune entrée assets ou preuve cible privée.
- [x] Garde publication écrite FIRST puis RED observé : métadonnées, story et section absentes; nouvelle garde digest du dashboard antérieur entier.
- [x] Fullbuild CMake i386 Debug frais : configuration initiale exit 1 (GLEW), retry explicite exit 0, build exit 0; binaire ELF Intel 80386 avec debug_info.
- [x] Réparation de provenance RE804 implémentée en TDD, sans édition production et sans remplacement du hash baseline.
- [ ] Revue indépendante de la réparation : pending.
- [ ] Nouvelle revue finale indépendante de la publication, des hashes et des logs avant toute décision commit.
- [ ] AnimateItem / DoorControl : aucune activation autorisée; runtime et gameplay non effectués.

## Portée exacte et histoire
GetChange réel est défini dans SPEC_PSXPC_N/CONTROL_S.C. Seul delta déjà intégré par le parent après revue : reset local du compteur avant chaque liste de ranges du changement admissible. GAME/ITEMS.C compilé, pas appelant exercé. RE805 reste un checkpoint historique volontairement RED sur son état antérieur, non un résultat actuel; sa story et ses métadonnées ne sont pas réécrites. La publication RE806 distingue intégration revue et activation des appelants : aucune activation AnimateItem ni DoorControl, aucune registration ajoutée, aucun gameplay, pas de GREEN global.

## Domaine et sûreté
1440 cas synthétiques indépendants par mode : counts zéro à trois, trois changements, cinq frames, deux offsets et trois états. Les 48 divergences baseline identifient le même reset, pas 48 défauts indépendants. Public normal et strict ASan/UBSan i386 C++11 O0, leaks désactivés; aucun replay cible frais, aucune garantie universelle, LP64 ou optimisations alternatives non exercés. Ni assets en entrée ni raw cible dans cette publication. Aucun screenshot : aucun jeu exécuté.

## Acceptation fullbuild
La commande demandée avec Debug et flags C/C++ -m32 a réellement échoué en configuration : Could NOT find GLEW (missing: GLEW_LIBRARY). Ce premier échec reste dans le ledger et les logs, non masqué. Le cache antérieur a fourni une dépendance GLEW existante ELF i386 vérifiée, explicitement passée lors du retry sans modifier CMake ni aucune source; aucune donnée de jeu utilisée. Le retry configure exit 0, fullbuild exit 0 et cible MAIN liée à 100 %. Avertissements compilateur conservés (formats, conversions et taille de buffer notamment) : build réussi ne signifie pas dépôt sain, absence de défauts ou gameplay validé. Aucun lancement du binaire. Acceptation limitée à la compilation/link i386 Debug, indépendante du contrat synthétique; pas de GREEN global.

## Préservation et calendrier
Dashboard : section exactement nommée re806-getchange-integration et digest de tous les octets antérieurs; exclusions successeur nominatives seulement si les tests historiques échouent. BLOCKED001/002 restent supprimés et report-tech inchangé/non suivi. Aucun stage/commit/push. Parent owner 857519. Autorisation jusqu’à 12:00 Paris : recherche stop 11:25, revue 11:45, owner 11:55; budget worker maximal 550 secondes, commandes bornées extérieurement. La revue finale de publication reste à réaliser par un indépendant.

## Vérification élargie — échec historique conservé et réparation de provenance
Les premiers résultats restent historiques : 15 tests et deux sous-tests ciblés; 33 tests et deux sous-tests élargis passants, un échec RE804. FAIL original conservé : verdict.json et REPORT.md de la revue finale ne sont pas réécrits. La migration autorisée de la garde RE804 ne remplace pas son hash gelé : la source courante doit être le candidat exact approuvé, avec métadonnées RE806 integration_approved/source_integrated vraies et digest de revue d’intégration épinglé. Le retrait en mémoire de la seule ligne de reset unique, à son emplacement approuvé, doit reconstruire exactement la baseline immuable. Chaque autre hash et assertion de preuve RE804 reste inchangé; l’ancienne source identique conserve sa validité dans son contexte historique.

Tests sensibles écrits avant implémentation, RED constaté puis GREEN : ajout étranger, reset absent/déplacé/dupliqué et provenance falsifiée rejetés. Aucun snapshot complet ni preuve raw ajouté; tests portables sur les seuls octets versionnés. Résultats frais après réparation : commande élargie exacte du reviewer, 34 tests et deux sous-tests passants; extension publication RE800–RE806 avec garde provenance, 54 tests et deux sous-tests passants. unittest public normal/strict : un test, les deux modes GREEN1440, aucun skip ni exclusion supplémentaire; RE789 historique reste hors de cette suite bornée comme documenté auparavant. Les résultats frais sont consignés séparément dans le handoff de réparation, sans écraser les premiers échecs. revue réparation pending; revue publication pending. Le succès local des tests n’autorise ni acceptation globale ni commit. Les digests antérieurs complets du dashboard sont inchangés; les exclusions nominatives RE806 restent strictement bornées.
