#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "INPUTMAP.H"
#include "CONTROL.H"

static_assert(IN_FORWARD == INPUTMAP_IN_FORWARD, "IN_FORWARD contract");
static_assert(IN_BACK == INPUTMAP_IN_BACK, "IN_BACK contract");
static_assert(IN_LEFT == INPUTMAP_IN_LEFT, "IN_LEFT contract");
static_assert(IN_RIGHT == INPUTMAP_IN_RIGHT, "IN_RIGHT contract");
static_assert(IN_JUMP == INPUTMAP_IN_JUMP, "IN_JUMP contract");
static_assert(IN_DRAW == INPUTMAP_IN_DRAW, "IN_DRAW contract");
static_assert(IN_ACTION == INPUTMAP_IN_ACTION, "IN_ACTION contract");
static_assert(IN_WALK == INPUTMAP_IN_WALK, "IN_WALK contract");
static_assert(IN_LOOK == INPUTMAP_IN_LOOK, "IN_LOOK contract");
static_assert(IN_ROLL == INPUTMAP_IN_ROLL, "IN_ROLL contract");
static_assert(IN_DUCK == INPUTMAP_IN_DUCK, "IN_DUCK contract");
static_assert(IN_SPRINT == INPUTMAP_IN_SPRINT, "IN_SPRINT contract");
static_assert(IN_UNK1 == INPUTMAP_RAW_SELECT, "select contract");
static_assert(IN_UNK8 == INPUTMAP_RAW_START, "start contract");
static_assert(IN_DPAD_UP == INPUTMAP_RAW_UP, "up contract");
static_assert(IN_DPAD_DOWN == INPUTMAP_RAW_DOWN, "down contract");
static_assert(IN_DPAD_LEFT == INPUTMAP_RAW_LEFT, "left contract");
static_assert(IN_DPAD_RIGHT == INPUTMAP_RAW_RIGHT, "right contract");
static_assert(IN_L1 == INPUTMAP_RAW_L1, "L1 contract");
static_assert(IN_L2 == INPUTMAP_RAW_L2, "L2 contract");
static_assert(IN_R1 == INPUTMAP_RAW_R1, "R1 contract");
static_assert(IN_R2 == INPUTMAP_RAW_R2, "R2 contract");
static_assert(IN_TRIANGLE == INPUTMAP_RAW_TRIANGLE, "triangle contract");
static_assert(IN_CIRCLE == INPUTMAP_RAW_CIRCLE, "circle contract");
static_assert(IN_CROSS == INPUTMAP_RAW_CROSS, "cross contract");
static_assert(IN_SQUARE == INPUTMAP_RAW_SQUARE, "square contract");

static int set_token(InputMapSnapshot* snapshot, const char* token)
{
	char copy[128];
	char* first;
	char* second;
	char* third;

	snprintf(copy, sizeof(copy), "%s", token);
	first = copy;
	second = strchr(first, ':');
	if (!second)
	{
		return 0;
	}
	*second++ = '\0';
	third = strchr(second, ':');
	if (third)
	{
		*third++ = '\0';
	}

	if (strcmp(first, "K") == 0)
	{
		InputMapBinding binding;
		char error[128];
		if (!InputMap_ParseBinding(INPUTMAP_DEVICE_KEYBOARD, second, &binding, error, sizeof(error)) ||
		    binding.type != INPUTMAP_BIND_KEY)
		{
			return 0;
		}
		snapshot->keyboard[binding.code] = 1;
		return 1;
	}
	if (strcmp(first, "P") == 0)
	{
		InputMapBinding binding;
		char error[128];
		if (!InputMap_ParseBinding(INPUTMAP_DEVICE_GAMEPAD, second, &binding, error, sizeof(error)) ||
		    binding.type != INPUTMAP_BIND_PAD_BUTTON)
		{
			return 0;
		}
		snapshot->pad_buttons[binding.code] = 1;
		return 1;
	}
	if (strcmp(first, "A") == 0)
	{
		InputMapBinding binding;
		char error[128];
		float value;
		if (!third || !InputMap_ParseBinding(INPUTMAP_DEVICE_GAMEPAD, second, &binding, error, sizeof(error)) ||
		    binding.type != INPUTMAP_BIND_PAD_AXIS)
		{
			return 0;
		}
		value = (float)atof(third);
		snapshot->pad_axes[binding.code] = value;
		return 1;
	}
	return 0;
}

static void print_actions(unsigned long bits)
{
	int action;
	int first = 1;
	printf("actions=");
	for (action = 0; action < INPUTMAP_ACTION_COUNT; ++action)
	{
		unsigned long mask = 0;
		switch (action)
		{
		case INPUTMAP_ACTION_FORWARD: mask = 0x00000001UL; break;
		case INPUTMAP_ACTION_BACK: mask = 0x00000002UL; break;
		case INPUTMAP_ACTION_LEFT: mask = 0x00000004UL; break;
		case INPUTMAP_ACTION_RIGHT: mask = 0x00000008UL; break;
		case INPUTMAP_ACTION_JUMP: mask = 0x00000010UL; break;
		case INPUTMAP_ACTION_DRAW: mask = 0x00000020UL; break;
		case INPUTMAP_ACTION_ACTION: mask = 0x00000040UL; break;
		case INPUTMAP_ACTION_WALK: mask = 0x00000080UL; break;
		case INPUTMAP_ACTION_LOOK: mask = 0x00000200UL; break;
		case INPUTMAP_ACTION_DUCK: mask = 0x20000000UL; break;
		case INPUTMAP_ACTION_SPRINT: mask = 0x40000000UL; break;
		default: break;
		}
		if (mask && (bits & mask))
		{
			printf("%s%s", first ? "" : ",", InputMap_ActionName(action));
			first = 0;
		}
	}
	printf("\n");
}

int main(int argc, char** argv)
{
	if (argc < 2)
	{
		fprintf(stderr, "usage: %s <defaults-save|eval|error|flags> ...\n", argv[0]);
		return 2;
	}

	if (strcmp(argv[1], "defaults-save") == 0)
	{
		InputMap map;
		if (argc != 3)
		{
			return 2;
		}
		InputMap_Defaults(&map);
		if (!InputMap_Save(&map, argv[2]))
		{
			printf("error=%s\n", InputMap_LastError());
			return 1;
		}
		printf("saved=%s\n", argv[2]);
		return 0;
	}

	if (strcmp(argv[1], "eval") == 0)
	{
		InputMap map;
		InputMapSnapshot snapshot;
		int i;
		int loaded;
		unsigned long actions;
		unsigned short pad;

		if (argc < 3)
		{
			return 2;
		}
		loaded = InputMap_Load(&map, argv[2]);
		if (loaded < 0)
		{
			printf("error=%s\n", InputMap_LastError());
			return 1;
		}
		memset(&snapshot, 0, sizeof(snapshot));
		for (i = 3; i < argc; ++i)
		{
			if (!set_token(&snapshot, argv[i]))
			{
				printf("error=bad token %s\n", argv[i]);
				return 1;
			}
		}
		actions = InputMap_EvaluateActions(&map, &snapshot);
		pad = InputMap_EvaluatePad(&map, &snapshot, 1, 1);
		print_actions(actions);
		printf("pad=%04X\n", pad);
		printf("loaded=%d\n", loaded);
		printf("use_control_option=%d\n", map.use_control_option);
		printf("keyboard=%d\n", map.keyboard_enabled);
		printf("gamepad=%d\n", map.gamepad_enabled);
		printf("index=%d\n", map.gamepad_index);
		printf("deadzone=%.2f\n", (double)map.axis_deadzone);
		return 0;
	}

	if (strcmp(argv[1], "error") == 0)
	{
		InputMap map;
		int loaded;
		if (argc != 3)
		{
			return 2;
		}
		loaded = InputMap_Load(&map, argv[2]);
		printf("loaded=%d\n", loaded);
		printf("error=%s\n", InputMap_LastError());
		return 0;
	}

	fprintf(stderr, "unknown command\n");
	return 2;
}
