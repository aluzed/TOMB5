#include "INPUTMAP.H"

#include <ctype.h>
#include <errno.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <SDL_scancode.h>

#define INPUTMAP_LINE_MAX 1024

typedef struct
{
	const char* name;
	const char* alias;
	unsigned long action_bit;
	unsigned short pad_bit;
} InputMapActionDef;

static const InputMapActionDef action_defs[INPUTMAP_ACTION_COUNT] =
{
	{ "forward", "up",      INPUTMAP_IN_FORWARD, INPUTMAP_RAW_UP },
	{ "back",    "down",    INPUTMAP_IN_BACK,    INPUTMAP_RAW_DOWN },
	{ "left",    "left",    INPUTMAP_IN_LEFT,    INPUTMAP_RAW_LEFT },
	{ "right",   "right",   INPUTMAP_IN_RIGHT,   INPUTMAP_RAW_RIGHT },
	{ "action",  "confirm", INPUTMAP_IN_ACTION,  INPUTMAP_RAW_CROSS },
	{ "jump",    "jump",    INPUTMAP_IN_JUMP,    INPUTMAP_RAW_SQUARE },
	{ "draw",    "cancel",  INPUTMAP_IN_DRAW,    INPUTMAP_RAW_TRIANGLE },
	{ "roll",    "roll",    INPUTMAP_IN_ROLL,    INPUTMAP_RAW_CIRCLE },
	{ "look",    "look",    INPUTMAP_IN_LOOK,    INPUTMAP_RAW_L1 },
	{ "duck",    "crouch",  INPUTMAP_IN_DUCK,    INPUTMAP_RAW_L2 },
	{ "walk",    "walk",    INPUTMAP_IN_WALK,    INPUTMAP_RAW_R1 },
	{ "sprint",  "run",     INPUTMAP_IN_SPRINT,  INPUTMAP_RAW_R2 },
	{ "start",   "pause",   0,          INPUTMAP_RAW_START },
	{ "select",  "inventory", 0,        INPUTMAP_RAW_SELECT }
};

typedef struct
{
	const char* name;
	int code;
} InputMapName;

static const InputMapName keyboard_names[] =
{
	{ "A", SDL_SCANCODE_A }, { "B", SDL_SCANCODE_B }, { "C", SDL_SCANCODE_C },
	{ "D", SDL_SCANCODE_D }, { "E", SDL_SCANCODE_E }, { "F", SDL_SCANCODE_F },
	{ "G", SDL_SCANCODE_G }, { "H", SDL_SCANCODE_H }, { "I", SDL_SCANCODE_I },
	{ "J", SDL_SCANCODE_J }, { "K", SDL_SCANCODE_K }, { "L", SDL_SCANCODE_L },
	{ "M", SDL_SCANCODE_M }, { "N", SDL_SCANCODE_N }, { "O", SDL_SCANCODE_O },
	{ "P", SDL_SCANCODE_P }, { "Q", SDL_SCANCODE_Q }, { "R", SDL_SCANCODE_R },
	{ "S", SDL_SCANCODE_S }, { "T", SDL_SCANCODE_T }, { "U", SDL_SCANCODE_U },
	{ "V", SDL_SCANCODE_V }, { "W", SDL_SCANCODE_W }, { "X", SDL_SCANCODE_X },
	{ "Y", SDL_SCANCODE_Y }, { "Z", SDL_SCANCODE_Z },
	{ "0", SDL_SCANCODE_0 }, { "1", SDL_SCANCODE_1 }, { "2", SDL_SCANCODE_2 },
	{ "3", SDL_SCANCODE_3 }, { "4", SDL_SCANCODE_4 }, { "5", SDL_SCANCODE_5 },
	{ "6", SDL_SCANCODE_6 }, { "7", SDL_SCANCODE_7 }, { "8", SDL_SCANCODE_8 },
	{ "9", SDL_SCANCODE_9 },
	{ "F1", SDL_SCANCODE_F1 }, { "F2", SDL_SCANCODE_F2 }, { "F3", SDL_SCANCODE_F3 },
	{ "F4", SDL_SCANCODE_F4 }, { "F5", SDL_SCANCODE_F5 }, { "F6", SDL_SCANCODE_F6 },
	{ "F7", SDL_SCANCODE_F7 }, { "F8", SDL_SCANCODE_F8 }, { "F9", SDL_SCANCODE_F9 },
	{ "F10", SDL_SCANCODE_F10 }, { "F11", SDL_SCANCODE_F11 }, { "F12", SDL_SCANCODE_F12 },
	{ "UP", SDL_SCANCODE_UP }, { "DOWN", SDL_SCANCODE_DOWN },
	{ "LEFT", SDL_SCANCODE_LEFT }, { "RIGHT", SDL_SCANCODE_RIGHT },
	{ "SPACE", SDL_SCANCODE_SPACE }, { "RETURN", SDL_SCANCODE_RETURN },
	{ "ESCAPE", SDL_SCANCODE_ESCAPE }, { "TAB", SDL_SCANCODE_TAB },
	{ "BACKSPACE", SDL_SCANCODE_BACKSPACE }, { "DELETE", SDL_SCANCODE_DELETE },
	{ "INSERT", SDL_SCANCODE_INSERT }, { "HOME", SDL_SCANCODE_HOME },
	{ "END", SDL_SCANCODE_END }, { "PAGEUP", SDL_SCANCODE_PAGEUP },
	{ "PAGEDOWN", SDL_SCANCODE_PAGEDOWN },
	{ "LSHIFT", SDL_SCANCODE_LSHIFT }, { "RSHIFT", SDL_SCANCODE_RSHIFT },
	{ "LCTRL", SDL_SCANCODE_LCTRL }, { "RCTRL", SDL_SCANCODE_RCTRL },
	{ "LALT", SDL_SCANCODE_LALT }, { "RALT", SDL_SCANCODE_RALT },
	{ "CAPSLOCK", SDL_SCANCODE_CAPSLOCK }, { "NUMLOCK", SDL_SCANCODE_NUMLOCKCLEAR },
	{ "SCROLLLOCK", SDL_SCANCODE_SCROLLLOCK },
	{ "PAUSE", SDL_SCANCODE_PAUSE }, { "PRINTSCREEN", SDL_SCANCODE_PRINTSCREEN },
	{ "MENU", SDL_SCANCODE_MENU },
	{ "GRAVE", SDL_SCANCODE_GRAVE }, { "MINUS", SDL_SCANCODE_MINUS },
	{ "EQUALS", SDL_SCANCODE_EQUALS }, { "LEFTBRACKET", SDL_SCANCODE_LEFTBRACKET },
	{ "RIGHTBRACKET", SDL_SCANCODE_RIGHTBRACKET },
	{ "BACKSLASH", SDL_SCANCODE_BACKSLASH }, { "SEMICOLON", SDL_SCANCODE_SEMICOLON },
	{ "APOSTROPHE", SDL_SCANCODE_APOSTROPHE }, { "COMMA", SDL_SCANCODE_COMMA },
	{ "PERIOD", SDL_SCANCODE_PERIOD }, { "SLASH", SDL_SCANCODE_SLASH },
	{ "KP0", SDL_SCANCODE_KP_0 }, { "KP1", SDL_SCANCODE_KP_1 },
	{ "KP2", SDL_SCANCODE_KP_2 }, { "KP3", SDL_SCANCODE_KP_3 },
	{ "KP4", SDL_SCANCODE_KP_4 }, { "KP5", SDL_SCANCODE_KP_5 },
	{ "KP6", SDL_SCANCODE_KP_6 }, { "KP7", SDL_SCANCODE_KP_7 },
	{ "KP8", SDL_SCANCODE_KP_8 }, { "KP9", SDL_SCANCODE_KP_9 },
	{ "KP_ENTER", SDL_SCANCODE_KP_ENTER }, { "KP_PLUS", SDL_SCANCODE_KP_PLUS },
	{ "KP_MINUS", SDL_SCANCODE_KP_MINUS },
	{ "KP_MULTIPLY", SDL_SCANCODE_KP_MULTIPLY },
	{ "KP_DIVIDE", SDL_SCANCODE_KP_DIVIDE },
	{ "KP_PERIOD", SDL_SCANCODE_KP_PERIOD },
	{ NULL, 0 }
};

static const InputMapName keyboard_aliases[] =
{
	{ "ENTER", SDL_SCANCODE_RETURN },
	{ "ESC", SDL_SCANCODE_ESCAPE },
	{ "CTRL", SDL_SCANCODE_LCTRL },
	{ "SHIFT", SDL_SCANCODE_LSHIFT },
	{ "ALT", SDL_SCANCODE_LALT },
	{ "SPACEBAR", SDL_SCANCODE_SPACE },
	{ NULL, 0 }
};

static const InputMapName pad_buttons[] =
{
	{ "A", INPUTMAP_PAD_A },
	{ "B", INPUTMAP_PAD_B },
	{ "X", INPUTMAP_PAD_X },
	{ "Y", INPUTMAP_PAD_Y },
	{ "BACK", INPUTMAP_PAD_BACK },
	{ "SELECT", INPUTMAP_PAD_BACK },
	{ "GUIDE", INPUTMAP_PAD_GUIDE },
	{ "START", INPUTMAP_PAD_START },
	{ "LEFTSTICK", INPUTMAP_PAD_LEFTSTICK },
	{ "LS", INPUTMAP_PAD_LEFTSTICK },
	{ "RIGHTSTICK", INPUTMAP_PAD_RIGHTSTICK },
	{ "RS", INPUTMAP_PAD_RIGHTSTICK },
	{ "LEFTSHOULDER", INPUTMAP_PAD_LEFTSHOULDER },
	{ "LB", INPUTMAP_PAD_LEFTSHOULDER },
	{ "RIGHTSHOULDER", INPUTMAP_PAD_RIGHTSHOULDER },
	{ "RB", INPUTMAP_PAD_RIGHTSHOULDER },
	{ "DPAD_UP", INPUTMAP_PAD_DPAD_UP },
	{ "DPAD_DOWN", INPUTMAP_PAD_DPAD_DOWN },
	{ "DPAD_LEFT", INPUTMAP_PAD_DPAD_LEFT },
	{ "DPAD_RIGHT", INPUTMAP_PAD_DPAD_RIGHT },
	{ NULL, 0 }
};

static const InputMapName pad_axes[] =
{
	{ "LEFTX-", INPUTMAP_AXIS_LEFTX * 2 + 0 },
	{ "LEFTX+", INPUTMAP_AXIS_LEFTX * 2 + 1 },
	{ "LEFTY-", INPUTMAP_AXIS_LEFTY * 2 + 0 },
	{ "LEFTY+", INPUTMAP_AXIS_LEFTY * 2 + 1 },
	{ "RIGHTX-", INPUTMAP_AXIS_RIGHTX * 2 + 0 },
	{ "RIGHTX+", INPUTMAP_AXIS_RIGHTX * 2 + 1 },
	{ "RIGHTY-", INPUTMAP_AXIS_RIGHTY * 2 + 0 },
	{ "RIGHTY+", INPUTMAP_AXIS_RIGHTY * 2 + 1 },
	{ "TRIGGERLEFT", INPUTMAP_AXIS_TRIGGERLEFT * 2 + 1 },
	{ "LT", INPUTMAP_AXIS_TRIGGERLEFT * 2 + 1 },
	{ "TRIGGERRIGHT", INPUTMAP_AXIS_TRIGGERRIGHT * 2 + 1 },
	{ "RT", INPUTMAP_AXIS_TRIGGERRIGHT * 2 + 1 },
	{ NULL, 0 }
};

static char last_error[256];

static void set_error(const char* fmt, ...)
{
	va_list args;
	va_start(args, fmt);
	vsnprintf(last_error, sizeof(last_error), fmt, args);
	va_end(args);
	last_error[sizeof(last_error) - 1] = '\0';
}

static int equal_ignore_case(const char* a, const char* b)
{
	while (*a && *b)
	{
		if (tolower((unsigned char)*a) != tolower((unsigned char)*b))
		{
			return 0;
		}
		++a;
		++b;
	}
	return *a == '\0' && *b == '\0';
}

static char* trim(char* text)
{
	char* end;
	while (*text && isspace((unsigned char)*text))
	{
		++text;
	}
	end = text + strlen(text);
	while (end > text && isspace((unsigned char)end[-1]))
	{
		--end;
	}
	*end = '\0';
	return text;
}

static void lower(char* text)
{
	while (*text)
	{
		*text = (char)tolower((unsigned char)*text);
		++text;
	}
}

static int parse_bool(const char* text, int* out)
{
	if (equal_ignore_case(text, "1") || equal_ignore_case(text, "true") ||
	    equal_ignore_case(text, "yes") || equal_ignore_case(text, "on"))
	{
		*out = 1;
		return 1;
	}
	if (equal_ignore_case(text, "0") || equal_ignore_case(text, "false") ||
	    equal_ignore_case(text, "no") || equal_ignore_case(text, "off"))
	{
		*out = 0;
		return 1;
	}
	return 0;
}

static int parse_int(const char* text, int* out)
{
	char* end = NULL;
	long value;
	if (!text || !*text)
	{
		return 0;
	}
	errno = 0;
	value = strtol(text, &end, 10);
	if (errno != 0 || end == text || *end != '\0')
	{
		return 0;
	}
	*out = (int)value;
	return 1;
}

static int parse_float(const char* text, float* out)
{
	char* end = NULL;
	double value;
	if (!text || !*text)
	{
		return 0;
	}
	errno = 0;
	value = strtod(text, &end);
	if (errno != 0 || end == text || *end != '\0' || value != value)
	{
		return 0;
	}
	*out = (float)value;
	return 1;
}

static int action_from_name(const char* name)
{
	int i;
	for (i = 0; i < INPUTMAP_ACTION_COUNT; ++i)
	{
		if (equal_ignore_case(name, action_defs[i].name) ||
		    (action_defs[i].alias && equal_ignore_case(name, action_defs[i].alias)))
		{
			return i;
		}
	}
	return -1;
}

static const char* keyboard_name(int code)
{
	int i;
	for (i = 0; keyboard_names[i].name; ++i)
	{
		if (keyboard_names[i].code == code)
		{
			return keyboard_names[i].name;
		}
	}
	return NULL;
}

static int keyboard_code(const char* name)
{
	int i;
	for (i = 0; keyboard_names[i].name; ++i)
	{
		if (equal_ignore_case(name, keyboard_names[i].name))
		{
			return keyboard_names[i].code;
		}
	}
	for (i = 0; keyboard_aliases[i].name; ++i)
	{
		if (equal_ignore_case(name, keyboard_aliases[i].name))
		{
			return keyboard_aliases[i].code;
		}
	}
	return -1;
}

static const char* pad_button_name(int code)
{
	int i;
	for (i = 0; pad_buttons[i].name; ++i)
	{
		if (pad_buttons[i].code == code && strcmp(pad_buttons[i].name, "SELECT") != 0 &&
		    strcmp(pad_buttons[i].name, "LS") != 0 && strcmp(pad_buttons[i].name, "RS") != 0 &&
		    strcmp(pad_buttons[i].name, "LB") != 0 && strcmp(pad_buttons[i].name, "RB") != 0)
		{
			return pad_buttons[i].name;
		}
	}
	return NULL;
}

static int pad_button_code(const char* name)
{
	int i;
	for (i = 0; pad_buttons[i].name; ++i)
	{
		if (equal_ignore_case(name, pad_buttons[i].name))
		{
			return pad_buttons[i].code;
		}
	}
	return -1;
}

static int pad_axis_code(const char* name, int* axis, int* direction)
{
	int i;
	for (i = 0; pad_axes[i].name; ++i)
	{
		if (equal_ignore_case(name, pad_axes[i].name))
		{
			*axis = pad_axes[i].code / 2;
			*direction = (pad_axes[i].code % 2) ? 1 : -1;
			return 1;
		}
	}
	return 0;
}

static const char* pad_axis_name(int axis, int direction)
{
	int i;
	for (i = 0; pad_axes[i].name; ++i)
	{
		if (pad_axes[i].code / 2 == axis && ((pad_axes[i].code % 2) ? 1 : -1) == direction &&
		    strcmp(pad_axes[i].name, "LT") != 0 && strcmp(pad_axes[i].name, "RT") != 0)
		{
			return pad_axes[i].name;
		}
	}
	return NULL;
}

static void binding_none(InputMapBinding* binding)
{
	binding->type = INPUTMAP_BIND_NONE;
	binding->code = 0;
	binding->direction = 0;
}

void InputMap_Defaults(InputMap* map)
{
	int action;
	int i;

	if (!map)
	{
		return;
	}

	memset(map, 0, sizeof(*map));
	map->keyboard_enabled = 1;
	map->gamepad_enabled = 1;
	map->gamepad_index = 0;
	map->gamepad_guid[0] = '\0';
	map->axis_deadzone = 0.5f;
	map->use_control_option = 0;

	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		for (i = 0; i < INPUTMAP_MAX_BINDINGS; ++i)
		{
			binding_none(&map->bindings[INPUTMAP_DEVICE_KEYBOARD][action][i]);
			binding_none(&map->bindings[INPUTMAP_DEVICE_GAMEPAD][action][i]);
		}
	}

	/* Keyboard defaults: WASD + arrows, PSX buttons on the historical keys. */
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_FORWARD][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_FORWARD][0].code = SDL_SCANCODE_W;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_FORWARD][1].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_FORWARD][1].code = SDL_SCANCODE_UP;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_BACK][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_BACK][0].code = SDL_SCANCODE_S;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_BACK][1].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_BACK][1].code = SDL_SCANCODE_DOWN;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LEFT][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LEFT][0].code = SDL_SCANCODE_A;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LEFT][1].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LEFT][1].code = SDL_SCANCODE_LEFT;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_RIGHT][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_RIGHT][0].code = SDL_SCANCODE_D;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_RIGHT][1].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_RIGHT][1].code = SDL_SCANCODE_RIGHT;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_ACTION][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_ACTION][0].code = SDL_SCANCODE_C;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_JUMP][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_JUMP][0].code = SDL_SCANCODE_X;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_DRAW][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_DRAW][0].code = SDL_SCANCODE_Z;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_ROLL][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_ROLL][0].code = SDL_SCANCODE_V;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LOOK][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_LOOK][0].code = SDL_SCANCODE_LSHIFT;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_DUCK][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_DUCK][0].code = SDL_SCANCODE_LCTRL;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_WALK][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_WALK][0].code = SDL_SCANCODE_RSHIFT;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_SPRINT][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_SPRINT][0].code = SDL_SCANCODE_RCTRL;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_START][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_START][0].code = SDL_SCANCODE_RETURN;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_SELECT][0].type = INPUTMAP_BIND_KEY;
	map->bindings[INPUTMAP_DEVICE_KEYBOARD][INPUTMAP_ACTION_SELECT][0].code = SDL_SCANCODE_SPACE;

	/* Gamepad defaults: D-pad + left stick, standard PSX button roles. */
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_FORWARD][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_FORWARD][0].code = INPUTMAP_PAD_DPAD_UP;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_FORWARD][1].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_FORWARD][1].code = INPUTMAP_AXIS_LEFTY;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_FORWARD][1].direction = -1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_BACK][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_BACK][0].code = INPUTMAP_PAD_DPAD_DOWN;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_BACK][1].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_BACK][1].code = INPUTMAP_AXIS_LEFTY;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_BACK][1].direction = 1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LEFT][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LEFT][0].code = INPUTMAP_PAD_DPAD_LEFT;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LEFT][1].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LEFT][1].code = INPUTMAP_AXIS_LEFTX;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LEFT][1].direction = -1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_RIGHT][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_RIGHT][0].code = INPUTMAP_PAD_DPAD_RIGHT;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_RIGHT][1].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_RIGHT][1].code = INPUTMAP_AXIS_LEFTX;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_RIGHT][1].direction = 1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_ACTION][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_ACTION][0].code = INPUTMAP_PAD_A;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_JUMP][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_JUMP][0].code = INPUTMAP_PAD_X;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_DRAW][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_DRAW][0].code = INPUTMAP_PAD_Y;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_ROLL][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_ROLL][0].code = INPUTMAP_PAD_B;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LOOK][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_LOOK][0].code = INPUTMAP_PAD_LEFTSHOULDER;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_DUCK][0].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_DUCK][0].code = INPUTMAP_AXIS_TRIGGERLEFT;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_DUCK][0].direction = 1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_WALK][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_WALK][0].code = INPUTMAP_PAD_RIGHTSHOULDER;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_SPRINT][0].type = INPUTMAP_BIND_PAD_AXIS;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_SPRINT][0].code = INPUTMAP_AXIS_TRIGGERRIGHT;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_SPRINT][0].direction = 1;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_START][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_START][0].code = INPUTMAP_PAD_START;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_SELECT][0].type = INPUTMAP_BIND_PAD_BUTTON;
	map->bindings[INPUTMAP_DEVICE_GAMEPAD][INPUTMAP_ACTION_SELECT][0].code = INPUTMAP_PAD_BACK;
}

const char* InputMap_EnvPath(void)
{
	const char* value = getenv("TOMB5_INPUT_CONFIG");
	return (value && *value) ? value : NULL;
}

const char* InputMap_LastError(void)
{
	return last_error;
}

const char* InputMap_ActionName(int action)
{
	if (action < 0 || action >= INPUTMAP_ACTION_COUNT)
	{
		return "?";
	}
	return action_defs[action].name;
}

int InputMap_ActionFromName(const char* name)
{
	return name ? action_from_name(name) : -1;
}

const char* InputMap_DeviceName(int device)
{
	switch (device)
	{
	case INPUTMAP_DEVICE_KEYBOARD: return "keyboard";
	case INPUTMAP_DEVICE_GAMEPAD: return "gamepad";
	default: return "?";
	}
}

int InputMap_ParseBinding(int device, const char* text, InputMapBinding* out,
                          char* err, size_t errlen)
{
	const char* value = text ? text : "";
	int axis;
	int direction;

	if (err && errlen)
	{
		err[0] = '\0';
	}
	if (!out)
	{
		return 0;
	}

	binding_none(out);
	if (!*value || equal_ignore_case(value, "none") || strcmp(value, "-") == 0)
	{
		return 1;
	}

	if (device == INPUTMAP_DEVICE_KEYBOARD)
	{
		int code = keyboard_code(value);
		if (code < 0)
		{
			if (err && errlen)
			{
				snprintf(err, errlen, "unknown keyboard key '%s'", value);
			}
			return 0;
		}
		out->type = INPUTMAP_BIND_KEY;
		out->code = (unsigned short)code;
		return 1;
	}

	if (device != INPUTMAP_DEVICE_GAMEPAD)
	{
		if (err && errlen)
		{
			snprintf(err, errlen, "unknown device '%d'", device);
		}
		return 0;
	}

	if (pad_axis_code(value, &axis, &direction))
	{
		out->type = INPUTMAP_BIND_PAD_AXIS;
		out->code = (unsigned short)axis;
		out->direction = (signed char)direction;
		return 1;
	}

	{
		int code = pad_button_code(value);
		if (code < 0)
		{
			if (err && errlen)
			{
				snprintf(err, errlen, "unknown gamepad control '%s'", value);
			}
			return 0;
		}
		out->type = INPUTMAP_BIND_PAD_BUTTON;
		out->code = (unsigned short)code;
		return 1;
	}
}

int InputMap_BindingFromKey(int scancode, InputMapBinding* out)
{
	if (!out || scancode < 0 || scancode >= INPUTMAP_KEY_COUNT ||
	    !keyboard_name(scancode))
	{
		return 0;
	}
	binding_none(out);
	out->type = INPUTMAP_BIND_KEY;
	out->code = (unsigned short)scancode;
	return 1;
}

int InputMap_BindingFromButton(int button, InputMapBinding* out)
{
	if (!out || button < 0 || button >= INPUTMAP_PAD_BUTTON_COUNT)
	{
		return 0;
	}
	binding_none(out);
	out->type = INPUTMAP_BIND_PAD_BUTTON;
	out->code = (unsigned short)button;
	return 1;
}

int InputMap_BindingFromAxis(int axis, int direction, InputMapBinding* out)
{
	if (!out || axis < 0 || axis >= INPUTMAP_PAD_AXIS_COUNT || (direction != 1 && direction != -1))
	{
		return 0;
	}
	binding_none(out);
	out->type = INPUTMAP_BIND_PAD_AXIS;
	out->code = (unsigned short)axis;
	out->direction = (signed char)direction;
	return 1;
}

int InputMap_FormatBinding(const InputMapBinding* binding, char* out, size_t outlen)
{
	const char* name = NULL;

	if (!out || outlen == 0)
	{
		return 0;
	}

	if (!binding || binding->type == INPUTMAP_BIND_NONE)
	{
		snprintf(out, outlen, "NONE");
		return 1;
	}

	switch (binding->type)
	{
	case INPUTMAP_BIND_KEY:
		name = keyboard_name(binding->code);
		break;
	case INPUTMAP_BIND_PAD_BUTTON:
		name = pad_button_name(binding->code);
		break;
	case INPUTMAP_BIND_PAD_AXIS:
		name = pad_axis_name(binding->code, binding->direction);
		break;
	default:
		break;
	}

	if (!name)
	{
		snprintf(out, outlen, "NONE");
		return 0;
	}
	snprintf(out, outlen, "%s", name);
	return 1;
}

static int parse_bindings(const char* value, int device, InputMapBinding* slots,
                          char* err, size_t errlen)
{
	char copy[512];
	char* cursor;
	const char* scan;
	int commas = 0;
	int count = 0;

	if (strlen(value) >= sizeof(copy))
	{
		if (err && errlen)
		{
			snprintf(err, errlen, "binding list is too long");
		}
		return 0;
	}
	for (scan = value; *scan; ++scan)
	{
		if (*scan == ',')
		{
			++commas;
		}
	}
	if (commas >= INPUTMAP_MAX_BINDINGS)
	{
		if (err && errlen)
		{
			snprintf(err, errlen, "more than %d bindings", INPUTMAP_MAX_BINDINGS);
		}
		return 0;
	}

	snprintf(copy, sizeof(copy), "%s", value);
	cursor = copy;
	while (count < INPUTMAP_MAX_BINDINGS)
	{
		char* comma = strchr(cursor, ',');
		char* item;
		if (comma)
		{
			*comma = '\0';
		}
		item = trim(cursor);
		if (!InputMap_ParseBinding(device, item, &slots[count], err, errlen))
		{
			return 0;
		}
		++count;
		if (!comma)
		{
			break;
		}
		cursor = comma + 1;
	}
	while (count < INPUTMAP_MAX_BINDINGS)
	{
		binding_none(&slots[count++]);
	}
	return 1;
}

static int parse_guid(const char* text)
{
	/* SDL GUID text is hex, dashes and optional braces; keep it bounded. */
	size_t length = strlen(text);
	size_t i;
	if (length >= 64)
	{
		return 0;
	}
	for (i = 0; i < length; ++i)
	{
		unsigned char c = (unsigned char)text[i];
		if (!isxdigit(c) && c != '-' && c != '{' && c != '}')
		{
			return 0;
		}
	}
	return 1;
}

static int parse_config(InputMap* map, FILE* file, const char* path)
{
	char line[INPUTMAP_LINE_MAX];
	char section[32] = "";
	int line_number = 0;

	while (fgets(line, sizeof(line), file))
	{
		char* text;
		char* comment;
		char* equals;
		char* key;
		char* value;
		++line_number;

		comment = strpbrk(line, "#;");
		if (comment)
		{
			*comment = '\0';
		}
		text = trim(line);
		if (!*text)
		{
			continue;
		}

		if (*text == '[')
		{
			char* close = strchr(text, ']');
			size_t length;
			if (!close || close[1] != '\0')
			{
				set_error("%s:%d: malformed section header", path, line_number);
				return -1;
			}
			*close = '\0';
			++text;
			length = strlen(text);
			if (length == 0 || length >= sizeof(section))
			{
				set_error("%s:%d: invalid section name", path, line_number);
				return -1;
			}
			snprintf(section, sizeof(section), "%s", text);
			lower(section);
			if (strcmp(section, "devices") != 0 && strcmp(section, "gameplay") != 0 &&
			    strcmp(section, "keyboard") != 0 && strcmp(section, "gamepad") != 0)
			{
				set_error("%s:%d: unknown section [%s]", path, line_number, section);
				return -1;
			}
			continue;
		}

		equals = strchr(text, '=');
		if (!equals)
		{
			set_error("%s:%d: expected key = value", path, line_number);
			return -1;
		}
		*equals = '\0';
		key = trim(text);
		value = trim(equals + 1);
		lower(key);

		if (strcmp(section, "devices") == 0)
		{
			if (strcmp(key, "keyboard") == 0)
			{
				if (!parse_bool(value, &map->keyboard_enabled))
				{
					set_error("%s:%d: keyboard must be 0 or 1", path, line_number);
					return -1;
				}
			}
			else if (strcmp(key, "gamepad") == 0)
			{
				if (!parse_bool(value, &map->gamepad_enabled))
				{
					set_error("%s:%d: gamepad must be 0 or 1", path, line_number);
					return -1;
				}
			}
			else if (strcmp(key, "gamepad_index") == 0)
			{
				if (!parse_int(value, &map->gamepad_index) || map->gamepad_index < -1)
				{
					set_error("%s:%d: gamepad_index must be -1 or a device index", path, line_number);
					return -1;
				}
			}
			else if (strcmp(key, "gamepad_guid") == 0)
			{
				if (!*value)
				{
					map->gamepad_guid[0] = '\0';
				}
				else if (!parse_guid(value))
				{
					set_error("%s:%d: gamepad_guid is not a valid GUID", path, line_number);
					return -1;
				}
				else
				{
					snprintf(map->gamepad_guid, sizeof(map->gamepad_guid), "%s", value);
				}
			}
			else if (strcmp(key, "axis_deadzone") == 0)
			{
				if (!parse_float(value, &map->axis_deadzone) || map->axis_deadzone < 0.0f ||
				    map->axis_deadzone > 1.0f)
				{
					set_error("%s:%d: axis_deadzone must be between 0 and 1", path, line_number);
					return -1;
				}
			}
			else
			{
				set_error("%s:%d: unknown devices key '%s'", path, line_number, key);
				return -1;
			}
		}
		else if (strcmp(section, "gameplay") == 0)
		{
			if (strcmp(key, "use_control_option") == 0)
			{
				if (!parse_bool(value, &map->use_control_option))
				{
					set_error("%s:%d: use_control_option must be 0 or 1", path, line_number);
					return -1;
				}
			}
			else
			{
				set_error("%s:%d: unknown gameplay key '%s'", path, line_number, key);
				return -1;
			}
		}
		else if (strcmp(section, "keyboard") == 0 || strcmp(section, "gamepad") == 0)
		{
			int device = (strcmp(section, "keyboard") == 0)
				? INPUTMAP_DEVICE_KEYBOARD : INPUTMAP_DEVICE_GAMEPAD;
			int action = action_from_name(key);
			char err[128];
			if (action < 0)
			{
				set_error("%s:%d: unknown action '%s'", path, line_number, key);
				return -1;
			}
			if (!parse_bindings(value, device,
			                    map->bindings[device][action], err, sizeof(err)))
			{
				set_error("%s:%d: %s", path, line_number, err);
				return -1;
			}
		}
		else
		{
			set_error("%s:%d: value outside a section", path, line_number);
			return -1;
		}
	}

	return 0;
}

int InputMap_Load(InputMap* map, const char* path)
{
	FILE* file;

	if (!map || !path)
	{
		set_error("invalid argument");
		return -1;
	}

	InputMap_Defaults(map);
	file = fopen(path, "rb");
	if (!file)
	{
		if (errno == ENOENT)
		{
			return 0;
		}
		set_error("cannot open %s: %s", path, strerror(errno));
		return -1;
	}

	if (parse_config(map, file, path) != 0)
	{
		fclose(file);
		InputMap_Defaults(map);
		return -1;
	}

	fclose(file);
	return 1;
}

static void write_binding(FILE* file, const InputMap* map, int device, int action, int slot)
{
	char text[64];
	if (!InputMap_FormatBinding(&map->bindings[device][action][slot], text, sizeof(text)))
	{
		snprintf(text, sizeof(text), "NONE");
	}
	fprintf(file, "%s", text);
}

int InputMap_Save(const InputMap* map, const char* path)
{
	FILE* file;
	int action;

	if (!map || !path)
	{
		set_error("invalid argument");
		return 0;
	}

	file = fopen(path, "wb");
	if (!file)
	{
		set_error("cannot write %s: %s", path, strerror(errno));
		return 0;
	}

	fprintf(file, "# TOMB5 input configuration\n");
	fprintf(file, "# Each action has two bindings per device; use NONE for an empty slot.\n");
	fprintf(file, "# Keyboard names are SDL scancode names (layout-independent).\n");
	fprintf(file, "# Gamepad names: A, B, X, Y, BACK, START, LEFTSHOULDER, RIGHTSHOULDER,\n");
	fprintf(file, "#   LEFTSTICK, RIGHTSTICK, DPAD_UP/DOWN/LEFT/RIGHT, LEFTX-/+, LEFTY-/+, RIGHTX-/+, TRIGGERLEFT/RIGHT.\n");
	fprintf(file, "# gamepad_index = -1 selects the first available controller; gamepad_guid overrides it.\n\n");
	fprintf(file, "[devices]\n");
	fprintf(file, "keyboard = %d\n", map->keyboard_enabled ? 1 : 0);
	fprintf(file, "gamepad = %d\n", map->gamepad_enabled ? 1 : 0);
	fprintf(file, "gamepad_index = %d\n", map->gamepad_index);
	fprintf(file, "gamepad_guid = %s\n", map->gamepad_guid);
	fprintf(file, "axis_deadzone = %.2f\n\n", (double)map->axis_deadzone);
	fprintf(file, "[gameplay]\n");
	fprintf(file, "use_control_option = %d\n\n", map->use_control_option ? 1 : 0);

	fprintf(file, "[keyboard]\n");
	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		fprintf(file, "%-9s = ", action_defs[action].name);
		write_binding(file, map, INPUTMAP_DEVICE_KEYBOARD, action, 0);
		fprintf(file, ", ");
		write_binding(file, map, INPUTMAP_DEVICE_KEYBOARD, action, 1);
		fprintf(file, "\n");
	}

	fprintf(file, "\n[gamepad]\n");
	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		fprintf(file, "%-9s = ", action_defs[action].name);
		write_binding(file, map, INPUTMAP_DEVICE_GAMEPAD, action, 0);
		fprintf(file, ", ");
		write_binding(file, map, INPUTMAP_DEVICE_GAMEPAD, action, 1);
		fprintf(file, "\n");
	}

	if (fclose(file) != 0)
	{
		set_error("cannot close %s: %s", path, strerror(errno));
		return 0;
	}
	return 1;
}

static int binding_active(const InputMap* map, const InputMapBinding* binding,
                          const InputMapSnapshot* snapshot, int keyboard, int gamepad)
{
	if (!binding || binding->type == INPUTMAP_BIND_NONE)
	{
		return 0;
	}

	switch (binding->type)
	{
	case INPUTMAP_BIND_KEY:
		return keyboard && binding->code < INPUTMAP_KEY_COUNT &&
		       snapshot->keyboard[binding->code] != 0;
	case INPUTMAP_BIND_PAD_BUTTON:
		return gamepad && binding->code < INPUTMAP_PAD_BUTTON_COUNT &&
		       snapshot->pad_buttons[binding->code] != 0;
	case INPUTMAP_BIND_PAD_AXIS:
		if (!gamepad || binding->code >= INPUTMAP_PAD_AXIS_COUNT)
		{
			return 0;
		}
		{
			float value = snapshot->pad_axes[binding->code];
			float deadzone = map->axis_deadzone;
			if (binding->code == INPUTMAP_AXIS_TRIGGERLEFT ||
			    binding->code == INPUTMAP_AXIS_TRIGGERRIGHT)
			{
				return value > deadzone;
			}
			return binding->direction < 0 ? value < -deadzone : value > deadzone;
		}
	default:
		return 0;
	}
}

static int action_active(const InputMap* map, const InputMapSnapshot* snapshot,
                         int action, int keyboard, int gamepad, int slot)
{
	return binding_active(map, &map->bindings[INPUTMAP_DEVICE_KEYBOARD][action][slot],
	                      snapshot, keyboard, gamepad) ||
	       binding_active(map, &map->bindings[INPUTMAP_DEVICE_GAMEPAD][action][slot],
	                      snapshot, keyboard, gamepad);
}

unsigned long InputMap_EvaluateActions(const InputMap* map, const InputMapSnapshot* snapshot)
{
	unsigned long result = 0;
	int action;
	int slot;

	if (!map || !snapshot)
	{
		return 0;
	}

	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		if (action_defs[action].action_bit == 0)
		{
			continue;
		}
		for (slot = 0; slot < INPUTMAP_MAX_BINDINGS; ++slot)
		{
			if (action_active(map, snapshot, action, map->keyboard_enabled,
			                  map->gamepad_enabled, slot))
			{
				result |= action_defs[action].action_bit;
				break;
			}
		}
	}
	return result;
}

unsigned short InputMap_EvaluatePad(const InputMap* map, const InputMapSnapshot* snapshot,
                                    int include_keyboard, int include_gamepad)
{
	unsigned short result = 0xFFFF;
	int action;
	int slot;

	if (!map || !snapshot)
	{
		return result;
	}

	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		if (action_defs[action].pad_bit == 0)
		{
			continue;
		}
		for (slot = 0; slot < INPUTMAP_MAX_BINDINGS; ++slot)
		{
			if (action_active(map, snapshot, action, include_keyboard && map->keyboard_enabled,
			                  include_gamepad && map->gamepad_enabled, slot))
			{
				result &= (unsigned short)~action_defs[action].pad_bit;
				break;
			}
		}
	}
	return result;
}
