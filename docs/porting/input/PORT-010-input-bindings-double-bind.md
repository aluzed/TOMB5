# PORT-010 — Double bind et actions sémantiques

Status: Done — implémentation et tests locaux ; revue indépendante non faite.

[Index](README.md) · [Recette Linux32](../linux32.md)

## Objectif

Mapper chaque action sur **deux bindings par device** (clavier et manette), avec
les mêmes actions côté jeu que la manette PSX d'origine, sans dépendre du schéma
`ControlOption` quand le keymap est actif.

## Portée

- Actions : `forward`, `back`, `left`, `right`, `action`, `jump`, `draw`, `roll`,
  `look`, `duck`, `walk`, `sprint`, `start`, `select`.
- Deux colonnes par action dans `[keyboard]` et `[gamepad]`.
- Clavier : scancodes SDL (indépendants de la disposition ; `W` désigne la
  position physique QWERTY-W, soit Z sur AZERTY).
- Manette : boutons SDL et axes avec seuil (`LEFTX-`, `LEFTY+`, `TRIGGERLEFT`,
  `TRIGGERRIGHT`, etc.).
- `[gameplay] use_control_option = 0` (défaut) : les actions du keymap sont
  autoritatives. `1` conserve les cinq schémas PSX historiques.

## Implémentation

- `InputMap_EvaluateActions` construit les bits `IN_*` sémantiques.
- `InputMap_EvaluatePad` construit les bits PSX actifs-bas pour les menus/titre
  (`action` → Cross, `draw` → Triangle, directions → D-pad, `start`/`select`).
- `SPEC_PSXPC_N/PSXINPUT.C` : si le keymap est actif et `use_control_option = 0`,
  `InputMap_PollActions()` remplace la table `pad_cons` ; `IN_SELECT`/`IN_DESELECT`
  issus de Cross/Triangle restent disponibles pour les menus et l'inventaire.

## Acceptation locale

- `forward = W, UP` : les deux touches produisent `IN_FORWARD` et le bit D-pad.
- `forward = DPAD_UP, LEFTY-` : bouton et axe produisent la même action ; un
  axe sous la deadzone ne produit rien.
- Double bind vérifié sur les deux devices (17 tests).
- L’éditeur en jeu (PORT-012) capture la prochaine touche/bouton/axe et écrit
  le slot sélectionné immédiatement.
- Build `build-c` (recette) et `build-e` (build final) : `C` sur `New Game` atteint la scène de Rome
  (`build/porting/launch-inputmap-default`, `build/porting/launch-inputmap-e2`).
- Configuration personnalisée `action = SPACE` : `Espace` remplace `C` pour
  quitter le menu et atteindre la scène (`build/porting/launch-inputmap-custom`).

## Limites

Entrées digitales : les axes sont des seuils, pas une valeur analogique continue.
Pas de remappage en jeu. La manette n'a pas été testée physiquement ; seuls les
parseurs, les bits et la configuration ont été vérifiés. Les combinaisons de
touches simultanées ne sont pas testées au-delà de l'OR des bindings.
