# RE919 — publication fidèle de la preuve exécutable OpenBIOS RE918

## Progression
- [x] RE918 privé accepté et inventaires producteur92 / reviewer92 authentifiés.
- [x] Publication metadata TDD RED avant générateur, ZERO nouvelle exécution cible/native.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW ; worktree-only, aucun stage/commit/push.

## Evidence
PCSX-Redux / nugget OpenBIOS, source MIT psxexec.s inchangée compilée ELF MIPS-I. Attribution source et pins ci-dessous ; aucun source tiers redistribué. Quatre aller-retours ABI synthétiques et quatre mutants exécutés par producteur et reviewer fresh. Une entrée authentique positive et un mutant link chacun, pas deux positives. Caller construit → backend compilé → véritable entrée jeu → SW RA via AT exécuté, arrêt immédiatement suivant. 1778397 visites ordonnées, RAM entière2097152 octets,32GPR comparés à un oracle stdlib indépendant reconstruit depuis ISO ; aucune nouvelle replay RE919.

## Blockers
OPENBIOS_REPLACEMENT_NOT_SONY_BIOS : RA Sony UNKNOWN. Backend de remplacement, caller et contexte initial construits. Pas de full natural boot, retour SDK positif, secteur CD succès, gameplay, hardware ni intégration. Unicorn MIPS32 avec loads immédiats, pas certification load-delay R3000. Quatre fixtures finies, pas totalité ABI ; RETURN synthétique n'est pas retour jeu. Global FAIL/procedure FAIL/integration=false. firstFAIL KSEG API producteur et BOOT parser reviewer préservés, retries distincts ; FAIL historiques non réhabilités. BLOCKED-001/002 suppressions utilisateur, report-tech, cache, assets et archives froides préservés ; firstFAIL893 intact.

## Acceptance
- [x] Schéma récursif exact types/valeurs/counts/timing/pins et inconnus rejetés.
- [x] Guards contenu brut/secret/binaire avec benign sur même chemin admis.
- [x] Story/tracker/evidence/blockers et dashboard versionné à suffixe exact ; inverse restitue prédécesseur byte-identique, sans réécriture de ses hashes.
- [ ] Revue indépendante des hashes publics finaux ; metadata GREEN ne vaut pas intégration.

## Restant à faire
Continuer explicitement depuis ce backend de remplacement vers startup/CD sans oracle hardware imaginaire ni secteur/SDK positif fabriqué ; provenance Sony et boot complet restent ouverts.

{
  "RE918": {
    "accepted_scope": "PRIVATE_OPENBIOS_ROUNDTRIP_AND_AUTHENTIC_GAME_RA_SAVE",
    "firstFAIL": [
      "Producer KSEG API physical-memory access error preserved; retry keeps CPU KSEG addresses.",
      "Reviewer BOOT parser firstFAIL preserved; corrected parser retry distinct.",
      "Historical global/procedure FAIL not rehabilitated."
    ],
    "frontier": "Constructed ABI caller -> unchanged MIT exec assembled ELF MIPS-I -> authentic game entry -> SW RA via AT executed -> immediate stop. Replacement backend RA, not Sony RA.",
    "limits": [
      "Four synthetic ABI domains: BSS empty/nonempty and selected/unselected stack; not complete ABI.",
      "Each game_entry_prefixes=2 means ONE positive and ONE actual link mutant, not two positives.",
      "Independent CPU positive counts are separate comparisons, not extra game target positives.",
      "Constructed BIOS caller and initial RAM outside payload; no natural full boot, SDK return, CD success sector, gameplay or integration.",
      "MIPS32 Unicorn immediate loads; no R3000 load-delay certification.",
      "Synthetic RETURN fixture is not game return; real game stop immediately after RA store."
    ],
    "oracle": "Independent stdlib reconstruction from ISO and fresh binaries; full ordered visits, final RAM and32GPR. Software comparison, not hardware.",
    "producer": {
      "code_mutants_rejected": 4,
      "game_code_mutants_rejected": 1,
      "game_entry_prefixes": 2,
      "game_mutant_target_visits": 1778397,
      "game_positive_prefixes": 1,
      "game_target_visits": 1778397,
      "gpr_compared": 32,
      "independent_game_cpu_prefixes": 1,
      "roundtrips": 4,
      "whole_ram_bytes_compared": 2097152
    },
    "reviewer": {
      "code_mutants_rejected": 4,
      "game_code_mutants_rejected": 1,
      "game_entry_prefixes": 2,
      "game_mutant_target_visits": 1778397,
      "game_positive_prefixes": 1,
      "game_target_visits": 1778397,
      "gpr_compared": 32,
      "independent_game_cpu_prefixes": 1,
      "roundtrips": 4,
      "whole_ram_bytes_compared": 2097152
    },
    "timing": {
      "producer_game_seconds": 5.583026170730591,
      "reviewer_closure_seconds": 328.76693964004517
    }
  },
  "attribution": {
    "copyright": [
      "Copyright (c) 2020 PCSX-Redux authors"
    ],
    "license": "MIT",
    "nugget_commit": "7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30",
    "project": "PCSX-Redux / nugget OpenBIOS",
    "redistributed_source": false,
    "redux_commit": "c313b116e6a55786bc127c9b3a07a90b55d97c21",
    "source_path": "src/mips/openbios/kernel/psxexec.s",
    "source_sha256": "baa154b1eb86343f1fd468b17f46dab155fb836e023ca2d4eeedce2c3c73ef8c",
    "source_unchanged": true,
    "source_url": "https://github.com/pcsx-redux/nugget/blob/7ffc2b14b3ec4b912e7e79f6e31101ff3f24cc30/openbios/kernel/psxexec.s"
  },
  "authentication": {
    "re918-openbios": {
      "entries": 92,
      "manifest_sha256": "093dc01dadd97038aef080264f77aac05e1607d2ca3bbb07330a4f78e912142a",
      "seal_file_sha256": "a47cb98851a0e28b9da66f8a097158f82bd26fed03ddb936856985e0e38ba591",
      "verdict_sha256": "342348ea06fa915a2f1a78e0f5350178f53c452cb5f290b0fe529b7218e3f46a"
    },
    "re918-review": {
      "entries": 92,
      "manifest_sha256": "09095261de2d785f41787f8ef93d214cbdf83300b64459c9b867b5744f605d9e",
      "seal_file_sha256": "dfac3c0fa6b4f24add8273edccf8975fa2f851ad3388672ad207a1c1160a0d70",
      "verdict_sha256": "f6f2321435d75b9ef95c9243b123f83f877d1903ffbbd48318eb365aceea336d"
    }
  },
  "authentication_scope": "Publisher freshly authenticated both complete private92-member inventories; parent earlier verified same roots. No numerical replay.",
  "backend_boundary": "OPENBIOS_REPLACEMENT_NOT_SONY_BIOS",
  "fresh_execution_scope": "PUBLIC_METADATA_TESTS_ONLY",
  "fresh_native": 0,
  "fresh_target": 0,
  "global_scope": "FAIL",
  "integration": false,
  "naturalcaller": "BLOCKED",
  "procedure_scope": "FAIL",
  "production_patch": false,
  "publication_review": "PENDING_INDEPENDENT_EXACT_HASH_REVIEW",
  "schema": "re919-openbios-executable-proof-publication-v1"
}
