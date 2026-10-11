# RE921 — publication metadata de la continuation OpenBIOS RE920

## Progression
- [x] Inventaires complets producteur76 / reviewer3174 / firstFAIL1573 authentifiés.
- [x] TDD RED avant générateur ; aucune nouvelle exécution cible/native.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.

## Evidence
PCSX-Redux / nugget OpenBIOS complet MIT inchangé compilé GCC MIPSel. Enveloppe ABI/RAM construite : copyDataAndInitializeBSS → copyA0table → installKernelHandlers → exec → entrée SLUS authentique → SW RA → user_initheap retourné naturellement. Pas de hook retour BIOS/SDK ni secteur injecté. Un positif1976489visites et une ablation machine1976497 pour chacun producteur/reviewer ; six rejets JSON et sept méthodes sémantiques, pas sept exécutions. B0 fallback peut revenir sans sémantique A0. Oracle CPU indépendant reconstruit depuis ISO : RAM entière2097152octets,32GPR,1976489visites orderedPC. ROM identique sauf20octets GNUbuildID, tous les autres octets identiques ; enveloppe identique. Visites pas instructions retirées. Aucun source tiers redistribué.

## Blockers
OPENBIOS_REPLACEMENT_NOT_SONY_BIOS ; Sony RA UNKNOWN. Frontière I_MASK écriture16bits tentée NONretirée. Aucun modèle MMIO ou secteur succès fabriqué. Natural reset/full boot/CD/hardware/gameplay/integration=false ; contexte ABI et RAM initial construit, modèle loads immédiats et branch delay slots, pas certification R3000. Global FAIL/procedure FAIL historiques maintenus. firstFAIL ROMidentity reviewer, mirror/BFD/negative producer et original INCOMPLETE1608 sans seal final préservés ; aucune réhabilitation. BLOCKED-001/002 suppressions utilisateur, report-tech, cache, assets/cold archives/seals/firstFAIL et RE893partial intacts.

## Acceptance
- [x] Schéma exact récursif types/valeurs/counts/pins, inconnus rejetés.
- [x] Guards raw/secret/binary avec benign même chemin.
- [x] Story/tracker/evidence/blockers et dashboards suffixe exact ; inverse reconstitue chaque prédécesseur sans modifier ses hashes.
- [ ] Revue indépendante exacte des hashes PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; tests publication ne valent pas intégration.

Aucune production modifiée, aucun job/successeur lancé. Suite complète non rejouée ; compatibilité collection explicitement inventoriée. Prochaine hypothèse RE922 interrupt/MMIO depuis références libres vers startup/CD, non exécutée ici.

{
  "RE920": {
    "B0_fallback_return_permitted": true,
    "BIOS_SDK_return_doubles": false,
    "CD_proof": false,
    "CPU_model": "immediate loads branch delay slots coherent four RAM mirrors software only",
    "Sony_RA": "UNKNOWN",
    "accepted_scope": "PRIVATE_COMPILED_OPENBIOS_STARTUP_A0_39_PREFIX",
    "execution_order": [
      "copyDataAndInitializeBSS",
      "copyA0table",
      "installKernelHandlers",
      "exec",
      "authentic SLUS entry",
      "SW RA",
      "user_initheap natural return"
    ],
    "frontier": "I_MASK 16-bit write attempted nonretired",
    "gameplay_proof": false,
    "hardware_proof": false,
    "initial_state": "constructed ABI and RAM; reviewer reconstructed from ISO",
    "injected_sectors": false,
    "natural_full_boot": false,
    "natural_reset": false,
    "producer": {
      "ablation_visits": 1976497,
      "actual_machine_ablations": 1,
      "input_pins_verified": 22,
      "positive_prefixes": 1,
      "positive_visits": 1976489,
      "semantic_JSON_rejections": 6,
      "semantic_test_methods": 7,
      "source_files_verified": 1384
    },
    "reviewer": {
      "GNU_build_ID_bytes_excluded": 20,
      "ablation_visits": 1976497,
      "actual_machine_ablations": 1,
      "all_other_ROM_bytes_identical": true,
      "concerns": [],
      "envelope_identical": true,
      "fresh_full_rom_identity": false,
      "gpr_compared": 32,
      "independent_interpreter_prefixes": 1,
      "ordered_pc_compared": 1976489,
      "positive_prefixes": 1,
      "positive_visits": 1976489,
      "rom_identity_except_GNU_build_ID": true,
      "whole_ram_bytes_compared": 2097152
    }
  },
  "attribution": {
    "copyright": [
      "Copyright (c) 2025 PCSX-Redux authors"
    ],
    "license": "MIT",
    "nugget_commit": "7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30",
    "project": "PCSX-Redux / nugget OpenBIOS",
    "redistributed_source": false,
    "redux_commit": "c313b116e6a55786bc127c9b3a07a90b55d97c21",
    "reference_pins": {
      "src/core/psxhw.cc": {
        "bytes": 35035,
        "sha256": "db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de"
      },
      "src/core/psxmem.h": {
        "bytes": 14765,
        "sha256": "9e5658aeeef2f01af73a80f892f5e345fadee35c83d2f220daeafb40409fe6a0"
      },
      "src/mips/openbios/kernel/alloc.c": {
        "bytes": 12356,
        "sha256": "88cb79e09ab9f7a7eff8f700d496ae4c473372ac2be9b0546c47a410c710061d"
      },
      "src/mips/openbios/kernel/handlers.c": {
        "bytes": 15987,
        "sha256": "a5c97ce2e554ef07ba40e3e69c31d9fc7da328e4edcd5cc02f92a8f69bccadd3"
      }
    },
    "source_url": "https://github.com/pcsx-redux/nugget/blob/7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30/openbios/kernel/alloc.c",
    "sources_unchanged": true
  },
  "authentication": {
    "re920-recovery01": {
      "entries": 76,
      "manifest_schema": "re920.recovery.inventory.v1",
      "manifest_sha256": "3560d82679ee9f0b7a6af003a6622f2540ad0a76e7eb02b82789f570c0305c0f",
      "seal_file_sha256": "e75abaf22a27198200251c9edd3f1b1ad156b32b27249828b91f64ed6c992f61",
      "seal_schema": "re920.recovery.seal.v1",
      "verdict_sha256": "95801b85eeba70366c91d3afc1398389dfd415d5c4abec023e225b3c4ab27f9d"
    },
    "re920-review": {
      "entries": 3174,
      "manifest_schema": "re920.review.inventory.v1",
      "manifest_sha256": "3f609ed8dff3f217ff0f37f4ea8f14a5ff33714d823958742335ad15c5a69510",
      "seal_file_sha256": "3a2d500c9ffcf1654b4568f4b17374a0351d58a38e735a363e76584a68e96548",
      "seal_schema": "re920.review.seal.v1",
      "verdict_sha256": "053adc87274f9e6cb7380abef53e92d51fa9d2e436cfb7b7ef0d2484adce3bbc"
    },
    "re920-review/attempt01": {
      "entries": 1573,
      "manifest_schema": "re920.review.inventory.v1",
      "manifest_sha256": "72cd4ceb41065708cf146eb81c87f3353a9231e988371a3da04d31279c622e75",
      "seal_file_sha256": "50ea7d4a68b2d2263b92bcb836e5361a33e50beac1b1bc799736724ac47dc915",
      "seal_schema": "re920.review.seal.v1",
      "verdict_sha256": "e15bd6f3c5acd86a69774b1b705e1f805d32ce5d6a1f2c1f0a61c24cc0854d23"
    }
  },
  "authentication_scope": "Fresh full inventories and nested firstFAIL authenticated; no numerical replay",
  "backend_boundary": "OPENBIOS_REPLACEMENT_NOT_SONY_BIOS",
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "global_scope": "FAIL",
  "historical": {
    "BFD_format_FAIL": true,
    "RE893_partial_preserved": true,
    "first_reviewer_ROM_identity_FAIL": true,
    "global_procedure_FAIL_retained": true,
    "incorrect_negative_FAIL": true,
    "initial_mirror_FAIL": true,
    "original_incomplete_members": 1608,
    "original_no_final_seal": true
  },
  "integration": false,
  "naturalcaller": "BLOCKED",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_EXACT_HASH_REVIEW",
  "schema": "re921-openbios-continuation-proof-publication-v1"
}
