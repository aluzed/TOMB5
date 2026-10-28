# Input keymap — tickets PORT-009 à PORT-012

Série dédiée au remappage clavier/manette du port PSXPC_N. Elle est distincte du
lot initial figé `docs/porting/backlog.json` (qui interdit tout statut Done) et
ne modifie pas ses contrats historiques.

Statut global : **implémentation locale vérifiée**, pas de revue indépendante.

| Ticket | Objet | Statut |
|---|---|---|
| [PORT-009](PORT-009-input-config-devices.md) | Fichier `INPUT.CFG`, device clavier/manette, index/GUID | Done local |
| [PORT-010](PORT-010-input-bindings-double-bind.md) | Double bind, actions sémantiques, bits PSX, menus | Done local |
| [PORT-011](PORT-011-input-validation-tests.md) | Validation stricte, sauvegarde déterministe, tests | Done local |
| [PORT-012](PORT-012-in-game-editor.md) | Éditeur de keymap en jeu (F1), sauvegarde à chaque modification | Done local |

## Fichiers

- `EMULATOR/INPUTMAP.H` / `EMULATOR/INPUTMAP.C` : parseur, format, évaluation pure.
- `EMULATOR/LIBPAD.C` : snapshot SDL, choix du device, génération du fichier.
- `SPEC_PSXPC_N/PSXINPUT.C` : application des actions sémantiques (bypass des
  schémas PSX quand `use_control_option = 0`).
- `EMULATOR/INPUTUI.C/H` + `SPEC_PSXPC_N/INPUTUIDRAW.C` : éditeur modal en jeu.
- `tests/porting/inputmap_harness.cpp` / `tests/porting/test_inputmap.py` : tests.
- `docs/porting/linux32.md` : section « Keymap configurable ».

## Limites communes

L'éditeur en jeu (PORT-012) écrit le fichier à chaque modification ; pas de
hot reload des périphériques, pas de test sur manette physique dans cet
environnement (aucune manette connectée). Les entrées restent digitales : les
axes servent de seuils, pas de valeur analogique progressive.
