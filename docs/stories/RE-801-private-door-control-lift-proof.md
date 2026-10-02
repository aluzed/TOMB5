# RE-801 — Preuve privée exécutée de la branche lift DoorControl

## Résultat et périmètre
**Preuve privée seulement, aucune intégration source** : branche lift `trigger_flags==1`, gate PSX_VERSION/PSXPC_TEST/i386. DoorControl reste un **stub** en production; ProcessClosedDoors non implémenté, registration inactive, aucun runtime/full-game-link/gameplay : **pas de GREEN global**. OpenThatDoor et ShutThatDoor intégrés RE-800/797 restent des helpers bornés, pas une fermeture de la chaîne door. Initializer RE-798 toujours privé/non intégré.

## Preuve nouvelle réellement exécutée
16 séquences corrélées de six appels CPU/RAM préservés, soit 96 appels; 8342 visites authentifiées par rejeu. Le premier reviewer a exécuté deux rejeux cible frais (initial et audit réparé), ainsi que native normal/strict ASan+UBSan. Baseline actual-TU compilée : RED comportemental 96/96 échecs dans chaque mode, dont 80 input_failures et 16 event_failures. Candidat privé : 96/96 GREEN par mode, sans doubles comportementaux cible/native. OpenThatDoor, ShutThatDoor, GetBoundsAccurate et GetFrames_CL sont les vrais services; observation wrappers, renommage de définitions de symboles et forward declarations seulement lors de compilation TU instrumentée.

12 appels bounds, six interpolés, quatre open, quatre shut, huit clamps, 56 événements. Premier ledger copies défectueux (références de liste mutable ensuite vidée); rejeu indépendant réparé et audit de huit entrées copies. 11 mutants **expected-output** rejetés : dix régions et un événement, aucun mutant du code. Ces états sont corrélés, pas un produit cartésien complet.

Projection native 2293 octets de régions sélectionnées, layouts target/native 92/82 octets avec relocation et projection packed explicites. La cible assert l'égalité RAM finale sauf stack; les full RAM dumps ne sont pas archivés. Pas de couverture exhaustive des écritures transitoires. Préconditions : buffers valides et disjoints, animation et timers bornés. Ordre mesh différent équivalent seulement sans alias; overflow, pointers invalides, grands/négatifs timers, autres animations, autres callers et branches non-lift restent hors preuve. ASan/UBSan strict avec leak checking désactivé; pas preuve de production-link, matériel ni gameplay.

## Attribution et erreurs conservées
Le worker producteur a atteint son timeout après les artifacts privés : résultat de délégation échoué distinct des fichiers existants. Les compilations initiales échouées ne sont pas le RED comportemental obtenu après retry. Premier oracle copies et première compilation ABI échoués puis réparés, sans effacement des logs. Premier reviewer arrêté par **provider** avant verdict : ses tests réussis ne valaient pas approbation.

Une revue indépendante **archivale** finale a ensuite émis un verdict PASS limité à la preuve privée, sans nouvelle compilation ni exécution cible/native; 1708 hashes d'artifacts vérifiés, aucun blocage logique/sécurité dans ce périmètre. Ses erreurs checker et retries sont conservés. Le tool a atteint un timeout **après** création du verdict : artifact présent et hash vérifié, pas succès inventé du worker. Cette publication n'est pas elle-même approuvée par ce verdict technique.

## Empreintes sûres
- Candidat privé : `d98fe4690e47a82fbfa6fe09f5e01f6b33b99f86ba365e29da8080272a8e65d7`.
- Verdict archivage : `2a77bd27399493cfd29bddaeeb738bd834611fd227a39f9aaf68e06353e23803`.
- Baseline production : `a538fca3ca3bd0426570d60b7a1c8b3a44d4d96c66b59990a04e716ef4e295ff`.
- Métadonnées : `docs/reverse/generated/re801-private-door-control.json`.
Comptes, hashes et noms symboliques uniquement : aucun asset, adresse brute, coordonnée, opcode, dump, harness privé ou code propriétaire publié.

## Critères de reprise — RE-802
Une **nouvelle** branche générique non-lift predicate/state : authentifier dépendances réelles et transitions sur objet valide; test actual-TU RED comportemental avant candidat privé, comparaison état/trace, GREEN borné et revue indépendante. Ne pas répéter anciennes matrices helpers; chemin spécial timer distinct. Dépendance manquante = blocker précis, jamais retour simulé pour revendiquer équivalence. RE-802 planifiée/non prouvée; pas GO supplémentaire ni registration.

Autorisation parent renouvelée jusqu'à 03:00; recherche 02:20, revue 02:40, owner 02:50. Ces bornes ne constituent pas une nouvelle autorisation d'intégration ou runtime. Histoires/métadonnées précédentes gelées; dashboard append-only et BLOCKED-004 courant mis à jour. BLOCKED-001/002 supprimés ne sont pas restaurés; aucun stage/commit.

## Tracker
- [x] Nouvelle branche lift cible exécutée et CPU/RAM conservés.
- [x] Baseline comportementale RED et candidat privé GREEN, normal/strict ASan+UBSan.
- [x] Attribution fraîche séparée de la revue finale archivale et des erreurs worker/provider.
- [x] Limites, hashes et checkpoint public sûrs; production inchangée.
- [ ] RE-802 non-lift predicate/state à prouver séparément.
- [ ] Intégration DoorControl, ProcessClosedDoors et initializer élargi.
- [ ] Registration cohérente, callback naturel, fullbuild et gameplay.
