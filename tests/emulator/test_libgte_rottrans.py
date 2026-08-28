import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_rot_trans_applies_current_rotation_and_translation(tmp_path):
    source = tmp_path / "rot_trans_harness.cpp"
    executable = tmp_path / "rot_trans_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX matrix = {};
            SVECTOR input = {12, -5, 6, 0};
            VECTOR output = {};
            long flag = -1;

            matrix.m[0][0] = ONE;
            matrix.m[1][1] = ONE;
            matrix.m[2][2] = ONE;
            matrix.t[0] = 100;
            matrix.t[1] = -200;
            matrix.t[2] = 300;
            SetRotMatrix(&matrix);
            SetTransMatrix(&matrix);
            RotTrans(&input, &output, &flag);

            assert(output.vx == 112);
            assert(output.vy == -205);
            assert(output.vz == 306);
            assert(flag == 0);
            return 0;
        }
        """
    )
    subprocess.run(
        [
            "g++",
            "-ffunction-sections",
            "-fdata-sections",
            "-Wl,--gc-sections",
            "-I/usr/include/SDL2",
            "-I",
            str(REPO / "EMULATOR"),
            str(source),
            str(REPO / "EMULATOR" / "LIBGTE.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
