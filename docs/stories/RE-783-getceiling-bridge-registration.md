# RE-783 — Contrat consommateur GetCeiling et registration des bridges (adaptation bornée)

Statut : **correction source + composition validées BORNÉES — publication/fusion PENDING**.
Date : 28 septembre 2026. Branche `re/blocked-001-deepseek`, baseline `a10b06bb`.
Parent : BLOCKED-001 ; suite de RE-781/RE-782. Aucun raw/adresse cible dans ce document public.

## Tracker
- [x] Contrat consommateur cible authentifié dynamiquement (128 cas / 128 callbacks, vrais corps
  BridgeFlatCeiling/BridgeTilt1Ceiling/BridgeTilt2Ceiling), pointeur de sortie réel et initialisé.
- [x] Correction `GetCeiling` sous `#if PSX_VERSION && PSXPC_TEST` (legacy conservé), corps RE-781/RE-782
  inchangés.
- [x] Registration six slots bridge + MIP 3072 dans `ObjectObjects()`, adaptateurs exactement typés,
  aucun cast de pointeur incompatible, précondition output valide ET initialisé ; `UNIMPLEMENTED` conservé.
- [x] Preuves publiques rerunnables composition/observer, current/baseline, normal+UBSan.
- [ ] Publication/fusion : **PENDING** revue finale ; guards/commit allowlist non fournis.
- [ ] Gameplay non validé ; dette sanitaire préexistante et 7 échecs RE-778 / FAIL fade non résolus.

## Décision et types
`GetCeiling` initialise puis relit un accumulateur `int` réel passé au callback `void` ; la valeur est
propagée. Adaptateurs `int/int*` (slot) ↔ `long/long*` (corps) via temporaire, conversion scalaire
seule. Aucun élargissement backend : guard `PSX_VERSION && PSXPC_TEST` ; PC_VERSION legacy (NULL/non
initialisé) non activé. **Modèle logiciel** synthétique, **pas de runtime** ; , pas console/boot ; aucune prétention de buffer
RAM complet. Preuves brutes privées référencées symboliquement sous `build/` ignoré.

## Preuves publiques (rerunnables)
`tests/reverse/fixtures/re783/` et `test_re783_bridge_composition.py` :
- composition : current **296 assertions / 0 échec** ; baseline **296 / 52** (installation absente, SKIP).
- observer (contrat, vrais corps, EXPECT nonNULL) : current **514 / 0** ; baseline **514 / 132**.
- UBSan : mêmes cardinalités, aucun diagnostic runtime positif.

## Build (rectificatif)
Commandes CMake avec ajout explicite **-m32** et sortie redirigée vers objet temporaire — résultats
ELF32/ILP32. La configuration CMake par défaut produit des objets ELF64 ; `USE_32_BIT_ADDR` seul ne
définit pas l'ABI. Pas de configuration/link moteur complet, pas de fullbuild.

## Limites / historique
Historique erroné conservé **privé** (lot7 MIP 5120 erroné, lot11 fixture trigger, lot17
offsets loaded, lot18 comparaison tautologique, lot24 runner/setup) — non revendu PASS. 7 échecs
RE-778 et FAIL fade préexistants demeurent.

Modèle logiciel synthétique ; pas de runtime.

modèle logiciel
