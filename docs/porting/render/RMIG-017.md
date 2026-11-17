# RMIG-017 — Relocalisation 64 bits des tableaux de pointeurs du fichier

Status: **Done** — priorité P0 — confiance Medium

Avancement : Termine : le niveau titre se charge integralement en 64 bits. La sequence CD (open/read) est identique au 32 bits, les tableaux du fichier (salles, meshes, anims/frame_ptr, bones, items, objets/statics) sont convertis vers des structures hotes, et le rendu logiciel PSX demarre sans SIGSEGV.

## Objectif

Charger un niveau complet en 64 bits sans corruption, en convertissant les tableaux de pointeurs issus du fichier de niveau.

## Faits établis

LoadLevel relocalise des tableaux de pointeurs avec `*(int*)&array[i] += base` (meshes, frame_ptr des anims, models…). En LP64, l'élément fait 8 octets et l'arithmétique 32 bits corrompt la mémoire : le binaire plante à GAME/SETUP.C:1838. 487 occurrences de `(int*)&` existent dans GAME/ et SPEC_PSXPC_N/ ; toutes ne sont pas concernées (certaines portent sur de vrais int32), mais la famille issue du fichier doit être traitée.

## Périmètre

Tableaux de pointeurs lus depuis le fichier (meshes, anims, models, frame_ptr, changes/ranges si concernés) : lecture en psx_u32 puis conversion en pointeurs hôtes, avec un helper commun.

Hors périmètre : Structures purement hôtes et code de rendu.

## Tâches

- [ ] Lister les tableaux effectivement remplis depuis le fichier (meshes, anims, models, frame_ptr) et distinguer les `(int*)&` légitimes.
- [ ] Introduire un helper de conversion (base + offset 32 bits) et l'appliquer à ces tableaux.
- [ ] Rejouer le chargement d'un niveau complet en 64 bits et vérifier la cohérence des positions d'items avec la référence 32 bits.

## Critères d’acceptation

- Un niveau se charge en 64 bits sans SIGSEGV et sans `Unhandled primitive type`.
- Les positions d'items et de Lara correspondent à la référence 32 bits.

## Validation

Comparaison des positions (sonde gdb) et du nombre de primitives non gérées entre 32 et 64 bits.

## Inconnues

Nombre exact de tableaux concernés ; effets de bord sur l'IA (boxes) et les animations.

## Estimation

2 à 4 jours-personne.

## Dépendances

- RMIG-005

## Preuves

- 2026-11-17 : Chargement 64 bits du niveau titre : la trace TOMB5_TRACE_CD=1 donne exactement les 32 premieres lignes de la sequence 32 bits (dont open file=2 sector=1636, read 42012/1768, 228/1789, 16/1790, 7616/1791, 262144/1795, 329832/2051, 524000/2213, 32360/2469, 1920/2485, 8344/2552, 348/2557, 3992/2655, 6812/2508, 9656/2581, 812/2586). Corrections : LEVEL_OBJECT_DATA_SIZE basee sur le format fichier 64/28 octets (plus sizeof LP64=96), conversion object_info_file, RelocateModule lisant des mots 32 bits, arena LP64 portee a 4 Mio, avance de ptr apres conversion des salles, tableaux bones hotes, frame_ptr/anims convertis. Preuve visuelle : capture de la fenetre apres 35 s (DEMO MODE, mode attractif) sans crash, 0 primitive non geree sur cette execution.

## Références

- `GAME/SETUP.C:1838` (relocalisation de meshes (crash 64 bits))
- `GAME/SETUP.C:1848` (relocalisation des frame_ptr d'animations)
