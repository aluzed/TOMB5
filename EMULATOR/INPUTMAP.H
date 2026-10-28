#ifndef INPUTMAP_H
#define INPUTMAP_H

/*
 * Configurable input mapping for the PSXPC_N port.
 *
 * The module is deliberately free of SDL calls so it can be unit-tested on the
 * host. LIBPAD.C fills an InputMapSnapshot from SDL and evaluates it here.
 *
 * Each action has two bindings per device.  A binding is a keyboard scancode,
 * a game-controller button or a game-controller axis direction.  The same
 * physical input may be bound to several actions; the evaluator simply ORs
 * them, matching the original pad behaviour.
 */

#include <stddef.h>

#define INPUTMAP_MAX_BINDINGS 2
#define INPUTMAP_KEY_COUNT 512
#define INPUTMAP_PAD_BUTTON_COUNT 15
#define INPUTMAP_PAD_AXIS_COUNT 6

/* Semantic input bits, kept in sync with GAME/CONTROL.H (input_buttons).
 * They are duplicated here so the emulator module has no game-header
 * dependency; inputmap_harness.cpp static-asserts the values. */
#define INPUTMAP_IN_FORWARD 0x00000001UL
#define INPUTMAP_IN_BACK    0x00000002UL
#define INPUTMAP_IN_LEFT    0x00000004UL
#define INPUTMAP_IN_RIGHT   0x00000008UL
#define INPUTMAP_IN_JUMP    0x00000010UL
#define INPUTMAP_IN_DRAW    0x00000020UL
#define INPUTMAP_IN_ACTION  0x00000040UL
#define INPUTMAP_IN_WALK    0x00000080UL
#define INPUTMAP_IN_LOOK    0x00000200UL
#define INPUTMAP_IN_ROLL    0x00001000UL
#define INPUTMAP_IN_DUCK    0x20000000UL
#define INPUTMAP_IN_SPRINT  0x40000000UL

/* Active-high raw PSX pad bits (see input_raw in CONTROL.H). */
#define INPUTMAP_RAW_SELECT 0x0001
#define INPUTMAP_RAW_START  0x0008
#define INPUTMAP_RAW_UP     0x0010
#define INPUTMAP_RAW_RIGHT  0x0020
#define INPUTMAP_RAW_DOWN   0x0040
#define INPUTMAP_RAW_LEFT   0x0080
#define INPUTMAP_RAW_L2     0x0100
#define INPUTMAP_RAW_R2     0x0200
#define INPUTMAP_RAW_L1     0x0400
#define INPUTMAP_RAW_R1     0x0800
#define INPUTMAP_RAW_TRIANGLE 0x1000
#define INPUTMAP_RAW_CIRCLE   0x2000
#define INPUTMAP_RAW_CROSS    0x4000
#define INPUTMAP_RAW_SQUARE   0x8000


typedef enum
{
	INPUTMAP_DEVICE_KEYBOARD = 0,
	INPUTMAP_DEVICE_GAMEPAD = 1,
	INPUTMAP_DEVICE_COUNT = 2
} InputMapDevice;

typedef enum
{
	INPUTMAP_BIND_NONE = 0,
	INPUTMAP_BIND_KEY,
	INPUTMAP_BIND_PAD_BUTTON,
	INPUTMAP_BIND_PAD_AXIS
} InputMapBindType;

typedef enum
{
	INPUTMAP_PAD_A = 0,
	INPUTMAP_PAD_B,
	INPUTMAP_PAD_X,
	INPUTMAP_PAD_Y,
	INPUTMAP_PAD_BACK,
	INPUTMAP_PAD_GUIDE,
	INPUTMAP_PAD_START,
	INPUTMAP_PAD_LEFTSTICK,
	INPUTMAP_PAD_RIGHTSTICK,
	INPUTMAP_PAD_LEFTSHOULDER,
	INPUTMAP_PAD_RIGHTSHOULDER,
	INPUTMAP_PAD_DPAD_UP,
	INPUTMAP_PAD_DPAD_DOWN,
	INPUTMAP_PAD_DPAD_LEFT,
	INPUTMAP_PAD_DPAD_RIGHT
} InputMapPadButton;

typedef enum
{
	INPUTMAP_AXIS_LEFTX = 0,
	INPUTMAP_AXIS_LEFTY,
	INPUTMAP_AXIS_RIGHTX,
	INPUTMAP_AXIS_RIGHTY,
	INPUTMAP_AXIS_TRIGGERLEFT,
	INPUTMAP_AXIS_TRIGGERRIGHT
} InputMapPadAxis;

typedef enum
{
	INPUTMAP_ACTION_FORWARD = 0,
	INPUTMAP_ACTION_BACK,
	INPUTMAP_ACTION_LEFT,
	INPUTMAP_ACTION_RIGHT,
	INPUTMAP_ACTION_ACTION,
	INPUTMAP_ACTION_JUMP,
	INPUTMAP_ACTION_DRAW,
	INPUTMAP_ACTION_ROLL,
	INPUTMAP_ACTION_LOOK,
	INPUTMAP_ACTION_DUCK,
	INPUTMAP_ACTION_WALK,
	INPUTMAP_ACTION_SPRINT,
	INPUTMAP_ACTION_START,
	INPUTMAP_ACTION_SELECT,
	INPUTMAP_ACTION_COUNT
} InputMapAction;

typedef struct
{
	unsigned char type;   /* InputMapBindType */
	unsigned short code;  /* scancode, pad button or pad axis */
	signed char direction;/* +1/-1 for axes, 0 otherwise */
} InputMapBinding;

typedef struct
{
	int keyboard_enabled;
	int gamepad_enabled;
	int gamepad_index;         /* -1 = first available controller */
	char gamepad_guid[64];     /* optional exact device GUID */
	float axis_deadzone;       /* 0.0 .. 1.0 */
	int use_control_option;    /* 1 = keep the legacy PSX control schemes */
	InputMapBinding bindings[INPUTMAP_DEVICE_COUNT][INPUTMAP_ACTION_COUNT][INPUTMAP_MAX_BINDINGS];
} InputMap;

typedef struct
{
	unsigned char keyboard[INPUTMAP_KEY_COUNT];
	unsigned char pad_buttons[INPUTMAP_PAD_BUTTON_COUNT];
	float pad_axes[INPUTMAP_PAD_AXIS_COUNT];
} InputMapSnapshot;

/* Fill a map with the built-in defaults (WASD + arrows, PSX-style pad). */
void InputMap_Defaults(InputMap* map);

/* 1 = loaded, 0 = file missing (map reset to defaults), -1 = parse error. */
int InputMap_Load(InputMap* map, const char* path);

/* 1 = written.  The output is deterministic and can be loaded again. */
int InputMap_Save(const InputMap* map, const char* path);

/* Optional environment override used by LIBPAD.C: TOMB5_INPUT_CONFIG. */
const char* InputMap_EnvPath(void);

const char* InputMap_LastError(void);
const char* InputMap_ActionName(int action);
int InputMap_ActionFromName(const char* name);
const char* InputMap_DeviceName(int device);

/* Parse/format one binding.  Error text is written to err (may be NULL). */
int InputMap_ParseBinding(int device, const char* text, InputMapBinding* out,
                          char* err, size_t errlen);
int InputMap_FormatBinding(const InputMapBinding* binding, char* out, size_t outlen);

/* Pure evaluation.  IN_* bits are returned for EvaluateActions; EvaluatePad
 * returns active-low PSX pad bits (0xFFFF = nothing pressed). */
unsigned long InputMap_EvaluateActions(const InputMap* map, const InputMapSnapshot* snapshot);
unsigned short InputMap_EvaluatePad(const InputMap* map, const InputMapSnapshot* snapshot,
                                    int include_keyboard, int include_gamepad);

/* Build a binding from an SDL scancode/button/axis for the in-game editor. */
int InputMap_BindingFromKey(int scancode, InputMapBinding* out);
int InputMap_BindingFromButton(int button, InputMapBinding* out);
int InputMap_BindingFromAxis(int axis, int direction, InputMapBinding* out);

/* Implemented by LIBPAD.C after SDL initialisation. */
int InputMap_IsActive(void);
int InputMap_UsesControlOption(void);
unsigned long InputMap_PollActions(void);

/* In-game editor accessors.  Every mutator writes INPUT.CFG immediately. */
const InputMap* InputMap_Current(void);
const char* InputMap_ConfigPath(void);
int InputMap_SaveCurrent(void);
int InputMap_UpdateBinding(int device, int action, int slot, const InputMapBinding* binding);
int InputMap_UpdateDevices(int keyboard_enabled, int gamepad_enabled, int gamepad_index);
int InputMap_ResetDefaultsAndSave(void);
int InputMap_ApplyGamepadConfig(void);
int InputMap_GamepadCount(void);
const char* InputMap_GamepadNameAt(int index);

#endif
