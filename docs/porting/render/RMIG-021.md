# RMIG-021 — Campagne 64 bits : parcours du Colosseum

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Niveau 3 stable et salles cles rendues en 64 bits : 15 (gladiateur/cle), 90 (Roman God/arene), 102 (serrure 2/porte). Outil TOMB5_START_POS operationnel. Reste le parcours/puzzle complet et la correction du rendu deforme pre-existant.

## Objectif

Parcourir The Colosseum (niveau 3) en 64 bits et valider la stabilite/rendu des salles du parcours.

## Faits établis

TOMB5_START_LEVEL=3 charge le niveau 3 (The Colosseum, 125 salles). Le decor est rendu, Lara est visible/deplacable (pos 90642,4608,52736 room 20), le processus reste stable. Le rendu du sable est encore deforme par endroits et la camera peut regarder un mur sombre apres deplacement.

## Périmètre

SPEC_PSXPC_N/ROOMLET* / DRAW*, GAME/EFFECTS/control du niveau 3.

Hors périmètre : Vulkan, ImGui, RT.

## Tâches

- [ ] Rejouer le parcours 12 -> 26 -> 27 -> 108 -> 15 -> 18 -> 100 -> 90 -> 102 -> 110 -> 83 -> 111 -> 85 -> 70 en 64 bits.
- [ ] Corriger les derniers polygones deformes/rendu sable observes dans le Colosseum.
- [ ] Verifier les sauvegardes F5/F6 aux etapes cles du parcours.

## Critères d’acceptation

- Le parcours du Colosseum est realisable sans SIGSEGV en 64 bits.
- Les salles cles et les objets du parcours sont rendus correctement.
- Une sauvegarde en milieu de niveau est rechargee correctement.

## Validation

Execution 64 bits avec captures et journal, comparaison avec le parcours 32 bits documente.

## Inconnues

Le rendu deforme du sable peut venir de la sous-division (SubDiv/div3tab/div4tab) ou de la projection des grands polygones.

## Estimation

1 a 2 jours-personne.

## Dépendances

- RMIG-020

## Preuves

- 2026-11-17 : TOMB5_START_LEVEL=3 : [DRAW] lvl=3 nrooms=125 room=20, [LARA] pos=(90642,4608,52736) mesh_bits=FFFFFFFF, 3897 sommets, processus stable apres deplacement Up. Capture du Colosseum (arene de sable, murs) correcte mais sable partiellement deforme.
- 2026-11-18 : TOMB5_START_LEVEL=3 + TOMB5_START_POS=43364,768,52325,12,-16384 place Lara en room 12 et le gameplay repond (deplacement Up change pos/room, camera room 26). Une chute volontaire depuis la corniche declenche un GAME OVER attendu (pas un crash). Comparaison 32 bits au meme point : le sable et les grands polygones sont egalement deformes, donc ce defaut visuel est pre-existant et non specifique au 64 bits.
- 2026-11-18 : Salles validees en 64 bits via TOMB5_START_LEVEL=3 + TOMB5_START_POS : room15 (48640,1024,58880) rendue avec bannieres/colonnes ; room90 (48640,512,70144) rendue avec arene/arches/ciel, Lara visible ; room102 (49664,512,62976) rendue avec porte/serrure. Aucun SIGSEGV, processus stable. Coordonnees de room : R15 x=45056 z=53248, R90 x=46080 z=65536, R102 x=48128 z=60416 ; items : gladiateur probable obj59 room15, Roman God obj61 item79 room90 (48154,512,69120), keyhole2 obj259 room102, pickup final obj220 room70 (55808,7936,70144).
- 2026-11-18 : Tentative de reprise en room 12 (40448,1023,51712) avec TOMB5_SKIP_CUTSCENE : Lara est placee en room 12 mais est immediate repoussee en room 14 (y=6144, anim 25) par le demarrage/cinematique du niveau. Les reprises directes en rooms 15/90/102 restent valides. Le parcours depuis la corniche doit donc se faire en jeu (ou via une sauvegarde 64 bits native) ; la compatibilite des sauvegardes 32 bits reste un point ouvert.
- 2026-11-18 : Outils de debug ajoutes : TOMB5_SKIP_CUTSCENE (force GLOBAL_playing_cutseq/cutseq_num/cutseq_trig a 0) et TOMB5_START_POS_HOLD=n (force la position START_POS pendant n frames). Avec hold=600, la position room12 est maintenue mais le niveau reste en fade (ScreenFade=239, fading=1) sans progression observable : la cinematique/le start trigger garde la main. Les reprises directes en rooms 15/90/102 restent la voie valide pour tester le rendu.
- 2026-11-18 : Clignotement de Lara corrige en 64 bits. Les primitives de Lara etaient generees et parsees chaque frame (laraPrims 286..418) mais la bbox ecran alternait corps complet / sous-ensemble. La desactivation de l interpolation (TOMB5_NO_LARA_INTERP=1) stabilisait le modele. Cause : dans DEL_CalcLaraMatrices_Interpolated_ASM, l adaptation LP64 affectait s0=lara_matrices avant mTranslateXYZ_CL(s0[6..8]) (translation lue dans les rotations), et l arithmetique du squelette utilisait des index short* sur le tableau hote bones (long, 8 octets). Correction : pointeur m0 separe pour les matrices, pointeur long* b1 avec index en mots. Validation : bbox pleine chaque frame, lara_matrices stable autour de (-8,155,1295), captures stables ; build 32 bits inchange.

## Références

- `docs/porting/colosseum-walkthrough.md:7` (parcours salle par salle)
- `SPEC_PSXPC_N/DRAWOBJ.C:680` (SubDiv/div tables)
