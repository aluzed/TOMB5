#include "LOT.H"

#include "CAMERA.H"
#include "SPECIFIC.H"
#include "MALLOC.H"
#include "BOX.H"
#include "DRAW.H"
#include "CONTROL.H"
#include "OBJECTS.H"
#include "LARA.H"

#if PC_VERSION
#include "INIT.H"
#endif

int slots_used;
short nAIObjects;
struct AIOBJECT* AIObjects;
struct creature_info* baddie_slots;

//void /*$ra*/ CreateZone(struct ITEM_INFO *item /*$t1*/)
void CreateZone(struct ITEM_INFO* item)//4E330, 4E794
{
	struct creature_info* creature;
	struct room_info* r;
	struct box_node* node;
	short* zone;
	short* flip;
	short zone_number, flip_number;
	int i;

	creature = (struct creature_info*)item->data;
	r = &room[item->room_number];
	item->box_number = r->floor[((item->pos.z_pos - r->z) >> 10) + r->x_size * ((item->pos.x_pos - r->x) >> 10)].box;

	if (creature->LOT.fly)
	{
		creature->LOT.zone_count = 0;

		for (i = 0; i < number_boxes; i++)
		{
			node = &creature->LOT.node[i];
			node->box_number = i;
			creature->LOT.zone_count++;
		}
	}
	else
	{
		zone = ground_zone[creature->LOT.zone][0];
		flip = ground_zone[creature->LOT.zone][1];
		zone_number = zone[item->box_number];
		flip_number = flip[item->box_number];
		creature->LOT.zone_count = 0;
		node = creature->LOT.node;

		for (i = 0; i < number_boxes; i++)
		{
			if (*zone == zone_number || *flip == flip_number)
			{
				node->box_number = i;
				node++;
				creature->LOT.zone_count++;
			}

			zone++;
			flip++;
		}
	}
}

//Only called when enemy is triggered
void InitialiseSlot(short item_number /*$s0*/, int slot /*$a1*/)//4E13C, 4E5A0 (F)
{
	struct creature_info* creature = &baddie_slots[slot];
	struct ITEM_INFO* item = &items[item_number];
	item->data = creature;

	creature->item_num = item_number;
	creature->mood = BORED_MOOD;
	creature->joint_rotation[0] = 0;
	creature->joint_rotation[1] = 0;
	creature->joint_rotation[2] = 0;
	creature->joint_rotation[3] = 0;

	creature->alerted = 0;
	creature->head_left = 0;
	creature->head_right = 0;
	creature->reached_goal = 0;
	creature->hurt_by_lara = 0;
	creature->patrol2 = 0;
	creature->jump_ahead = 0;
	creature->monkey_ahead = 0;

	creature->maximum_turn = ANGLE(1);

	creature->flags = 0;
	creature->enemy = 0;

	creature->LOT.can_jump = FALSE;
	creature->LOT.can_monkey = FALSE;

	creature->LOT.is_jumping = FALSE;
	creature->LOT.is_monkeying = FALSE;

	creature->LOT.step = 256;
	creature->LOT.drop = -512;
	creature->LOT.block_mask = 16384;
	creature->LOT.fly = 0;
	creature->LOT.zone = BASIC_ZONE;

	switch (item->object_number)
	{
	case SAS:
	case BLUE_GUARD:
	case MAFIA2:
	case SAILOR:
		creature->LOT.step = SECTOR(1);
		creature->LOT.drop = SECTOR(-1);
		creature->LOT.can_jump = TRUE;
		creature->LOT.zone = HUMAN_ZONE;
		break;

	case HITMAN:
		creature->LOT.step = SECTOR(1);
		creature->LOT.drop = SECTOR(-1);
		creature->LOT.can_jump = TRUE;
		creature->LOT.can_monkey = TRUE;
		creature->LOT.zone = HUMAN_ZONE;
		break;

	case CROW:
	case WILLOWISP:
	case REAPER:
	case GREEN_TEETH:
	case ATTACK_SUB:
		creature->LOT.step = SECTOR(20);
		creature->LOT.drop = SECTOR(-20);
		creature->LOT.fly = 16;
		creature->LOT.zone = FLYER_ZONE;
		break;
	}

	ClearLOT(&creature->LOT);

	if (item_number != lara.item_number)
		CreateZone(item);

	slots_used++;
}

int EnableBaddieAI(short item_number, int Always)//4DF0C(<), 4E370 (F)
{
	int x;
	int y;
	int z;
	int worstslot;
	int slot;
	int worstdist;
	int dist;
	struct ITEM_INFO* item;
	struct creature_info* creature;

	if (items[item_number].data == NULL)
	{
		creature = &baddie_slots[0];

		if (slots_used < 5)
		{
			//loc_4DF68
			for(slot = 0; slot < 5; slot++, creature++)
			{
				if (creature->item_num == -1)
				{
					//loc_4E0C4
					InitialiseSlot(item_number, slot);
					return 1;
				}
			}
		}
		//loc_4DF88
		if (!Always)
		{
			item = &items[item_number];

			x = (item->pos.x_pos - camera.pos.x) >> 8;
			y = (item->pos.y_pos - camera.pos.y) >> 8;
			z = (item->pos.z_pos - camera.pos.z) >> 8;

			worstdist = (x * x) + (y * y) + (z * z);
		}
		else
		{
			//loc_4E000
			worstdist = 0;
		}

		//loc_4E01C
		worstslot = -1;
		creature = &baddie_slots[0];

		//loc_4E030
		for(slot = 0; slot < 5; slot++, creature++)
		{
			item = &items[creature->item_num];
			x = (item->pos.x_pos - camera.pos.x) >> 8;
			y = (item->pos.y_pos - camera.pos.y) >> 8;
			z = (item->pos.z_pos - camera.pos.z) >> 8;
			dist = (x * x) + (y * y) + (z * z);

			if (worstdist < dist)
			{
				worstdist = dist;
				worstslot = slot;
			}
			//loc_4E0A4
		}

		if (worstslot >= 0)
		{
			//loc_4E0CC
			items[baddie_slots[worstslot].item_num].status = 3;
			DisableBaddieAI(baddie_slots[worstslot].item_num);
			InitialiseSlot(item_number, worstslot);
			return 1;
		}

	}//loc_4E128
	
	return 0;
}

void DisableBaddieAI(short item_num)//4DEC0, 4E324 (F)
{
	struct ITEM_INFO* item = &items[item_num];
	struct creature_info* creature = (struct creature_info*)item->data;

	item->data = NULL;

	if (creature)
	{
		creature->item_num = -1;
		slots_used--;
	}
}

void InitialiseLOTarray(int allocmem)//4DE40(<), 4E2A4(<) (F)
{
	int i;

	if (allocmem)
		baddie_slots = (struct creature_info *)game_malloc(5 * sizeof(struct creature_info));
	
	for (i = 0; i < 5; i++)
	{
		baddie_slots[i].item_num = -1;

		if (allocmem)
		{
			baddie_slots[i].LOT.node = (struct box_node*)game_malloc(number_boxes * sizeof(struct box_node));
		}
	}

	slots_used = 0;
}

void ClearLOT(struct lot_info* LOT) // (F)
{
	struct box_node* node;
	int i;

	LOT->tail = 2047;
	LOT->head = 2048;
	LOT->search_number = 0;
	LOT->target_box = 2047;
	LOT->required_box = 2047;

	for(i = 0, node = LOT->node; i < number_boxes; i++, node++)
	{
		node->next_expansion = 2047;
		node->exit_box = 2047;
		node->search_number = 0;
	}
}