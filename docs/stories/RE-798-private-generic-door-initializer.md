# RE-798 — Initialiseur générique : prototype privé vérifié, activation bloquée

## Résultat concret
Prototype privé de la TU complète DOOR.C lié aux vraies GETSTUFF.C, COLLIDE_S.C et MALLOC.C : GetDoor, ItemNewRoom, game_malloc et ShutThatDoor réels, liaison normale sans suppression de symboles non résolus. **32/32 GREEN normal et 32/32 ASan+UBSan**, sans diagnostic runtime ; 32 appels cible authentifiés complets fraîchement rejoués. Quatre orientations et trois dimensions binaires flip/navbox/portail ; buffers complets sélectionnés comparés, pas RAM entière. Aucune nouvelle exécution du jeu.

Le premier RED était un échec de link pour initialiseur absent, pas un RED comportemental d'un corps existant. Après ajout privé, un RED comportemental réel de **16/32 cas portail** a révélé des labels ABI incorrects dans le handoff RE796 : champs **InDrawRoom** et **draw_room**, non flags/flag3. Correction du prototype après ce RED, sans modifier l'oracle. Revue indépendante : probe compilé sur headers réels, reconstruction des buffers, rejouage normal/sanitizers et mutations sensibles. Les preuves brutes et le delta restent en build ignoré.

Allocation cible 92 bytes conservée explicitement malgré structure native 82 ; projection et rebasing des pointeurs atteints, pas conversion générale de layout. GetDoor normalisé dans le domaine sentinel/room testé seulement. Non-head et mises à jour différées de listes, coordonnées/origines élargies, destinations indépendantes de flip, allocation failure et branches spécialisées manquent.

## Tracker
- [x] Fixtures avant prototype, RED de link puis RED comportemental discriminant conservés.
- [x] Vraies TUs et helpers liés, cible 32/32 et source privée 32/32 dans les deux modes.
- [x] Correction des labels ABI attribuée ; revue indépendante bornée PASS persistée.
- [ ] Domaine générique élargi et ordered events natifs complets.
- [ ] OpenThatDoor, DoorControl, ProcessClosedDoors et branches spécialisées vérifiés.
- [ ] Initialiseur intégré et gameplay naturel : **ObjectObjects non activé**.

## Preuves et reprise
Verdict privé `build/reverse/autonomy-20261002/re798-initializer-review/verdict.json`, SHA256 `eebc7730a0c0f3bb04716c50ed6e172a661f7876c7a35a5d9e2668ec0da0744d`. Source production livrée au début de cette unité : `87f46475`, DOOR.C SHA256 `4fd35a2eb49a68ae7c79c7cd6e27955d3e065d1850c1216276c400086fd8c055`, inchangée pendant le prototype. Ce digest est historique, pas un verrou sur les futures évolutions du fichier.

RE-799 : preuve bornée de l'ouverture et fermeture des dépendances, puis élargissement du domaine de l'initialiseur avant toute activation. Une tentative de délégation OpenThatDoor a été refusée par le fournisseur avant réalisation ; aucun résultat pour ce helper n'est revendiqué. L'autorisation deadline existante reste valable jusqu'au 2 octobre 23h, sans GO intermédiaire ; checkpoint n'est pas travail continu garanti. **pas de GREEN global**, ni fullbuild, preuve hardware ou activation production de l'initialiseur.
