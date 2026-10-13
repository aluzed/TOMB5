void AnimateItem(struct ITEM_INFO* item)
{
assert(re943_fixture_domain(item));
assert(item && anims && changes && ranges && commands && item->anim_number==0 && !item->gravity_status);
ANIM_STRUCT* a=&anims[item->anim_number];
assert(!a->number_commands && !a->velocity && !a->acceleration && !a->Xvelocity && !a->Xacceleration);
item->hit_status=0;item->touch_bits=0;
item->frame_number=static_cast<short>(static_cast<unsigned short>(item->frame_number)+1u);
if(a->number_changes>0 && GetChange(item,a)){
 a=&anims[item->anim_number];item->current_anim_state=a->current_anim_state;
 if(item->required_anim_state==item->current_anim_state)item->required_anim_state=0;
}
assert(item->frame_number<=a->frame_end && !a->number_commands && !a->velocity && !a->acceleration && !a->Xvelocity && !a->Xacceleration);
item->speed=0;
}
