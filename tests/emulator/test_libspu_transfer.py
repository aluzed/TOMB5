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


def test_reverb_state_can_be_enabled_disabled_and_queried(tmp_path):
    source = tmp_path / "spu_reverb_state_harness.cpp"
    executable = tmp_path / "spu_reverb_state_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"

        int main(void) {
            assert(SpuGetReverb() == SPU_OFF);
            assert(SpuSetReverb(SPU_ON) == SPU_ON);
            assert(SpuGetReverb() == SPU_ON);
            assert(SpuSetReverb(SPU_CLEAR) == SPU_ON);
            assert(SpuGetReverb() == SPU_ON);
            assert(SpuSetReverb(SPU_OFF) == SPU_OFF);
            assert(SpuGetReverb() == SPU_OFF);
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


def test_mute_state_uses_the_control_register_mute_bit(tmp_path):
    source = tmp_path / "spu_mute_harness.cpp"
    executable = tmp_path / "spu_mute_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern unsigned short* _spu_RXX;

        int main(void) {
            _spu_RXX[213] = 0x1234;
            assert(SpuGetMute() == SPU_OFF);
            assert(SpuSetMute(SPU_ON) == SPU_ON);
            assert(SpuGetMute() == SPU_ON);
            assert(_spu_RXX[213] == 0x5234);

            assert(SpuSetMute(SPU_OFF) == SPU_OFF);
            assert(SpuGetMute() == SPU_OFF);
            assert(_spu_RXX[213] == 0x1234);
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


def test_set_common_attr_applies_only_the_masked_cd_input_fields(tmp_path):
    source = tmp_path / "spu_common_attr_harness.cpp"
    executable = tmp_path / "spu_common_attr_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern SpuCommonAttr dword_424;
        extern unsigned short* _spu_RXX;

        int main(void) {
            SpuCommonAttr attr = {};
            dword_424.cd.volume.left = 1;
            dword_424.cd.volume.right = 2;
            dword_424.cd.mix = SPU_OFF;
            _spu_RXX[192] = 0x1234;

            attr.mask = SPU_COMMON_CDVOLL | SPU_COMMON_CDVOLR | SPU_COMMON_CDMIX;
            attr.cd.volume.left = 0x1111;
            attr.cd.volume.right = -0x2222;
            attr.cd.mix = SPU_ON;
            SpuSetCommonAttr(&attr);

            assert(dword_424.cd.volume.left == 0x1111);
            assert(dword_424.cd.volume.right == -0x2222);
            assert(dword_424.cd.mix == SPU_ON);
            assert(_spu_RXX[192] == 0x1234);

            attr.mask = SPU_COMMON_CDVOLL;
            attr.cd.volume.left = -3;
            attr.cd.volume.right = 99;
            attr.cd.mix = SPU_OFF;
            SpuSetCommonAttr(&attr);

            assert(dword_424.cd.volume.left == -3);
            assert(dword_424.cd.volume.right == -0x2222);
            assert(dword_424.cd.mix == SPU_ON);
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


def test_set_common_attr_applies_only_the_masked_cd_reverb_field(tmp_path):
    source = tmp_path / "spu_common_cd_reverb_harness.cpp"
    executable = tmp_path / "spu_common_cd_reverb_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern SpuCommonAttr dword_424;

        int main(void) {
            SpuCommonAttr attr = {};
            dword_424.cd.reverb = SPU_OFF;
            dword_424.cd.mix = SPU_ON;

            attr.mask = SPU_COMMON_CDREV;
            attr.cd.reverb = SPU_ON;
            attr.cd.mix = SPU_OFF;
            SpuSetCommonAttr(&attr);

            assert(dword_424.cd.reverb == SPU_ON);
            assert(dword_424.cd.mix == SPU_ON);
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


def test_set_common_attr_updates_only_requested_master_volume_fields(tmp_path):
    source = tmp_path / "spu_common_master_attr_harness.cpp"
    executable = tmp_path / "spu_common_master_attr_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern SpuCommonAttr dword_424;

        int main(void) {
            SpuCommonAttr attr = {};
            dword_424.mvol.left = 10;
            dword_424.mvol.right = 20;
            dword_424.mvolmode.left = 30;

            attr.mask = SPU_COMMON_MVOLL;
            attr.mvol.left = 1234;
            attr.mvol.right = 5678;
            SpuSetCommonAttr(&attr);

            assert(dword_424.mvol.left == 1234);
            assert(dword_424.mvol.right == 20);
            assert(dword_424.mvolmode.left == 30);
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


def test_set_common_attr_applies_only_the_masked_external_input_fields(tmp_path):
    source = tmp_path / "spu_common_external_attr_harness.cpp"
    executable = tmp_path / "spu_common_external_attr_harness"
    source.write_text(
        """
        #include <assert.h>
        #include "LIBSPU.H"
        extern SpuCommonAttr dword_424;

        int main(void) {
            SpuCommonAttr attr = {};
            dword_424.ext.volume.left = 1;
            dword_424.ext.volume.right = 2;
            dword_424.ext.reverb = SPU_OFF;
            dword_424.ext.mix = SPU_OFF;
            dword_424.cd.mix = SPU_ON;

            attr.mask = SPU_COMMON_EXTVOLL | SPU_COMMON_EXTVOLR |
                        SPU_COMMON_EXTREV | SPU_COMMON_EXTMIX;
            attr.ext.volume.left = -3;
            attr.ext.volume.right = 4;
            attr.ext.reverb = SPU_ON;
            attr.ext.mix = SPU_ON;
            attr.cd.mix = SPU_OFF;
            SpuSetCommonAttr(&attr);

            assert(dword_424.ext.volume.left == -3);
            assert(dword_424.ext.volume.right == 4);
            assert(dword_424.ext.reverb == SPU_ON);
            assert(dword_424.ext.mix == SPU_ON);
            assert(dword_424.cd.mix == SPU_ON);
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
