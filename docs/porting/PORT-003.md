## Progression vérifiée du 2026-09-19

PORT-003, PORT-004, PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Trois parcours neufs : saut/réception et première transition room 0 → room 2 observés par entrées réelles. Défaut regard reproduit ; réarmement lara.look manquant attribué par Ghidra et corrigé sous PSX_VERSION && PSXPC_TEST (validation i386). RED réel 60 failed / 56 passed, GREEN 116 passed sur TU intégral avec services doublés explicitement ; 251 tests publics PASS. GLEW et jeu reconstruits dans un dossier neuf ; parcours après patch : tête contrôlée sans rotation du corps, mais vue noire du regard toujours présente (LookCamera stub). Relâchement, pause, retour titre et exits applicatifs/GDB 0 pour les trois runs ; 15/13/13 captures inspectées. Aucun Done ; recette complète commandes/caméra/collisions, interactions, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit02-controls-0824/. Détails complémentaires : docs/porting/runtime-controls.md.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-002, PORT-003 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Lancement frais : New Game termine LoadLevel vers 71 s, scène avec Lara et locomotion minimale vérifiées par entrées réelles et captures inspectées ; pause, Quit/Yes, retour titre puis fermeture normale (application et GDB exit 0). Aucun patch loader : observation précédente trop courte. Sept tests des archives du 18 septembre réussis, sans nouveaux runtimes pour ces archives. Source jeu inchangée depuis 73faba47 ; binaire existant authentifié, pas de rebuild dans cette unité. PORT-001 reste en cours, PORT-004 et suivants bloqués pour recette intégrée ; campagne, collisions étendues, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit01-0757/.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

# PORT-003 — Nouvelle partie et première scène jouable

[Tracker](README.md) · [Tableau HTML](index.html#PORT-003)

Status: Blocked

Priorité : P0

Motif : Recette intégrée bloquée tant que PORT-002 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-002

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Démarrer une nouvelle partie depuis le menu et voir Lara dans le premier niveau des données de référence.

## Faits existants — base eac6d930

S_LoadLevelFile appelle le chargement du niveau ; LoadLevel reconstruit les rooms ; DoLevel relie chargement, caméra, contrôle et dessin. Ces sources présentes ne prouvent pas un niveau jouable. RE-772 n’a pas validé cette transition.

## Portée

Premier niveau des données choisies (Rome attendu, à confirmer par le gameflow), chargement complet et boucle graphique active.

## Exclusions

Campagne entière, fidélité de chaque effet et parcours complet exclus ; pas de succès fondé sur un loader isolé.

## Tâches — implémentation non commencée

- [ ] Fixer jeu de données légal, niveau attendu et recette menu vers nouvelle partie.
- [ ] Identifier le premier obstacle intégré et ses dépendances réelles sans neutraliser silencieusement les services.
- [ ] Corriger seulement après preuve/recette sensible, puis répéter depuis un processus neuf.

## Critères d’acceptation futurs

- [ ] Depuis Nouvelle partie, Lara et une géométrie de niveau identifiable sont visibles sans appel direct de test au loader.
- [ ] Animation et caméra évoluent pendant au moins 60 secondes ; les journaux distinguent crash, timeout et fermeture demandée.
- [ ] Trois relancements reproduisent la même arrivée, avec identité du niveau et configuration archivées.

## Validation et capture attendues

Capture privée de la transition et de la scène, trace de chargement, hash binaire ; absence de crash sur cette fenêtre seulement.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Identité effective du premier niveau, intégrité des données, overlays, animations, dépendances rendu/audio encore à vérifier en intégration.

## Estimation indicative

5–15 jours-personne exploratoires ; aucune garantie tant que PORT-002 n’est pas franchi. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `SPEC_PSXPC_N/ROOMLOAD.C:62` — S_LoadLevelFile.
- `GAME/SETUP.C:1208` — LoadLevel.
- `GAME/GAMEFLOW.C:1209` — DoLevel.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
