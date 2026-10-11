# RE915 — publication sûre du diagnostic fini RE914

## Progression
- [x] RED/GREEN metadata public-only, aucun replay numérique nouveau.
- [x] Quatre namespaces RE914 authentifiés exact sets/size/SHA/seals ; retry01 et audit-annex strict passed true empty errors/concerns.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only aucun stage/commit/push.

## Evidence
Header PC/SP/GP/payload/MD5 CONTRIBUTING authentifiés : entrée POST BIOS, pas power reset. Producteur1target1oracle indépendant, acceptedreview1target1CPUoracle ; cumulreview1target2oracle inclut firstFAIL Unicorn absent après oracle. Comparaison complète 2MiB RAM/32registercarriers/knownness/ordre PC/accesses égale : 1778375visits,355674accesses,355672interpretedstores,2loads ; visites pas instructions retirées. 9known23UNKNOWN carriers jamais authentiquement consommés. BSS/stack/heap setup fini exécuté ; arrêt AVANT SW RA inconnu parce que BIOS RA absent header. Producteur3/review5 sensitivity checks. GPU/Timer writes0, SDK/BIOS doubles0, RA injection0, RE910/912replays0, native compile/run/runtime0. Setup GPU statique non atteint.

## Blockers
Functional BLOCKED/global FAIL/procedure FAIL/integration=false/naturalcaller BLOCKED. Zéros hors payload CONSTRUCTED, pas RAM naturelle. Oracle CPU logiciel indépendant pas hardware. FirstFAIL et checker errors immuables, retry distinct ; booléen audit ADDI rejeté tel quel et clarification audit-annex : une ADDI exécutée, non-overflow vérifié, pas approbation universelle de l'émulateur. Upstream hardware preconditions toujours bloquantes. Producer232.40task232.44outer reviewer297.65task297.69outer sourceanchor304.6 origine distincte. BLOCKED-001/002 user deletes/report-tech/cache/cold archives/RE893partial préservés.

## Acceptance
- [x] Schema recursive exact bool/int/float types/scalars ; contrôles négatifs et benign mêmes chemins légitimes.
- [x] Dashboard versionné/maintenu suffixe unique inverse exact RE913 ; historical pins unchanged.
- [x] Public-only sans ignored proofs ; compatibility same baseline nodeids, pas global GREEN.
- [ ] Revue indépendante exacte des hashes publics PENDING.

## Next — RE916
Contrat/producteur BIOS Exec RA authentique ou capture authentifiée de l'état d'entrée ; pas RA arbitraire ni secteur CD positif. Aucun sourcepatch/sourceproduction/native/runtime/cleanup/cron autorisé par cette publication.

{
  "RE914": {
    "ADDI": {
      "checked_no_overflow": true,
      "executed": 1,
      "historical_boolean_rejected_as_written": true,
      "no_syscall_COP_status_reached": true,
      "universal_emulator_approval": false
    },
    "comparison": {
      "RAM_bytes": 2097152,
      "UNKNOWN_carriers": 23,
      "accesses": 355674,
      "full_RAM_GPR_PC_order_accesses_knownness_equal": true,
      "interpreted_loads": 2,
      "interpreted_stores": 355672,
      "known_GPR": 9,
      "ordered_visits": 1778375,
      "register_carriers": 32,
      "visits_not_retired_instructions": true
    },
    "diagnostic": "PASS_STRICT_FINITE_ONLY_WITH_ADDI_CLARIFICATION",
    "first_FAIL_preserved": true,
    "functional_GREEN": 0,
    "functional_passed": false,
    "next": "RE916 authentic BIOS Exec RA producer entry contract or authenticated state capture; upstream hardware gates remain BLOCKED; no positive CD sector or RA constant",
    "producer": {
      "accepted_target_runs": 1,
      "independent_stdlib_oracle": 1,
      "sensitivity_checks": 3
    },
    "producer_outer_seconds": 232.44,
    "producer_task_seconds": 232.4,
    "reviewer_accepted": {
      "fresh_target": 1,
      "independent_CPU_oracle": 1,
      "sensitivity_checks": 5
    },
    "reviewer_cumulative": {
      "accepted_successor": "retry01",
      "clarification": "retry01/audit-annex ZERO fresh executions",
      "first_attempt": "FAIL_UNICORN_MISSING_AFTER_ORACLE",
      "fresh_target": 1,
      "independent_CPU_oracle": 2
    },
    "reviewer_outer_seconds": 297.69,
    "reviewer_task_seconds": 297.65,
    "source_anchor_seconds_distinct": 304.6,
    "startup": {
      "BIOS_RA_absent_header": true,
      "BSS_clear_stack_heap_setup": "FINITE_AUTHENTIC_EXECUTED_PREFIX",
      "GPU_Timer_writes": 0,
      "GPU_setup_static_not_reached": true,
      "RAM_outside_payload": "CONSTRUCTED_ZERO_NOT_NATURAL_RAM",
      "RE910_RE912_replays": 0,
      "SDK_BIOS_return_doubles": 0,
      "arbitrary_RA_injection": false,
      "entry": "POST_BIOS_EXECUTABLE_ENTRY_NOT_POWER_RESET",
      "header_PC_SP_GP_payload_MD5_CONTRIBUTING_authenticated": true,
      "native_compiles": 0,
      "native_runs": 0,
      "runtime": 0,
      "stop_before_unknown_RA_store": true,
      "unknown_carriers_authentically_consumed": false
    }
  },
  "authentication": {
    "re914-review": {
      "entries": 10,
      "manifest_sha256": "c5898099313c086f6cf9a4729ef10432f3bafde6b236959f7610bd8ed1e9f960",
      "seal_sha256": "e45761d32e5a5cc2fb4c86543201110357f5df1b095508ffb4eabba9a0257b22",
      "verdict_sha256": "6c5a4fde50aa11cca7fd874de1d438d53a7978b743648e8948f6a31951590840"
    },
    "re914-review/retry01": {
      "entries": 19,
      "manifest_sha256": "b3215020dcf88bea53306150db7a4966b28ecb539a493f7e3a08670c47392f39",
      "seal_sha256": "777f654cffd26a95ea476b7a92f58cdc12ff96fdd3149e0379cf23258bbf6cb5",
      "verdict_sha256": "61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17"
    },
    "re914-review/retry01/audit-annex": {
      "entries": 5,
      "manifest_sha256": "5878bce63f84c183e177fe7abb6f9153901b64deed508e1366a4dad874618e1d",
      "seal_sha256": "11aa37b63112888e47cf154c6cf22bf5bd0ca94b183406128ba2bc21f8ff6a16",
      "verdict_sha256": "61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17"
    },
    "re914-startup-hardware-provenance": {
      "entries": 17,
      "manifest_sha256": "355d7516262b1719ec6dcc47363523ecb1a2cc8cde00c9bbd9f8a0a981d3a614",
      "seal_sha256": "6fa6f705d2b432661f28082cd637b404d484e17273933893612fcb0d8b6ff5c4",
      "verdict_sha256": "61434fd898e98df40a81d7d9168834f308c952bdbd02a72b501a5fe1bffb6e17"
    }
  },
  "authentication_scope": "all four RE914 root namespaces exact sets sizes hashes seals freshly verified; no numerical replay",
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "global_scope": "FAIL",
  "integration": false,
  "naturalcaller": "BLOCKED",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_EXACT_HASH_REVIEW",
  "schema": "re915-header-startup-diagnostic-publication-v1"
}
