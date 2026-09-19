// Actual GAME/LARA.C regression. No copied implementation or target bytes.
// Only dispatch tables and unrelated animation/physics/services are doubles.
#include "LARA.H"
#include "CAMERA.H"
#include "COLLIDE.H"
#include "CONTROL.H"
#include "GAMEFLOW.H"
#include "LARAFIRE.H"
#include INPUT_H
#include <cstdio>
#include <cstdlib>
#include <cstring>

long input, BinocularRange, LaserSight;
unsigned short gfLevelFlags;
struct CAMERA_INFO camera;
static int clear_look, observed, control_calls, service_step, errors;
static long observed_input;
static short observed_head;
static unsigned short observed_flags;
static ITEM_INFO fixture_item;
static COLL_INFO fixture_coll;

static unsigned short flags() {
    unsigned short value;
    // Check the independently attributed look storage, not later ABI offsets.
    memcpy(&value, reinterpret_cast<unsigned char*>(&lara) + 68, sizeof(value));
    return value;
}
static void require(bool ok, const char* message) {
    if (!ok) { fprintf(stderr, "FAIL %s\n", message); ++errors; }
}
static void control(ITEM_INFO* item, COLL_INFO* coll) {
    require(item == &fixture_item && coll == &fixture_coll, "dispatch arguments");
    require(service_step++ == 0, "control order");
    ++control_calls;
    observed = lara.look;
    observed_input = input;
    observed_head = lara.head_y_rot;
    observed_flags = flags();
    if (clear_look) lara.look = FALSE;
}
static void collision(ITEM_INFO*, COLL_INFO*) {
    require(service_step++ == 3, "collision order");
}
// Explicit service doubles: no animation, world, collision, gun or triggers.
void AnimateLara(ITEM_INFO*) { require(service_step++ == 1, "animation order"); }
void LaraBaddieCollision(ITEM_INFO*, COLL_INFO*) { require(service_step++ == 2, "baddie order"); }
void UpdateLaraRoom(ITEM_INFO*, int height) {
    require(service_step++ == 4 && height == -381, "room service arguments/order");
}
void LaraGun() { require(service_step++ == 5, "gun order"); }
void TestTriggers(short* trigger, int heavy, int heavy_flags) {
    require(service_step++ == 6 && !trigger && !heavy && !heavy_flags, "trigger arguments/order");
}
// Strong test definitions replace only weak symbols on the private TU object.
void (*lara_control_routines[NUM_LARA_STATES + 1])(ITEM_INFO*, COLL_INFO*);
void (*lara_collision_routines[NUM_LARA_STATES + 1])(ITEM_INFO*, COLL_INFO*);

static void frame(long keys, int inhibit) {
    input = keys; clear_look = inhibit; service_step = 0;
    // Synthetic frame setup, not execution of the real camera controller.
    camera.type = CHASE_CAMERA;
    LaraAboveWater(&fixture_item, &fixture_coll);
    require(service_step == 7, "full wrapper returned through all services");
    printf("FRAME observed=%d final=%d input=%ld head=%d flags=%u camera=%d calls=%d\n",
           observed, lara.look, observed_input, observed_head, observed_flags, camera.type, control_calls);
}
int main(int argc, char** argv) {
    if (argc != 6) return 2;
    const int initial = atoi(argv[1]), keys = atoi(argv[2]), inhibit = atoi(argv[3]);
    const unsigned short neighbors = static_cast<unsigned short>(atoi(argv[4]) & ~4);
    const int sequence = atoi(argv[5]);
    memset(&lara, 0, sizeof(lara));
    memcpy(reinterpret_cast<unsigned char*>(&lara) + 68, &neighbors, sizeof(neighbors));
    lara.look = initial;
    require(flags() == (neighbors | (initial ? 4 : 0)), "real header look bit ABI");
    lara_item = &fixture_item;
    fixture_item.current_anim_state = STATE_LARA_STOP;
    lara_control_routines[STATE_LARA_STOP] = control;
    lara_collision_routines[STATE_LARA_STOP] = collision;
    if (sequence) {
        // Controller inhibits frame 1; frame 2 consumes that inhibition but
        // rearms; frame 3 recovers genuine LookLeftRight and consumes RIGHT.
        lara.look = TRUE;
        frame(IN_LOOK | IN_RIGHT, 1);
        require(observed == 1 && lara.look == 0 && observed_head == ANGLE(2), "sequence inhibition");
        lara.head_y_rot = lara.torso_y_rot = 0;
        frame(IN_LOOK | IN_RIGHT, 0);
        require(observed == 1 && lara.look == 1 && observed_head == 0 && (observed_input & IN_RIGHT), "sequence rearm frame");
        frame(IN_LOOK | IN_RIGHT, 0);
        require(observed == 1 && lara.look == 1 && observed_head == ANGLE(2) && !(observed_input & IN_RIGHT), "sequence recovery frame");
    } else {
        lara.head_y_rot = lara.torso_y_rot = 800;
        frame(keys, inhibit);
        const bool looking = initial && (keys & IN_LOOK);
        const int expected_head = looking ? 800 + ((keys & IN_LEFT) ? -ANGLE(2) : ((keys & IN_RIGHT) ? ANGLE(2) : 0)) : 700;
        const long expected_input = looking ? keys & ~((keys & IN_LEFT) ? IN_LEFT : IN_RIGHT) : keys;
        require(observed == 1, "control must observe look rearmed after Look/Reset");
        require(lara.look == !inhibit, "controller may clear rearmed look");
        require(observed_head == expected_head && lara.torso_y_rot == expected_head, "genuine Look/Reset head and torso");
        require(observed_input == expected_input, "genuine directional input consumption");
        require(camera.type == (looking ? LOOK_CAMERA : CHASE_CAMERA), "genuine Look camera selection");
    }
    require((observed_flags & ~4) == neighbors && (flags() & ~4) == neighbors, "adjacent flags preserved");
    return errors ? 1 : 0;
}
