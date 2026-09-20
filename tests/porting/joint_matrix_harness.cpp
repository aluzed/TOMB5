// Synthetic matrices/vectors; CALCLARA and LIBGTE remain real translation units.
#include "SPECIFIC.H"
#include "CALCLARA.H"
#include "LARA.H"
#include "DRAW.H"
#include "GTEREG.H"
#include <cstring>
#include <cstdio>

struct MATRIX3D lara_joint_matrices[15];
struct ITEM_INFO item;
struct ITEM_INFO* lara_item = &item;

int main()
{
    static_assert(sizeof(void*) == 4 && sizeof(long) == 4, "i386 ABI required");
    static_assert(sizeof(MATRIX3D) == 32, "joint matrix layout");
    const int values[] = {0, 1, 0xfff, 0x1000, 0x1fff, 0x2000, 0x4000,
                          0x7fff, 0x8000, 0x9001, 0xabcd, 0xefff, 0xf000, 0xffff};
    int failures = 0;
    for (int value : values)
    for (int variant = 0; variant < 2; ++variant)
    for (int vector = 0; vector < 3; ++vector)
    {
        memset(&gteRegs, 0, sizeof(gteRegs));
        const unsigned before[8] = {0x1234fedc, 0x80017fff,
            0xabcd0000u | (unsigned)value, 0xffff3456, 0xffff8123,
            0x12345678, 0xfedcba98, 0x87654321};
        memcpy(&gteRegs.CP2C, before, sizeof(before));
        int joint[8] = {0x1000, 0, 0x1000, 0, 0x1000, 101, -202, 303};
        if (variant)
        {
            joint[0] = 0x0200f000; joint[1] = 0x1000fc00;
            joint[2] = (int)0xff000800u; joint[3] = 0x0400f800;
            joint[4] = -4096;
        }
        memcpy(&lara_joint_matrices[8], joint, sizeof(joint));
        MATRIX3D saved_joint = lara_joint_matrices[8];
        item.pos.x_pos = 12345; item.pos.y_pos = -23456; item.pos.z_pos = 34567;
        PHD_VECTOR pos = {vector == 0 ? 0 : (vector == 1 ? 16 : -65539),
                          vector == 0 ? 16 : (vector == 1 ? -64 : 32769),
                          vector == 0 ? 64 : (vector == 1 ? 100 : -98305)};
        int input[3] = {(int)pos.x, (int)pos.y, (int)pos.z};
        short rotation[9];
        memcpy(rotation, joint, sizeof(rotation));
        int expected[3];
        for (int row = 0; row < 3; ++row)
        {
            long long sum = 0;
            for (int column = 0; column < 3; ++column)
                sum += (long long)rotation[row * 3 + column] * input[column];
            expected[row] = (int)(sum >> 12) + joint[5 + row]
                           + (row == 0 ? 12345 : row == 1 ? -23456 : 34567);
        }
        GetLaraJointPos(&pos, 8);
        unsigned after[8];
        memcpy(after, &gteRegs.CP2C, sizeof(after));
        bool restored = memcmp(before, after, sizeof(before)) == 0;
        bool position = pos.x == expected[0] && pos.y == expected[1] && pos.z == expected[2];
        bool joint_unchanged = memcmp(&saved_joint, &lara_joint_matrices[8], sizeof(saved_joint)) == 0;
        printf("{\"value\":%d,\"variant\":%d,\"vector\":%d,\"restored\":%d,"
               "\"position\":%d,\"joint_unchanged\":%d,\"before\":%u,\"after\":%u}\n",
               value, variant, vector, restored, position, joint_unchanged, before[2], after[2]);
        failures += !restored || !position || !joint_unchanged;
    }
    return failures ? 1 : 0;
}
