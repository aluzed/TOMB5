// Entirely synthetic data; no captured RAM, assets or executable inputs.
// Contract is final-buffer equality only on disjoint buffers, not store order.
#include "DOOR.H"
#include "BOX.H"
#include "LOT.H"
#include <cstddef>
#include <cstdio>
#include <cstring>

box_info* boxes;
creature_info* baddie_slots;
static_assert(sizeof(void*) == 4, "i386 backend required");

template<class T> static void put(unsigned char* buffer, size_t offset, T value) {
    std::memcpy(buffer + offset, &value, sizeof(value));
}
static bool same(const void* a, const void* b, size_t n) {
    return std::memcmp(a, b, n) == 0;
}
static int failures = 0, cases = 0;
static void check(int present, short block, unsigned short overlap, int mode,
                  const unsigned char directions[4], int lift) {
    const bool mesh_present[6][4] = {
        {false, false, false, false}, {false, true, true, true},
        {true, false, true, false}, {true, true, true, false},
        {true, false, true, true}, {true, true, true, true}
    };
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
    DOORPOS_DATA* records[] = {&door.d1, &door.d1flip, &door.d2, &door.d2flip};
    for (int i = 0; i != 4; ++i) records[i]->floor = nullptr;
    door.d1.floor = present ? &floors[selected] : nullptr;
    door.d1.block = block;
    // Distinct synthetic saved floor; every byte is observably different.
    std::memset(&door.d1.data, 97, sizeof(door.d1.data));
    // Direct stores avoid creating misaligned short** for packed members.
    door.dptr1 = mesh_present[mode][0] ? meshes[0] : nullptr;
    door.dptr2 = mesh_present[mode][1] ? meshes[1] : nullptr;
    door.dptr3 = mesh_present[mode][2] ? meshes[2] : nullptr;
    door.dptr4 = mesh_present[mode][3] ? meshes[3] : nullptr;
    door.dn1 = directions[0]; door.dn2 = directions[1];
    door.dn3 = directions[2]; door.dn4 = directions[3];
    door.item = &item;
    const int selected_box = block == 2047 ? 9 : block;
    box_buffer[selected_box].overlap_index = static_cast<short>(overlap);
    boxes = box_buffer; baddie_slots = creatures; LiftDoor = lift;
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
        put(expected_floors, selected * sizeof(FLOOR_INFO), door.d1.data);
        if (block != 2047) {
            // Lift gate affects overlap only: LOT reset is unconditional here.
            if (!lift)
                put<short>(expected_boxes, selected_box * sizeof(box_info) +
                           offsetof(box_info, overlap_index),
                           static_cast<short>(overlap & ~BOX_BLOCKED));
            for (int i = 0; i != 5; ++i)
                put<short>(expected_creatures, i * sizeof(creature_info) +
                           offsetof(creature_info, LOT) + offsetof(lot_info, target_box), 2047);
        }
    }
    if (mesh_present[mode][0])
        for (int i = 0; i != 4; ++i)
            if (mesh_present[mode][i]) {
                // Select exactly one component. Bit 0 wins over bit 1.
                const int component = (directions[i] & 1) ? 0 :
                                      (directions[i] & 2) ? 1 : 2;
                const short sign = (directions[i] & 128) ? -1 : 1;
                put<short>(expected_meshes, i * sizeof(meshes[0]) +
                           component * sizeof(short), sign);
            }
    OpenThatDoor(&door.d1, &door);
    const bool ok[] = {
        same(floors, expected_floors, sizeof(floors)),
        same(box_buffer, expected_boxes, sizeof(box_buffer)),
        same(creatures, expected_creatures, sizeof(creatures)),
        same(meshes, expected_meshes, sizeof(meshes)),
        same(&door, expected_door, sizeof(door)),
        same(&item, expected_item, sizeof(item)),
        boxes == original_boxes && baddie_slots == original_slots && LiftDoor == lift
    };
    ++cases;
    bool passed = true;
    for (unsigned i = 0; i != sizeof(ok)/sizeof(ok[0]); ++i) passed &= ok[i];
    if (!passed) {
        ++failures;
        std::printf("FAIL case=%d floor=%d block=%d overlap=%u mesh=%d lift=%d dn=%u,%u,%u,%u buffers=%d%d%d%d%d%d%d\n",
                    cases, present, block, overlap, mode, lift,
                    directions[0], directions[1], directions[2], directions[3],
                    ok[0], ok[1], ok[2], ok[3], ok[4], ok[5], ok[6]);
    }
}
int main() {
    const short blocks[] = {2047, 0, 7, 15};
    const unsigned short overlaps[] = {1, 32769, 16385};
    const unsigned char values[] = {0, 1, 2, 3, 128, 129, 130, 131};
    for (int present = 0; present != 2; ++present)
    for (int b = 0; b != 4; ++b)
    for (int o = 0; o != 3; ++o)
    for (int m = 0; m != 6; ++m)
    for (int n = 0; n != 8; ++n)
    for (int lift = 0; lift != 2; ++lift) {
        const unsigned char directions[] = {values[n], static_cast<unsigned char>(values[n] ^ 128),
            static_cast<unsigned char>(values[n] ^ 3), static_cast<unsigned char>(values[n] ^ 131)};
        check(present, blocks[b], overlaps[o], m, directions, lift);
    }
    // Each full-byte sweep has all four meshes present; no field is masked.
    for (int field = 0; field != 4; ++field)
    for (int n = 0; n != 256; ++n) {
        unsigned char directions[] = {129, 2, 131, 0};
        directions[field] = static_cast<unsigned char>(n);
        check(1, 7, 49157, 5, directions, 0);
    }
    std::printf("SUMMARY cases=%d failures=%d\n", cases, failures);
    return failures ? 1 : 0;
}
