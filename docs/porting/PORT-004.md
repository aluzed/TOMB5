## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Menu pause réordonné : Resume, Game Settings, Quit (Game Settings au-dessus de Quit). Le dispatch existant est conservé (case 2 = Quit, case 3 = Settings) par échange explicite 2↔3 après Requester. Vérifié au clavier : Game Settings ouvre bien SFX/Music/Configure Controls/Screen Adjust/Automatic Targeting ; Quit ouvre la confirmation « Are you sure you want to quit ? ». Preuves pause-order-kbd-20261029/ et pause-quit-20261029/. Build-pause SHA256 870166e1030a5399d88271eec135e66e59bbedff03ad485ca9f1827acaba1ae8; tests/porting+emulator 4174 PASS. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004, PORT-008 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Défaut reproductible lié aux stubs : sortir les armes (Y manette) rend la vue 3D entièrement noire, HUD visible ; rengainer (Y) restaure la scène. Cause : CombatCamera (GAME/CAMERA.C:1638) a son corps sous #if 0 || PC_VERSION et tombe sur UNIMPLEMENTED. NTSC : moyennes 0,1018 → 0 → 0,1025, 63 appels CombatCamera. Preuve build/porting/vpad-draw-20261029/. Le combat aux armes est inutilisable, en plus des pickups/interactions déjà bloqués. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Hotplug manette validé en synthétique : contrôleur Xbox 360 virtuel créé après le lancement du jeu, détecté via SDL_CONTROLLERDEVICEADDED ([INPUT] Gamepad 0: X360 Controller), puis A déclenche New Game (cutseq name: 1, 1610 occurrences) et la scène de Rome s'affiche. Preuve build/porting/vpad-hotplug-20261029/. Matériel physique toujours non testé, hot reload du keymap non validé. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-29

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-29T12:00:00+01:00. Linux32 provisoire.

Manette validée en synthétique : contrôleur Xbox 360 virtuel créé via /dev/uinput, détecté par SDL (GUID 030081b85e0400008e02000014010000, nom X360 Controller). Le bouton A déclenche New Game (cutseq name: 1) et le stick gauche déplace Lara vers l'arche ; captures 01-after-a.png / 02-after-forward.png. Preuve build/porting/vpad-20261029/. Ce n'est pas une manette physique : hotplug et matériel réel non testés. Build-cm SHA256 da21fdc774bb70ea0df85c257752b51f8f72b02136f182b30eb980120305588b. Aucun Done.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-10-28

PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-10-28T15:00:00+01:00. Linux32 provisoire.

Keymap clavier/manette livré (INPUT.CFG, double bind, éditeur F1, 17 tests, 496 PASS) et build-j vérifié. PORT-004 : HUD debug Camera X/Y/Z retiré ; LookCamera remplacé par une implémentation de port fonctionnelle (joint de tête, angles tête/torse, rig de poursuite, retour au suivi) ; réinitialisation du clavier sur perte de focus ; déconnexion manette traitée par instance SDL. Parcours réel sur build-l (SHA256 3b6863…4747) : avance/relâchement, rotations, saut, action, regard gauche/droite avec retour, pause/Resume, scène stable sans entrée, fermeture normale exit 0 ; 15 captures inspectées. Aucun contrôleur physique, pas d'équivalence cible de LookCamera, caméra combat et collisions étendues non validées. Preuves privées : build/porting/port004-final-l-20261028.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-20

PORT-004, PORT-005 — **In progress**. Autorisation bornée jusqu’au 2026-09-20T12:00:00+02:00. Linux32 provisoire.

Deux corrections intégrées : restauration complète R22 (RED66/84 puis84PASS) et mgLOS, deux omissions géométriques (RED28/111 puis111PASS, backend PSX_VERSION && PSXPC_TEST i386). Suite publique après source :446 passed. Build GLEW+jeu neuf ; un parcours réel avec 13 captures inspectées, scène/déplacement/pause/retour titre et exits application/GDB0. LookCamera reste stub en production, regard noir persistant. Reconstruction privée non intégrée : corps avec vrais joint/vue/collision/LOS,79/79 accords fonctionnels mais12/79 écarts GTE bruts conservés ; géométrie/RNG doublés, matrices synthétiques, niveaux11/12 exclus. Module11/12 attribué et239cas privés, ABI moteur à fermer. Aucun Done ni preuve campagne. Prochaine preuve : frontière GTE et module natif avant intégration caméra. Détails : docs/porting/camera-foundations.md ; preuves build/reverse/autonomy-20260920-1200/.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

## Progression vérifiée du 2026-09-19

PORT-003, PORT-004 — **In progress**. Autorisation bornée jusqu’au 2026-09-19T10:00:00+02:00. Linux32 provisoire.

Nouveau parcours natif complet avec 13 captures inspectées, retour titre et exits application/GDB 0. Préconditions LookCamera et matrices du joint observées sans injection ; vue noire du regard persistante. Trois exports Ghidra authentifiés (13 fonctions), 384 cas de préfixes cible avec RAM construite, arrêts avant transfert COP2 ou première arithmétique GTE ; rejeu parent identique. Aucun calcul GTE complet ni équivalence actual-TU démontré ; aucun nouveau patch jeu ni rebuild. Candidat de restauration de matrice identifié statiquement, correction bloquée avant RED réel. Aucun Done. Preuves privées : build/reverse/autonomy-20260919-1000/unit03-look-0923/. Détails : docs/porting/runtime-look.md.

Détails : [scène et parcours runtime](runtime-level.md).

Aucun Done attribué. Les blocs suivants sont historiques ; leurs tests documentaires ne constituent pas une validation du jeu.

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
