# RE-799 — OpenThatDoor : preuve corrective privée, intégration non acceptée

## Résultat concret
Candidat privé de la **TU complète DOOR.C** avec vrais headers i386 : baseline stub **2944 échecs / 3328** (build0/run1), puis **3328/3328 normal et 3328/3328 ASan+UBSan** (build0/run0), aucun diagnostic runtime en modes fail-fast. Rejeu cible authentifié complet : **3328 appels**, vraie routine de copie exécutée sans retour simulé ; 401792 visites de hooks, pas instructions retirées, et 2176 copies.

Matrice exacte : 2304 cas cartésiens floor/bloc/overlap/mesh/directions/LiftDoor, plus 1024 sweeps indépendants couvrant les 256 valeurs de chacun des quatre champs direction. Revue indépendante : buffers initiaux et attendus reconstruits, ABI vérifié par probe compilé sur vrais headers, cible fraîche reproduite, native fraîche RED/GREEN/sanitizer. Cinq mutations de résultats attendus rejetées : contrôles de sensibilité du harness, **pas mutants du code**.

Le candidat restaure le floor sauvegardé, distingue le gate LiftDoor du reset des cinq LOT et choisit un seul axe/sign de mesh. **Source production inchangée**, ObjectObjects non activé ; l'acceptation porte sur le privé seulement. Pas de runtime du jeu ni fullbuild, pas de GREEN global.

## Limites et incidents conservés
Domaine buffers disjoints, floor valide ou null, blocs valides sélectionnés ou sentinel, cinq creatures, troisième pointeur mesh obligatoire lorsque le premier est actif. Deux pointeurs optionnels et trois shorts accessibles ; LiftDoor seulement absent/présent. Le target écrit mesh dans l'ordre 1,3,2,4, le candidat 1,2,3,4 : égalité finale uniquement sans alias. Copie native memcpy également limitée aux régions disjointes. Tous les appels utilisent le premier sous-record de door ; les autres callsites ne sont pas prouvés.

Projection door cible92/native82 et rebasing des pointeurs ; comparaison des régions complètes sélectionnées, pas RAM entière/stack/registers/write-set exhaustif. GP synthétique et offset de globale, extraction/relocation héritées ; pas startup ou preuve matérielle. L'échec initial de link (LiftDoor redéfini dans la fixture) et celui de compilation (memcpy non déclaré) sont observables dans le transcript, mais leurs logs de build ont été remplacés par les reruns ; ne pas prétendre à des archives séparées. Ils ne sont pas le RED comportemental. Déclaration extern et include standard gated corrigés avant GREEN. Première tentative de délégation helper refusée par le fournisseur sans exécution ; parent a réalisé la preuve, seconde délégation revue terminée normalement.

## Tracker
- [x] Fixtures/oracle avant candidat et RED comportemental actual-TU discriminant.
- [x] Cible authentifiée complète et source privée normal/sanitizers GREEN bornés.
- [x] Revue indépendante persistée, limites et incidents séparés.
- [x] Dashboard et métadonnées publiques sûres, sans dump/code brut/asset.
- [ ] Régression publique actual-TU et revue d'intégration de OpenThatDoor.
- [ ] Domaines initializer élargis, DoorControl et ProcessClosedDoors.
- [ ] Registration cohérente puis callback bridge naturel et gameplay.

## Preuves / Critères de reprise
Verdict `build/reverse/autonomy-20261002/re799-review/verdict.json` : SHA256 d443ff41b4750ae7941aeae5b18114f836c3ab77c69519c88d30c59f1cd4f0b9. Candidat privé SHA256 c8334730c0a3a7f6879bd93feaafe612d663851621b225c60b4f75faa268a96a. Métadonnées `docs/reverse/generated/re799-door-open-proof.json`; aucun fichier build nécessaire aux quatre tests publics de publication.

**RE-800** : écrire une régression publique actual-TU sensible (pas simple fingerprint d'archive), tester le candidat avec le gate effectif et les préconditions documentées, obtenir une acceptation explicite d'intégration avant patch production. Puis fermeture de DoorControl/ProcessClosedDoors et domaines non-head/différés/spécialisés initializer selon BLOCKED-004 ; ne pas activer un producer incomplet. Le GREEN privé ne ferme pas ces blockers. Aucune nouvelle autorisation par ce handoff : échéance utilisateur 2 octobre 23h, travail après échéance interdit.
