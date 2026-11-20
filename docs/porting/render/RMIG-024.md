# RMIG-024 — Parite niveau 2 : objets de decor manquants en 64 bits (salle 194)

Status: **In progress** — priorité P2 — confiance Medium

Avancement : Ouvert pendant la validation des cinematiques : la divergence se reproduit sans cutscene, donc elle est independante du declencheur. Etats d'items et camera identiques ; piste principale : dessin des meshes de room / ordering.

## Objectif

Retrouver l'image identique 32/64 sur la vue de la salle 194 du niveau 2 (Trajan's Markets), ou une lampe suspendue et un relief de dragon manquent au build 64 bits.

## Faits établis

Avec TOMB5_START_POS=55808,0,30208,117,-32768 (sans aucune cinematique), 300 frames : mean_abs_diff=0.268, 3379 pixels differents dont 2872 a plus de 8. Le build 64 bits ne dessine pas une lampe suspendue ni un relief de dragon visibles en 32 bits. Les 151 items sont identiques (objet, status, flags, anim, frame, room, position), la camera est identique (55808,-769,31538), room=194, ndraw=16, draw0=194. [PH] montre toutefois que le 32 bits emet ~2x plus de vertices (7323 vs 3951) et des primitives 0x26/0x2E absentes en 64 bits ; a verifier s'il s'agit d'un double draw du backend GL ou des objets manquants.

## Périmètre

DRAWPHAS.C / LIBGPU.C / ROOMLETB.C : liste des meshes de room, ordering table et profondeur par bucket.

Hors périmètre : Cinematiques (validees separement), Vulkan/RT.

## Tâches

- [ ] Comparer les listes de meshes de room 194 (et voisines) entre 32 et 64 bits.
- [ ] Determiner si les primitives 0x26/0x2E et le surplus de vertices du 32 bits sont un double draw ou du decor reel.
- [ ] Corriger le chemin de dessin des meshes/objets manquants en 64 bits.
- [ ] Verifier la parite byte-identique sur cette vue et sur la scene de reference.

## Critères d’acceptation

- Capture 32/64 identique sur TOMB5_START_POS=55808,0,30208,117,-32768.
- Aucune regression sur la scene de reference (niveau 3, 63041e5c...).

## Validation

check_parity.sh + captures ciblees avec TOMB5_START_POS + [PH]/[DRAW].

## Inconnues

Les objets manquants peuvent etre des meshes statiques de room, des ANIMATING items ou un probleme d'ordering/depth.

## Estimation

1 a 2 jours-personne.

## Dépendances

- RMIG-007

## Preuves

- 2026-11-20 : Reproduction : TOMB5_START_POS=55808,0,30208,117,-32768, niveau 2, 300 frames, sans cutscene. 64 bits : mean_abs_diff=0.268 vs 32 bits, 3379 pixels differents (2872 > 8). La lampe et le relief de dragon sont absents en 64. [DRAW] identique (room=194, ndraw=16, draw0=194) ; items identiques sur les 151 entrees. [PH] : 7323 vertices en 32 contre 3951 en 64, plus 0x26=30 et 0x2E=16 seulement en 32.

## Références

- `SPEC_PSXPC_N/DRAWPHAS.C:352` ([DRAW] camera/room/ndraw)
- `EMULATOR/LIBGPU.C:570` ([PH] histogramme de primitives)
- `scripts/porting/check_parity.sh:1` (parite 32/64)
