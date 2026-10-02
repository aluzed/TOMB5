// Synthetic contract only: no asset, executable payload, or captured game state.
#include "DOOR.H"
#include "BOX.H"
#include "LOT.H"
#include <cstddef>
#include <cstdio>
#include <cstring>

box_info* boxes;
creature_info* baddie_slots;
static_assert(sizeof(void*) == 4, "This backend requires an i386 build");

// Expected buffers are copies of the input with only contract-authorized byte
// ranges replaced. They never come from another execution of ShutThatDoor.
template<class T> static void put(unsigned char* buffer, size_t offset, T value) {
    std::memcpy(buffer + offset, &value, sizeof(value));
}
static bool same(const void* actual, const void* expected, size_t bytes) {
    return std::memcmp(actual, expected, bytes) == 0;
}

int main() {
    const short blocks[] = {2047, 0, 7, 15};
    const unsigned short overlaps[] = {1, 32769, 16385};
    // First two exercise the absent primary gate, including populated others.
    // Remaining four cover all optional mesh combinations with mandatory third.
    const bool mesh_present[6][4] = {
        {false, false, false, false}, {false, true, true, true},
        {true, false, true, false}, {true, true, true, false},
        {true, false, true, true}, {true, true, true, true}
    };
    int cases = 0, failures = 0;
    for (int present = 0; present != 2; ++present)
    for (int b = 0; b != 4; ++b)
    for (int o = 0; o != 3; ++o)
    for (int m = 0; m != 6; ++m) {
        FLOOR_INFO floors[32];
        box_info box_buffer[16];
        creature_info creatures[5];
        short meshes[4][8];
        DOOR_DATA door;
        ITEM_INFO item = {};
        std::memset(floors, 53, sizeof(floors));
        std::memset(box_buffer, 71, sizeof(box_buffer));
        std::memset(creatures, 0, sizeof(creatures));
        std::memset(&door, 83, sizeof(door));
        for (int i = 0; i != 5; ++i) {
            creatures[i].joint_rotation[0] = 101 + i;
            creatures[i].flags = 117 + i;
            creatures[i].LOT.head = 131 + i;
            creatures[i].LOT.tail = 149 + i;
            creatures[i].LOT.search_number = 167 + i;
            creatures[i].LOT.target_box = 181 + i;
            creatures[i].LOT.required_box = 199 + i;
            creatures[i].LOT.target.x = 211 + i;
        }
        for (int i = 0; i != 4; ++i)
            for (int j = 0; j != 8; ++j) meshes[i][j] = 241 + 17*i + j;
        const int selected = 11;
        floors[selected].fx = m;
        floors[selected].stopper = (b + o + m) % 2;
        DOORPOS_DATA* records[] = {&door.d1, &door.d1flip, &door.d2, &door.d2flip};
        for (int i = 0; i != 4; ++i) records[i]->floor = nullptr;
        door.d1.floor = present ? &floors[selected] : nullptr;
        door.d1.block = blocks[b];
        // Direct member stores preserve the real header's packed alignment;
        // taking short** to these packed pointer members would be undefined.
        door.dptr1 = mesh_present[m][0] ? meshes[0] : nullptr;
        door.dptr2 = mesh_present[m][1] ? meshes[1] : nullptr;
        door.dptr3 = mesh_present[m][2] ? meshes[2] : nullptr;
        door.dptr4 = mesh_present[m][3] ? meshes[3] : nullptr;
        door.item = &item;
        // Sentinel cases still have an initialized neighbor to detect stray writes.
        const int selected_box = blocks[b] == 2047 ? 9 : blocks[b];
        box_buffer[selected_box].overlap_index = static_cast<short>(overlaps[o]);
        boxes = box_buffer;
        baddie_slots = creatures;
        box_info* const original_boxes = boxes;
        creature_info* const original_slots = baddie_slots;
        unsigned char expected_floors[sizeof(floors)], expected_boxes[sizeof(box_buffer)];
        unsigned char expected_creatures[sizeof(creatures)], expected_meshes[sizeof(meshes)];
        unsigned char expected_door[sizeof(door)], expected_item[sizeof(item)];
        std::memcpy(expected_floors, floors, sizeof(floors));
        std::memcpy(expected_boxes, box_buffer, sizeof(box_buffer));
        std::memcpy(expected_creatures, creatures, sizeof(creatures));
        std::memcpy(expected_meshes, meshes, sizeof(meshes));
        std::memcpy(expected_door, &door, sizeof(door));
        std::memcpy(expected_item, &item, sizeof(item));
        if (present) {
            // Human contract: close the selected cell, retaining fx and stopper.
            FLOOR_INFO closed = floors[selected];
            closed.index = 0;
            closed.box = 2047;
            closed.pit_room = closed.sky_room = 255;
            closed.floor = closed.ceiling = -127;
            put(expected_floors, selected * sizeof(FLOOR_INFO), closed);
            // Every non-sentinel block is blocked, regardless of its high bit;
            // exactly five LOT destinations become the no-box sentinel.
            if (blocks[b] != 2047) {
                put<short>(expected_boxes, selected_box * sizeof(box_info) +
                           offsetof(box_info, overlap_index),
                           static_cast<short>(overlaps[o] | BOX_BLOCKED));
                for (int i = 0; i != 5; ++i)
                    put<short>(expected_creatures, i * sizeof(creature_info) +
                               offsetof(creature_info, LOT) + offsetof(lot_info, target_box), 2047);
            }
        }
        // Mesh closure is independent of floor presence. Only the first three
        // shorts change, and only when the primary pointer gate is populated.
        if (mesh_present[m][0])
            for (int i = 0; i != 4; ++i)
                if (mesh_present[m][i])
                    std::memset(expected_meshes + i * sizeof(meshes[0]), 0, 3 * sizeof(short));
        ShutThatDoor(&door.d1, &door);
        const bool floor_ok = same(floors, expected_floors, sizeof(floors));
        const bool box_ok = same(box_buffer, expected_boxes, sizeof(box_buffer));
        const bool creature_ok = same(creatures, expected_creatures, sizeof(creatures));
        const bool mesh_ok = same(meshes, expected_meshes, sizeof(meshes));
        const bool door_ok = same(&door, expected_door, sizeof(door));
        const bool globals_ok = boxes == original_boxes && baddie_slots == original_slots;
        const bool item_ok = same(&item, expected_item, sizeof(item));
        ++cases;
        if (!(floor_ok && box_ok && creature_ok && mesh_ok && door_ok && globals_ok && item_ok)) {
            ++failures;
            std::printf("FAIL floor=%d block=%d overlap=%u mesh=%d buffers=%d%d%d%d%d%d%d\n",
                        present, blocks[b], overlaps[o], m, floor_ok, box_ok, creature_ok,
                        mesh_ok, door_ok, globals_ok, item_ok);
        }
    }
    std::printf("SUMMARY cases=%d failures=%d\n", cases, failures);
    return failures ? 1 : 0;
}
