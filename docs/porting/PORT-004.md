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
