# PORT-001 — Build Linux32 reproductible

[Tracker](README.md) · [Tableau HTML](index.html#PORT-001)

Status: Todo

Priorité : P0

Motif : Prêt à planifier ; aucune implémentation autorisée par ce lot.

Dépendances : Aucune

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Pouvoir construire et lancer la même application depuis un environnement documenté, sans dépendre du répertoire privé d’un précédent essai.

## Faits existants — base eac6d930

RE-772 rapporte un build ELF32 réussi avec GLEW privé ; le build ELF64 a crashé dans LoadLevel. Linux.cmake recherche SDL2/OpenGL/GLEW mais ne fixe pas à lui seul l’ABI 32-bit.

## Portée

Toolchain, options effectives, dépendances i386, chemins de données fournis légalement, lancement et fermeture.

## Exclusions

Reconstruction menu, correctifs gameplay, port natif64 et redistribution des données exclus.

## Tâches — implémentation non commencée

- [ ] Documenter une recette neuve avec versions et architecture de chaque dépendance ; adapter seulement après autorisation d’implémentation.
- [ ] Reproduire dans un nouveau build tree et archiver flags, ELF, résolution des bibliothèques et hash avant lancement.
- [ ] Documenter le placement des données utilisateur et tester absence de données avec diagnostic exploitable.

## Critères d’acceptation futurs

- [ ] Deux builds neufs à partir du même commit aboutissent sans dépendance cachée à runtime-1058 ; identité bit-à-bit du binaire non exigée.
- [ ] Le binaire est ELF32, ses bibliothèques sont compatibles, le splash est capturé depuis ce binaire et une fermeture normale est observée.
- [ ] Une dépendance ou donnée absente produit une erreur attribuable et une procédure de résolution.

## Validation et capture attendues

Logs configure/build/ldd et application distincts, capture privée avec hash du binaire ; recette rejouée indépendamment. Un timeout ne remplace pas une fermeture normale.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Disponibilité des dépendances sur une autre machine, variantes de données et nécessité d’un conteneur à décider.

## Estimation indicative

1–3 jours-personne pour industrialiser la recette existante ; hors résolution de défauts runtime nouveaux. Confiance : Medium. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `docs/stories/RE-772-build-runtime-observable.md:15` — Build32 et limites.
- `SPEC_PSXPC_N/PLATFORM/Linux.cmake:3` — Dépendances Linux.
- `SPEC_PSXPC_N/CMakeLists.txt:11` — Options indépendantes du build type.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
