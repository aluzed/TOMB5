# PORT-011 — Validation, sauvegarde déterministe et tests

Status: Done — implémentation et tests locaux ; revue indépendante non faite.

[Index](README.md) · [Recette Linux32](../linux32.md)

## Objectif

Refuser une configuration invalide avec un message attribuable, produire un
fichier déterministe et couvrir le parseur/l'évaluateur par des tests host.

## Portée

- Validation stricte : sections connues, actions connues, clés/boutons/axes
  connus, deux bindings maximum, booléens, index, GUID, deadzone.
- Erreurs avec nom de fichier et numéro de ligne ; repli sur les défauts.
- `InputMap_Save` déterministe et rechargeable.
- Tests sans données de jeu ni manette.

## Implémentation

- `set_error("%s:%d: ...")` dans `EMULATOR/INPUTMAP.C`.
- `InputMap_Load` remet les défauts en cas d'erreur et retourne `-1` ; `LIBPAD.C`
  journalise et continue avec les défauts plutôt que de planter.
- `tests/porting/inputmap_harness.cpp` : commandes `defaults-save`, `eval`,
  `error` ; static-asserts entre `INPUTMAP_IN_*`/`INPUTMAP_RAW_*` et
  `GAME/CONTROL.H`.
- `tests/porting/test_inputmap.py` : 17 tests.

## Couverture vérifiée

- 17/17 tests keymap PASS.
- Suite porting complète : **496 PASS**.
- Cas couverts : défauts + deux colonnes, double bind clavier et manette,
  boutons/axes/triggers, deadzone, devices désactivés, bits Start/Select,
  commentaires/casse/espaces, clé inconnue, action inconnue, section inconnue,
  plus de deux bindings, GUID invalide, index invalide, slots vides, fichier
  absent.

## Limites

Le harness est compilé en 64 bits sur l'hôte ; le binaire de jeu est vérifié en
ELF32 i386 (`build-e`, SHA256 `f20b6523d743bd4ba1c566633700dfeed9850deababa64ac1bf309bf2f4b0de4` ; les builds `build-c`/`build-d` avaient le même code hors journalisation des manettes et validation NaN).
Pas de fuzzing, pas de test de permissions/disque plein, pas de test de fichier
concurrent. Une revue indépendante reste à faire.
