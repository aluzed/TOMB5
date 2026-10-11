# RE898 — publication metadata privée nonzero, v1

ARCHIVED; fresh PUBLIC_METADATA_TESTS_ONLY. PENDING_INDEPENDENT_EXACT_HASH_REVIEW.

## Progression
- [x] RED frais générateur absent avant implémentation.
- [x] Verdicts archivés indépendants lus, hashes vérifiés; pas de nouveaux replays privés.
- [x] Schéma exact récursif et fixtures publiques déterministes; tracker trois lignes.
- [x] Dashboard maintenu append-only et versionné, inverse exact prédécesseur.
- [ ] Revue indépendante des hashes publics exacts.
- [ ] Intégration production distincte, non autorisée.

## Evidence

### RE895 — PASS_PRIVATE_FINITE_DIRECT_INTERPOLATEMATRIX
{
  "callee_returned": true,
  "caller_returned": false,
  "candidate_sha256": "22940da9716976618ed031853f59c0044b04fa8d373aff2fab0c187fc762ec51",
  "domain": "one constructed nonorthonormal unequal signed pair; fractions1/2/3 rate4",
  "fullraw_verdict": "PASS_FINITE",
  "gte_commands": 0,
  "historical_failures": [
    "provider refusal after discovery/bootstrap: zero execution, distinct from actual 5.316s driver",
    "historical unledgered discovery retained",
    "inherited caller/bridge labels wrong; callee returned, NOT caller"
  ],
  "manifest_entries": 261,
  "native_matrix": {
    "baseline_red": 6,
    "candidate_green": 6,
    "noop_red": 6,
    "rollback_green": 4,
    "rollback_red": 2
  },
  "private_delta": "one full32 assignment; nine rotation expressions sensitive; no public source patch",
  "producer": {
    "cpu": 3,
    "math": 3,
    "native": 24,
    "target": 3
  },
  "review_verdict_sha256": "c62e45e752532018fd2a52a58d8abd03b6f3bd09e4d5d44066a32bf1e32473d5",
  "reviewer_accepted": {
    "cpu": 3,
    "math": 3,
    "native": 24,
    "target": 3
  },
  "scope": "PASS_PRIVATE_FINITE_DIRECT_INTERPOLATEMATRIX",
  "ticket": "RE895"
}

### RE896 — PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL
{
  "callee_returned": true,
  "caller_returned": true,
  "candidate_sha256": "22940da9716976618ed031853f59c0044b04fa8d373aff2fab0c187fc762ec51",
  "domain": "constructed real GetJointAbsPosition packed unequal nonzero Y using authentic table; fractions1/2/3",
  "fullraw_verdict": "FAIL_FOUR_BYTES",
  "geometry": "PASS, three positions sensitive to primary and secondary ablations",
  "historical_failures": [
    "first producer fullraw FAIL remains immutable",
    "initial reviewer math oracle FAIL and finalizer/header-only attempts preserved",
    "characterization PASS is NOT strict code approval; FULLRAW FAIL retained"
  ],
  "last_writer": "secondary iRotY dynamically attributed; target full32 versus native16 stores",
  "manifest_entries": 246,
  "positions": [
    [
      26,
      -35,
      35
    ],
    [
      31,
      -43,
      44
    ],
    [
      36,
      -50,
      53
    ]
  ],
  "producer": {
    "cpu": 6,
    "math": 3,
    "native": 18,
    "target": 3
  },
  "review_manifest_entries": 250,
  "review_verdict_sha256": "72ed116273e8c2b030e971c4a1bf0f93ac2b07cf7066a2114eb6e4a298a3d18c",
  "reviewer_accepted": {
    "cpu": 3,
    "native": 6,
    "target": 3
  },
  "reviewer_debugger": {
    "native": 7
  },
  "reviewer_initial": {
    "cpu": 3,
    "native": 3,
    "target": 3
  },
  "reviewer_total": {
    "cpu": 6,
    "native": 16,
    "target": 6
  },
  "scope": "PASS_FINITE_CHARACTERIZATION_NOT_STRICT_CODE_APPROVAL",
  "ticket": "RE896"
}

### RE897 — PASS_FINITE_FULLRAW_REPAIR
{
  "audit_additional": {
    "native": 0,
    "target": 0
  },
  "audit_manifest_entries": 50,
  "audit_verdict_sha256": "4b1484555cd6b804ada4ccc0dacddf8b0035b77e89735b856fd3b5ab7b3849bf",
  "callee_returned": true,
  "caller_returned": true,
  "candidate_sha256": "a9be03a8196e8f73bae09ede0d0aa270ee50cf1d6d0daf91fe8a0103c80610a2",
  "domain": "two finite constructed Y caller domains, i386 O0/O2 normal and strict; not natural",
  "fullraw_verdict": "PASS_FINITE",
  "historical_failures": [
    "first producer math decode FAIL:3 target/3 CPU/0 native;47 inventory entries",
    "first reviewer setup FAIL:zero execution;6 inventory entries",
    "RE896 historical FULLRAW FAIL never overwritten by later repair"
  ],
  "manifest_entries": 535,
  "native_matrix": {
    "baseline_red": 12,
    "candidate_green": 24,
    "rollback_first": 12,
    "rollback_second": 12
  },
  "private_delta": "two explicit signed full32 register-member writes; inherited RE895 pointer cast remains private",
  "producer": {
    "cpu": 6,
    "math": 6,
    "native": 60,
    "target": 6
  },
  "review_manifest_entries": 539,
  "review_verdict_sha256": "1dcd2e05ad1603f7dbd80fc9b84643d6799cda14e3d912314fd75a5a4951a419",
  "reviewer_accepted": {
    "cpu": 6,
    "math": 6,
    "native": 60,
    "target": 6
  },
  "rollback_scope": "RAW-only sensitivity; geometry unchanged, not geometric ablation proof",
  "scope": "PASS_FINITE_FULLRAW_REPAIR",
  "ticket": "RE897"
}

Les comptes producteur/reviewer sont archivés, distincts des tests publics RE898. RE896 total inclut initial3 target/3 CPU/3 native et debugger7 native; accepté3/3/6 seulement. RE897 audit ajoute zéro replay. RE896 FULLRAW FAIL quatre bytes immuable, caractérisation géométrie PASS seulement.

## Blockers
integration=false; production_patch=false; public_helpers_green=false. Global FAIL / procédure historique FAIL.
constructed finite i386 domains only; shared actual target/native LIBGTE software is not hardware; independent CPU/math not saturation; no natural upstream, general axes, portable ABI, gameplay or hardware proof. FULLRAW2528 is a projection, not whole native RAM. O2 accepted only for RE897 finite domain, not global pointer-cast portability.
Public MATHS inchangé, ancien mRotY seulement; GetSpheres stub, helpers privés non intégrés. Inherited wrong caller/bridge labels RE895 explicitement qualifiés. Premiers FAIL producteur et reviewer conservés; aucun seal rétrocertifié. BLOCKED-001/002 supprimés par utilisateur restent supprimés, rapport technique untracked conservé. Aucun screenshot runtime ni nouvelle compilation cible/native.

## Acceptance
- [x] Types stricts bool/int, drift hash/count/frontière et champs inconnus rejetés.
- [x] Secrets, raw tokens, chemins hors scope et heavy assets rejetés avec contrôles bénins.
- [x] Export public-only sans dépendance proof ignorée.
- [x] Inverse exact maintenu et RE894, bytes historiques non normalisés.
- [ ] PENDING_INDEPENDENT_EXACT_HASH_REVIEW: auteur non reviewer.
- [ ] GREEN global, gameplay/hardware/saturation/naturalité non revendiqués.

## Handoff
RE899: provenance naturelle upstream OU nouvel axe géométriquement sensible; autorisation et revue séparées, ne pas répéter matrices Y fermées.
[Metadata](../generated/re898-private-proof-publication-v1.json) · [Tracker](../generated/re898-private-proof-tracker-v1.csv) · [Dashboard](../tomb5-progress-dashboard-re898-v1.html).
