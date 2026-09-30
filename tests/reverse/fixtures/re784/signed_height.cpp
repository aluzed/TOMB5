// Synthetic terminal cells: signed byte scaling and sentinel state only.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstring>
#include <cstddef>
#include <type_traits>
static_assert(sizeof(void*) == 4 && sizeof(int) == 4 && sizeof(long) == 4, "i386 ABI");
static_assert(sizeof(FLOOR_INFO) == 8 && offsetof(FLOOR_INFO, floor) == 5 && offsetof(FLOOR_INFO, ceiling) == 7, "floor layout");
room_info room_storage[1]; room_info* room = room_storage;
short data[16]; short* floor_data = data;
ITEM_INFO item_storage[1]; ITEM_INFO* items = item_storage;
object_info object_storage[1]; object_info* objects = object_storage;
int height_type, tiltxoff, tiltyoff, OnObject; short* trigger_index;
int main(int argc, char** argv) {
    if (argc != 2 || (strcmp(argv[1], "floor") && strcmp(argv[1], "ceiling"))) return 2;
    const bool ceiling = !strcmp(argv[1], "ceiling");
    int cases = 0, failures = 0;
    // Includes both extreme signed values and -127 sentinel; run negative first for UBSan RED.
    for (int value = -128; value <= 127; ++value) {
        FLOOR_INFO cell; memset(&cell, 0, sizeof cell);
        cell.pit_room = cell.sky_room = 255;
        const signed char byte = static_cast<signed char>(value);
        // Preserve the byte representation independently of the compiler's plain-char mode.
        memcpy(ceiling ? &cell.ceiling : &cell.floor, &byte, 1);
        FLOOR_INFO before; memcpy(&before, &cell, sizeof cell);
        height_type = 101; tiltxoff = 102; tiltyoff = 103; OnObject = 104;
        trigger_index = data + 7;
        const int result = ceiling ? GetCeiling(&cell, 1131, 100, 1757) : GetHeight(&cell, 1131, 100, 1757);
        const bool globals_ok = ceiling ?
            (height_type == 101 && tiltxoff == 102 && tiltyoff == 103 && OnObject == 104 && trigger_index == data + 7) :
            (height_type == 0 && tiltxoff == 0 && tiltyoff == 0 && OnObject == 0 && trigger_index == (value == -127 ? data + 7 : nullptr));
        const bool ok = result == value * 256 && globals_ok && !memcmp(&cell, &before, sizeof cell);
        ++cases; if (!ok) ++failures;
        printf("ROW family=%s value=%d result=%d state=%d unchanged=%d\n", argv[1], value, result, globals_ok, !memcmp(&cell, &before, sizeof cell));
    }
    printf("SUMMARY cases=%d failures=%d\n", cases, failures);
    return failures ? 1 : 0;
}
