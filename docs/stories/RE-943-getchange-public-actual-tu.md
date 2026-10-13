# RE943 — publication actual-TU GetChange

PUBLICATION_REVIEW_REQUIRED. integration=false, production_ready=false, globalprocedure=false ; naturalité BLOCKED.

[Dashboard](../reverse/tomb5-progress-dashboard-re943-v1.html)

## Tracker
- [x] Baseline normal/strict RED16 avant candidate test-only.
- [x] Candidate normal/strict GREEN16, mutants exacts 8/4/15.
- [x] GetChange réel instrumenté ; buffers sélectionnés complets et événements entrée/sortie.
- [ ] Revue indépendante des hashes publics exacts REQUIRED.

Fixtures synthétiques indépendamment attendues et authentifiées par hashes archivés. Tests PASS signifie caractérisation RED/GREEN, jamais activation AnimateItem. Aucun replay target neuf, matériel ni startup naturel.

Exécution : `python3 tests/reverse/test_re943_getchange_actual_tu.py`. Prérequis publics : GCC multilib i386, ASan/UBSan i386, headers SDL2/GLEW système ; Linux ELF32 little-endian. Leak detection désactivée ; autres sanitizers fail-fast, stderr exécution vide hors rejet intentionnel. Sources complètes CONTROL.C, CONTROL_S.C et CAMERA.C compilées, jamais fonction copiée seule.

Cleanup : scratch reproductible supprimé, archives/pins/seals/firstFAIL conservés. Aucun stage/commit/push ; sources production et index préservés. RE930 BIU/kernel/SPU/unité refusée exclus.
