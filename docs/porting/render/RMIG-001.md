# RMIG-001 — Étude 32 vs 64 bits du raytracing Vulkan

Status: **Done** — priorité P0 — confiance Medium

Avancement : Terminé : mesures 32/64 bits, conclusion et plan enregistrés.

## Objectif

Décider si le raytracing matériel est atteignable sur la cible actuelle, avec des mesures et non des suppositions.

## Faits établis

Sonde Vulkan identique compilée -m32 et -m64 sur la machine (RTX 2080 Ti, driver 580.178, Vulkan 1.4.312). En 32 bits le GPU expose 233 extensions sans aucune extension RT ; en 64 bits il en expose 248 avec VK_KHR_acceleration_structure, VK_KHR_ray_query, VK_KHR_ray_tracing_pipeline et VK_NV_ray_tracing. llvmpipe expose le RT dans les deux cas (logiciel).

## Périmètre

Énumération des périphériques et extensions par largeur de binaire ; conclusion sur la cible à retenir.

Hors périmètre : Écriture du backend, migration du code, réglages de performance.

## Tâches

- [ ] Écrire une sonde C qui crée une instance Vulkan et liste les périphériques et extensions RT.
- [ ] Compiler la même sonde en -m32 et -m64 et comparer les jeux d'extensions du GPU et de llvmpipe.
- [ ] Consigner la conclusion et ses conséquences sur l'ordre des travaux.

## Critères d’acceptation

- Les deux exécutions produisent une liste d'extensions exploitable et reproductible.
- La conclusion (RT matériel impossible en 32 bits sur cette machine) est étayée par les sorties, pas par la documentation constructeur.

## Validation

Sorties des deux binaires de la sonde, conservées dans /tmp/opencode/vkprobe (probe2.c) ; plan écrit dans docs/porting/vulkan-64bit-plan.md.

## Inconnues

Comportement sur une autre machine ou un autre pilote ; support RT 32 bits chez d'autres fabricants.

## Estimation

0,5 jour-personne (fait).

## Dépendances

- aucune

## Preuves

- 2026-11-17 : Sonde Vulkan -m32 : 233 extensions, aucune RT sur la RTX 2080 Ti ; -m64 : 248 extensions avec toutes les extensions RT. Commit 666bf08d (plan). — `666bf08d`

## Références

- `docs/porting/vulkan-64bit-plan.md:1` (plan et mesures)
- `EMULATOR/EMULATOR_PLATFORM_SETUP.H:18` (sélection du backend OGL)
