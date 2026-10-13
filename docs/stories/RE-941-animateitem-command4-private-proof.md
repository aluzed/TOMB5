# RE-941 — AnimateItem commande4 : preuve privée finie, publication exécutable

**PUBLICATION_REVIEW_REQUIRED** — revue indépendante des hashes publics requise.
Integration=false ; production_ready=false ; naturalité BLOCKED ; globalprocedure=false.
Aucune activation production, modification README, stage, commit ou push.

## Tracker
- [x] Preuve privée finale et revue stricte indépendante authentifiées, sans rejouer les matrices fermées.
- [x] Nouveau contrat public écrit avant candidat ; RED de setup conservé, puis baseline CONTROL.C courant compilé frais : behavioral RED16 avant publication du candidat.
- [x] Harness public reconstruit exactement 16 fixtures synthétiques (12 end-frame, 4 contrôles), table trigonométrique réelle complète et trois objets complets.
- [x] Oracle Python indépendante : fingerprints initiaux/attendus vérifiés contre buffers approuvés archivés ; aucun input privé au runtime.
- [x] Candidat strictement test-only ; domaine fini asserté par reconstruction littérale de tous les buffers, pas snapshot arbitraire ; rejet invalid-domain exécuté.
- [x] Normal/strict16 GREEN ; mutants mauvais objet cas0/1/2/3, omission status0/1/3/4/5/7/8/9/11, overwrite after_death6/10.
- [x] Export public-only MINIMAL des seules dépendances source/headers publiques nécessaires ; aucun asset ni header ignoré.
- [x] Cleanup DONE : scratch export propre à cette publication supprimé après inventaire exact avant/après ; archives historiques intactes, aucune économie disque globale revendiquée.
- [ ] Revue indépendante exacte des cinq fichiers publics : REQUIRED.
- [ ] Naturalité / intégration : BLOCKED.

## Contrat borné
Commande4 seulement après dépassement frame_end. ITEM.object_number sélectionne objet64,
flags objet+50 masque2 intelligent ; ITEM.after_death+48 (pas hit_points+34) devient1
si intelligent et zéro ; status devient2, autres bits conservés. Deux commandes4
successives. Changement animation/frame/states ensuite ; contrôles ne dispatchent pas.
16908 octets/cas : ITEM144, ANIM80, CHANGE12, RANGE32, COMMAND64,
TRIG16384, OBJECT192. Objets et tables comparés entièrement.
CONTROL.C complet courant, CONTROL_S.C/GetChange et CAMERA.C réels compilés/liés ;
GetChange non atteint. Candidate temporaire, source production inchangée.
ABI GCC i386 C++11 : ptr/int/long4, SDL2/GLEW publics, multilib et sanitizers requis.
ASan+UBSan fail-fast ; leaks désactivés ; stderr strict vide. Exécuter :
`python3 -B tests/reverse/test_re941_animateitem_command4.py`.
Tests publics PASS vérifient baseline16 différences, normal/strict0 et mutants4/9/2,
identités exactes et contrôles préservés ; ce n'est pas un GO production.

## Réserves conservées
Ancien candidat privé wrong-field hit_points rejeté (cas2/6/10), remplacement global
intermédiaire refusé, timeout124 outer-mutex/child lock-aware conservé sans
rétrocertification. Revue : diagnostics visites dupliquées instrumentées conservés ;
émulateur frais sans hooks mémoire pour trace, décodeur indépendant, RAM complète
pile comprise. Loads instrumentés non revendiqués égaux. Aucun claim ordre complet
des stores natifs, traces événements natifs vides, hardware ou gameplay. Publication
ajoute exécutions natives fraîches seulement, zéro target replay. Globalprocedure=false
reste distinct du PASS fini. Bootstrap transport auteur /tmp hors ledger canonique,
installations réelles et builds/runs sous mutex par opération avec owner vivant.
RE930 BIU/kernel/SPU et unité fournisseur historiquement refusée exclus.

## Handoff unique
Commande6 temporisée : attribuer effect_routines et son producteur réel puis
composition caller→callback authentifiée bornée/actual-TU avant extension privée.
Ne pas rouvrir mouvements/interpolation ; AnimateItem complet reste non prouvé.

[Dashboard](../reverse/tomb5-progress-dashboard-re941-v1.html) ·
[Prédécesseur inchangé](RE-940-animateitem-movement-private-proof.md)
