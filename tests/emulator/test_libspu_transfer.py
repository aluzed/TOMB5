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
