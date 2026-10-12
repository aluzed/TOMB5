# RE929 — publication metadata CPU exception RE928

## Progression
- [x] Inventaires exacts, tailles/SHA/seals authentifiés ; closure03 strict PASS82 membres.
- [x] Source et données witness : 128exceptions + 8RFE = 136 ; six mutants chacun136. TDD RED/GREEN canonical/public-only, ZERO replay numérique.
- [ ] PENDING_INDEPENDENT_REVIEW ; worktree-only aucun stage/commit/push.

## Evidence
SYSCALL franchi +42completed/43visits restored ; fresh1981129completed/1981130visits. BEV hérité -> ROM vecteur -> flushCache, arrêt AVANT BIU store non complété. RAM entière2MiB,32GPR,CP0,orderedPC,MMIO/clocks comparés indépendamment. Zéro nouveau service retourné, handlerRAM et RFE retour naturel NON obtenus. Witness extrait/adapté PCSX-Redux GPL-2.0-or-later ; ROM OpenBIOS MIT réutilisée, non recompilée, backend nonSony. Copyrights depuis headers authentifiés ; aucun source tierce redistribuée.

## Reviewhistory
closure03 strict PASS fini archivé, neuf racines833membres ; closure-time32targetchecks/5atomicrejections, ZERO nouveau CPU/build/witness. Self-report264 REJECTED, code/données136. closure01 SEALED FAIL73 immutable ; originalreview UNSEALED et closure02 UNSEALED conservées. firstFAIL, historique TDD/authoringgap et global/procedure FAIL maintenus non rétrocertifiés.

## Blockers
Loads immédiats/software oracle, pas hardware. RFE/BD/BREAK construits seulement ; pas naturel handlerRAM/retour kernel. Sony/reset/CD/GPU/hardware/gameplay non prouvés, integration=false production_patch=false. BLOCKED-001/002 suppressions utilisateur, report/cache/assets/coldarchives/seals/firstFAIL/RE893partial préservés.

## Acceptance
Schema récursif types exacts et leaf mutants ; guards metadata/raw/secret/binary/paths ; dashboard versionné et maintained suffix inverse RE927 exact. Adapters immédiats inversibles exact HEAD, sans changer pins historiques. Compatibility baseline/current/export mêmes deux FAIL historiques RE830, pas full-suite PASS. Public-only sans preuve privée. PENDING_INDEPENDENT_REVIEW exact-public-hash.

## Handoff
Next RE930 BIU/cache et vraie initialisationCPU/kernel/thread avant Exec, sans BEV effacé ni thread injecté. Aucun nouveau job/successeur ni changement production.

{
  "BEV_inherited": true,
  "archived_counts": {
    "closure_atomic_rejects": 5,
    "closure_target_checks": 32,
    "completed": 1981129,
    "exception_cases": 128,
    "gpr": 32,
    "mutant_comparisons_each": 136,
    "mutants": 6,
    "resume_completed": 42,
    "resume_visits": 43,
    "reviewer_attempts": {
      "accepted_fresh": 2,
      "failed_fresh": 1,
      "fresh": 3,
      "restored": 3
    },
    "rfe_cases": 8,
    "transitive_members": 833,
    "transitive_roots": 9,
    "visits": 1981130,
    "whole_ram_bytes": 2097152,
    "witness_comparisons": 136
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
          "Copyright (C) 2023 PCSX-Redux authors",
          "g_system->printf(_(\"Copyright (C) 2019-%i PCSX-Redux authors\\n\"), 2025);"
        ],
        "license": "GPL-2.0-or-later",
        "path": "src/core/r3000a.cc",
        "sha256": "77a2068343e98fc10728007f2943db164aa39b3a00d083434c31cdcb0046083c",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/r3000a.cc"
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
    "re918-openbios": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "093dc01dadd97038aef080264f77aac05e1607d2ca3bbb07330a4f78e912142a",
      "members": 92,
      "seal_sha256": "a47cb98851a0e28b9da66f8a097158f82bd26fed03ddb936856985e0e38ba591"
    },
    "re920-recovery01": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "3560d82679ee9f0b7a6af003a6622f2540ad0a76e7eb02b82789f570c0305c0f",
      "members": 76,
      "seal_sha256": "e75abaf22a27198200251c9edd3f1b1ad156b32b27249828b91f64ed6c992f61"
    },
    "re922-interrupt-mmio": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "3a7465def56d0074975152e05edd4d7807a23a84c0775d2503046156d72cc1c1",
      "members": 112,
      "seal_sha256": "5d2b37d4687bf165ebeed2ee2c6605f059a05a8a9727ab9045193d13447707cf"
    },
    "re924-dma-mmio": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "c425623ea296d3700c125d8cbe0adc104f7694ae13f04c0ed6c9f1417fcc464a",
      "members": 85,
      "seal_sha256": "fab8b8b58f8312cc1578701ab1803a79610a1398846b083b822896e74f516a56"
    },
    "re924-review": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "555c64baa95f28115235e5b5a9b73a0a65e8998531b39b00f45293f28769d823",
      "members": 70,
      "seal_sha256": "a99abe186b996e5cad9acd8e09c96b4b878f985aecdc9e2800c8c61ffd79bd77"
    },
    "re924-review-scope-clarification01": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "8ef0f29125e4306d196d1e664576df7610b1f85c04a9afa3de8851dfcabb4e11",
      "members": 7,
      "seal_sha256": "39e44a8df73d8d757f1a9ffc3dfdff2ef6cbe4cc12a256606b450973b4e28b45"
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
    },
    "re927-parent-delivery": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "89ad4758378bee74b7d6983ce562e8a22e3edd39af2d7c517b8be703d1b17c10",
      "members": 5,
      "seal_sha256": "951817953f629796f17a7835ec41323b6e11baf6acaffd35f1c836c8de18cb87"
    },
    "re928-cpu-exception": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "3c7015a8ca058a435dcdbb31fd3562b1906a8876b567339d1917daebdc228e86",
      "members": 131,
      "seal_sha256": "ad90a3adbcd9df24ad2613c87954d0bf13795586b0344a3a9ba6edbf41c3967b"
    },
    "re928-parent-checkpoint": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "5283e2de479b15ba285750bdad71c9b3af2d20e0ed7d2222d938b7ffd3beca5b",
      "members": 6,
      "seal_sha256": "8fa6281f7da7b2650fb1f55d8822f8ac0e154fd8fbfae99d4ec4f3d731d7a006"
    },
    "re928-review-closure01": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "cc08412bff27e459273629e3d977df52a67db150e2db849d6a58253fc734004c",
      "members": 73,
      "seal_sha256": "cd7cdc19036866f4398c453b74b3d2cb7736cf71c0ce75ccd2eb59e91f454e9a"
    },
    "re928-review-closure03": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "217a9ad86857927a31520923fe30088b396f297da94ca7df9858d53b480e8dea",
      "members": 82,
      "seal_sha256": "c94198919ab3348494ba57142157a229e00800c8bbe68e01e791370b6be781cf"
    }
  },
  "backend_boundary": "RE928-PCSX-Redux-CPU-exception-subset",
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "frontier": "BEFORE_BIU_STORE",
  "global_scope": "FAIL",
  "integration": false,
  "kernel_RAM_handler_reached": false,
  "limitations": [
    "Immediate-load software CPU semantics, not hardware oracle",
    "RFE/BD/BREAK constructed only; no natural kernel return",
    "Reused OpenBIOS ROM, no fresh firmware compilation",
    "Device branches not traversed are not approved",
    "Global/procedure FAIL unchanged: historical bootstrap/TDD/accounting limitations",
    "Sony/reset/CD/GPU/hardware/gameplay not proved",
    "BEV inherited ROM vector then flushCache; stop before BIU store; no natural RAM handler or RFE return"
  ],
  "natural_RFE": 0,
  "naturalcaller": "BLOCKED",
  "new_service_returns": 0,
  "next_scope": "real CPU/kernel/thread initialization before Exec; no BEV clear or injected thread",
  "next_ticket": "RE930",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_REVIEW",
  "review_history": {
    "closure01": "SEALED_FAIL_PRESERVED",
    "closure02": "UNSEALED_PRESERVED",
    "closure03": "STRICT_FINITE_PASS",
    "firstFAIL": "all historical errors and rejected attempts retained",
    "original_review": "UNSEALED_PRESERVED",
    "self_report_264": "REJECTED",
    "strict_concerns": [],
    "strict_logic_errors": [],
    "strict_passed": true
  },
  "rom_fresh_build": false,
  "schema": "re929-cpu-exception-proof-publication-v1"
}
