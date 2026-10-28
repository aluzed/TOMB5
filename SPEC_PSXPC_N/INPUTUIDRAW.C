#include "INPUTUI.H"
#include "INPUTMAP.H"

#include <SDL.h>

#include "GPU.H"
#include "MISC.H"
#include "TEXT_S.H"
#include "TYPES.H"

#include <stdio.h>
#include <string.h>

#define UI_WIDTH 512
#define UI_LEFT 12
#define UI_TOP 6
#define UI_RIGHT 500
#define UI_BOTTOM 234
#define UI_ROW_HEIGHT 16
#define UI_ACTION_FIRST_ROW 46
#define UI_ACTION_X 16
#define UI_KEYBOARD_X 110
#define UI_GAMEPAD_X 280
#define UI_COLOUR_TEXT 2
#define UI_COLOUR_SELECTED 1
#define UI_COLOUR_HINT 5

static void slot_text(const InputMap* map, int device, int action, int slot,
                      char* out, size_t outlen)
{
	const InputMapBinding* binding = &map->bindings[device][action][slot];

	if (binding->type == INPUTMAP_BIND_KEY)
	{
		const char* name = SDL_GetKeyName(SDL_GetKeyFromScancode((SDL_Scancode)binding->code));
		snprintf(out, outlen, "%s", (name && *name) ? name : "?");
		return;
	}

	if (!InputMap_FormatBinding(binding, out, outlen) || strcmp(out, "NONE") == 0)
	{
		snprintf(out, outlen, "-");
	}
}

static void build_pair(const InputMap* map, int device, int action, int selected_slot,
                       char* out, size_t outlen)
{
	char first[32];
	char second[32];
	slot_text(map, device, action, 0, first, sizeof(first));
	slot_text(map, device, action, 1, second, sizeof(second));

	if (selected_slot == 0)
	{
		snprintf(out, outlen, "[%s],%s", first, second);
	}
	else if (selected_slot == 1)
	{
		snprintf(out, outlen, "%s,[%s]", first, second);
	}
	else
	{
		snprintf(out, outlen, "%s,%s", first, second);
	}
}

static void draw_actions(const InputMap* map)
{
	int action;
	int column = InputUI_SelectedColumn();
	int selected = InputUI_SelectedAction();
	char line[128];
	int y;

	PrintString(UI_WIDTH / 2, 12, UI_COLOUR_TEXT, (char*)"INPUT SETTINGS", FF_CENTER);

	snprintf(line, sizeof(line), "Keyboard %s   Gamepad %s   Pad %d/%d",
	         map->keyboard_enabled ? "ON" : "OFF",
	         map->gamepad_enabled ? "ON" : "OFF",
	         map->gamepad_index,
	         InputMap_GamepadCount());
	PrintString(UI_WIDTH / 2, 28, UI_COLOUR_HINT, line, FF_CENTER);

	{
		int first = selected < 9 ? 0 : selected - 8;
		int last = first + 9;
		if (last > INPUTMAP_ACTION_COUNT)
		{
			last = INPUTMAP_ACTION_COUNT;
		}
		for (action = first; action < last; ++action)
		{
			char keyboard[96];
			char gamepad[96];
			int colour = (action == selected) ? UI_COLOUR_SELECTED : UI_COLOUR_TEXT;
			y = UI_ACTION_FIRST_ROW + (action - first) * UI_ROW_HEIGHT;

		build_pair(map, INPUTMAP_DEVICE_KEYBOARD, action,
		           column < 2 ? column : -1, keyboard, sizeof(keyboard));
		build_pair(map, INPUTMAP_DEVICE_GAMEPAD, action,
		           column >= 2 ? column - 2 : -1, gamepad, sizeof(gamepad));

			if (action == selected)
			{
				PrintString(UI_ACTION_X - 10, y, UI_COLOUR_SELECTED, (char*)">", 0);
			}
			PrintString(UI_ACTION_X, y, colour, (char*)InputMap_ActionName(action), 0);
			PrintString(UI_KEYBOARD_X, y, colour, keyboard, 0);
			PrintString(UI_GAMEPAD_X, y, colour, gamepad, 0);
			}
	}

	if (InputUI_IsCapturing())
	{
		PrintString(UI_WIDTH / 2, 196, UI_COLOUR_SELECTED,
		            (char*)"Press a key or gamepad control", FF_SMALL | FF_CENTER);
		snprintf(line, sizeof(line), "for %s / %s %d - Esc cancels",
		         InputMap_ActionName(selected),
		         column < 2 ? "keyboard" : "gamepad",
		         (column < 2 ? column : column - 2) + 1);
		PrintString(UI_WIDTH / 2, 212, UI_COLOUR_HINT, line, FF_SMALL | FF_CENTER);
	}
	else
	{
		snprintf(line, sizeof(line), "%s", InputUI_Status());
		if (line[0])
		{
			PrintString(UI_WIDTH / 2, 196, UI_COLOUR_TEXT, line, FF_SMALL | FF_CENTER);
		}
		PrintString(UI_WIDTH / 2, 218, UI_COLOUR_HINT,
		            (char*)"Arrows  Enter bind  Tab devices  R defaults  Esc close",
		            FF_SMALL | FF_CENTER);
	}
}

static void draw_devices(const InputMap* map)
{
	char line[160];
	int row = InputUI_DeviceRow();
	const char* name;

	PrintString(UI_WIDTH / 2, 12, UI_COLOUR_TEXT, (char*)"INPUT DEVICES", FF_CENTER);

	if (row == 0) PrintString(60 - 10, 50, UI_COLOUR_SELECTED, (char*)">", FF_SMALL);
	PrintString(60, 50, row == 0 ? UI_COLOUR_SELECTED : UI_COLOUR_TEXT,
	            (char*)(map->keyboard_enabled ? "Keyboard: ON" : "Keyboard: OFF"), FF_SMALL);

	if (row == 1) PrintString(60 - 10, 74, UI_COLOUR_SELECTED, (char*)">", FF_SMALL);
	PrintString(60, 74, row == 1 ? UI_COLOUR_SELECTED : UI_COLOUR_TEXT,
	            (char*)(map->gamepad_enabled ? "Gamepad: ON" : "Gamepad: OFF"), FF_SMALL);

	if (row == 2) PrintString(60 - 10, 98, UI_COLOUR_SELECTED, (char*)">", FF_SMALL);
	snprintf(line, sizeof(line), "Gamepad index: %d (%d controller%s)",
	         map->gamepad_index, InputMap_GamepadCount(),
	         InputMap_GamepadCount() == 1 ? "" : "s");
	PrintString(60, 98, row == 2 ? UI_COLOUR_SELECTED : UI_COLOUR_TEXT, line, FF_SMALL);

	name = InputMap_GamepadNameAt(map->gamepad_index);
	if (name)
	{
		snprintf(line, sizeof(line), "Name: %.70s", name);
		PrintString(60, 122, UI_COLOUR_HINT, line, FF_SMALL);
	}

	if (map->gamepad_guid[0])
	{
		snprintf(line, sizeof(line), "GUID: %.60s", map->gamepad_guid);
		PrintString(60, 138, UI_COLOUR_HINT, line, FF_SMALL);
	}

	snprintf(line, sizeof(line), "Config: %.60s", InputMap_ConfigPath());
	PrintString(60, 154, UI_COLOUR_HINT, line, FF_SMALL);

	snprintf(line, sizeof(line), "%s", InputUI_Status());
	if (line[0])
	{
		PrintString(UI_WIDTH / 2, 196, UI_COLOUR_TEXT, line, FF_SMALL | FF_CENTER);
	}
	PrintString(UI_WIDTH / 2, 218, UI_COLOUR_HINT,
	            (char*)"Up/Down  Left/Right  Tab actions  R defaults  Esc close",
	            FF_SMALL | FF_CENTER);
}

void InputUI_Draw(void)
{
	const InputMap* map;

	InputUI_NotifyDraw();
	if (!InputUI_IsOpen())
	{
		return;
	}

	DrawF4(0, 0, 512, 240, 0, 0x2A200000);
	DrawF4(0, 0, 512, 240, 0, 0x2A200000);
	DrawF4(0, 0, 512, 240, 0, 0x2A200000);
	DrawF4(0, 0, 512, 240, 0, 0x2A200000);
	DrawF4(0, 0, 512, 240, 0, 0x2A200000);
	map = InputMap_Current();
	if (!map)
	{
		return;
	}

	if (InputUI_Screen() == 0)
	{
		draw_actions(map);
	}
	else
	{
		draw_devices(map);
	}

}
