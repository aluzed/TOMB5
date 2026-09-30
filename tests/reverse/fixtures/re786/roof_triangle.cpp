// Synthetic roof records, actual production GetCeiling translation unit.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstring>
static_assert(sizeof(void*) == 4 && sizeof(long) == 4 && sizeof(FLOOR_INFO) == 8, "i386 ABI");
room_info room_storage[1]; room_info* room = room_storage;
short data[16]; short* floor_data = data;
ITEM_INFO item_storage[1]; ITEM_INFO* items = item_storage;
object_info object_storage[1]; object_info* objects = object_storage;
int height_type, tiltxoff, tiltyoff, OnObject; short* trigger_index;
static int signed5(int v) { return v < 16 ? v : v - 32; }
static int oracle(int type, int offset, int x, int z) {
    // Corners of the constructed shape: heights -1, -2, -4, -7.
    const bool reverse = type == 9 || type == 15 || type == 16;
    const bool first = reverse ? x + z > 1024 : z < x;
    const int dz = first ? -6 : -2;
    const int dx = first ? (reverse ? 1 : -3) : (reverse ? -3 : 1);
    int result = 3072 + signed5(offset) * 256;
    result += dz < 0 ? (z * dz >> 2) : -((1023 - z) * dz >> 2);
    result += dx < 0 ? ((1023 - x) * dx >> 2) : -(x * dx >> 2);
    return static_cast<short>(result);
}
int main() {
    const int types[] = {9, 10, 15, 16, 17, 18};
    const int coords[][2] = {{100,200},{200,100},{512,512},{900,200},{200,900},{824,200},{825,200},{823,200}};
    int cases = 0, failures = 0;
    for (int type : types) for (int offset = 0; offset < 32; ++offset) for (const auto& coord : coords) {
        const int x=coord[0], z=coord[1];
        FLOOR_INFO cell; memset(&cell, 0, sizeof cell);
        cell.pit_room=cell.sky_room=255; cell.ceiling=12; cell.index=1;
        memset(data, 0, sizeof data);
        data[1]=static_cast<short>(32768 | type | (offset << 5) | (offset << 10));
        data[2]=0x7421;
        short original_data[16]; memcpy(original_data,data,sizeof data);
        FLOOR_INFO original_cell; memcpy(&original_cell,&cell,sizeof cell);
        height_type=101; tiltxoff=102; tiltyoff=103; OnObject=104; trigger_index=data+9;
        const int got=GetCeiling(&cell,x,100,z), expected=oracle(type,offset,x,z);
        const bool unchanged=!memcmp(data,original_data,sizeof data) && !memcmp(&cell,&original_cell,sizeof cell);
        const bool state=height_type==101 && tiltxoff==102 && tiltyoff==103 && OnObject==104 && trigger_index==data+9;
        ++cases; if (got!=expected || !state || !unchanged) ++failures;
        printf("ROW type=%d offset=%d x=%d z=%d result=%d expected=%d state=%d unchanged=%d\n",type,offset,x,z,got,expected,state,unchanged);
    }
    printf("SUMMARY cases=%d failures=%d\n",cases,failures);
    return failures ? 1 : 0;
}
