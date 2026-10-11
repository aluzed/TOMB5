# RE925 — publication metadata DMA RE924

## Progression
- [x] Preuves privées archivées authentifiées : ensembles exacts85/70/7, tailles/SHA/seals.
- [x] TDD RED puis GREEN metadata canonical/public-only, zéro replay numérique.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, pas stage/commit/push.

## Evidence
RE924-PCSX-Redux-DPCR-DICR-subset : DPCR réellement franchi, retours A0:13/B0:19, arrêt AVANT Timer1 MODE write32 non complété. 1980769 instructions complétées/1980770 visites ; +4274 depuis RE922, reprise4274/4275. Observation du hook suivant, pas retraite microarchitecture. RAM entière2097152octets,32GPR, PC/MMIO ordonnés concordent avec decoder reviewer frais indépendant. Producteur11méthodes,45comparaisons DICR; reviewer45 +2048semées,54width/alias,4refus atomiques. DICR construit seulement, jamais traversé naturellement. Publication ajoute ZERO target/native/replay. Witness extrait/adapté GPL-2.0-or-later, pas émulateur complet; ROM OpenBIOS MIT réutilisée, pas compilation firmware fraîche. Copyright (C) 2023 PCSX-Redux authors pour psxhw.cc et psxmem.h ; URLs/digests explicites dans metadata. Aucune source tierce redistribuée.

## Reviewhistory
Original verdict passed=false, deux concerns : REJECTED inchangé. Clarification01 distincte SCOPED_PASS_ARCHIVE_ONLY, strict passed=true/errors=[]/concerns=[], ZERO nouvelle exécution. Concerns originales et limitations conservées intégralement. firstFAIL producteur, reviewer import et decoder initial inutilisé erroné retenus ; corrigés dans invocations distinctes, aucun rejet rétrocertifié.

## Blockers
ABI/RAM/caller construits, loads immédiats et quatre miroirs RAM, pas load-delay/cache. Aucun transfert DMA/scheduling/completion, événements timer, IRQ active/exception, reset naturel/Sony, secteurs CD, hardware/gameplay/intégration prouvés. Global FAIL/procedure FAIL maintenus ; integration=false. BLOCKED-001/002 restent supprimés selon volonté utilisateur, non restaurés. Aucun patch production.

## Acceptance
Authentification documentaire et tests publics seulement, pas numerical replay. Export sans build/private dependency. Compatibility baseline/current/export même collection et mêmes nodeids des deux FAIL historiques RE830, non affaiblis. Dashboard suffix exact réversible sur bytes prédécesseurs RE923 ; guards raw/secret/binary et allowlist explicite. Livraison worktree-only ; revue indépendante exact-hash PENDING_INDEPENDENT_EXACT_HASH_REVIEW.

{
  "archived_counts": {
    "additional_completed": 4274,
    "gpr": 32,
    "mmio_attempts": 5,
    "ordered_pc": 1980770,
    "producer_DICR_comparisons": 45,
    "producer_methods": 11,
    "resume_completed": 4274,
    "resume_visits": 4275,
    "retired": 1980769,
    "reviewer_DICR_comparisons": 45,
    "reviewer_atomic_rejections": 4,
    "reviewer_seeded_comparisons": 2048,
    "reviewer_width_alias_cases": 54,
    "supported_dma": 1,
    "supported_mmio": 4,
    "visits": 1980770,
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
        "copyright": "Copyright (C) 2023 PCSX-Redux authors",
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxhw.cc",
        "sha256": "db7fbff756774848150fa1acf0e7c04c3bd2c5a87e3b4aacffcacd88e21388de",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxhw.cc"
      },
      {
        "copyright": "Copyright (C) 2023 PCSX-Redux authors",
        "license": "GPL-2.0-or-later",
        "path": "src/core/psxmem.h",
        "sha256": "9e5658aeeef2f01af73a80f892f5e345fadee35c83d2f220daeafb40409fe6a0",
        "url": "https://github.com/grumpycoders/pcsx-redux/blob/c313b116e6a55786bc127c9b3a07a90b55d97c21/src/core/psxmem.h"
      }
    ],
    "third_party_source_redistributed": false
  },
  "authentication": {
    "re924-dma-mmio": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "c425623ea296d3700c125d8cbe0adc104f7694ae13f04c0ed6c9f1417fcc464a",
      "members": 85,
      "seal_sha256": "fab8b8b58f8312cc1578701ab1803a79610a1398846b083b822896e74f516a56",
      "verdict_sha256": "820e97617b44de7b83797d2a006d88b8d7591f95f80d29b29fd719bffc34e3ee"
    },
    "re924-review": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "555c64baa95f28115235e5b5a9b73a0a65e8998531b39b00f45293f28769d823",
      "members": 70,
      "seal_sha256": "a99abe186b996e5cad9acd8e09c96b4b878f985aecdc9e2800c8c61ffd79bd77",
      "verdict_sha256": "561a877c4ab57ddd94979db3f090ffcc5799578f0f8abe437f25171808246c72"
    },
    "re924-review-scope-clarification01": {
      "exactset_all_sizes_hashes": true,
      "manifest_sha256": "8ef0f29125e4306d196d1e664576df7610b1f85c04a9afa3de8851dfcabb4e11",
      "members": 7,
      "seal_sha256": "39e44a8df73d8d757f1a9ffc3dfdff2ef6cbe4cc12a256606b450973b4e28b45",
      "verdict_sha256": "b97f3ae3194b1a7a141f14e7b2351a4574e3d9dd9c513bad0260d3994b0ec23c"
    }
  },
  "backend_boundary": "RE924-PCSX-Redux-DPCR-DICR-subset",
  "dicr_natural": false,
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "frontier": "SDK_TIMER1_MODE_write32_BEFORE_EFFECT",
  "global_scope": "FAIL",
  "integration": false,
  "limitations": [
    "natural reset boot",
    "hardware equivalence",
    "DMA channel transfers/scheduling",
    "active CPU exception delivery",
    "load delays/cache",
    "timer semantics after stopping frontier",
    "CD sectors",
    "gameplay",
    "production integration",
    "DICR seulement construit; jamais travers\u00e9 naturellement",
    "ROM r\u00e9utilis\u00e9e, aucun build firmware frais",
    "witness extrait/adapt\u00e9, pas build complet PCSX-Redux",
    "ABI/RAM/caller construits; pas boot reset naturel",
    "comparaisons ind\u00e9pendantes du trajet, pas preuve universelle du decoder ni de toutes branches",
    "aucune certification exhaustive des d\u00e9couvertes/transactions historiques",
    "aucune publication, mutation git, jobs ou production"
  ],
  "naturalcaller": "BLOCKED",
  "oracle": "fresh independent reviewer decoder full RAM/GPR/ordered PC/MMIO; finite software not hardware",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_EXACT_HASH_REVIEW",
  "retirement": "previous instruction completed at next code hook; not microarchitectural retirement",
  "returned_services": [
    "A0:13",
    "B0:19"
  ],
  "review_history": {
    "clarification01": "SCOPED_PASS_ARCHIVE_ONLY",
    "clarification_new_replays": 0,
    "firstFAIL": "producer tests and reviewer import/decoder failures retained, corrected invocations distinct",
    "original": "REJECTED",
    "original_concerns": [
      "Incidents reviewer conserv\u00e9s : import initial FAIL corrig\u00e9 par invocation distincte; branche DICR inutilis\u00e9e du decoder initial rejet\u00e9e puis corrig\u00e9e et r\u00e9ex\u00e9cut\u00e9e distinctement. Aucun rejet initial r\u00e9trocertifi\u00e9.",
      "Proc\u00e9dure globale historique FAIL conserv\u00e9e : incidents ant\u00e9rieurs et discovery-ledger non exhaustif ne sont pas r\u00e9trocertifi\u00e9s par cette revue fra\u00eeche."
    ],
    "original_passed": false
  },
  "rom_fresh_build": false,
  "schema": "re925-dma-proof-publication-v1"
}
