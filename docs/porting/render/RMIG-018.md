# RMIG-018 — Rendu 64 bits : mots PSX 32 bits et buffers bas

Status: **Done** — priorité P0 — confiance Medium

Avancement : Termine : rendu logiciel 64 bits stable sur l ecran titre/attractif.

## Objectif

Faire fonctionner le rendu logiciel PSX en LP64 sans corruption de pointeurs tronques.

## Faits établis

En LP64 `unsigned long` fait 8 octets : P_TAG passait de 12 a 20 octets et POLY_F3 de 24 a 32, alors que le jeu ecrit des primitives au format 32 bits. Les buffers GPU (OT, polygones, tsv_buffer, scratchpads de rendu), les matrices temporaires et certaines listes vivaient au-dessus de 4 Gio et etaient tronques par les casts (int) du code PSX.

## Périmètre

EMULATOR/LIBGPU.* et TYPES.H (type PSX_ULONG), SPEC_PSXPC_N (GPU, MISC, ANIMITEM, ROOMLET1-4, LIGHT, DRAWOBJ, CALCLARA, 3D_OBJ), GAME/DELTAPAK.C (temp_rotation_buffer), allocation basse PORT_LowAlloc.

Hors périmètre : Vulkan, shaders, parite visuelle.

## Tâches

- [ ] Introduire PSX_ULONG (32 bits en LP64, unsigned long sinon) pour les mots PSX et les structures de primitives.
- [ ] Allouer sous 4 Gio les buffers manipules via des int : OT, polygones, tsv_buffer, scratchpads, matrices temporaires.
- [ ] Adapter les acces aux listes stashees et aux tableaux meshes/bones a la disposition hote.

## Critères d’acceptation

- sizeof(P_TAG)=12 et sizeof(POLY_F3)=24 en 64 bits, identiques au 32 bits.
- Aucun SIGSEGV pendant 35 s du mode attractif 64 bits ; capture DEMO MODE.
- Build 32 bits toujours vert et tests 4188 PASS.

## Validation

Comparaison des tailles via gdb, execution 64 bits + capture de fenetre, suite de tests.

## Inconnues

Primitives PSX restant non gerees par l emulateur (voir RMIG-019).

## Estimation

2 a 3 jours-personne.

## Dépendances

- RMIG-017

## Preuves

- 2026-11-17 : gdb 64 bits : sizeof(P_TAG)=12, sizeof(POLY_F3)=24 (identiques au 32 bits). Execution de 35 s sans SIGSEGV, capture /tmp/opencode/title64.png montrant DEMO MODE. Les erreurs "Unhandled primitive type" passent de 702 a 0-77 selon la frame (suivi RMIG-019).
- 2026-11-17 : Complement : apres conversion des u_long restants de LIBGPU (DR_ENV/DR_*), les tailles de toutes les primitives et environnements sont identiques entre 32 et 64 bits, et le compteur de primitives non gerees tombe a 0 (RMIG-019).

## Références

- `EMULATOR/LIBGPU.H:366` (P_TAG/POLY_* : champs tag/len en PSX_ULONG)
- `SPEC_PSXPC_N/GPU.C:36` (allocation basse des tables OT/polygones)
- `SPEC_PSXPC_N/MALLOC.C:63` (PORT_LowAlloc (mmap MAP_32BIT))
