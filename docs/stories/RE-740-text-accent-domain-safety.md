# RE-740 — Text accent domain: safe glyph lookup and bounded measurement

## Statut et périmètre

**Recherche/implémentation partielle, sûre côté hôte — pas une reconstruction complète des accents.**
Unité cohérente après RE-732/733/739 : domaine des caractères accentués (0x80..0xAD)
dans `SPEC_PSXPC_N/TEXT_S.C::GetStringLength`, avec correction des indexations
provoquant des lectures hors limites et une mesure partielle prouvable
structurellement.

Autorisation implicite : poursuite du reverse engineering (prompt projet). Pas de
réouverture des inventaires terminaux. Aucun asset, dump binaire brut ou donnée
non versionnée ajouté.

## Problèmes observés (preuve dans le dépôt)

- `AccentTable` est `char[46][2]` (`GAME/TEXT.C`/`GAME/TEXT.H`) ; le code utilisait
  `AccentTable[0][c - 0x80]` (indexation 2D incorrecte) puis `assert(0)`.
- Après l’assert, le chemin retombait sur `CharDef[c - 33]` avec `c` accentué
  (0x80..0xAD), donc indices 95..140 alors que `CharDef` fait 106 entrées :
  lecture hors limites/UB côté hôte.
- `PrintString` (commentaires/logique) indique une substitution via `AccentTable`
  en glyphe de base + glyphe d’accent optionnel ; l’accent n’est pas dessiné quand
  l’élément accent vaut espace (`0x20`), ce qui rend la **mesure du glyphe de base
  seule** défendable structurellement pour ce sous-cas.

## Modifications

`SPEC_PSXPC_N/TEXT_S.C` (`GetStringLength`) :
- lecture du caractère en `unsigned char` (corrige la classification des octets
  0x80+ sur plateformes où `char` est signé ; nécessaire pour atteindre le domaine
  accentué sans changer le comportement ASCII).
- indexation corrigée : `AccentTable[c - 0x80][0]` (base) / `[1]` (accent).
- résolution du glyphe de base via le domaine normal (`c < 0x20` → `CharDef[c+74]`,
  `< 0x80` → `CharDef[c-33]`, espace traité comme chemin existant), sans utiliser
  `CharDef[c-33]` avec le caractère accentué brut.
- accent `== 0x20` (pas d’overlay) : mesure des métriques du glyphe de base
  (largeur avec échelle, YOffset/h, `t5=1` conservé). **Inférence structurelle**
  depuis la logique de rendu commentée ; à confirmer par preuve binaire si besoin
  de marquage `(F)/(D)`.
- base espace / hors domaine / accent overlay (`!= 0x20`) : `assert(0)` conservé
  (combinaison d’étendue/largeur de l’overlay et cas RE-732 « zone précédant le
  premier glyphe » pour les 12 entrées `{' ',' '}` non prouvés ici).

Aucun marqueur `(F)`, `(D)`, `(**)`, `(ND)` modifié. `PrintString` non modifié
(chemin accentué toujours `assert(0)`).

## Vérification

- `tests/emulator/test_re740_text_accent_domain.py` : harness synthétique compilant
  la vraie TU (`-DNDEBUG` pour éviter les asserts sur les sous-cas non exercés) ;
  vérifie base+accent-espace → métriques du glyphe de base, respect de `ScaleFlag`,
  et non-régression ASCII.
- Régression ciblée : `tests/emulator/test_text_measurement.py`,
  `test_text_layout.py`, `test_text_colour.py` — tous verts.

Commande :
`python3 -m pytest tests/emulator/test_re740_text_accent_domain.py tests/emulator/test_text_measurement.py tests/emulator/test_text_layout.py tests/emulator/test_text_colour.py -q`

## Limites / next step

- **Non prouvé/reconstruit** : combinaison largeur/étendue base+accent quand overlay
  dessiné ; 12 entrées `{' ',' '}` (RE-732 : substitution espace puis zone précédant
  le premier glyphe) ; sélection/rendu accentué dans `PrintString` ; domaine exact
  des octets admis au-delà de 0x80..0xAD.
- Ne pas retirer `assert(0)` des cas overlay/base-espace sans preuve binaire.
- Prochaine unité cohérente : preuve binaire de la mesure/rendu accentué (ou
  formalisation sûre du domaine espace/espace) avant toute prétention de
  reconstruction complète ; sinon cluster texte différent (sélection de glyphes
  hors accents) selon disponibilité de preuve.
