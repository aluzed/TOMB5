"""Garde-fou sur la fusion clavier/manette dans `Emulator_UpdateInput`.

`kbInputs` et `controllerInputs` sont deux masques **actifs au niveau bas**
(0xFFFF = aucune touche).  Les combiner avec un ET exige donc le *meme*
bouton sur le clavier **et** sur la manette : des qu'une manette est
branchee, ni le clavier ni la manette ne produisent d'entree.  C'est
exactement le symptome observe en jeu (`inputBusy = 0` alors que
`PadConnected = 1`, Lara figee malgre les touches).

La combinaison correcte est un OU (pression sur l'une ou l'autre source).
Ce test lit la source pour eviter toute regression silencieuse : le bug ne
se voit ni a la compilation ni dans les tests fonctionnels existants.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EMULATOR_C = ROOT / "EMULATOR" / "EMULATOR.C"


def test_keyboard_and_controller_masks_are_ored():
    text = EMULATOR_C.read_text(errors="ignore")

    assert "kbInputs & controllerInputs" not in text, (
        "Emulator_UpdateInput combine les masques clavier/manette avec un ET : "
        "des qu'une manette est branchee, aucune entree ne passe."
    )
    assert text.count("(unsigned short)(kbInputs | controllerInputs)") == 2, (
        "les deux chemins d'entree (normal et debug) doivent fusionner "
        "clavier et manette avec un OU"
    )
