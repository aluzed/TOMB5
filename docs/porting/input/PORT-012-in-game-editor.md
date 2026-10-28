# PORT-012 — Éditeur de keymap en jeu

Status: Done — implémentation et recette locale ; revue indépendante non faite.

[Index](README.md) · [Recette Linux32](../linux32.md)

## Objectif

Configurer clavier et manette **dans le jeu**, sans éditer le fichier à la main :
ouvrir un écran de configuration, choisir une action et un slot, presser la
touche/le bouton à associer, et écrire `INPUT.CFG` **immédiatement** à chaque
modification.

## Utilisation

| Touche / bouton | Action |
|---|---|
| `F1` | Ouvrir/fermer l'éditeur (titre ou jeu actif) |
| `Échap` | Fermer, ou annuler la capture en cours |
| Flèches / D-pad | Choisir l'action ou la ligne |
| Gauche/Droite | Choisir la colonne (clavier 1/2, manette 1/2) ou changer un device |
| Entrée / Espace / A | Passer en capture, ou activer la ligne device |
| `Tab` / Back | Écran Actions ↔ écran Devices |
| `R` | Restaurer les bindings par défaut et sauvegarder |
| `B` / Start | Fermer depuis la manette |

L'écran Actions affiche les quatre bindings de chaque action, avec la colonne
active entre crochets. L'écran Devices règle `keyboard`, `gamepad` et l'index de
manette (ordinal de contrôleur), et affiche le GUID ainsi que le chemin du
fichier. Les noms clavier affichés sont les **libellés de la disposition
courante** (AZERTY : `Z`, `Q`, `W`…) ; le fichier, lui, stocke les scancodes
physiques (`W`, `A`, `Z`…), donc il reste indépendant de la disposition.

## Implémentation

- `EMULATOR/INPUTUI.C/H` : état de l'écran, navigation, capture SDL, sauvegarde
  immédiate via `InputMap_UpdateBinding` / `InputMap_UpdateDevices` /
  `InputMap_ResetDefaultsAndSave`.
- `SPEC_PSXPC_N/INPUTUIDRAW.C` : rendu avec `PrintString`/`DrawF4`, panneau
  modal, liste scrollable de 9 actions, écran devices.
- `EMULATOR/EMULATOR.C` : `InputUI_HandleEvent` est appelé avant le traitement
  des événements de jeu ; F1 ouvre l'éditeur.
- `SPEC_PSXPC_N/TITSEQ.C` : le titre ne dessine plus son menu quand l'éditeur
  est ouvert ; `InputUI_NotifyDraw` autorise F1 uniquement quand le chemin de
  dessin normal est actif.
- `SPEC_PSXPC_N/DRAWPHAS.C` : l'éditeur est dessiné en fin de frame.
- `GAME/CONTROL.C` : `ControlPhase` est gelé tant que l'éditeur est ouvert.
- `GAME/HEALTH.C` : le HUD debug `Camera X/Y/Z` est masqué pendant l'édition.

## Recette locale

- F1 au titre : écran lisible, 9 lignes visibles, scroll, footer (`build/porting/ui-evidence-20261028/title-ui.png`).
- Capture d'une touche : `left` / clavier 2 → `A`, statut « Saved left = A »
  (`build/porting/ui-evidence-20261028/bound-left-A.png`) et `INPUT.CFG` contient `left = A, A`.
- Modification via l'UI puis jeu : `action = C, SPACE` écrit par l'UI,
  `Espace` quitte le menu et atteint la scène de Rome (`build/porting/ui-evidence-20261028/e2e-space-level.png`).
- F1 en jeu : overlay affiché, simulation gelée, `Échap` reprend le jeu
  (`build/porting/ui-evidence-20261028/gameplay-ui.png`, `gameplay-resumed.png`).
- Écran Devices : `Keyboard: OFF` puis retour ON, index de manette, `R` restaure
  les défauts (`build/porting/ui-evidence-20261028/devices-keyboard-off.png`, `devices-reset.png`).
- Build final `build-j` ELF32 i386, SHA256
  `30c014c2ca3ce1dac76dc932a529e2f8b9fb51a61444e82bc4cd1a46da233626`.

## Limites

- L'overlay est modal mais le panneau reste semi-transparent ; la scène est
  visible derrière (choix visuel, pas un défaut fonctionnel).
- Pas de souris, pas de remappage des touches de l'éditeur lui-même (`F1`,
  `Échap` sont réservés), pas de hot-plug de manette.
- F1 n'est accepté que quand `DrawPhaseGame`/`TitleOptions` tourne : pas pendant
  une FMV, l'inventaire ou le menu pause.
- Pas de revue indépendante, pas de manette physique testée.
