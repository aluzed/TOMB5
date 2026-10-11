# RE906 — publication sûre RE905 metadata-only

## Progression
- [x] RED discriminant avant générateur, GREEN metadata seulement.
- [x] Seals/verdicts sélectionnés authentifiés; inventories parent, pas replay frais.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW.

## Evidence
{
  "archived_loader_inputs": {
    "RE853": 49,
    "RE855": 62,
    "fresh_loaders": 0,
    "manifest_entries_total": 111
  },
  "authentication": {
    "re905-review": {
      "manifest_entries": 55,
      "manifest_sha256": "5371df70d8a630be4615432d20cdaab64776014fafb61b379d21ca75419de1b4",
      "seal_sha256": "af2e8dea14ae23f2ed2a9dbd236aab967cfd6d4af72e9fbef24def42616d9067",
      "verdict_sha256": "17c4841d7be2b7ff453d83b82e4e61063ecf5782530efc9f1a3dfa6ad0d0227c"
    },
    "re905-upstream-provenance": {
      "manifest_entries": 50,
      "manifest_sha256": "dd1aa0c3d0f868d8b56422c10af59a16bc1991fecf0ed62ffdbf564dc17a700a",
      "seal_sha256": "7eba768c655c3cfe59cc95611766d0e9154332465ff79db1a79474e89a28f0db",
      "verdict_sha256": "8f371b405acbee95125df9cc8925e959fa08341f8a0a14844d8186e45223df8c"
    }
  },
  "consumer": {
    "bytes_each": 20,
    "fraction": 0,
    "frame_size": 10,
    "frame_windows": 2,
    "kind": "explicit constructed arguments and return frontier in retained CPU/RAM; not natural caller",
    "rate": 1
  },
  "failures": [
    "initial insensitive frame-store NOP: frame0 already framebase0; retained and replaced by distinct sensitive mutant",
    "producer and reviewer UC_ERR_EXCEPTION memory-write-hook failures retained; retry without hook; cause not diagnosed",
    "two parent read-only schema failures retained; not technical results"
  ],
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "global_scope": "FAIL",
  "integration": false,
  "limits": "archived loader inputs, fresh prefix normal-only; selected projection independent oracle, not whole RAM; zero native InitialiseItem return; no ASan/UBSan, natural caller, GetJointAbsPosition, startup, gameplay, hardware or global equivalence.",
  "naturalcaller": "BLOCKED",
  "next_objective": "real object284 registration/relocation then InitialiseItem continuation AddActiveItem room/floor/callback; ControlBlinker pos.x unassigned is unsafe hypothesis, not activation",
  "next_ticket": "RE907",
  "normal_only": true,
  "prefix": {
    "animation": 578,
    "frame": 0,
    "item": 128,
    "native_build": "whole actual ITEMS.C i386 O0 normal",
    "native_projection_bytes": 144,
    "object": 284,
    "stop": "before first suffix write; no InitialiseItem return"
  },
  "procedure_scope": "FAIL",
  "producer": {
    "GetFrames_returns": 1,
    "GetJointAbsPosition_calls": 0,
    "accepted_prefixes": 4,
    "initial_failed_prefixes": 3,
    "native_prefixes": 1,
    "native_returns": 0,
    "sensitive_mutants": 2,
    "target_prefixes": 7,
    "unmodified_prefixes": 2
  },
  "production_patch": false,
  "public_helpers_green": false,
  "publication_review": "PENDING_INDEPENDENT_EXACT_HASH_REVIEW",
  "reviewer": {
    "GetFrames_returns": 1,
    "GetJointAbsPosition_calls": 0,
    "accepted_prefixes": 4,
    "failed_consumer_prefixes": 2,
    "native_prefixes": 1,
    "native_returns": 0,
    "sensitive_mutants": 2,
    "target_prefixes": 6
  },
  "schema": "re906-upstream-prefix-publication-v1",
  "strict_sanitizers_executed": false
}

## Blockers
integration=false; global FAIL / procédure FAIL; naturalcaller BLOCKED.
firstFAIL et retries immuables: causalité hook non diagnostiquée. Animation antérieure0 incompatible corrigée par préfixe authentique578, pas activation source.
BLOCKED-001/002 restent supprimés, rapport technique untracked conservé.

## Acceptance
- [x] Schéma exact types/comptes/hash, inverse append RE904 strict.
- [x] Gardes contenu/path sur même chemin permis, export public-only.
- [ ] Revue indépendante exacte publique.
- [ ] Naturalité, suffixe InitialiseItem, sanitizers et équivalence globale non prouvés.

## Handoff
real object284 registration/relocation then InitialiseItem continuation AddActiveItem room/floor/callback; ControlBlinker pos.x unassigned is unsafe hypothesis, not activation
