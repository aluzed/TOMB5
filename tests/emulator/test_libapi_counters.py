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


def test_start_rcnt_rejects_invalid_counter_without_changing_enable_bits(tmp_path):
    source = tmp_path / "invalid_start_rcnt_harness.cpp"
    executable = tmp_path / "invalid_start_rcnt_harness"
    source.write_text(
        """
        #include <assert.h>
        extern long StartRCnt(long spec);
        extern int dword_300[];
        int main(void) {
            dword_300[1] = 0;
            assert(StartRCnt(3) == 0);
            assert(dword_300[1] == 0);
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


def test_get_sp_returns_the_value_most_recently_set(tmp_path):
    source = tmp_path / "get_sp_harness.cpp"
    executable = tmp_path / "get_sp_harness"
    source.write_text(
        """
        #include <assert.h>
        extern unsigned long SetSp(unsigned long newsp);
        extern unsigned long GetSp();
        int main(void) {
            SetSp(0x12345678UL);
            assert(GetSp() == 0x12345678UL);
            SetSp(0x801FFFE0UL);
            assert(GetSp() == 0x801FFFE0UL);
            assert(SetSp(0x1000UL) == 0x801FFFE0UL);
            assert(GetSp() == 0x1000UL);
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
