#include "LIBPAD.H"

#include "LIBETC.H"
#include "EMULATOR.H"
#include "INPUTMAP.H"

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if defined(SDL2)
#include <SDL.h>

SDL_GameController* padHandle[MAX_CONTROLLERS];
#endif

unsigned char* padData[MAX_CONTROLLERS];
const unsigned char* keyboardState;

static InputMap g_inputMap;
static int g_inputMapReady = 0;
#if defined(SDL2)
static SDL_GameController* g_selectedPad = NULL;
#endif
static char g_inputConfigPath[1024];

static int input_file_exists(const char* path)
{
	FILE* file = fopen(path, "rb");
	if (file)
	{
		fclose(file);
		return 1;
	}
	return 0;
}

static void input_join_path(char* out, size_t outlen, const char* directory, const char* name)
{
	size_t length = directory ? strlen(directory) : 0;
	int needs_slash = length > 0 && directory[length - 1] != '/' && directory[length - 1] != '\\';
	snprintf(out, outlen, "%s%s%s", directory ? directory : "", needs_slash ? "/" : "", name);
}

static int input_save_default_config(void)
{
	if (InputMap_Save(&g_inputMap, g_inputConfigPath))
	{
		return 1;
	}

#if defined(SDL2)
	{
		char fallback[1024];
		char* directory = SDL_GetPrefPath("TOMB5", "Chronicles");
		if (!directory)
		{
			eprinterr("cannot write default input config: %s\n", InputMap_LastError());
			return 0;
		}
		input_join_path(fallback, sizeof(fallback), directory, "input.cfg");
		SDL_free(directory);
		if (!InputMap_Save(&g_inputMap, fallback))
		{
			eprinterr("cannot write default input config: %s\n", InputMap_LastError());
			return 0;
		}
		snprintf(g_inputConfigPath, sizeof(g_inputConfigPath), "%s", fallback);
		return 1;
	}
#else
	eprinterr("cannot write default input config: %s\n", InputMap_LastError());
	return 0;
#endif
}

static void input_config_load(void)
{
	const char* environment = InputMap_EnvPath();
	int result;

	g_inputConfigPath[0] = '\0';
	if (environment)
	{
		snprintf(g_inputConfigPath, sizeof(g_inputConfigPath), "%s", environment);
	}
	else if (input_file_exists("INPUT.CFG"))
	{
		snprintf(g_inputConfigPath, sizeof(g_inputConfigPath), "INPUT.CFG");
	}
	else
	{
#if defined(SDL2)
		char* pref = SDL_GetPrefPath("TOMB5", "Chronicles");
		if (pref)
		{
			char candidate[1024];
			input_join_path(candidate, sizeof(candidate), pref, "input.cfg");
			if (input_file_exists(candidate))
			{
				snprintf(g_inputConfigPath, sizeof(g_inputConfigPath), "%s", candidate);
			}
			SDL_free(pref);
		}
#endif
		if (!g_inputConfigPath[0])
		{
			snprintf(g_inputConfigPath, sizeof(g_inputConfigPath), "INPUT.CFG");
		}
	}

	result = InputMap_Load(&g_inputMap, g_inputConfigPath);
	if (result == 0)
	{
		InputMap_Defaults(&g_inputMap);
		if (input_save_default_config())
		{
			printf("[INPUT] Default configuration written to %s\n", g_inputConfigPath);
		}
	}
	else if (result < 0)
	{
		eprinterr("Input configuration: %s; using defaults\n", InputMap_LastError());
	}
	else
	{
		printf("[INPUT] Configuration loaded from %s\n", g_inputConfigPath);
	}

	if (!g_inputMap.keyboard_enabled && !g_inputMap.gamepad_enabled)
	{
		eprinterr("Both keyboard and gamepad are disabled; no input will be produced\n");
	}
	g_inputMapReady = 1;
}

#if defined(SDL2)
static int input_guid_matches(SDL_JoystickGUID guid, const char* text)
{
	char normalized[33];
	char actual[33];
	int length = 0;
	const char* cursor;

	if (!text || !*text)
	{
		return 0;
	}
	for (cursor = text; *cursor; ++cursor)
	{
		if (isxdigit((unsigned char)*cursor))
		{
			if (length >= 32)
			{
				return 0;
			}
			normalized[length++] = (char)tolower((unsigned char)*cursor);
		}
	}
	if (length != 32)
	{
		return 0;
	}
	normalized[32] = '\0';
	SDL_JoystickGetGUIDString(guid, actual, sizeof(actual));
	return SDL_strcasecmp(normalized, actual) == 0;
}

static SDL_GameController* input_open_gamepad(void)
{
	int count = SDL_NumJoysticks();
	int chosen = -1;
	int i;

	if (count <= 0)
	{
		eprinterr("Failed to locate a connected gamepad\n");
		return NULL;
	}

	{
		int ordinal = 0;
		for (i = 0; i < count; ++i)
		{
			if (SDL_IsGameController(i))
			{
				char guid[33];
				const char* name = SDL_JoystickNameForIndex(i);
				SDL_JoystickGetGUIDString(SDL_JoystickGetDeviceGUID(i), guid, sizeof(guid));
				printf("[INPUT] Available gamepad %d (SDL %d): %s (%s)\n",
				       ordinal, i, name ? name : "?", guid);
				++ordinal;
			}
		}
	}

	if (g_inputMap.gamepad_guid[0])
	{
		for (i = 0; i < count; ++i)
		{
			if (SDL_IsGameController(i) &&
			    input_guid_matches(SDL_JoystickGetDeviceGUID(i), g_inputMap.gamepad_guid))
			{
				chosen = i;
				break;
			}
		}
		if (chosen < 0)
		{
			eprinterr("Configured gamepad GUID %s was not found\n", g_inputMap.gamepad_guid);
		}
	}

	if (chosen < 0 && g_inputMap.gamepad_index >= 0)
	{
		int ordinal = 0;
		for (i = 0; i < count; ++i)
		{
			if (SDL_IsGameController(i))
			{
				if (ordinal == g_inputMap.gamepad_index)
				{
					chosen = i;
					break;
				}
				++ordinal;
			}
		}
	}

	if (chosen < 0)
	{
		for (i = 0; i < count; ++i)
		{
			if (SDL_IsGameController(i))
			{
				chosen = i;
				break;
			}
		}
	}

	if (chosen < 0)
	{
		eprinterr("No SDL game controller is available\n");
		return NULL;
	}

	{
		SDL_GameController* pad = SDL_GameControllerOpen(chosen);
		if (!pad)
		{
			eprinterr("Failed to open gamepad %d: %s\n", chosen, SDL_GetError());
			return NULL;
		}
		else
		{
			char guid[33];
			const char* name = SDL_GameControllerName(pad);
			SDL_JoystickGetGUIDString(SDL_JoystickGetDeviceGUID(chosen), guid, sizeof(guid));
			printf("[INPUT] Gamepad %d: %s (%s)\n",
			       chosen, name ? name : "?", guid);
			if (!g_inputMap.gamepad_guid[0])
			{
				snprintf(g_inputMap.gamepad_guid, sizeof(g_inputMap.gamepad_guid), "%s", guid);
			}
		}
		return pad;
	}
}

static void input_snapshot_keyboard(InputMapSnapshot* snapshot)
{
	const Uint8* state = SDL_GetKeyboardState(NULL);
	if (state)
	{
		memcpy(snapshot->keyboard, state,
		       sizeof(snapshot->keyboard) < SDL_NUM_SCANCODES
		           ? sizeof(snapshot->keyboard) : SDL_NUM_SCANCODES);
	}
}

static void input_snapshot_pad(InputMapSnapshot* snapshot, SDL_GameController* pad)
{
	static const SDL_GameControllerButton buttons[INPUTMAP_PAD_BUTTON_COUNT] =
	{
		SDL_CONTROLLER_BUTTON_A,
		SDL_CONTROLLER_BUTTON_B,
		SDL_CONTROLLER_BUTTON_X,
		SDL_CONTROLLER_BUTTON_Y,
		SDL_CONTROLLER_BUTTON_BACK,
		SDL_CONTROLLER_BUTTON_GUIDE,
		SDL_CONTROLLER_BUTTON_START,
		SDL_CONTROLLER_BUTTON_LEFTSTICK,
		SDL_CONTROLLER_BUTTON_RIGHTSTICK,
		SDL_CONTROLLER_BUTTON_LEFTSHOULDER,
		SDL_CONTROLLER_BUTTON_RIGHTSHOULDER,
		SDL_CONTROLLER_BUTTON_DPAD_UP,
		SDL_CONTROLLER_BUTTON_DPAD_DOWN,
		SDL_CONTROLLER_BUTTON_DPAD_LEFT,
		SDL_CONTROLLER_BUTTON_DPAD_RIGHT
	};
	static const SDL_GameControllerAxis axes[INPUTMAP_PAD_AXIS_COUNT] =
	{
		SDL_CONTROLLER_AXIS_LEFTX,
		SDL_CONTROLLER_AXIS_LEFTY,
		SDL_CONTROLLER_AXIS_RIGHTX,
		SDL_CONTROLLER_AXIS_RIGHTY,
		SDL_CONTROLLER_AXIS_TRIGGERLEFT,
		SDL_CONTROLLER_AXIS_TRIGGERRIGHT
	};
	int i;

	if (!pad)
	{
		return;
	}

	for (i = 0; i < INPUTMAP_PAD_BUTTON_COUNT; ++i)
	{
		snapshot->pad_buttons[i] = SDL_GameControllerGetButton(pad, buttons[i]) ? 1 : 0;
	}
	for (i = 0; i < INPUTMAP_PAD_AXIS_COUNT; ++i)
	{
		float value = (float)SDL_GameControllerGetAxis(pad, axes[i]) / 32767.0f;
		if (value < -1.0f) value = -1.0f;
		if (value > 1.0f) value = 1.0f;
		snapshot->pad_axes[i] = value;
	}
}
#endif

int InputMap_IsActive(void)
{
	return g_inputMapReady;
}

int InputMap_UsesControlOption(void)
{
	return g_inputMap.use_control_option;
}

unsigned long InputMap_PollActions(void)
{
	InputMapSnapshot snapshot;
	memset(&snapshot, 0, sizeof(snapshot));
#if defined(SDL2)
	input_snapshot_keyboard(&snapshot);
	if (g_selectedPad)
	{
		input_snapshot_pad(&snapshot, g_selectedPad);
	}
#endif
	return InputMap_EvaluateActions(&g_inputMap, &snapshot);
}

const InputMap* InputMap_Current(void)
{
	return &g_inputMap;
}

const char* InputMap_ConfigPath(void)
{
	return g_inputConfigPath;
}

int InputMap_SaveCurrent(void)
{
	if (!g_inputConfigPath[0])
	{
		return 0;
	}
	return InputMap_Save(&g_inputMap, g_inputConfigPath);
}

int InputMap_UpdateBinding(int device, int action, int slot, const InputMapBinding* binding)
{
	if (device < 0 || device >= INPUTMAP_DEVICE_COUNT ||
	    action < 0 || action >= INPUTMAP_ACTION_COUNT ||
	    slot < 0 || slot >= INPUTMAP_MAX_BINDINGS || !binding)
	{
		return 0;
	}
	g_inputMap.bindings[device][action][slot] = *binding;
	return InputMap_SaveCurrent();
}

#if defined(SDL2)
static void input_reopen_gamepad(void)
{
	if (g_selectedPad)
	{
		SDL_GameControllerClose(g_selectedPad);
		g_selectedPad = NULL;
	}
	padHandle[0] = NULL;
	if (g_inputMap.gamepad_enabled)
	{
		g_selectedPad = input_open_gamepad();
		padHandle[0] = g_selectedPad;
	}
}
#endif

int InputMap_ApplyGamepadConfig(void)
{
#if defined(SDL2)
	input_reopen_gamepad();
#endif
	return 1;
}

int InputMap_UpdateDevices(int keyboard_enabled, int gamepad_enabled, int gamepad_index)
{
	int saved;
	if (gamepad_index < -1)
	{
		return 0;
	}
	g_inputMap.keyboard_enabled = keyboard_enabled ? 1 : 0;
	g_inputMap.gamepad_enabled = gamepad_enabled ? 1 : 0;
	g_inputMap.gamepad_index = gamepad_index;
	saved = InputMap_SaveCurrent();
#if defined(SDL2)
	input_reopen_gamepad();
#endif
	return saved;
}

int InputMap_ResetDefaultsAndSave(void)
{
	int saved;
	InputMap_Defaults(&g_inputMap);
	saved = InputMap_SaveCurrent();
#if defined(SDL2)
	input_reopen_gamepad();
#endif
	return saved;
}

int InputMap_GamepadCount(void)
{
#if defined(SDL2)
	int count = 0;
	int i;
	for (i = 0; i < SDL_NumJoysticks(); ++i)
	{
		if (SDL_IsGameController(i))
		{
			++count;
		}
	}
	return count;
#else
	return 0;
#endif
}

const char* InputMap_GamepadNameAt(int index)
{
#if defined(SDL2)
	int ordinal = 0;
	int i;
	if (index < 0)
	{
		return NULL;
	}
	for (i = 0; i < SDL_NumJoysticks(); ++i)
	{
		if (SDL_IsGameController(i))
		{
			if (ordinal == index)
			{
				return SDL_JoystickNameForIndex(i);
			}
			++ordinal;
		}
	}
	return NULL;
#else
	(void)index;
	return NULL;
#endif
}

void PadInitDirect(unsigned char* pad1, unsigned char* pad2)
{
	if (pad1 != NULL)
	{
		padData[0] = pad1;
		padData[0][0] = 0xFF;
	}

	if (pad2 != NULL)
	{
		padData[1] = pad2;
		padData[1][0] = 0xFF;
	}

#if defined(SDL2)
	if (SDL_InitSubSystem(SDL_INIT_GAMECONTROLLER) < 0)
	{
		eprinterr("Failed to initialise subsystem GAMECONTROLLER\n");
	}

	keyboardState = SDL_GetKeyboardState(NULL);
#endif

	input_config_load();

#if defined(SDL2)
	if (g_inputMap.gamepad_enabled)
	{
		g_selectedPad = input_open_gamepad();
		if (g_selectedPad)
		{
			padHandle[0] = g_selectedPad;
		}
	}
	else
	{
		printf("[INPUT] Gamepad disabled by configuration\n");
	}
#endif
}

void PadInitMtap(unsigned char* unk00, unsigned char* unk01)
{
	UNIMPLEMENTED();
}

void PadInitGun(unsigned char* unk00, int unk01)
{
	UNIMPLEMENTED();
}

int PadChkVsync()
{
	UNIMPLEMENTED();
	return 0;
}

void PadStartCom()
{
	UNIMPLEMENTED();
}

void PadStopCom()
{
	UNIMPLEMENTED();
}

unsigned int PadEnableCom(unsigned int unk00)
{
	UNIMPLEMENTED();
	return 0;
}

void PadEnableGun(unsigned char unk00)
{
	UNIMPLEMENTED();
}

void PadRemoveGun()
{
	UNIMPLEMENTED();
}

int PadGetState(int port)
{
#if defined(SDL2)
#if _DEBUG || 1
	return PadStateStable;//FIXME should check if keyboard is connected
#endif
	if (!(SDL_GameControllerGetAttached(padHandle[port])))
	{
		return PadStateDiscon;
	}
	else
	{
		return PadStateStable;
	}

	return 0;
#else
	return 0;
#endif
}

int PadInfoMode(int unk00, int unk01, int unk02)
{
	return 7;//?
}

int PadInfoAct(int unk00, int unk01, int unk02)
{
	UNIMPLEMENTED();
	return 0;
}

int PadInfoComb(int unk00, int unk01, int unk02)
{
	UNIMPLEMENTED();
	return 0;
}

int PadSetActAlign(int unk00, unsigned char* unk01)
{
	UNIMPLEMENTED();
	return 0;
}

int PadSetMainMode(int socket, int offs, int lock)
{
	UNIMPLEMENTED();
	return 0;
}

void PadSetAct(int unk00, unsigned char* unk01, int unk02)
{
	UNIMPLEMENTED();
}

#if defined(SDL2)
unsigned short UpdateGameControllerInput(SDL_GameController* pad)
{
	InputMapSnapshot snapshot;
	memset(&snapshot, 0, sizeof(snapshot));
	input_snapshot_pad(&snapshot, pad);
	return InputMap_EvaluatePad(&g_inputMap, &snapshot, 0, 1);
}
#endif

unsigned short UpdateKeyboardInput()
{
	InputMapSnapshot snapshot;
	memset(&snapshot, 0, sizeof(snapshot));
#if defined(SDL2)
	input_snapshot_keyboard(&snapshot);
#endif
	return InputMap_EvaluatePad(&g_inputMap, &snapshot, 1, 0);
}

unsigned short UpdateKeyboardInputDebug()
{
	unsigned short ret = 0xFFFF;

#if defined(SDL2)
	//Not initialised yet
	if (keyboardStateDebug == NULL)
	{
		return ret;
	}

	SDL_PumpEvents();

	if (keyboardStateDebug[SDL_SCANCODE_X])//Square
	{
		ret &= ~0x8000;
	}

	if (keyboardStateDebug[SDL_SCANCODE_V])//Circle
	{
		ret &= ~0x2000;
	}

	if (keyboardStateDebug[SDL_SCANCODE_Z])//Triangle
	{
		ret &= ~0x1000;
	}

	if (keyboardStateDebug[SDL_SCANCODE_C])//Cross
	{
		ret &= ~0x4000;
	}

	if (keyboardStateDebug[SDL_SCANCODE_LSHIFT])//L1
	{
		ret &= ~0x400;
	}

	if (keyboardStateDebug[SDL_SCANCODE_RSHIFT])//R1
	{
		ret &= ~0x800;
	}

	if (keyboardStateDebug[SDL_SCANCODE_UP])//UP
	{
		ret &= ~0x10;
	}

	if (keyboardStateDebug[SDL_SCANCODE_DOWN])//DOWN
	{
		ret &= ~0x40;
	}

	if (keyboardStateDebug[SDL_SCANCODE_LEFT])//LEFT
	{
		ret &= ~0x80;
	}

	if (keyboardStateDebug[SDL_SCANCODE_RIGHT])//RIGHT
	{
		ret &= ~0x20;
	}

	if (keyboardStateDebug[SDL_SCANCODE_LCTRL])//L2
	{
		ret &= ~0x100;
	}

	if (keyboardStateDebug[SDL_SCANCODE_RCTRL])//R2
	{
		ret &= ~0x200;
	}

	if (keyboardStateDebug[SDL_SCANCODE_SPACE])//SELECT
	{
		ret &= ~0x1;
	}

	if (keyboardStateDebug[SDL_SCANCODE_RETURN])//START
	{
		ret &= ~0x8;
	}
#endif
	return ret;
}
