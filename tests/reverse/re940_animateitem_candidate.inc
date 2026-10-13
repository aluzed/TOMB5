// Private test-only finite movement candidate, never a production implementation.
void AnimateItem(struct ITEM_INFO* item)
{
 extern bool re940_fixture_domain(const ITEM_INFO*);
 assert(re940_fixture_domain(item));
 assert(item && anims && item->anim_number==0 && !item->gravity_status);
 ANIM_STRUCT* a=&anims[item->anim_number];
 assert(a->number_changes==0 && a->number_commands==0);
 assert(item->frame_number>=3 && item->frame_number<=10);
 assert(item->frame_number+1<=a->frame_end);
 item->hit_status=0;
 item->touch_bits=0;
 ++item->frame_number;
 int d=item->frame_number-a->frame_base;
 unsigned v=(unsigned)a->velocity+(unsigned)a->acceleration*(unsigned)d;
 unsigned x=(unsigned)a->Xvelocity+(unsigned)a->Xacceleration*(unsigned)d;
 item->speed=(short)((int)v>>16);
 int lateral=(int)x>>16;
 unsigned idx=((unsigned short)item->pos.y_rot>>3)&0x1ffe;
 unsigned li=(((unsigned short)item->pos.y_rot+16384)>>3)&0x1ffe;
 int dx=(rcossin_tbl[idx]*item->speed)>>12;
 int dz=(rcossin_tbl[idx+1]*item->speed)>>12;
 // Preserve the attributable overwritten lateral-X contribution, not intuition.
 item->pos.x_pos+=dx+(dx>>12);
 item->pos.z_pos+=dz+((rcossin_tbl[li+1]*lateral)>>12);
}
