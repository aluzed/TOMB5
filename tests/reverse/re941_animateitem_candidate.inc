// Test-only exact finite16 domain; never activate production.
void AnimateItem(struct ITEM_INFO* item)
{
 extern bool re941_fixture_domain(const ITEM_INFO*);
 assert(re941_fixture_domain(item));
 assert(item && anims && objects && commands && item->anim_number==0 && !item->gravity_status);
 ANIM_STRUCT* a=&anims[0];
 assert(!a->number_changes && a->number_commands==2 && commands[a->command_index]==4 && commands[a->command_index+1]==4);
 assert(a->velocity==0 && a->acceleration==0 && a->Xvelocity==0 && a->Xacceleration==0);
 item->hit_status=0;item->touch_bits=0;++item->frame_number;
 if(item->frame_number>a->frame_end){
  for(int j=0;j<a->number_commands;++j){
   if(objects[item->object_number].intelligent && item->after_death==0)item->after_death=1;
   item->status=2;
  }
  item->anim_number=a->jump_anim_num;item->frame_number=a->jump_frame_num;a=&anims[item->anim_number];
  if(item->current_anim_state!=a->current_anim_state){item->current_anim_state=a->current_anim_state;item->goal_anim_state=a->current_anim_state;}
  if(item->required_anim_state==item->current_anim_state)item->required_anim_state=0;
  assert(a->number_commands==0 && a->number_changes==0);
 }
 item->speed=0;
}
