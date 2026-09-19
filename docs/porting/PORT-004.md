## Progression vérifiée du 2026-09-19

PORT-003, PORT-004, PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Trois parcours neufs : saut/réception et première transition room 0 → room 2 observés par entrées réelles. Défaut regard reproduit ; réarmement lara.look manquant attribué par Ghidra et corrigé sous PSX_VERSION && PSXPC_TEST (validation i386). RED réel 60 failed / 56 passed, GREEN 116 passed sur TU intégral avec services doublés explicitement ; 251 tests publics PASS. GLEW et jeu reconstruits dans un dossier neuf ; parcours après patch : tête contrôlée sans rotation du corps, mais vue noire du regard toujours présente (LookCamera stub). Relâchement, pause, retour titre et exits applicatifs/GDB 0 pour les trois runs ; 15/13/13 captures inspectées. Aucun Done ; recette complète commandes/caméra/collisions, interactions, sauvegarde et audio non validés. Preuves privées : build/reverse/autonomy-20260919-1000/unit02-controls-0824/. Détails complémentaires : docs/porting/runtime-controls.md.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

# PORT-004 — Commandes et caméra de base utilisables

[Tracker](README.md) · [Tableau HTML](index.html#PORT-004)

Status: Blocked

Priorité : P0

Motif : Recette intégrée bloquée tant que PORT-003 ne sont pas validés ; rédaction terminée, travail non commencé.

Dépendances : PORT-003

Cadrage proposé : Linux 32-bit / PSXPC_N en premier : proposition de cadrage, PAS décision utilisateur définitivement validée.

## Objectif utilisateur

Contrôler Lara et garder une vue exploitable avec un clavier de référence, puis une manette choisie.

## Faits existants — base eac6d930

UpdateKeyboardInput et S_UpdateInput existent. LookCamera est un stub dans GAME/CAMERA.C ; cela ne prouve pas la cause du splash. Le suivi caméra est distinct de la solidité complète des collisions.

## Portée

Marche/course, rotation, saut, action, regard, pause et relâchement ; scène ouverte comme recette indépendante de PORT-005.

## Exclusions

Toutes manettes, remapping complet/accessibilité et caméra combat avancée exclus ; obstacles/salles traités dans PORT-005.

## Tâches — implémentation non commencée

- [ ] Définir une table de commandes visible et une recette en scène ouverte.
- [ ] Caractériser touches maintenues/edges, focus et déconnexion ; attribuer les fonctions manquantes requises.
- [ ] Compléter le regard/suivi nécessaire et ajouter des contrôles absence d’entrée/relâchement.

## Critères d’acceptation futurs

- [ ] Chaque commande listée produit une réponse identifiable ; relâchement et perte de focus ne laissent pas une action bloquée.
- [ ] Pause arrête la simulation et reprise la réactive sans perdre le contrôle.
- [ ] Regard puis retour au suivi gardent Lara visible en scène ouverte ; une déconnexion/reconnexion est récupérable.

## Validation et capture attendues

Séquence privée d’entrées/captures en jeu, mesures position/caméra symboliques et témoins sans entrée ; recette obstacles additionnelle dans PORT-005.

Captures, assets, exécutables et données restent dans des dossiers ignorés ; seuls scripts, tests et métadonnées sûrs seront versionnables.

## Inconnues

Combinaison des branches d’entrée, disponibilité physique d’une manette et contrat du regard à confirmer.

## Estimation indicative

5–15 jours-personne pour le socle ; périphériques supplémentaires non compris. Confiance : Low. Jugement de planification, pas une mesure ; à réviser après les dépendances, non une promesse de délai.

## Références consultables

- `EMULATOR/LIBPAD.C:240` — UpdateKeyboardInput.
- `SPEC_PSXPC_N/PSXINPUT.C:91` — S_UpdateInput.
- `GAME/CAMERA.C:1596` — LookCamera.

## Progression séparée

- [x] Ticket rédigé.
- [ ] Travail fonctionnel autorisé et démarré.
- [ ] Recette observable validée ; revue avant passage à Done.
