import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_pcread_returns_the_number_of_bytes_read(tmp_path):
    input_file = tmp_path / "input.bin"
    input_file.write_bytes(b"TOMB5")
    source = tmp_path / "pcread_harness.cpp"
    executable = tmp_path / "pcread_harness"
    source.write_text(
        f"""
        #include <assert.h>
        #include <stdint.h>
        #include "LIBSN.H"

        int main(void) {{
            char path[] = "{input_file}";
            char buffer[6] = {{0}};
            uintptr_t handle = PCopen(path, 0, 0);

            assert(handle != (uintptr_t)-1);
            assert(PCread(handle, buffer, 5) == 5);
            assert(buffer[0] == 'T');
            assert(buffer[4] == '5');
            assert(PCclose(handle) == 0);
            return 0;
        }}
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
            str(REPO / "EMULATOR" / "LIBSN.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_pcwrite_returns_the_number_of_bytes_written(tmp_path):
    output_file = tmp_path / "output.bin"
    source = tmp_path / "pcwrite_harness.cpp"
    executable = tmp_path / "pcwrite_harness"
    source.write_text(
        f"""
        #include <assert.h>
        #include <stdint.h>
        #include "LIBSN.H"

        int main(void) {{
            char path[] = "{output_file}";
            char data[] = "TOMB5";
            uintptr_t handle = PCopen(path, 1, 0);

            assert(handle != (uintptr_t)-1);
            assert(PCwrite(handle, data, 5) == 5);
            assert(PCclose(handle) == 0);
            return 0;
        }}
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
            str(REPO / "EMULATOR" / "LIBSN.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
    assert output_file.read_bytes() == b"TOMB5"


def test_pccreat_returns_a_writable_handle_for_a_new_file(tmp_path):
    output_file = tmp_path / "created.bin"
    source = tmp_path / "pccreat_harness.cpp"
    executable = tmp_path / "pccreat_harness"
    source.write_text(
        f"""
        #include <assert.h>
        #include <stdint.h>
        #include "LIBSN.H"

        int main(void) {{
            char path[] = "{output_file}";
            char data[] = "TOMB5";
            uintptr_t handle = PCcreat(path, 0);

            assert(handle != (uintptr_t)-1);
            assert(PCwrite(handle, data, 5) == 5);
            assert(PCclose(handle) == 0);
            return 0;
        }}
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
            str(REPO / "EMULATOR" / "LIBSN.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
    assert output_file.read_bytes() == b"TOMB5"
