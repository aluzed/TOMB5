import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_stop_rcnt_clears_only_the_requested_counter_enable_bit(tmp_path):
    source = tmp_path / "stop_rcnt_harness.cpp"
    executable = tmp_path / "stop_rcnt_harness"
    source.write_text(
        """
        #include <assert.h>
        extern long StopRCnt(long spec);
        extern int dword_300[];
        int main(void) {
            dword_300[1] = 0x7f;
            assert(StopRCnt(1) == 1);
            assert(dword_300[1] == 0x5f);
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
            str(REPO / "EMULATOR" / "LIBAPI.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_stop_rcnt_rejects_invalid_counter_without_changing_enable_bits(tmp_path):
    source = tmp_path / "invalid_stop_rcnt_harness.cpp"
    executable = tmp_path / "invalid_stop_rcnt_harness"
    source.write_text(
        """
        #include <assert.h>
        extern long StopRCnt(long spec);
        extern int dword_300[];
        int main(void) {
            dword_300[1] = 0x7f;
            assert(StopRCnt(3) == 0);
            assert(dword_300[1] == 0x7f);
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
            str(REPO / "EMULATOR" / "LIBAPI.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
