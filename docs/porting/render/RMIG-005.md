# RMIG-005 — Code manipulant les champs convertis

Status: **Blocked** — priorité P1 — confiance Medium

Avancement : Bloqué par RMIG-003/004.

## Objectif

Adapter le code qui lit/écrit les champs convertis, en particulier la relocation du niveau et la restauration de sauvegarde.

## Faits établis

LoadLevel relocalise les pointeurs stockés dans les structures ; sgRestoreGame et PortSave_ApplyPending réinjectent des états. Toute conversion de type doit être répercutée là où des long servent de conteneurs.

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
