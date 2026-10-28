#include "EMULATOR.H"

#include "INPUTUI.H"
#include "INPUTMAP.H"

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INPUTUI_SCREEN_ACTIONS 0
#define INPUTUI_SCREEN_DEVICES 1
#define INPUTUI_DEVICE_ROWS 3
#define INPUTUI_COLUMNS 4

static int g_open = 0;
static int g_screen = INPUTUI_SCREEN_ACTIONS;
static int g_selected = 0;
static int g_column = 0;
static int g_capture = 0;
static int g_capture_column = 0;
static int g_device_row = 0;
static char g_status[192];
#if defined(SDL2)
static Uint32 g_last_draw_ms = 0;
#endif

static void set_status(const char* format, ...)
{
	va_list args;
	va_start(args, format);
	vsnprintf(g_status, sizeof(g_status), format, args);
	va_end(args);
	g_status[sizeof(g_status) - 1] = '\0';
}

static int binding_device(int column)
{
	return column < 2 ? INPUTMAP_DEVICE_KEYBOARD : INPUTMAP_DEVICE_GAMEPAD;
}

static int binding_slot(int column)
{
	return column < 2 ? column : column - 2;
}

static void apply_binding(const InputMapBinding* binding)
{
	char text[32];
	int device = binding_device(g_capture_column);
	int slot = binding_slot(g_capture_column);
	int saved;

	if (!InputMap_FormatBinding(binding, text, sizeof(text)))
	{
		snprintf(text, sizeof(text), "NONE");
	}
	saved = InputMap_UpdateBinding(device, g_selected, slot, binding);
	if (saved)
	{
		set_status("Saved %s = %s", InputMap_ActionName(g_selected), text);
	}
	else
	{
		set_status("Save failed: %s", InputMap_LastError());
	}
	g_capture = 0;
}

static void begin_capture(void)
{
	g_capture = 1;
	g_capture_column = g_column;
	set_status("Press a key or gamepad control (Esc cancels)");
}

static void reset_defaults(void)
{
	if (InputMap_ResetDefaultsAndSave())
	{
		set_status("Default bindings restored and saved");
	}
	else
	{
		set_status("Reset failed: %s", InputMap_LastError());
	}
}

static void toggle_device(int row)
{
	const InputMap* map = InputMap_Current();
	int saved;
	int index;

	if (!map)
	{
		return;
	}

	if (row == 0)
	{
		saved = InputMap_UpdateDevices(!map->keyboard_enabled, map->gamepad_enabled,
		                              map->gamepad_index);
		if (saved)
		{
			set_status("Keyboard %s",
			           InputMap_Current()->keyboard_enabled ? "enabled" : "disabled");
		}
		else
		{
			set_status("Save failed: %s", InputMap_LastError());
		}
	}
	else if (row == 1)
	{
		saved = InputMap_UpdateDevices(map->keyboard_enabled, !map->gamepad_enabled,
		                              map->gamepad_index);
		if (saved)
		{
			set_status("Gamepad %s",
			           InputMap_Current()->gamepad_enabled ? "enabled" : "disabled");
		}
		else
		{
			set_status("Save failed: %s", InputMap_LastError());
		}
	}
	else
	{
		int count = InputMap_GamepadCount();
		index = map->gamepad_index;
		if (count > 0)
		{
			index = (index + 1) % count;
		}
		else
		{
			index = 0;
		}
		saved = InputMap_UpdateDevices(map->keyboard_enabled, map->gamepad_enabled, index);
		if (saved)
		{
			const char* name = InputMap_GamepadNameAt(index);
			set_status("Gamepad index %d%s%s", index, name ? ": " : "", name ? name : "");
		}
		else
		{
			set_status("Save failed: %s", InputMap_LastError());
		}
	}
}

static void move_vertical(int delta)
{
	if (g_screen == INPUTUI_SCREEN_ACTIONS)
	{
		g_selected = (g_selected + delta + INPUTMAP_ACTION_COUNT) % INPUTMAP_ACTION_COUNT;
	}
	else
	{
		g_device_row = (g_device_row + delta + INPUTUI_DEVICE_ROWS) % INPUTUI_DEVICE_ROWS;
	}
}

static void move_horizontal(int delta)
{
	if (g_screen == INPUTUI_SCREEN_ACTIONS)
	{
		g_column = (g_column + delta + INPUTUI_COLUMNS) % INPUTUI_COLUMNS;
	}
	else
	{
		toggle_device(g_device_row);
	}
}

static void confirm(void)
{
	if (g_screen == INPUTUI_SCREEN_ACTIONS)
	{
		begin_capture();
	}
	else
	{
		toggle_device(g_device_row);
	}
}

#if defined(SDL2)
static void handle_key(SDL_Scancode scancode)
{
	if (g_capture)
	{
		InputMapBinding binding;
		if (scancode == SDL_SCANCODE_ESCAPE || scancode == SDL_SCANCODE_F1)
		{
			g_capture = 0;
			set_status("Binding cancelled");
			return;
		}
		if (InputMap_BindingFromKey(scancode, &binding))
		{
			apply_binding(&binding);
		}
		else
		{
			set_status("Unsupported key; press another or Esc");
		}
		return;
	}

	switch (scancode)
	{
	case SDL_SCANCODE_F1:
	case SDL_SCANCODE_ESCAPE:
		InputUI_Close();
		return;
	case SDL_SCANCODE_UP:
		move_vertical(-1);
		return;
	case SDL_SCANCODE_DOWN:
		move_vertical(1);
		return;
	case SDL_SCANCODE_LEFT:
		move_horizontal(-1);
		return;
	case SDL_SCANCODE_RIGHT:
		move_horizontal(1);
		return;
	case SDL_SCANCODE_RETURN:
	case SDL_SCANCODE_SPACE:
		confirm();
		return;
	case SDL_SCANCODE_TAB:
		g_screen = g_screen == INPUTUI_SCREEN_ACTIONS
			? INPUTUI_SCREEN_DEVICES : INPUTUI_SCREEN_ACTIONS;
		return;
	case SDL_SCANCODE_R:
		reset_defaults();
		return;
	default:
		return;
	}
}

static void handle_button(Uint8 button)
{
	if (g_capture)
	{
		InputMapBinding binding;
		if (InputMap_BindingFromButton(button, &binding))
		{
			apply_binding(&binding);
		}
		return;
	}

	switch (button)
	{
	case SDL_CONTROLLER_BUTTON_DPAD_UP:
		move_vertical(-1);
		break;
	case SDL_CONTROLLER_BUTTON_DPAD_DOWN:
		move_vertical(1);
		break;
	case SDL_CONTROLLER_BUTTON_DPAD_LEFT:
		move_horizontal(-1);
		break;
	case SDL_CONTROLLER_BUTTON_DPAD_RIGHT:
		move_horizontal(1);
		break;
	case SDL_CONTROLLER_BUTTON_A:
		confirm();
		break;
	case SDL_CONTROLLER_BUTTON_B:
	case SDL_CONTROLLER_BUTTON_START:
		InputUI_Close();
		break;
	case SDL_CONTROLLER_BUTTON_BACK:
		g_screen = g_screen == INPUTUI_SCREEN_ACTIONS
			? INPUTUI_SCREEN_DEVICES : INPUTUI_SCREEN_ACTIONS;
		break;
	default:
		break;
	}
}

static void handle_axis(Sint16 value, Uint8 axis)
{
	InputMapBinding binding;
	int direction;

	if (!g_capture)
	{
		return;
	}
	if (axis >= SDL_CONTROLLER_AXIS_TRIGGERLEFT)
	{
		if (value <= 16000)
		{
			return;
		}
		direction = 1;
	}
	else if (value > 20000)
	{
		direction = 1;
	}
	else if (value < -20000)
	{
		direction = -1;
	}
	else
	{
		return;
	}
	if (InputMap_BindingFromAxis(axis, direction, &binding))
	{
		apply_binding(&binding);
	}
}
#endif

#if defined(SDL2)
int InputUI_HandleEvent(const SDL_Event* event)
{
	if (!event)
	{
		return 0;
	}

	if (!g_open)
	{
		if (event->type == SDL_KEYDOWN && !event->key.repeat &&
		    event->key.keysym.scancode == SDL_SCANCODE_F1 && InputUI_CanOpen())
		{
			InputUI_Open();
			return 1;
		}
		return 0;
	}

	switch (event->type)
	{
	case SDL_KEYDOWN:
		if (event->key.repeat)
		{
			return 1;
		}
		handle_key(event->key.keysym.scancode);
		return 1;
	case SDL_KEYUP:
		return 1;
	case SDL_CONTROLLERBUTTONDOWN:
		handle_button(event->cbutton.button);
		return 1;
	case SDL_CONTROLLERBUTTONUP:
		return 1;
	case SDL_CONTROLLERAXISMOTION:
		handle_axis(event->caxis.value, event->caxis.axis);
		return 1;
	case SDL_CONTROLLERDEVICEADDED:
	case SDL_CONTROLLERDEVICEREMOVED:
		return 0;
	case SDL_QUIT:
	case SDL_WINDOWEVENT:
		return 0;
	default:
		return 0;
	}
}
#endif

int InputUI_IsOpen(void)
{
	return g_open;
}

void InputUI_Open(void)
{
	g_open = 1;
	g_screen = INPUTUI_SCREEN_ACTIONS;
	g_selected = 0;
	g_column = 0;
	g_capture = 0;
	g_capture_column = 0;
	g_device_row = 0;
	g_status[0] = '\0';
}

void InputUI_Close(void)
{
	g_open = 0;
	g_capture = 0;
}

void InputUI_NotifyDraw(void)
{
#if defined(SDL2)
	g_last_draw_ms = SDL_GetTicks();
#endif
}

int InputUI_CanOpen(void)
{
#if defined(SDL2)
	if (!g_last_draw_ms)
	{
		return 0;
	}
	return (SDL_GetTicks() - g_last_draw_ms) < 100;
#else
	return 0;
#endif
}

int InputUI_Screen(void)
{
	return g_screen;
}

int InputUI_SelectedAction(void)
{
	return g_selected;
}

int InputUI_SelectedColumn(void)
{
	return g_column;
}

int InputUI_DeviceRow(void)
{
	return g_device_row;
}

int InputUI_IsCapturing(void)
{
	return g_capture;
}

const char* InputUI_Status(void)
{
	return g_status;
}
