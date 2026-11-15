#include "LION.H"

#include "DRAW.H"
#include "BOX.H"
#include "LARA.H"
#include "OBJECTS.H"
#include "SETUP.H"
#include "CONTROL.H"
#include "TOMB4FX.H"
#include "STYPES.H"

#include "EFFECTS.H"
#include "SOUND.H"
#include "GETSTUFF.H"
#include "GAMEFLOW.H"
#include "SPHERES.H"
#include "MATHS.H"
#include "DEBRIS.H"
#if PC_VERSION
#include "GAME.H"
#endif

#if PSX_VERSION || PSXPC_VERSION || SAT_VERSION
#include "MISC.H"
#include "FXTRIG.H"
#endif

struct BITE_INFO LION_BITE_1 = { -2, -10, 0x0FA, 0x15 };
struct BITE_INFO LION_BITE_2 = { -2, -10, 0x84, 0x15 };

void InitialiseLion(short item_num)
{
	struct ITEM_INFO* item = &items[item_num];
	
	InitialiseCreature(item_num);
	item->anim_number = objects[LION].anim_index;
	item->frame_number = anims[objects[LION].anim_index].frame_base;
	item->goal_anim_state = 1;
	item->current_anim_state = 1;
}

void LionControl(short item_num)
{
	short angle;
	short required;
	char *data;
	struct ITEM_INFO* item;
	short Lion_Object;
	short Lion_DefaultAnim;
	short Creature_Turn;
	short Creature_Angle;
	short requiredAngle;
	short requiredAnimState;
	int v9;
	int v10;
	struct AI_info info;
	struct creature_info* crinfo;

	if (CreatureActive(item_num))
	{
		requiredAngle = 0;
		Creature_Angle = 0;
		angle = 0;
		required = 0;
		crinfo = (struct creature_info*)items[item_num].data;
		item = &items[item_num];
		if (items[item_num].hit_points <= 0)
		{
			item->hit_points = 0;
			if (item->current_anim_state != 5)
			{
				Lion_Object = objects[LION].anim_index + (GetRandomControl() & 1) + 7;
				item->anim_number = Lion_Object;
				Lion_DefaultAnim = anims[Lion_Object].frame_base;
				item->current_anim_state = 5;
				item->frame_number = Lion_DefaultAnim;
			}
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		}
		CreatureAIInfo(item, &info);
		if (info.ahead)
			required = info.angle;
		GetCreatureMood(item, &info, 1);
		CreatureMood(item, &info, 1);
		Creature_Turn = CreatureTurn(item, crinfo->maximum_turn);
		Creature_Angle = Creature_Turn;
		requiredAngle = -16 * Creature_Turn;
		switch (item->current_anim_state)
		{
		case 1:
			crinfo->maximum_turn = 0;
			requiredAnimState = item->required_anim_state;
			if (requiredAnimState)
			{
				item->goal_anim_state = requiredAnimState;
				CreatureTilt(item, angle);
				CreatureJoint(item, 0, requiredAngle);
				CreatureJoint(item, 1, required);
				CreatureAnimation(item_num, Creature_Angle, 0);
				return;
			}
			if (crinfo->mood == BORED_MOOD)
			{
				if (!(GetRandomControl() & 0x3F))
					item->goal_anim_state = 2;
				CreatureTilt(item, angle);
				CreatureJoint(item, 0, requiredAngle);
				CreatureJoint(item, 1, required);
				CreatureAnimation(item_num, Creature_Angle, 0);
				return;
			}
			if (info.ahead)
			{
				if (item->touch_bits & 0x200048)
				{
					item->goal_anim_state = 7;
					CreatureTilt(item, angle);
					CreatureJoint(item, 0, requiredAngle);
					CreatureJoint(item, 1, required);
					CreatureAnimation(item_num, Creature_Angle, 0);
					return;
				}
				if (info.distance < 0x100000)
				{
					item->goal_anim_state = 4;
					CreatureTilt(item, angle);
					CreatureJoint(item, 0, requiredAngle);
					CreatureJoint(item, 1, required);
					CreatureAnimation(item_num, Creature_Angle, 0);
					return;
				}
			}
			item->goal_anim_state = 3;
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		case 2:
			crinfo->maximum_turn = ANGLE(2);
			if (crinfo->mood == BORED_MOOD)
				if (GetRandomControl() < 128)
				{
					item->required_anim_state = 6;
					item->goal_anim_state = 1;
				}
			item->goal_anim_state = 1;
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		case 3:
			crinfo->maximum_turn = ANGLE(5);
			angle = Creature_Turn;
			if (crinfo->mood == BORED_MOOD)
			{
				if (info.ahead && info.distance < 0x100000)
				{
					item->goal_anim_state = 1;
				}
				else if (item->touch_bits & 0x200048 && info.ahead)
				{
					item->goal_anim_state = 1;
				}
				else if (crinfo->mood != ESCAPE_MOOD)
				{
					if (GetRandomControl() < 128)
					{
						item->required_anim_state = 6;
						item->goal_anim_state = 1;
					}
				}
			}
			else
			{
				item->goal_anim_state = 1;
			}
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		case 4:
			if (!item->required_anim_state && item->touch_bits & 0x200048)
			{
				lara_item->hit_points -= 200;
				lara_item->hit_status = TRUE;
				CreatureEffectT(item, &LION_BITE_1, 10, item->pos.y_rot, DoBloodSplat);
				item->required_anim_state = 1;
			}
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		case 7:
			crinfo->maximum_turn = ANGLE(1);
			if (!item->required_anim_state && item->touch_bits & 0x200048)
			{
				CreatureEffectT(item,&LION_BITE_2,10,item->pos.y_rot, DoBloodSplat);
				lara_item->hit_points -= 60;
				lara_item->hit_status = TRUE;
				item->required_anim_state= 1;
			}
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		default:
			CreatureTilt(item, angle);
			CreatureJoint(item, 0, requiredAngle);
			CreatureJoint(item, 1, required);
			CreatureAnimation(item_num, Creature_Angle, 0);
			return;
		}
	}
}
/* Porté depuis TOMB5pc/game/gladiatr.cpp (gladiateur du Colosseum). */
static struct BITE_INFO gladiator_hit = { 0, 0, 0, 16 };

void InitialiseGladiator(short item_number)
{
	struct ITEM_INFO* item;

	item = &items[item_number];
	InitialiseCreature(item_number);
	item->anim_number = objects[GLADIATOR].anim_index;
	item->frame_number = anims[item->anim_number].frame_base;
	item->goal_anim_state = 1;
	item->current_anim_state = 1;

	if (item->trigger_flags == 1)
		item->meshswap_meshbits = -1;
}

void GladiatorControl(short item_number)
{
	struct ITEM_INFO* item;
	struct creature_info* gladiator;
	struct room_info* r;
	struct FLOOR_INFO* floor;
	struct AI_info info;
	struct PHD_VECTOR pos;
	long distance, dx, dz, front;
	short tilt, angle, head_x, head, torso_y, da;

	if (!CreatureActive(item_number))
		return;

	tilt = 0;
	angle = 0;
	head = 0;
	head_x = 0;
	torso_y = 0;
	item = &items[item_number];
	gladiator = (struct creature_info*)item->data;

	if (item->hit_points <= 0)
	{
		item->hit_points = 0;

		if (item->current_anim_state != 6)
		{
			item->anim_number = objects[GLADIATOR].anim_index + 16;
			item->frame_number = anims[item->anim_number].frame_base;
			item->current_anim_state = 6;
		}
	}
	else
	{
		if (item->ai_bits)
			GetAITarget(gladiator);
		else if (gladiator->hurt_by_lara)
			gladiator->enemy = lara_item;

		CreatureAIInfo(item, &info);

		if (gladiator->enemy == lara_item)
		{
			distance = info.distance;
			da = info.angle;
			front = 1;
		}
		else
		{
			dx = lara_item->pos.x_pos - item->pos.x_pos;
			dz = lara_item->pos.z_pos - item->pos.z_pos;
			da = (short)(phd_atan_asm(dz, dx) - item->pos.y_rot);
			front = abs(da) < 0x4000;
			distance = dx * dx + dz * dz;
		}

		GetCreatureMood(item, &info, 1);
		CreatureMood(item, &info, 1);
		angle = CreatureTurn(item, gladiator->maximum_turn);

		if (info.ahead)
		{
			torso_y = info.angle >> 1;
			head = info.angle >> 1;
			head_x = info.x_angle;
		}

		switch (item->current_anim_state)
		{
		case 1:
			gladiator->flags = 0;
			gladiator->maximum_turn = gladiator->mood == BORED_MOOD ? 0 : 364;
			head = da;

			if ((item->ai_bits & AI_GUARD) || (!(GetRandomControl() & 0x1F) && (info.distance > 0x100000 || gladiator->mood != ATTACK_MOOD)))
				head = AIGuard(gladiator);
			else if (item->ai_bits & AI_PATROL1)
				item->goal_anim_state = 2;
			else if (gladiator->mood == ESCAPE_MOOD)
				item->goal_anim_state = (lara.target != item && info.ahead && !item->hit_status) ? 1 : 2;
			else if (gladiator->mood != BORED_MOOD && (!(item->ai_bits & AI_FOLLOW) || (!gladiator->reached_goal && distance <= 0x400000)))
			{
				if (lara.target == item && front && distance < 0x240000 && (GetRandomControl() & 1) &&
					(lara.gun_type == WEAPON_SHOTGUN || !(GetRandomControl() & 0xF)) && item->mesh_bits == (unsigned long)-1)
					item->goal_anim_state = 4;
				else if (info.bite && info.distance < 0xA3C29)
					item->goal_anim_state = (GetRandomControl() & 1) ? 8 : 9;
				else
					item->goal_anim_state = 2;
			}
			else if (item->required_anim_state)
				item->goal_anim_state = item->required_anim_state;
			else if (!(GetRandomControl() & 0x3F))
				item->goal_anim_state = 2;

			break;

		case 2:
			gladiator->flags = 0;
			head = da;
			gladiator->maximum_turn = gladiator->mood == BORED_MOOD ? 364 : 1274;

			if (item->ai_bits & AI_PATROL1)
			{
				item->goal_anim_state = 2;
				head = 0;
			}
			else if (gladiator->mood == ESCAPE_MOOD)
				item->goal_anim_state = 3;
			else if (gladiator->mood == BORED_MOOD)
			{
				if (!(GetRandomControl() & 0x3F))
					item->goal_anim_state = 1;
			}
			else if (info.distance < 0x100000)
				item->goal_anim_state = 1;
			else if (info.bite && info.distance < 0x400000)
				item->goal_anim_state = 11;
			else if (!info.ahead || info.distance > 0x240000)
				item->goal_anim_state = 3;

			break;

		case 3:
			gladiator->LOT.is_jumping = 0;

			if (info.ahead)
				head = info.angle;

			gladiator->maximum_turn = 2002;
			tilt = angle / 2;

			if (item->ai_bits & AI_GUARD)
			{
				gladiator->maximum_turn = 0;
				item->goal_anim_state = 1;
			}
			else if (gladiator->mood == ESCAPE_MOOD)
			{
				if (lara.target != item && info.ahead)
					item->goal_anim_state = 1;
			}
			else if (item->ai_bits & AI_FOLLOW)
			{
				if (gladiator->reached_goal || distance > 0x400000)
					item->goal_anim_state = 1;
			}
			else if (gladiator->mood == BORED_MOOD)
				item->goal_anim_state = 2;
			else if (info.distance < 0x240000)
				item->goal_anim_state = info.bite ? 10 : 2;

			break;

		case 4:

			if (item->hit_status)
			{
				if (!front)
					item->goal_anim_state = 1;
			}
			else if (lara.target != item || !(GetRandomControl() & 0x7F))
				item->goal_anim_state = 1;

			break;

		case 5:

			if (lara.target != item)
				item->goal_anim_state = 1;

			break;

		case 8:
		case 9:
		case 10:
		case 11:
			gladiator->maximum_turn = 0;

			if (abs(info.angle) < 1274)
				item->pos.y_rot += info.angle;
			else if (info.angle < 0)
				item->pos.y_rot -= 1274;
			else
				item->pos.y_rot += 1274;

			if (item->frame_number > anims[item->anim_number].frame_base + 10)
			{
				r = &room[item->room_number];
				pos.x = 0;
				pos.y = 0;
				pos.z = 0;
				GetJointAbsPosition(item, &pos, 16);
				floor = &r->floor[((pos.x - r->x) >> 10) * r->x_size + ((pos.z - r->z) >> 10)];

				if (floor->stopper)
				{
					for (int i = 0; i < r->num_meshes; i++)
					{
						if (!((r->mesh[i].z ^ pos.z) & ~1023) && !((r->mesh[i].x ^ pos.x) & ~1023) &&
							r->mesh[i].static_number >= 50 && r->mesh[i].static_number <= 59)
						{
							ShatterObject(0, &r->mesh[i], -64, lara_item->room_number, 0);
							SoundEffect(ShatterSounds[gfCurrentLevel][r->mesh[i].static_number - 50], (struct PHD_3DPOS*)&r->mesh[i].x, SFX_DEFAULT);
							r->mesh[i].Flags &= ~1;
							floor->stopper = 0;
							GetHeight(floor, pos.x, pos.y, pos.z);
							TestTriggers(trigger_index, 1, 0);
						}
					}
				}

				if (!gladiator->flags && (item->touch_bits & 0x6000))
				{
					lara_item->hit_points -= 120;
					lara_item->hit_status = 1;
					CreatureEffectT(item, &gladiator_hit, 10, item->pos.y_rot, DoBloodSplat);
					SoundEffect(SFX_LARA_THUD, &item->pos, SFX_DEFAULT);
					gladiator->flags = 1;
				}
			}

			break;
		}
	}

	CreatureTilt(item, tilt);
	CreatureJoint(item, 0, torso_y);
	CreatureJoint(item, 1, head_x);
	CreatureJoint(item, 2, head);
	CreatureAnimation(item_number, angle, 0);
}
