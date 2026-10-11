# RE901 — publication metadata X privée, v1

ARCHIVED; fresh PUBLIC_METADATA_TESTS_ONLY. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.

## Progression
- [x] RED47 générateur absent avant implémentation.
- [x] Verdicts et manifests/seals sélectionnés lus et hashes authentifiés, pas replay privé.
- [x] Schema récursif exact et tracker deux lignes.
- [x] Dashboard append-only et inverse exact deux prédécesseurs.
- [ ] Revue indépendante des hashes publics.
- [ ] Intégration production non autorisée.

## Evidence

### RE899
{
  "caller_returned": true,
  "candidate_sha256": "a9be03a8196e8f73bae09ede0d0aa270ee50cf1d6d0daf91fe8a0103c80610a2",
  "clarification_sha256": "2b30e59ec251669938aa3045b13892b4258a1670cf5bed2ca3f06f8141ba49a5",
  "domain": "constructed authentic packed X primary8192 secondary12288 fractions123 plus zero-axis controls",
  "fullraw_verdict": "FAIL",
  "historical_failures": [
    "FULLRAW four bytes mismatch and strict signed shift abort preserved",
    "historical passed=true with nonempty logic_errors rejected; separate passed=false clarification does not rewrite history"
  ],
  "historical_logic_errors": 2,
  "historical_passed_flag": true,
  "historical_schema_accepted": false,
  "positions": [
    [
      43,
      -28,
      50
    ],
    [
      51,
      -36,
      60
    ],
    [
      60,
      -44,
      70
    ]
  ],
  "producer": {
    "cpu": 9,
    "math": 9,
    "native": 36,
    "target": 9
  },
  "returned_cases": 24,
  "review_verdict_sha256": "813613eca1ac36af0b870aa51808e16b86191789c5f02d65b03f2a3767cb6a26",
  "reviewer_accepted": {
    "cpu": 9,
    "math": 9,
    "native": 36,
    "target": 9
  },
  "reviewer_debugger": 7,
  "scope": "PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL",
  "strict_abort_without_output": 12,
  "strict_verdict": "FAIL",
  "ticket": "RE899",
  "writer_annex_sha256": "0c97d0e57e654bac1fd93de4fb623856bf643057271dbf06840d3c55caae2e7c"
}

### RE900
{
  "baseline_matrix": {
    "attempts": 36,
    "raw_available": 24,
    "returns": 24
  },
  "baseline_sha256": "a9be03a8196e8f73bae09ede0d0aa270ee50cf1d6d0daf91fe8a0103c80610a2",
  "caller_returned": true,
  "candidate_matrix": {
    "attempts": 36,
    "raw_available": 36,
    "returns": 36
  },
  "candidate_sha256": "89999eaaf2818eb5b1073d8c206a8867c56e57a27a5155c8fcf297de08085f0c",
  "first_failure_counts": {
    "native": 147,
    "target": 9
  },
  "fullraw_verdict": "PASS_FINITE",
  "historical_failures": [
    "re900-x-repair sealed immutable: globally ambiguous rollback replacement assertion; candidate GREEN but missing rollback/audit completion. Recovery scope-constrains replacements; dispatcher signatures freshly nm-authenticated as short**, long.",
    "re900-x-repair-recovery sealed immutable: secondary VZ1 rollback candidate RAW is masked naturally by repaired primary full32 predecessor; primary-zero control exposes its 16-bit store. No output masks used. Fresh recovery02 checks this genuine control sensitivity."
  ],
  "private_delta": "five lines: three full32 X writers and two unsigned range-safe packings/sign conversions; no public production patch",
  "producer": {
    "cpu": 9,
    "math": 9,
    "native": 255,
    "target": 9
  },
  "producer_extra_probes": 3,
  "producer_roots_total": {
    "native": 585,
    "target": 27
  },
  "review_verdict_sha256": "0f5a9ac415f2bf759a855a40eeca3e49e5a8764eba4130dcc881af6ba377ab5f",
  "reviewer_accepted": {
    "cpu": 9,
    "math": 9,
    "native": 252,
    "target": 9
  },
  "rollback_matrices": {
    "rollback-packing0": {
      "attempts": 36,
      "raw_available": 24,
      "returns": 24
    },
    "rollback-packing1": {
      "attempts": 36,
      "raw_available": 24,
      "returns": 24
    },
    "rollback-primary-VZ1": {
      "attempts": 36,
      "raw_available": 36,
      "returns": 36
    },
    "rollback-secondary-VZ0": {
      "attempts": 36,
      "raw_available": 36,
      "returns": 36
    },
    "rollback-secondary-VZ1": {
      "attempts": 36,
      "raw_available": 36,
      "returns": 36
    }
  },
  "rollback_scope": "five classes36 each: writers RAW-only; packings sanitizer-only; secondary VZ1 masked by primary full32, primary-zero control discriminates; no output masks",
  "scope": "PASS_PRIVATE_FINITE_FULLRAW_STRICT_REPAIR",
  "second_failure_counts": {
    "native": 183,
    "target": 9
  },
  "strict_verdict": "PASS_FINITE",
  "ticket": "RE900",
  "width_annex": {
    "new_native": 0,
    "static_bodies": 16,
    "writer_checks": 32
  },
  "width_annex_sha256": "074fa8b114eda83ad765e66cc3b1f18249b2a42961b8592480a18497210ace8d"
}

## Blockers
integration=false; production_patch=false; public_helpers_green=false. Global FAIL / procédure FAIL.
finite constructed nonzero X and zero controls only; no natural startup, dual stacks, camera, general axes, saturation, portable ABI, GTE hardware or gameplay proof. Shared actual software LIBGTE is not hardware; independent CPU/math nonsaturating. RAW2528+Position12 is a selected projection, not whole native RAM.
RE899 historical passed=true/logic_errors rejeté, clarification distincte, FULLRAW/strict FAIL immuables. RE900 firstFAILs préservés; accepté9/255 vs total27/585; reviewer9/252. Source MATHS publique inchangée. BLOCKED-001/002 supprimés restent supprimés; rapport technique untracked conservé.

## Acceptance
- [x] Types bool/int, counts, pins, frontières et unknown keys discriminés.
- [x] Raw/secret/binary guards avec même chemin bénin.
- [x] Export public-only sans build privé.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW, auteur non reviewer.
- [ ] Naturalité/hardware/gameplay non prouvés.

## Handoff
RE902: natural upstream OU packed Z nouveau; ne pas répéter closed Y/X controls, autorisation séparée.
[Metadata](../generated/re901-private-proof-publication-v1.json) · [Tracker](../generated/re901-private-proof-tracker-v1.csv) · [Dashboard](../tomb5-progress-dashboard-re901-v1.html).
