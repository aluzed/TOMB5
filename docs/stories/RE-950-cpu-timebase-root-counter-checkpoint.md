# RE-950 — Timebase CPU et TU complète des root counters

Deux unités comportementales substantielles acceptées dans leur périmètre fini par des revues indépendantes fraîches. **INCOMPLETE ; integration=false ; production_patch=false ; aucune acceptation globale.** Publication PENDING : auteur et reviewer doivent être distincts.

## Tracker
- [RE949](RE-949-cd-init-scheduler-checkpoint.md) : enqueue CD et ordonnanceur conservés.
- Unité03 : timebase +2/+22 et arbitrage réels dans interpréteur épinglé. Dix visites supplémentaires DIAGNOSTIC après enqueue et avant update root-counter. Le branchTest global du préfixe hérité reste non prouvé.
- Unité04 : TU psxcounters.cc complète byte-identique, compilation normale avec headers de dépendances typés adaptés et doubles SPU/IRQ/vsync explicites. Contrat fini NTSC/PAL et VSyncWA ; pas build entier ni matériel.
- Prochaine frontière : **SPU_CURRENT_FRAMES_REQUIRED_BEFORE_NEXT_COUNTER_SET**. Deadline compteur naturelle toujours non produite dans le CPU. Produire réellement currentFrames, previousCycles, waitForGoal, atomic pending et configuration vidéo naturelle ; aucun seed deadline ou pending=false.

## Mesures
Unité03 : six tests, 1200 arbitrages, 15 ticks auteur et 24 ticks reviewer, huit mutants sensibles. Reviewer : oracle scalaire fraîchement recompilé puis CPU fresh/restored et RAM complète de 2097152 octets ; suffixe commun 314754 PCs et états vivants complets égaux hors listes historiques déclarées. Chronologies brutes conservées mais non identiques. Narrowing int32 depuis int64 maximal donnant -1 au compilateur testé : avertissement conservé, pas propriété portable du matériel.

Unité04 : huit tests, 693 projections effectivement assertées (112 matrice + 581 longues), 583 états longs archivés dont deux init non assertés, 545 updates restaurés compteur. Restauration état compteur, **pas replay CPU**. Huit mutants sensibles. La TU sans fournisseur SPU refuse réellement init : exit 3, stdout vide avant set. Doubles explicites, pas provenance naturelle.

Aucun callback CD dispatché, secteur ou gameplay. Entrée OpenBIOS/FIFOs construite, aucun reset naturel ni BIOS Sony. Aucun code privé copié ni production activée. Tests publics de contrat documentaire seulement, ni replay CPU ni build TU. Premier FAIL, erreurs, avertissements, mutants et retries reviewers conservés. Strict passed=false / finite_acceptance=true : pas PASS global ni intégration.

Sources : PCSX-Redux c313b116e6a55786bc127c9b3a07a90b55d97c21 GPL-2.0-or-later ; nugget 7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30 MIT. Permission de licence ≠ preuve matériel ou clean-room globale. [Métadonnées et pins](../reverse/generated/re950-cpu-counter-checkpoint.json) ; [dashboard](../reverse/tomb5-progress-dashboard-re950-cpu-counter-v1.html) ; [tests publics](../../tests/reverse/test_re950_cpu_counter_checkpoint.py).

## Nettoyage
zéro suppression ; archives immuables et assets conservés. Capacité libre mesurée : 21745172480 octets. Aucun staging, commit ou push ; état utilisateur protégé. Commandes, durées et résultats mesurés dans ledger privé ; HANDOFF, verdict et hashes avant seal. Budget checkpoint ≠ arrêt global : autorisation du 14 octobre 2026 jusqu’à 18 h applicable au prochain tick ; aucun job lancé.
