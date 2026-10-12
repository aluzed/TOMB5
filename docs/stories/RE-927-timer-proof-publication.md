# RE927 — publication metadata Timer1 RE926 corrigé

## Progression
- [x] Inventaires privés exacts153/107/4 et checkpoint4 authentifiés, schemas/seals/tailles/SHA et verdict strict lus avant tests.
- [x] TDD RED puis GREEN canonical/public-only ; ZERO replay numérique.
- [ ] PENDING_INDEPENDENT_REVIEW ; worktree-only, aucun stage/commit/push.

## Evidence
RE926-PCSX-Redux-Timer1-local-free-running-subset franchit un MODE write naturel, ZERO counter read naturel. Fresh1981087 instructions complétées/1981088visites, restored318/319 ; stop AVANT SYSCALL OpenBIOS EnterCriticalSection non complété. RAM entière2097152octets,32GPR, orderedPC/MMIO/serviceentries/returns comparés avec CPU indépendant reviewer. Producteur6méthodes/28comparaisons/5mutants sensibles ; reviewer28+512comparaisons/6atomiccontrols/6méthodes ; six target attempts dont trois accepted final, deux accepted final CPU runs. Publication ZERO target/native replay. ROM OpenBIOS MIT héritée authentifiée non recompilée ; sources PCSX-Redux GPL-2.0-or-later authentifiées par headers/blobs pinés. Witness extrait/adapté pas émulateur complet. Aucune source tierce redistribuée.

## Reviewhistory
Strict private PASS porte seulement sur finite corrected source/prefix ; ablation archivée clock7912652 REJECTED NON CERTIFIÉE conservée, corrected fresh7921560 distincte. firstFAIL/retries, découverte incomplète et auth prédécesseur tardive conservés ; global/procedure FAIL non rétrocertifiés. Cardinalité parent4, ancienne prose5 corrigée sans changer archives.

## Blockers
BIAS2/+20/NTSC et initialTimer/ABI/RAM construits, epoch locale, loads immédiats pas load-delay/cache ; pas fullscheduler, IRQ/gates/deadlines/DMA/exceptionCPU prouvés. Sony/reset/GPUSTAT/CD/hardware/gameplay non prouvés, integration=false, production_patch=false. BLOCKED-001/002 restent supprimés ; report/cache/assets/coldarchives/seals/firstFAIL/RE893partial préservés.

## Acceptance
Schema récursif types exacts, leaf mutants, guards raw/secret/binary/paths ; dashboard HTML versionné et maintained suffix exact inverse RE925 ; deux adapters reconstruisent HEAD sans affaiblir historique. Compatibility baseline/current/export mêmes deux FAIL RE830, pas full-suite PASS. Public-only sans build/private dependency. Revue indépendante exact-hash PENDING_INDEPENDENT_REVIEW.

## Handoff
Prochaine RE928 modèle CPU exception/SYSCALL cohérent sans retour double ; aucun nouveau job/successeur ni patch production autorisé par cette publication.

{
  "archived_counts": {
    "completed": 1981087,
    "gpr": 32,
    "producer_methods": 6,
    "producer_sensitive_mutants": 5,
    "producer_source_comparisons": 28,
    "resume_completed": 318,
    "resume_visits": 319,
    "reviewer_accepted_final_CPU_runs": 2,
    "reviewer_accepted_final_target_runs": 3,
    "reviewer_additional_source_comparisons": 512,
    "reviewer_atomic_controls": 6,
    "reviewer_fresh_target_attempts": 6,
    "reviewer_methods": 6,
    "reviewer_source_comparisons": 28,
    "visits": 1981088,
    "whole_ram_bytes": 2097152
  },
  "attribution": {
    "OpenBIOS_license": "MIT",
    "license": "GPL-2.0-or-later",
    "openbios_commit": "7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30",
    "pcsx_commit": "c313b116e6a55786bc127c9b3a07a90b55d97c21",
    "project": "PCSX-Redux / nugget OpenBIOS",
    "sources": [
      {
        "copyright": [
          "Copyright (C) 2010 by Blade_Arma"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxcounters.cc",
        "sha256": "b4406898c327a8bd1f289dff2c42f85c630ab80dddc5cf489c2ace11fad45831",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxcounters.cc"
      },
      {
        "copyright": [
          "Copyright (C) 2010 by Blade_Arma"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxcounters.h",
        "sha256": "85ef25a1a7f92f69f55030e97b0169eab9f1f8b1478d5d351136e920bac12484",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxcounters.h"
      },
      {
        "copyright": [
          "Copyright (C) 2023 PCSX-Redux authors"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxhw.cc",
        "sha256": "db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxhw.cc"
      },
      {
        "copyright": [
          "Copyright (C) 2022 PCSX-Redux authors"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxemulator.h",
        "sha256": "da2a56af7f0ae6d93e38b213e65be4606527b629013b6df02cdd991691e17a0b",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxemulator.h"
      },
      {
        "copyright": [
          "Copyright (C) 2023 PCSX-Redux authors"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxinterpreter.cc",
        "sha256": "0c9eca067b3ed23c0ea9fd84d9a3752af3c92f2281ebc05316fa1f385392f2e5",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxinterpreter.cc"
      }
    ],
    "third_party_source_redistributed": false
  },
  "authentication": {
    "re925-parent-delivery": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "a9bddde81c12329d6dc45a1fa94df2d97c1c4215d70342bf6a4acc4c8070d67d",
      "members": 4,
      "seal_sha256": "955dc9fb38343b600162b1e9b33d6364c3a29cac9edaaa0484425cc538ff1f6e"
    },
    "re926-parent-checkpoint": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "e4eeb24e785949963731cc130d9d76f27a5cec298438225dde523c71684f67a6",
      "members": 4,
      "seal_sha256": "c362a853b91019f740686afae263ab53fbcca3d5dfda8e4cbc9a84fe5c4f470d"
    },
    "re926-review": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "82f5f39fbf0b8beaaccb5a6ed4ca26061c55c9b4d0f3a41b08ae10263a344638",
      "members": 107,
      "seal_sha256": "566c999431f06d93c51ac1382abbba9b3efa21da06ae8c76c20e5de207cc7286"
    },
    "re926-timer-mmio": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "3f402188e536c1fe84ffbbf250cff8828582d99bd2e1dffe93cb88062461c2bb",
      "members": 153,
      "seal_sha256": "c37da1cbef04370433b31e4d0f8d09868e72ae131ad3432f796ef72cfe6380f7"
    }
  },
  "backend_boundary": "RE926-PCSX-Redux-Timer1-local-free-running-subset",
  "clock_model": "BIAS2 per instruction plus20 BIOS next-PC region; constructed NTSC settings and local Timer1 epoch; not full scheduler",
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "frontier": "BEFORE_SYSCALL_OpenBIOS_EnterCriticalSection",
  "global_scope": "FAIL",
  "integration": false,
  "limitations": [
    "constructed NTSC/settings/initial counter and ABI",
    "ROM reused, not rebuilt",
    "immediate loads, not hardware R3000 load delay",
    "no full scheduler, CPU exceptions or hardware oracle",
    "Sony/reset/GPUSTAT/CD/hardware/gameplay not proved",
    "Timer IRQ/gates/deadlines/DMA transfers unsupported"
  ],
  "natural_counter_reads": 0,
  "natural_mode_writes": 1,
  "naturalcaller": "BLOCKED",
  "next_ticket": "RE928",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_REVIEW",
  "retirement": "previous instruction completed at following hook, not hardware retirement",
  "review_history": {
    "accepted_scope": "finite corrected Timer1 source slice and authentic executable prefix only; NOT certification of stale archived ablation clock",
    "archived_clock": 7912652,
    "corrected_fresh_clock": 7921560,
    "firstFAIL": "all historical errors and rejected attempts retained",
    "global_concerns": [
      "archived backend-noirq timer_final.clock stale 7912652 versus corrected fresh 7921560; original mismatch preserved",
      "producer predecessor full authentication performed after first attempts",
      "historical firstFAILs and incomplete discovery ledger retained"
    ],
    "stale_ablation": "REJECTED_NON_CERTIFIED",
    "strict_concerns": [],
    "strict_logic_errors": [],
    "strict_passed": true
  },
  "rom_fresh_build": false,
  "schema": "re927-timer-proof-publication-v1"
}
