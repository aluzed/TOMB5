# RMIG-017 — Relocalisation 64 bits des tableaux de pointeurs du fichier

Status: **In progress** — priorité P0 — confiance Medium

Avancement : En cours : conversions faites pour meshes, anims (frame_ptr) et items (144 o) ; le chargement 64 bits avance jusqu'à RelocateModule et s'y arrête car la table des modules AI est lue à zéro.

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

- 2026-11-17 : GAME/SETUP.C : structs de format fichier anim_struct_file (40 o, frame_ptr 32 bits) et item_info_file (144 o, data 32 bits, drapeaux dans un mot 32 bits) avec static_assert, conversions LP64 vers meshes (numBones*2 entrées), anims (frame_ptr = frames + offset) et items (256 entrées, drapeaux dépliés bit par bit car un bitfield n'a pas d'adresse). relocationPtr typé psx_i32* (en long*, chaque champ de la table de modules était lu sur 8 octets et donnait des tailles/offsets nuls). Builds 32 et 64 bits verts, hash 32 bits inchangé (b9d8e710…). Nouveau point d'arrêt mesuré : RelocateModule reçoit un module et une table identiques (ptr == ptr2 == 0x4019724c) parce que relocationPtr[0..4] valent tous 0 ; level->numAiModules=5 et aiModuleIndices[0]=15 sont corrects, donc c'est la lecture de la table de modules (DEL_CDFS_Read de 1920 o dans tsv_buffer[256]) qui ne remplit pas le buffer.

## Références

- `GAME/SETUP.C:1838` (relocalisation de meshes (crash 64 bits))
- `GAME/SETUP.C:1848` (relocalisation des frame_ptr d'animations)
