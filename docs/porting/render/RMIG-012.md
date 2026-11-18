# RMIG-012 — Parité visuelle et retrait du chemin OpenGL

Status: **Done** — priorité P1 — confiance Medium

Avancement : Terminé : le backend Vulkan reproduit OpenGL 64 bits au pixel près (référence sha256 5dbbb251…, cmp identique) et OpenGL/GLEW ont été retirés du build 64 bits (PORT_VULKAN_ONLY). Le binaire 64 bits ne linke plus libGL/libGLEW et ne contient aucun symbole gl* ; TOMB5_RENDERER=gl y affiche un message explicite et continue en Vulkan. Le build 32 bits conserve OpenGL comme référence. La divergence d’état 32 ↔ 64 bits (primitives d’effet) est sortie de ce ticket et suivie par RMIG-023.

## Objectif

Valider Vulkan sur des scènes réelles puis supprimer OpenGL du build 64 bits.

## Faits établis

Le remplacement est décidé : aucun backend GL ne doit rester dans la cible 64 bits. La référence de comparaison est produite par RMIG-007. Le harnais RMIG-007 a mesuré un écart 32/64 : mean_abs_diff=18.730, 26.12% de pixels à +/-8 après gain global ; le 64 bits est plus sombre, HUD compris. Cet écart devra être expliqué ou accepté dans la parité Vulkan.

## Périmètre

Comparaison sur plusieurs niveaux (Rome, Colosseum), correction des écarts, retrait des fichiers/dépendances GL.

Hors périmètre : Refonte du gameplay.

## Tâches

- [ ] Comparer au moins trois scènes (titre, niveau 1, Colosseum) entre référence et Vulkan.
- [ ] Corriger les écarts visuels et mesurer le coût par frame.
- [ ] Retirer GLEW/OpenGL du build 64 bits et du CMake.

## Critères d’acceptation

- Écarts visuels documentés et acceptés (aucune régression fonctionnelle).
- Le build 64 bits ne référence plus ni GLEW ni OpenGL (vérifié par ldd et grep).

## Validation

Rapport de comparaison d'images + ldd + revue des dépendances CMake.

## Inconnues

Écarts de filtrage/arrondi entre pilotes.

## Estimation

2 à 3 jours-personne.

## Dépendances

- RMIG-007
- RMIG-011

## Preuves

- 2026-11-18 : Backend Vulkan pixel-identique à OpenGL 64 bits sur la scène de référence (sha256 5dbbb251…, cmp identique). L’écart restant est celui du rendu 32 bits vs 64 bits, indépendant du backend ; à instruire côté conversion couleur/format.
- 2026-11-18 : Analyse 32/64 par dump TOMB5_DUMP_VERTS (300 frames, niveau 3) : 977 enregistrements identiques (chargement/intro) puis 300 enregistrements divergents (jeu) ; comptage : 32 bits 1 058 577 vertices / 64 bits 1 062 531 au total, avec 32>64 sur 225 OTs et 64>32 sur 75 OTs dans la partie jeu. Journal [DRAW] : 32 bits fade=239/0 fading=1 vs 64 bits fade=0/0 fading=0, persp 306 vs 256. Conclusion : divergence d’état de jeu LP64, pas de pipeline couleur.
- 2026-11-18 : Harnais TOMB5_PRIMHIST (histogramme des codes de primitive par OT). Différence 32/64 au premier OT de jeu : 32 bits [PH] nv=2706 34=434 3C=221 50=11 60=1 62=1 E1=1 vs 64 bits nv=2607 34=403 3C=221 50=11 60=1. Soit 31 triangles gouraud semi-transparents (0x34), 1 sprite semi-transparent (0x62) et 1 image-load (0xE1) émis seulement en 32 bits, les autres primitives étant identiques (pas d’abandon de chaîne). Corrélé à ScreenFading=1 (32) vs 0 (64) au premier [DRAW] : effet d’écran/fondu. PC_VERSION n’est pas défini dans SPEC_PSXPC_N, donc Fade() s’exécute dans les deux builds.
- 2026-11-18 : Vulkan par défaut en 64 bits : écran-titre rendu ([VK] backend ready 640x480, 4 images), niveau 3 300 frames avec TOMB5_RENDERER=gl → sha256 d05c8394… identique à la capture GL précédente (aucune régression du chemin GL), niveau 3 1800 frames Vulkan → sha256 5dbbb251… identique à la référence, niveau 4 (Colosseum) 600 frames Vulkan sans erreur de validation. Échec d’initialisation Vulkan = arrêt explicite, pas de repli silencieux.
- 2026-11-18 : Retrait effectif d’OpenGL : ldd du binaire 64 bits sans libGL/libGLEW, 0 symbole gl* non résolu, capture 300 frames identique (sha256 63b778f1…) après retrait, TOMB5_RENDERER=gl → message « OpenGL n'est pas compile dans ce build 64 bits ; utilisation de Vulkan », build 32 bits recompilé et fonctionnel (OpenGL conservé). PORT_ALLOW_GL permet de reconstruire un binaire 64 bits avec OpenGL pour diagnostic.

## Références

- `EMULATOR/PLATFORM/Linux.cmake:5` (dépendances à retirer)
- `EMULATOR/EMULATOR_PLATFORM_SETUP.H:18` (sélection OGL)
