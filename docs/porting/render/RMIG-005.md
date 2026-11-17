# RMIG-005 — Code manipulant les champs convertis

Status: **In progress** — priorité P1 — confiance Medium

Avancement : En cours : arene sous 4 Gio (MAP_32BIT) et structure de format fichier pour les salles en place ; le chargement 64 bits atteint maintenant la relocalisation des tableaux de pointeurs et y plante, ce qui délimite le reste du travail.

## Objectif

Adapter le code qui lit/écrit les champs convertis, en particulier la relocation du niveau et la restauration de sauvegarde.

## Faits établis

LoadLevel lit les salles dans un buffer puis relocalise cinq champs par salle. Deux mécanismes supposent des adresses 32 bits : (1) le cast direct du buffer en struct room_info, corrigé par room_info_file + conversion ; (2) une famille d'instructions `*(int*)&array[i] += base` qui traite des tableaux de pointeurs comme des tableaux de int (meshes, frame_ptr des anims, models…). Mesure : 487 occurrences de `(int*)&` dans GAME/ et SPEC_PSXPC_N/. Le binaire 64 bits plante désormais dans LoadLevel à GAME/SETUP.C:1838 sur la relocalisation de `meshes`.

## Périmètre

GAME/SETUP.C (relocation), GAME/SAVEGAME.C, GAME/PORTSAVE.C, GAME/ITEMS.C et accès directs aux champs convertis.

Hors périmètre : Rendue, backend Vulkan.

## Tâches

- [ ] Introduire une arène de jeu garantie sous 4 Gio (mmap MAP_32BIT) — fait.
- [ ] Lire le format fichier des salles via une structure dédiée puis convertir vers la structure hôte — fait.
- [ ] Traiter la famille de relocalisations `*(int*)&array[i] += base` sur les tableaux de pointeurs issus du fichier (meshes, anims, models…), éventuellement en sous-ticket RMIG-017.
- [ ] Vérifier le chargement complet d'un niveau en 64 bits et l'absence d'`Unhandled primitive type`.

## Critères d’acceptation

- Un chargement de niveau complet ne produit aucun décalage (positions d'items comparées à la référence 32 bits).
- Sauvegarde puis rechargement donnent la même position et la même salle.

## Validation

Sonde runtime (positions d'items + lara) comparée entre build 32 et 64 bits.

## Inconnues

Effets de bord sur les zones/boxes des créatures.

## Estimation

2 jours-personne.

## Dépendances

- RMIG-003
- RMIG-004

## Preuves

- 2026-11-17 : Arène sous 4 Gio : MALLOC.C utilise mmap(MAP_32BIT) en LP64, ce qui garde valides les adresses 32 bits stockées dans les blocs relogés. Salles : struct room_info_file (80 o, pointeurs psx_u32) + static_assert, et conversion champ par champ vers room_info dans LoadLevel (chemin LP64), les blocs étant relocalisés depuis leur position fichier. Builds 32 et 64 bits verts, hash 32 bits inchangé (b9d8e710…). Nouvelle limite mesurée : le binaire 64 bits plante dans LoadLevel à GAME/SETUP.C:1838 (`((int*)&meshes)[i] += …`), première d'une famille de 487 `(int*)&` qui traitent des tableaux de pointeurs comme des int.

## Références

- `GAME/SETUP.C:1636` (relocation)
- `GAME/PORTSAVE.C:386` (application de la position)
