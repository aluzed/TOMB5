# RE-862 — candidat production mRotZ / MVMVA

Statut: revue independante PASS scoped enregistree; aucun stage, commit ou push au snapshot initial de revue.

## Contrat et progression
RED public sur TU completes inchangees, puis delta minimal examine prive:
mRotZ packing uint32 et conversion mRotX_signed32 existante; trois produits
CV signes multiplies par 4096LL dans le seul default MVMVA. Aucun autre opcode.
GREEN sur le meme hash de tests. Tests synthetiques uniquement, table CAMERA.C
versionnee. Pas de payload, RAM authentique ou mots cible publies.

36 rotations: oracle matriciel scalaire, 72 mots natifs preserves, ELF32/ELF64
O0/O2 normal/UBSan strict. 60 MVMVA: cv=0/1/3, sf/lm=0/1, extremes signes,
oracle produit entier64, MAC/IR/FLAG et banques64 completes, ELF32/ELF64
O0/O2 normal/ASan+UBSan strict. Branche cv=2 et matrice mx=3 exclues.
GetJointAbsPosition/GetFrames reels: fixture synthetique assignee par champs,
joints0/1, composition scalaire quart de tour, vec, MatrixStack/iMatrixStack
complets, GTE complet, pointeurs et item/anim/frame/bones/object preserves.
Composition ELF32 seulement O0/O2 normal/ASan+UBSan; conservation baseline
normal avant delta contre normal/strict apres delta. Aucun lien permissif.
-fpermissive (fpermissive) ELF64 limite au cast legacy hors chemin mmPushMatrix.
GC de sections: fonctions hors chemin compilees mais non executees.

Build Debug complet ELF32 incremental frais: MATHS.C et LIBGTE.C recompiles,
liaison MAIN reussie. Pas de runtime jeu; build != portabilite du jeu ELF64.

## Documentation et limites
RED historique RE859 observe apres ajout du seul bloc RE862. Exception exacte:
retirer seulement ce bloc nomme avant hash RE859, hash precedent inchange.
Nouveau guard epingle dashboard HEAD complet apres retrait RE862; mutations
section future inconnue et drift rejetees. Aucun document historique reecrit.
RE858 global FAIL preserve; ecarts natif/cible archives et limites procedurales
historiques restent distincts du PASS prive de contenu. Aucun oracle hardware,
aucune equivalence producteur gameplay revendiquee pour cette fixture.

Preuves operationnelles: build/reverse/autonomy-20261007/re862-integration-candidate.
Fichiers freezes et HANDOFF enumerent hashes exacts pour revue precommit.

## Verification finale
Selection finale: 14 tests passes (nouveaux RE862, guard RE859 et backend
libgte_rottrans), apres inscription des documents. Suite complete demandee
RE862+RE859+tests/emulator interrompue a 100 secondes: aucun PASS global
revendique, ledger incomplet pour cette tentative (trace outil seulement).
Build complet utilise aussi les flags legacy -fpermissive du projet; ce n'est
pas une preuve de compilation portable stricte de tout le jeu.

## Verification elargie du coordinateur apres cloture des statuts

Commande fraiche `python3 -m pytest -p no:cacheprovider -q` : tests RE862
mRotZ/composed/documentation, tests RE859 mRotX/documentation et tout
`tests/emulator` (bytecode desactive). **3684 passed in 103.97s, exit 0**.
Ledger exact : `build/reverse/autonomy-20261007/re862-closure/broad-tests-invocation.json`.
Ce resultat est distinct du timeout100s initial conserve et des tests reviewer.
Selection elargie, pas tous les tests du depot ni runtime jeu. Les checks
documentaires seront revalides apres cette inscription, sans replay prive.
