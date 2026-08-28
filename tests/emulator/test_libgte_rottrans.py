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


def test_normal_color_dpq_applies_identity_lighting_to_input_colour(tmp_path):
    source = tmp_path / "normal_color_dpq_harness.cpp"
    executable = tmp_path / "normal_color_dpq_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX identity = {};
            SVECTOR normal = {ONE, ONE, ONE, 0};
            CVECTOR input = {128, 64, 32, 0x7e};
            CVECTOR output = {};

            identity.m[0][0] = ONE;
            identity.m[1][1] = ONE;
            identity.m[2][2] = ONE;
            SetLightMatrix(&identity);
            SetColorMatrix(&identity);
            SetBackColor(0, 0, 0);
            SetFarColor(0, 0, 0);
            NormalColorDpq(&normal, &input, 0, &output);

            assert(output.r == input.r);
            assert(output.g == input.g);
            assert(output.b == input.b);
            assert(output.cd == input.cd);
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


def test_normal_color_col_applies_identity_lighting_to_input_colour(tmp_path):
    source = tmp_path / "normal_color_col_harness.cpp"
    executable = tmp_path / "normal_color_col_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX identity = {};
            SVECTOR normal = {ONE, ONE, ONE, 0};
            CVECTOR input = {128, 64, 32, 0x7e};
            CVECTOR output = {};

            identity.m[0][0] = ONE;
            identity.m[1][1] = ONE;
            identity.m[2][2] = ONE;
            SetLightMatrix(&identity);
            SetColorMatrix(&identity);
            SetBackColor(0, 0, 0);
            NormalColorCol(&normal, &input, &output);

            assert(output.r == input.r);
            assert(output.g == input.g);
            assert(output.b == input.b);
            assert(output.cd == input.cd);
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


def test_mul_matrix0_multiplies_fixed_point_rotation_without_overwriting_translation(tmp_path):
    source = tmp_path / "mul_matrix0_harness.cpp"
    executable = tmp_path / "mul_matrix0_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX left = {};
            MATRIX right = {};
            MATRIX result = {};

            left.m[0][0] = 0;
            left.m[0][1] = -ONE;
            left.m[1][0] = ONE;
            left.m[1][1] = 0;
            left.m[2][2] = ONE;

            right.m[0][0] = ONE;
            right.m[1][1] = ONE;
            right.m[2][2] = ONE;
            result.t[0] = 11;
            result.t[1] = 22;
            result.t[2] = 33;

            assert(MulMatrix0(&left, &right, &result) == &result);
            assert(result.m[0][0] == 0);
            assert(result.m[0][1] == -ONE);
            assert(result.m[1][0] == ONE);
            assert(result.m[1][1] == 0);
            assert(result.m[2][2] == ONE);
            assert(result.t[0] == 11);
            assert(result.t[1] == 22);
            assert(result.t[2] == 33);
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


def test_mul_matrix0_uses_a_64_bit_accumulator_for_three_q12_products():
    implementation = (REPO / "EMULATOR" / "LIBGTE.C").read_text()

    assert "long long value = 0;" in implementation


def test_mul_matrix_replaces_its_first_matrix_with_the_q12_product(tmp_path):
    source = tmp_path / "mul_matrix_harness.cpp"
    executable = tmp_path / "mul_matrix_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX left = {};
            MATRIX right = {};

            left.m[0][0] = 0;
            left.m[0][1] = -ONE;
            left.m[1][0] = ONE;
            left.m[1][1] = 0;
            left.m[2][2] = ONE;
            left.t[0] = 10;
            left.t[1] = 20;
            left.t[2] = 30;

            right.m[0][0] = ONE;
            right.m[1][1] = ONE;
            right.m[2][2] = ONE;

            assert(MulMatrix(&left, &right) == &left);
            assert(left.m[0][0] == 0);
            assert(left.m[0][1] == -ONE);
            assert(left.m[1][0] == ONE);
            assert(left.m[1][1] == 0);
            assert(left.m[2][2] == ONE);
            assert(left.t[0] == 10);
            assert(left.t[1] == 20);
            assert(left.t[2] == 30);
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


def test_mul_matrix2_replaces_its_second_matrix_with_the_q12_product(tmp_path):
    source = tmp_path / "mul_matrix2_harness.cpp"
    executable = tmp_path / "mul_matrix2_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBGTE.H"
        int main(void) {
            MATRIX left = {};
            MATRIX right = {};

            left.m[0][0] = 0;
            left.m[0][1] = -ONE;
            left.m[1][0] = ONE;
            left.m[1][1] = 0;
            left.m[2][2] = ONE;

            right.m[0][0] = ONE;
            right.m[1][1] = ONE;
            right.m[2][2] = ONE;
            right.t[0] = 40;
            right.t[1] = 50;
            right.t[2] = 60;

            assert(MulMatrix2(&left, &right) == &right);
            assert(right.m[0][0] == 0);
            assert(right.m[0][1] == -ONE);
            assert(right.m[1][0] == ONE);
            assert(right.m[1][1] == 0);
            assert(right.m[2][2] == ONE);
            assert(right.t[0] == 40);
            assert(right.t[1] == 50);
            assert(right.t[2] == 60);
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
