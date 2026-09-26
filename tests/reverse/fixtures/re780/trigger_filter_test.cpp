// Synthetic behavior tests; compile the complete source translation unit separately.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "SETUP.H"
#include <cstdio>
#include <cstring>
#include <vector>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <unistd.h>
static_assert(sizeof(void*) == 4 && sizeof(long) == 4 && sizeof(FLOOR_INFO) == 8, "32-bit ABI required");
room_info rooms[1]; room_info* room = rooms;
short data[256]; short* floor_data = data;
ITEM_INFO storage[4]; ITEM_INFO* items = storage;
object_info object_storage[2]; object_info* objects = object_storage;
int height_type, tiltxoff, tiltyoff, OnObject; short* trigger_index;
static std::vector<int> events;
static int bad_args;
static void callback(ITEM_INFO* item, int x, int y, int z, int* height) {
    events.push_back(int(item - storage));
    if (x != 117 || y != 231 || z != 349) ++bad_args;
    *height = 777; // Write-only fixture; RE-781 now propagates this output.
    OnObject = 91;
}
static unsigned short action(int type, int id, bool stop, bool extra = false) {
    return (type << 10) | id | (stop ? 32768 : 0) | (extra ? 16384 : 0);
}
static int checks, failures;
static bool run(const char* label, const std::vector<unsigned short>& words,
                const std::vector<int>& expected, bool present = true,
                unsigned inhibit = 0, bool protected_items = false) {
    std::memset(rooms, 0, sizeof rooms);
    std::memset(data, 0, sizeof data);
    std::memset(storage, 0, sizeof storage);
    std::memset(object_storage, 0, sizeof object_storage);
    items = storage;
    object_storage[0].floor = present ? callback : nullptr;
    for (int i = 0; i < 4; ++i) {
        storage[i].object_number = 0;
        storage[i].flags = (inhibit & (1u << i)) ? static_cast<short>(32768) : 0;
    }
    FLOOR_INFO floor{};
    floor.floor = 12; floor.pit_room = 255; floor.sky_room = 255; floor.index = 1;
    data[1] = static_cast<short>(32768 | TRIGGER_TYPE); data[2] = 0;
    for (unsigned i = 0; i < words.size(); ++i) data[i+3] = static_cast<short>(words[i]);
    short before_data[256]; std::memcpy(before_data, data, sizeof data);
    ITEM_INFO before_items[4]; std::memcpy(before_items, storage, sizeof storage);
    object_info before_objects[2]; std::memcpy(before_objects, object_storage, sizeof object_storage);
    events.clear(); bad_args = 0;
    height_type = 51; tiltxoff = 52; tiltyoff = 53; OnObject = 54; trigger_index = nullptr;
    void* guard = MAP_FAILED;
    if (protected_items) {
        guard = mmap(nullptr, 4096, PROT_NONE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (guard == MAP_FAILED) { std::perror("mmap"); return false; }
        items = static_cast<ITEM_INFO*>(guard);
    }
    short height = GetHeight(&floor, 117, 231, 349);
    if (protected_items) { munmap(guard, 4096); items = storage; }
    bool ok = events == expected && bad_args == 0 && height == (expected.empty() ? 3072 : 777) &&
        height_type == 0 && tiltxoff == 0 && tiltyoff == 0 &&
        OnObject == (expected.empty() ? 0 : 91) && trigger_index == data + 1 &&
        !std::memcmp(before_data, data, sizeof data) &&
        !std::memcmp(before_items, storage, sizeof storage) &&
        !std::memcmp(before_objects, object_storage, sizeof object_storage);
    std::printf("%s %s expected=", ok ? "PASS" : "FAIL", label);
    for (int e : expected) std::printf("%d,", e);
    std::printf(" actual="); for (int e : events) std::printf("%d,", e);
    std::printf(" height=%d args_errors=%d\n", height, bad_args);
    return ok;
}
static void check(const char* label, const std::vector<unsigned short>& words,
                  const std::vector<int>& expected, bool present = true, unsigned inhibit = 0) {
    ++checks; if (!run(label, words, expected, present, inhibit)) ++failures;
}
int main() {
    setvbuf(stdout, nullptr, _IONBF, 0);
    rlimit core_limit{0,0}; setrlimit(RLIMIT_CORE, &core_limit);
    for (int type = 0; type < 16; ++type)
      for (int bit = 0; bit < 2; ++bit)
       for (int present = 0; present < 2; ++present)
        for (int inhibit = 0; inhibit < 2; ++inhibit) {
            char label[96]; std::snprintf(label, sizeof label, "type%d-bit14%d-callback%d-inhibit%d", type, bit, present, inhibit);
            std::vector<unsigned short> words{action(type, 1, true, bit)};
            if (type == 1 || type == 12) words.push_back(32768);
            std::vector<int> expected;
            if (type == 0 && present && !inhibit) expected.push_back(1);
            check(label, words, expected, present, inhibit ? 2 : 0);
        }
    for (int type : {1, 12}) {
        char label[80];
        std::snprintf(label, sizeof label, "extended%d-header-stop-payload-continue", type);
        check(label, {action(type,1,true), 0, action(0,2,true)}, {2});
        std::snprintf(label, sizeof label, "extended%d-payload-stop", type);
        check(label, {action(type,1,false),32768,action(0,2,true)}, {});
        std::snprintf(label, sizeof label, "extended%d-payload-not-object", type);
        check(label, {action(type,1,false),3,action(0,2,true)}, {2});
    }
    check("object-stop-ignores-trailing", {action(0,1,true),action(0,2,true)}, {1});
    check("nonobject-stop-ignores-trailing", {action(8,1,true),action(0,2,true)}, {});
    check("mixed-order-inhibition", {action(8,1,false),action(0,2,false),action(1,1,false),3,action(0,1,false),action(12,1,false),0,action(15,3,false),action(0,3,true)}, {2,3}, true, 2);
    check("mixed-order-repeat", {action(0,2,false),action(8,1,false),action(0,1,false),action(0,2,true)}, {2,1,2});
    for (int type = 1; type < 16; ++type) {
        std::vector<unsigned short> words{action(type,1,true)};
        if (type == 1 || type == 12) words.push_back(32768);
        char label[80]; std::snprintf(label, sizeof label, "protected-items-type%d", type);
        ++checks;
        pid_t child = fork();
        if (child == 0) _exit(run(label, words, {}, true, 0, true) ? 0 : 1);
        int status = 0;
        if (child < 0 || waitpid(child, &status, 0) != child || !WIFEXITED(status) || WEXITSTATUS(status)) {
            ++failures;
            std::printf("FAIL %s child_status=%d\n", label, status);
        }
    }
    std::printf("SUMMARY checks=%d failures=%d\n", checks, failures);
    return failures ? 1 : 0;
}
