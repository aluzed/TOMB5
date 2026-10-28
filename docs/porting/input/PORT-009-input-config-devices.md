# PORT-009 — Fichier de configuration et choix du device

Status: Done — implémentation et tests locaux ; revue indépendante non faite.

[Index](README.md) · [Recette Linux32](../linux32.md)

## Objectif

Fournir un fichier `INPUT.CFG` lisible et modifiable, généré au premier lancement,
qui choisit le clavier, la manette ou les deux, et sélectionne la manette par
index ou par GUID.

## Portée

- Sections `[devices]` et `[gameplay]`.
- Clés `keyboard`, `gamepad`, `gamepad_index`, `gamepad_guid`, `axis_deadzone`,
  `use_control_option`.
- Résolution du chemin : `TOMB5_INPUT_CONFIG`, puis `INPUT.CFG` du répertoire
  courant, puis chemin préférentiel SDL, puis écriture dans le répertoire courant
  avec repli sur le chemin préférentiel.
- Écriture d'un fichier par défaut complet si aucun fichier n'existe.

## Implémentation

- `EMULATOR/INPUTMAP.C` : `InputMap_Defaults`, `InputMap_Load`, `InputMap_Save`,
  validation des booléens, index, GUID et deadzone.
- `EMULATOR/LIBPAD.C` : `input_config_load`, `input_save_default_config`,
  `input_open_gamepad` (GUID prioritaire, puis index, puis premier contrôleur).
- Le GUID détecté est journalisé ; il n'est pas réécrit dans un fichier existant.

## Acceptation locale

- Premier lancement sans fichier : `INPUT.CFG` créé, sections et deux colonnes
  présentes (`build/porting/data-ntsc/INPUT.CFG`).
- `[INPUT] Default configuration written to INPUT.CFG` dans le journal.
- `keyboard = 0` ignore les touches ; `gamepad = 0` ignore la manette (tests).
- `gamepad_index = -1` et les index valides sont acceptés ; `-2` est refusé.
- Un GUID invalide est refusé avec un message attribuable.
- L’écran Devices de l’éditeur en jeu (PORT-012) bascule clavier/manette, fait
  tourner l’index et sauvegarde immédiatement.

## Limites

Pas d'interface graphique de sélection, pas de hot reload, pas de test sur une
manette physique (aucun contrôleur connecté sur cet hôte). Le repli d'écriture
vers le chemin préférentiel n'est pas testé sur un répertoire réellement en
lecture seule.
