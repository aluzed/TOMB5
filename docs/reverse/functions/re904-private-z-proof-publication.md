# RE904 — publication metadata Z privée, v1

## Progression
- [x] RED46 générateur absent avant implémentation.
- [x] Seals/verdicts sélectionnés authentifiés, full inventories vérifiés auparavant par parent.
- [x] Schéma exact, tracker, dashboard append-only avec inverse.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW.

## Evidence

### RE902
{
  "causal_attribution": "four Z scratch stores native16 versus target32; iRotZ signed packing shifts UB; two secondary normal stores observed including same-value writes",
  "cpu": 9,
  "fullraw_verdict": "FAIL",
  "geometry": "PASS",
  "historical_failures": [
    "provider refusal RE902 112.45/112.5 preserved; no numerical replay",
    "first empty wrong-signature static bodies preserved, exact signature recovery separate"
  ],
  "math": 9,
  "native": {
    "aborts": 12,
    "attempts": 36,
    "position_mismatches": 0,
    "raw_mismatches": 24,
    "returns": 24
  },
  "producer_diagnostics": {
    "aborts": 1,
    "attempts": 4,
    "returns": 3
  },
  "review_verdict_sha256": "0058cc5efd78006adf62f5ccf4a04c5325d6ddb291c4235299ca22bccb31b256",
  "reviewer_diagnostics": {
    "aborts": 2,
    "attempts": 6,
    "returns": 4
  },
  "reviewer_native": {
    "aborts": 12,
    "attempts": 36,
    "returns": 24
  },
  "scope": "PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL",
  "strict_verdict": "FAIL",
  "target": 9,
  "ticket": "RE902"
}

### RE903
{
  "baseline_sha256": "89999eaaf2818eb5b1073d8c206a8867c56e57a27a5155c8fcf297de08085f0c",
  "candidate_sha256": "eee7b22f5cc66b314d144db227b187d40a4c0846d6248c03974c90a5f2308d01",
  "fullraw_verdict": "PASS_FINITE_SELECTED_PROJECTION",
  "historical_failures": [
    "original firstFAIL: unscoped rollback replaced inherited iRotX helper; recovery01 scoped exact iRotZ occurrence",
    "review discovery firstFAIL duplicate expression uniqueness; zero native executions",
    "initial failed static inspection preserved; accepted static annex zero replay"
  ],
  "producer_accepted": {
    "cpu": 9,
    "math": 9,
    "native_aborts": 38,
    "native_attempts": 291,
    "native_returns": 253,
    "probes": 3,
    "target": 9
  },
  "producer_firstfail": {
    "cpu": 9,
    "math": 9,
    "native_aborts": 26,
    "native_attempts": 255,
    "native_returns": 229,
    "probes": 3,
    "target": 9
  },
  "producer_roots_total": {
    "native_aborts": 64,
    "native_attempts": 546,
    "native_returns": 482,
    "target": 18
  },
  "repair": "six lines: four explicit full32 Z scratch clears plus two unsigned packings with explicit signed32 conversion; private candidate only",
  "review_verdict_sha256": "04f527e7f102cf1c0fe6fa02815658293ad3334c4a04c4c46b0a1addf6f53662",
  "reviewer": {
    "cpu": 9,
    "math": 9,
    "native_aborts": 36,
    "native_attempts": 288,
    "native_returns": 252,
    "target": 9
  },
  "rollback_summary": "four writer rollbacks36 each return36, RAW mismatches12 geometry unchanged; two packing rollbacks36 each return24 abort12, RAW/geometry same among returns; candidate36 GREEN O0/O2 normal/strict RAW2528+Position12",
  "scope": "PRIVATE_SCOPED_APPROVED_NOT_INTEGRATION",
  "stage_counts": {
    "baseline": {
      "UBSanaborts": 12,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 24,
      "raw_mismatches": 24,
      "returns": 24
    },
    "candidate": {
      "UBSanaborts": 0,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 36,
      "raw_mismatches": 0,
      "returns": 36
    },
    "rollback-packing0": {
      "UBSanaborts": 12,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 24,
      "raw_mismatches": 0,
      "returns": 24
    },
    "rollback-packing1": {
      "UBSanaborts": 12,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 24,
      "raw_mismatches": 0,
      "returns": 24
    },
    "rollback-primary-VZ0": {
      "UBSanaborts": 0,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 36,
      "raw_mismatches": 12,
      "returns": 36
    },
    "rollback-primary-VZ1": {
      "UBSanaborts": 0,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 36,
      "raw_mismatches": 12,
      "returns": 36
    },
    "rollback-secondary-VZ0": {
      "UBSanaborts": 0,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 36,
      "raw_mismatches": 12,
      "returns": 36
    },
    "rollback-secondary-VZ1": {
      "UBSanaborts": 0,
      "attempts": 36,
      "position_mismatches": 0,
      "raw_available": 36,
      "raw_mismatches": 12,
      "returns": 36
    }
  },
  "static_annex": {
    "baseline_bodies": 8,
    "candidate_bodies": 20,
    "compiled_storewidths": 32,
    "new_native": 0,
    "verdict_sha256": "bcae7a2fc3d79adcb9d84b7458a7fdc143e7fc8f95c6ec0e63eaf4e95aab4122"
  },
  "strict_verdict": "PASS_FINITE_CASES",
  "ticket": "RE903"
}

## Blockers
integration=false; production_patch=false; public_helpers_green=false. Global FAIL / procédure FAIL.
finite constructed Z nonsaturating callers only; no natural startup, dual stacks, camera, gameplay, GTE hardware, saturation, general axes or universal definedness. CPU/math independent; target bridge shares software LIBGTE. RAW2528+Position12 selected projection, not whole native RAM; aborts have no final projection.
firstFAIL, provider refusal et récupérations immuables distincts. Temps transport parent séparés du clock interne des proofs. Source MATHS publique inchangée. BLOCKED-001/002 supprimés restent supprimés; rapport technique untracked conservé.

## Acceptance
- [x] Types, counts, hashes, mutants non-noop, raw/secret/binary guards.
- [x] Export public-only sans build privé et compatibilité mêmes nodeids baseline.
- [ ] Revue indépendante exacte.
- [ ] Naturalité/hardware/gameplay non prouvés.

## Handoff
RE905: nouvel amont naturel séparément autorisé, pas répétition des contrôles X/Y/Z fermés.
[Metadata](../generated/re904-private-proof-publication-v1.json) · [Tracker](../generated/re904-private-proof-tracker-v1.csv) · [Dashboard](../tomb5-progress-dashboard-re904-v1.html).
