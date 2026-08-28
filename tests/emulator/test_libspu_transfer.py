import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]


def test_set_transfer_start_addr_aligns_address_and_updates_transfer_state(tmp_path):
    source = tmp_path / "spu_transfer_start_addr_harness.cpp"
    executable = tmp_path / "spu_transfer_start_addr_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short _spu_tsa;

        int main(void) {
            assert(SpuSetTransferStartAddr(0x12340) == 0x12340);
            assert(_spu_tsa == 0x2468);

            assert(SpuSetTransferStartAddr(0x12341) == 0x12348);
            assert(_spu_tsa == 0x2469);
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
            str(REPO / "EMULATOR" / "LIBSPU.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_get_transfer_start_addr_returns_the_aligned_transfer_address(tmp_path):
    source = tmp_path / "spu_get_transfer_start_addr_harness.cpp"
    executable = tmp_path / "spu_get_transfer_start_addr_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        int main(void) {
            SpuSetTransferStartAddr(0x54321);
            assert(SpuGetTransferStartAddr() == 0x54328);
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
            str(REPO / "EMULATOR" / "LIBSPU.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_get_transfer_mode_returns_the_last_requested_transfer_mode(tmp_path):
    source = tmp_path / "spu_get_transfer_mode_harness.cpp"
    executable = tmp_path / "spu_get_transfer_mode_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        int main(void) {
            SpuSetTransferMode(SPU_TRANSFER_BY_DMA);
            assert(SpuGetTransferMode() == SPU_TRANSFER_BY_DMA);

            SpuSetTransferMode(SPU_TRANSFER_BY_IO);
            assert(SpuGetTransferMode() == SPU_TRANSFER_BY_IO);

            SpuSetTransferMode(7);
            assert(SpuGetTransferMode() == 7);
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
            str(REPO / "EMULATOR" / "LIBSPU.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)


def test_set_transfer_callback_replaces_and_returns_the_previous_callback(tmp_path):
    source = tmp_path / "spu_transfer_callback_harness.cpp"
    executable = tmp_path / "spu_transfer_callback_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        static void first_callback(void) {}
        static void second_callback(void) {}

        int main(void) {
            assert(SpuSetTransferCallback(first_callback) == 0);
            assert(SpuSetTransferCallback(second_callback) == first_callback);
            assert(SpuSetTransferCallback(0) == second_callback);
            assert(SpuSetTransferCallback(first_callback) == 0);
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
            str(REPO / "EMULATOR" / "LIBSPU.C"),
            "-o",
            str(executable),
        ],
        check=True,
        cwd=REPO,
    )
    subprocess.run([str(executable)], check=True)
