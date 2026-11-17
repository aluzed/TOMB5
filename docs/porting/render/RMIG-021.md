# RMIG-021 — Campagne 64 bits : parcours du Colosseum

Status: **In progress** — priorité P1 — confiance Medium

Avancement : Niveau 3 charge et jouable en 64 bits ; outil TOMB5_START_POS=x,y,z,room,rot ajoute pour reprendre a la corniche (room 12). Le parcours complet reste a derouler ; le rendu de sable deforme est present aussi en 32 bits (pas une regression 64 bits).

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

## Références

- `docs/porting/colosseum-walkthrough.md:7` (parcours salle par salle)
- `SPEC_PSXPC_N/DRAWOBJ.C:680` (SubDiv/div tables)
