# RMIG-005 — Code manipulant les champs convertis

Status: **Todo** — priorité P1 — confiance Medium

Avancement : À démarrer (RMIG-004 terminé).

## Objectif

Adapter le code qui lit/écrit les champs convertis, en particulier la relocation du niveau et la restauration de sauvegarde.

## Faits établis

LoadLevel lit les enregistrements de salle directement dans struct room_info (DEL_CDFS_Read puis cast) et la relocalisation lit la taille dans le premier champ 32 bits ; les items passent par un format compact, mais room_info contient cinq pointeurs. En LP64 ces champs font 8 octets : le cast décale tous les champs suivants. C'est la cause probable des 'Unhandled primitive type' observés sur le binaire 64 bits (594 en 20 s) alors que le 32 bits est correct.

## Périmètre

GAME/SETUP.C (relocation), GAME/SAVEGAME.C, GAME/PORTSAVE.C, GAME/ITEMS.C et accès directs aux champs convertis.

Hors périmètre : Rendue, backend Vulkan.

## Tâches

- [ ] Recenser les écritures de champs convertis via des long et les adapter.
- [ ] Vérifier la relocation des pointeurs (uintptr_t) et l'absence de troncature.
- [ ] Rejouer un chargement de niveau 3 et une sauvegarde/reprise.

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

- à produire (aucune mesure pour l’instant)

## Références

- `GAME/SETUP.C:1636` (relocation)
- `GAME/PORTSAVE.C:386` (application de la position)
