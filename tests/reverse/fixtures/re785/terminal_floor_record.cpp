// Synthetic allocated floor-data suffixes; terminal floor records exclude following roof slope.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstring>
#include <cstddef>
static_assert(sizeof(void*) == 4 && sizeof(long) == 4 && sizeof(FLOOR_INFO) == 8, "i386 ABI");
room_info room_storage[1]; room_info* room = room_storage;
short data[16]; short* floor_data = data;
ITEM_INFO item_storage[1]; ITEM_INFO* items = item_storage;
object_info object_storage[1]; object_info* objects = object_storage;
int height_type, tiltxoff, tiltyoff, OnObject; short* trigger_index;
int main() {
    const int types[] = {2, 7, 8, 11, 12, 13, 14};
    const unsigned short slopes[] = {0, 1, 256, 65027};
    const int x = 1131, z = 1757, base = 3072;
    int cases = 0, failures = 0;
    for (int type : types) for (int terminal = 0; terminal <= 1; ++terminal) for (auto slope : slopes) {
        FLOOR_INFO cell; memset(&cell, 0, sizeof cell);
        cell.pit_room = cell.sky_room = 255; cell.ceiling = 12; cell.index = 1;
        memset(data, 0, sizeof data);
        data[1] = static_cast<short>(type | (terminal ? 32768 : 0));
        data[3] = static_cast<short>(32768 | 3); data[4] = static_cast<short>(slope);
        short original_data[16]; memcpy(original_data, data, sizeof data);
        FLOOR_INFO original_cell; memcpy(&original_cell, &cell, sizeof cell);
        height_type = 101; tiltxoff = 102; tiltyoff = 103; OnObject = 104; trigger_index = data + 9;
        const int got = GetCeiling(&cell, x, 100, z);
        int expected = base;
        if (!terminal) {
            const int a1 = static_cast<signed char>(slope >> 8), a2 = static_cast<signed char>(slope & 255);
            expected += a1 < 0 ? ((z & 1023) * a1 >> 2) : -(((1023 - z) & 1023) * a1 >> 2);
            expected += a2 < 0 ? (((1023 - x) & 1023) * a2 >> 2) : -((x & 1023) * a2 >> 2);
        }
        const bool unchanged = !memcmp(data, original_data, sizeof data) && !memcmp(&cell, &original_cell, sizeof cell);
        const bool state = height_type == 101 && tiltxoff == 102 && tiltyoff == 103 && OnObject == 104 && trigger_index == data + 9;
        ++cases; if (got != expected || !unchanged || !state) ++failures;
        printf("ROW type=%d terminal=%d slope=%u result=%d expected=%d state=%d unchanged=%d\n", type, terminal, slope, got, expected, state, unchanged);
    }
    printf("SUMMARY cases=%d failures=%d\n", cases, failures);
    return failures ? 1 : 0;
}
