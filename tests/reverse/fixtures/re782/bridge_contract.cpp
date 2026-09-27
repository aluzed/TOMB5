#include "OBJECTS.H"
#include "CONTROL.H"
#include "COLLIDE.H"
#include <cstdio>
#include <cstring>
#include <initializer_list>
#include <cstddef>

int height_type, OnObject;
static_assert(sizeof(long) == 4 && sizeof(int) == 4 && sizeof(void*) == 4, "i386 ABI");
static_assert(offsetof(ITEM_INFO, pos) == 64 && sizeof(ITEM_INFO) == 144, "attributed item layout");
using Callback = void (*)(ITEM_INFO*, long, long, long, long*);
static Callback callbacks[] = {BridgeFlatFloor, BridgeFlatCeiling, BridgeTilt1Floor,
    BridgeTilt1Ceiling, BridgeTilt2Floor, BridgeTilt2Ceiling};

int main()
{
    const int coordinates[][2] = {{0,0}, {1,3}, {1023,1022}, {1024,1025},
        {-1,-3}, {-1025,2047}, {1131,1757}};
    int checks = 0, failures = 0;
    for (int fn = 0; fn < 6; ++fn)
    for (int rotation : {0, -32768, 16384, -16384, 1234})
    for (const auto& coordinate : coordinates)
    for (int base : {-512, 4096})
    for (int delta : {-1, 0, 1})
    {
        int x = coordinate[0], z = coordinate[1];
        int offset = (rotation == 0 ? -x : rotation == -32768 ? x :
                      rotation == 16384 ? z : -z) & 1023;
        int level = base + (fn < 2 ? 0 : offset / (fn < 4 ? 4 : 2));
        int query = level + delta;
        bool ceiling = (fn & 1) != 0;
        bool writes = ceiling ? query > level : query <= level;
        ITEM_INFO item{};
        item.pos.x_pos = -3000;
        item.pos.y_pos = base;
        item.pos.z_pos = 7000;
        item.pos.y_rot = rotation;
        ITEM_INFO before;
        memcpy(&before, &item, sizeof item);
        struct { long before, height, after; } output = {1234567, -123456789, 7654321};
        height_type = 77;
        OnObject = 88;
        callbacks[fn](&item, x, query, z, &output.height);
        long expected = writes ? level + (ceiling ? 256 : 0) : -123456789;
        bool ok = output.height == expected && output.before == 1234567 &&
            output.after == 7654321 && !memcmp(&before, &item, sizeof item) &&
            height_type == (writes && !ceiling ? WALL : 77) &&
            OnObject == (writes && !ceiling ? 1 : 88);
        ++checks;
        if (!ok) ++failures;
        printf("%s fn=%d rotation=%d x=%d z=%d base=%d delta=%d expected=%ld actual=%ld\n",
               ok ? "PASS" : "FAIL", fn, rotation, x, z, base, delta, expected, output.height);
    }
    printf("SUMMARY checks=%d failures=%d\n", checks, failures);
    return failures ? 1 : 0;
}
