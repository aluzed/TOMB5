# RE-859 — mRotX : candidat production defined-bit32

**État : candidat testé, revue indépendante PASS scoped enregistrée ; aucun commit/stage/push au snapshot initial de revue.**

## Contrat et progression
- [x] Lire et hasher les preuves privées RE858 et leur revue sans rejouer les matrices cible.
- [x] RED public sur les vraies TU inchangées : UBSan signale le décalage signé dans mRotX, ligne 444. La géométrie baseline était déjà correcte ; aucune réparation de vecteur n’est revendiquée.
- [x] Correction minimale : temporaires uint32_t, conversion avant packing/décalage, négation modulaire, conversion signed32 arithmétique définie avant SetRotation. Pas de sizeof(long)==4, lambda GNU ou builtin memcpy.
- [x] GREEN : 36 cas synthétiques (trois matrices, douze angles dont négatifs/zéro), oracle scalaire indépendant avec division arithmétique et packing signed16. Table rcossin_tbl référencée depuis CAMERA.C, aucun dump public.
- [x] GNU C++11 ELF32 et ELF64, O0/O2, normal et UBSan strict : huit configurations réussies. Les 8 mots matrice et 64 mots backing GTE (72 mots complets) restent identiques au baseline normal, entre ABI et modes. Aucun sanitizer désactivé.
- [x] Build complet Debug ELF32 : configure et build exit 0 avec les bibliothèques 32-bit historiques déjà présentes ; warnings historiques conservés dans les logs.
- [x] Revue indépendante du candidat : PASS scoped sur les six fichiers ; clôture documentaire et contrôle des hashes finaux avant commit.

## Reproduction publique
```sh
flock -w5 build/reverse/autonomy-mutation.lock python3 -m pytest -q tests/reverse/test_re859_mrotx_actual_tu.py tests/reverse/test_re859_documentation.py
```
Le runner autonome accepte --phase green --output DIR ; en checkout neuf, il construit une référence normale locale, vérifie l’oracle puis compare les banques complètes aux modes stricts. La preuve TDD baseline inchangée est archivée séparément, avec hashes identiques des tests RED/GREEN. RE859_OWNER_PID est un contrôle opérationnel optionnel, pas un PID codé en dur dans le test.

## Portée et limites
Les deux TU complètes MATHS.C et LIBGTE.C sont compilées et liées avec -z defs, sans symboles non résolus ignorés ; --gc-sections exclut les fonctions étrangères au chemin retenu. ELF64 nécessite -fpermissive pour le cast pointeur/int historique dans mmPushMatrix, hors chemin mRotX. Ce test n’établit pas une portabilité générale du projet : MSVC, autres compilateurs/plateformes, strict-aliasing et matériel restent non testés. SetRotation et les conversions short historiques ne sont pas refactorisés.

**RE858 global FAIL reste conservé** : 24/30 banques source/cible privées diffèrent pour des transferts bruts GTE historiques ; le PASS concerne la préservation native et la matrice, pas une égalité brute cible. Le fulljoint strict archivé reste en échec plus tard dans mRotZ ; pas de nouvelle exécution fulljoint, pas de replay cible ni jeu/runtime. Aucune revendication skeleton, gameplay ou startup.

## Handoff et preuves
Dossier exclusif : build/reverse/autonomy-20261007/re859-integration-candidate/ (RED.json, GREEN.json, ledgers exact argv/cwd/start/end/exit, fullbuild-*.json, candidate-hashes.json, candidate-complete.diff, HANDOFF.md, verdict.json, seal.json).
Dashboard : section nouvelle RE-859 seulement, chaque octet historique préservé par un test de hash après retrait de cette section. Les archives historiques, suppressions utilisateur et index restent intacts.

### Hashes figés avant insertion documentaire
- `SPEC_PSXPC_N/MATHS.C` : `c2a6c006300903eac30e06abb7a67b66bbb4d427a78e287df48ce78d16e9c7bf`
- `tests/reverse/test_re859_mrotx_actual_tu.py` : `9bf1084cc9598ef57b6cc08b88236c2d53662aeea5ba2a114eba58401f21f588`
- `tests/reverse/re859_mrotx_actual_tu.cpp` : `2090ceac007669b8501b6f9abd66cb119d53c1d3bf01e2867bbad2d1934f651a`
- `tests/reverse/test_re859_documentation.py` : `e2261b1915223eb7ee30d431b4385ebbf6bec4f256a8470d3e7021c2f29d09dc`
