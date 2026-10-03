// Synthetic contract only: no game assets, captured memory or target bytes.
#include "CONTROL.H"
#include "ITEMS.H"
#include <cstdio>
#include <cstring>
ANIM_STRUCT* anims;
CHANGE_STRUCT* changes;
RANGE_STRUCT* ranges;
extern int GetChange(ITEM_INFO*, ANIM_STRUCT*);
static_assert(sizeof(void*)==4 && sizeof(ITEM_INFO)==144, "i386 fixture");
static int cases=0, failures=0, reset_failures=0;
static void check(int first_count,int second_count,int hit,int frame,int state_mode,int offset) {
 ITEM_INFO item, expected;
 std::memset(&item,53,sizeof(item));
 item.current_anim_state=state_mode==1?7:2;
 item.goal_anim_state=state_mode==2?11:7;
 item.anim_number=4;item.frame_number=frame;
 std::memcpy(&expected,&item,sizeof(item));
 ANIM_STRUCT animations[2]={}; CHANGE_STRUCT cs[5]={}; RANGE_STRUCT rs[12]={};
 animations[1].number_changes=3;animations[1].change_index=offset;
 for(int k=0;k<3;k++) {
  cs[offset+k].goal_anim_state=7;
  cs[offset+k].number_ranges=k==0?first_count:(k==1?second_count:1);
  cs[offset+k].range_index=1+4*k;
 }
 for(int k=0;k<12;k++) {
  rs[k].start_frame=80;rs[k].end_frame=90;
  rs[k].link_anim_num=20+k;rs[k].link_frame_num=100+k;
 }
 rs[5+hit].start_frame=10;rs[5+hit].end_frame=12;
 rs[9].start_frame=10;rs[9].end_frame=12;
 unsigned char old_a[sizeof(animations)],old_c[sizeof(cs)],old_r[sizeof(rs)];
 std::memcpy(old_a,animations,sizeof(animations));std::memcpy(old_c,cs,sizeof(cs));std::memcpy(old_r,rs,sizeof(rs));
 // Independent declarative oracle: enumerate all eligible (change,range)
 // pairs, then choose the lexicographically earliest matching pair.
 int selected=-1, rank=1000;
 if(item.current_anim_state!=item.goal_anim_state) {
  for(int c=0;c<5;c++) for(int r=0;r<12;r++) {
   bool owned=c>=offset && c<offset+3 && r>=cs[c].range_index && r<cs[c].range_index+cs[c].number_ranges;
   bool eligible=owned && cs[c].goal_anim_state==item.goal_anim_state && rs[r].start_frame<=frame && frame<=rs[r].end_frame;
   int order=12*c+r;
   if(eligible && order<rank){selected=r;rank=order;}
  }
 }
 if(selected>=0){expected.anim_number=rs[selected].link_anim_num;expected.frame_number=rs[selected].link_frame_num;}
 anims=animations;changes=cs;ranges=rs;
 int ret=GetChange(&item,&animations[1]);
 bool ok=ret==int(selected>=0) && !std::memcmp(&item,&expected,sizeof(item)) &&
  !std::memcmp(old_a,animations,sizeof(animations)) && !std::memcmp(old_c,cs,sizeof(cs)) && !std::memcmp(old_r,rs,sizeof(rs)) &&
  anims==animations && changes==cs && ranges==rs;
 cases++;if(!ok){failures++;if(first_count>0 && selected>=5)reset_failures++;}
 if(!ok && failures<=8)std::printf("FAIL first=%d second=%d hit=%d frame=%d state=%d offset=%d ret=%d selected=%d actual_anim=%d expected_anim=%d\n",first_count,second_count,hit,frame,state_mode,offset,ret,selected,item.anim_number,expected.anim_number);
}
int main(){
 const int frames[]={9,10,11,12,13};
 for(int first=0;first<=3;first++)for(int second=0;second<=3;second++)for(int hit=0;hit<3;hit++)
  for(int f:frames)for(int state=0;state<3;state++)for(int offset=0;offset<2;offset++)check(first,second,hit,f,state,offset);
 std::printf("SUMMARY cases=%d failures=%d reset_failures=%d\n",cases,failures,reset_failures);
 return failures?1:0;
}
