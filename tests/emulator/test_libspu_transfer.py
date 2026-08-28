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


def test_set_irq_callback_replaces_and_returns_the_previous_callback(tmp_path):
    source = tmp_path / "spu_irq_callback_harness.cpp"
    executable = tmp_path / "spu_irq_callback_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        static void first_callback(void) {}
        static void second_callback(void) {}

        int main(void) {
            assert(SpuSetIRQCallback(first_callback) == 0);
            assert(SpuSetIRQCallback(second_callback) == first_callback);
            assert(SpuSetIRQCallback(0) == second_callback);
            assert(SpuSetIRQCallback(first_callback) == 0);
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


def test_set_reverb_voice_updates_only_the_selected_voice_bits(tmp_path):
    source = tmp_path / "spu_reverb_voice_harness.cpp"
    executable = tmp_path / "spu_reverb_voice_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short* _spu_RXX;

        int main(void) {
            _spu_RXX[204] = 0x0002;
            _spu_RXX[205] = 0x0040;

            assert(SpuSetReverbVoice(SPU_ON, SPU_00CH | SPU_17CH) ==
                   (SPU_00CH | SPU_17CH));
            assert(_spu_RXX[204] == 0x0003);
            assert(_spu_RXX[205] == 0x0042);

            assert(SpuSetReverbVoice(SPU_OFF, SPU_00CH | SPU_17CH) ==
                   (SPU_00CH | SPU_17CH));
            assert(_spu_RXX[204] == 0x0002);
            assert(_spu_RXX[205] == 0x0040);
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


def test_get_reverb_voice_returns_the_current_24_voice_mask(tmp_path):
    source = tmp_path / "spu_get_reverb_voice_harness.cpp"
    executable = tmp_path / "spu_get_reverb_voice_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short* _spu_RXX;

        int main(void) {
            _spu_RXX[204] = 0xA55A;
            _spu_RXX[205] = 0xFFFF;
            assert(SpuGetReverbVoice() == 0xFFA55A);
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


def test_set_pitch_lfo_voice_updates_only_the_selected_voice_bits(tmp_path):
    source = tmp_path / "spu_pitch_lfo_voice_harness.cpp"
    executable = tmp_path / "spu_pitch_lfo_voice_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short* _spu_RXX;

        int main(void) {
            _spu_RXX[200] = 0x0002;
            _spu_RXX[201] = 0x0040;
            _spu_RXX[202] = 0x1111;
            _spu_RXX[203] = 0x2222;

            assert(SpuSetPitchLFOVoice(SPU_ON, SPU_00CH | SPU_17CH) ==
                   (SPU_00CH | SPU_17CH));
            assert(_spu_RXX[200] == 0x0003);
            assert(_spu_RXX[201] == 0x0042);
            assert(_spu_RXX[202] == 0x1111);
            assert(_spu_RXX[203] == 0x2222);

            assert(SpuSetPitchLFOVoice(SPU_OFF, SPU_00CH | SPU_17CH) ==
                   (SPU_00CH | SPU_17CH));
            assert(_spu_RXX[200] == 0x0002);
            assert(_spu_RXX[201] == 0x0040);
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


def test_get_pitch_lfo_voice_returns_the_current_24_voice_mask(tmp_path):
    source = tmp_path / "spu_get_pitch_lfo_voice_harness.cpp"
    executable = tmp_path / "spu_get_pitch_lfo_voice_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short* _spu_RXX;

        int main(void) {
            _spu_RXX[200] = 0xA55A;
            _spu_RXX[201] = 0xFFFF;
            assert(SpuGetPitchLFOVoice() == 0xFFA55A);
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


def test_get_common_master_volume_returns_the_current_register_values(tmp_path):
    source = tmp_path / "spu_get_common_master_volume_harness.cpp"
    executable = tmp_path / "spu_get_common_master_volume_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        int main(void) {
            short left = 0;
            short right = 0;

            SpuSetCommonMasterVolume(0x1234, 0x5678);
            SpuGetCommonMasterVolume(&left, &right);
            assert(left == 0x1234);
            assert(right == 0x5678);
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


def test_get_reverb_mode_depth_returns_the_configured_depth(tmp_path):
    source = tmp_path / "spu_get_reverb_mode_depth_harness.cpp"
    executable = tmp_path / "spu_get_reverb_mode_depth_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        int main(void) {
            short left = 0;
            short right = 0;

            SpuSetReverbModeDepth(0x1234, -0x1234);
            SpuGetReverbModeDepth(&left, &right);
            assert(left == 0x1234);
            assert(right == -0x1234);
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
