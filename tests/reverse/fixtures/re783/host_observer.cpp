// BLOCKED-001 lot21 — suite2 CONTRAT observateur exactement type + vrais corps derriere.
// Observer NULL sans deref mais EXPECT NONNULL (meme baseline). Assertions IDENTIQUES baseline/candidate.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "COLLIDE_S.H"
#include "LARA.H"
#include "SETUP.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstring>
#include <cstddef>
#include <initializer_list>

room_info rooms[1]; room_info* room = rooms;
short data[64]; short* floor_data = data;
ITEM_INFO storage[4]; ITEM_INFO* items = storage; ITEM_INFO* lara_item;
lara_info lara; unsigned char InItemControlLoop; short ItemNewRoomNo; short ItemNewRooms[256][2];
extern object_info* objects; object_info object_storage[NUMBER_OBJECTS];
int height_type, tiltxoff, tiltyoff, OnObject; short* trigger_index; FLOOR_INFO cells[16];
long bone_storage[4]; long* bones = bone_storage;
void InitialiseLaraLoad(short) { __builtin_trap(); }
static const int X=1131,Z=1757,IY=4096,ACC=8192;
static int off0(){return (-X)&1023;}
static int level_of(int o){return o==BRIDGE_TILT1?IY+(off0()>>2):o==BRIDGE_TILT2?IY+(off0()>>1):IY;}
static int checks=0,fails=0;
static void check(bool ok,const char* w){++checks; if(!ok){++fails;printf("FAIL %s\n",w);}}

struct EV{int slot,index,x,y,z,in,out,null;}; static EV ev[64]; static int ncall=0,null_seen=0;
static ITEM_INFO* itbase=0;
static void obs(int slot,ITEM_INFO* i,int x,int y,int z,int* h,void(*body)(ITEM_INFO*,long,long,long,long*)){
 if(h==NULL){null_seen=1; if(ncall<64){ev[ncall]={slot,itbase?(int)(i-itbase):-1,x,y,z,0,0,1};++ncall;} return;}
 int in=*h; long t=in; body(i,x,y,z,&t); *h=(int)t;
 if(ncall<64){ev[ncall]={slot,itbase?(int)(i-itbase):-1,x,y,z,in,(int)t,0};++ncall;}
}
static void ff(ITEM_INFO*i,int x,int y,int z,int*h){obs(0,i,x,y,z,h,BridgeFlatFloor);}
static void fc(ITEM_INFO*i,int x,int y,int z,int*h){obs(1,i,x,y,z,h,BridgeFlatCeiling);}
static void tf1(ITEM_INFO*i,int x,int y,int z,int*h){obs(2,i,x,y,z,h,BridgeTilt1Floor);}
static void tc1(ITEM_INFO*i,int x,int y,int z,int*h){obs(3,i,x,y,z,h,BridgeTilt1Ceiling);}
static void tf2(ITEM_INFO*i,int x,int y,int z,int*h){obs(4,i,x,y,z,h,BridgeTilt2Floor);}
static void tc2(ITEM_INFO*i,int x,int y,int z,int*h){obs(5,i,x,y,z,h,BridgeTilt2Ceiling);}
static int cslot(int o){return o==BRIDGE_FLAT?1:o==BRIDGE_TILT1?3:5;}
static void cc(){memset(cells,0,sizeof cells);rooms[0].floor=cells;rooms[0].x_size=4;rooms[0].y_size=4;
 for(auto&c:cells){c.ceiling=32;c.floor=32;c.pit_room=0xFF;c.sky_room=0xFF;} cells[5].index=1;
 memset(&lara,0,sizeof lara);InItemControlLoop=1;ItemNewRoomNo=0;memset(ItemNewRooms,0,sizeof ItemNewRooms);lara_item=storage;}

int main(){
 setvbuf(stdout,NULL,_IONBF,0);
 objects=object_storage; memset(object_storage,0,sizeof object_storage); memset(bone_storage,0,sizeof bone_storage);
 itbase=storage;
 object_storage[BRIDGE_FLAT].floor=ff; object_storage[BRIDGE_FLAT].ceiling=fc;
 object_storage[BRIDGE_TILT1].floor=tf1; object_storage[BRIDGE_TILT1].ceiling=tc1;
 object_storage[BRIDGE_TILT2].floor=tf2; object_storage[BRIDGE_TILT2].ceiling=tc2;
 for(int pr=0;pr<2;++pr){ int A=pr==0?BRIDGE_FLAT:BRIDGE_TILT1,B=pr==0?BRIDGE_TILT1:BRIDGE_TILT2;
  int los=level_of(A)<level_of(B)?level_of(A):level_of(B); int his=level_of(A)>level_of(B)?level_of(A):level_of(B);
  for(int rev=0;rev<2;++rev){ int objs[2]={rev?B:A,rev?A:B};
   for(int mask=0;mask<4;++mask) for(int qi=0;qi<4;++qi){
    int qs[4]={los-1,level_of(A),level_of(B),his+1}; int query=qs[qi];
    cc(); memset(data,0,sizeof data);
    data[1]=(short)(0x8000|4);data[2]=0;data[3]=1;data[4]=(short)(0x8000|2);
    for(int k=5;k<31;++k) data[2*k]=(short)0x8000;
    for(int k=1;k<=2;++k){storage[k].object_number=(short)objs[k-1];
     storage[k].flags=(short)((mask>>(k-1)&1)?0x8000:0);
     storage[k].pos.x_pos=-3000;storage[k].pos.y_pos=IY;storage[k].pos.z_pos=7000;storage[k].pos.y_rot=0;}
    ncall=0;null_seen=0;memset(ev,0,sizeof ev);
    short got=GetCeiling(&cells[5],X,query,Z);
    int want[2],ec=0; if(!(mask&1))want[ec++]=1; if(!(mask&2))want[ec++]=2;
    int ein[2],eout[2],prior=ACC; for(int j=0;j<ec;++j){int lv=level_of(objs[want[j]-1]);ein[j]=prior;prior=(query>lv)?lv+256:prior;eout[j]=prior;}
    check(null_seen==0,"ceil_no_null"); check(ncall==ec,"ceil_count"); check(got==prior,"ceil_return");
    for(int j=0;j<ec && j<ncall;++j){check(ev[j].index==want[j],"ceil_index");check(ev[j].slot==cslot(objs[want[j]-1]),"ceil_slot");
     check(ev[j].in==ein[j]&&ev[j].out==eout[j],"ceil_inout");check(ev[j].x==X&&ev[j].z==Z&&ev[j].y==query,"ceil_args");}
   }}}
 for(int fam=0;fam<3;++fam){ int obj=fam==0?BRIDGE_FLAT:fam==1?BRIDGE_TILT1:BRIDGE_TILT2;
  for(int q=0;q<2;++q){ int query=q==0?level_of(obj):level_of(obj)+1;
   cc(); memset(data,0,sizeof data);
   data[1]=(short)(0x8000|TRIGGER_TYPE);data[2]=0;data[3]=1;data[4]=(short)(0x8000|2);
   for(int k=1;k<=2;++k){storage[k].object_number=(short)obj;storage[k].flags=0;
    storage[k].pos.x_pos=-3000;storage[k].pos.y_pos=IY;storage[k].pos.z_pos=7000;storage[k].pos.y_rot=0;}
   ncall=0;null_seen=0;memset(ev,0,sizeof ev); short got=GetHeight(&cells[5],X,query,Z);
   int lv=level_of(obj); int ein[2]={ACC,ACC}, eout[2];
   eout[0]=(query<=lv)?lv:ACC; ein[1]=eout[0]; eout[1]=eout[0];
   int exp=(q==0)?lv:ACC;
   check(null_seen==0,"height_no_null"); check(ncall==2,"height_count"); check(got==exp,"height_return");
   for(int j=0;j<2 && j<ncall;++j){check(ev[j].index==j+1,"height_index");
    check(ev[j].slot==(obj==BRIDGE_FLAT?0:obj==BRIDGE_TILT1?2:4),"height_slot");
    check(ev[j].x==X&&ev[j].z==Z&&ev[j].y==query,"height_args");
    check(ev[j].in==ein[j]&&ev[j].out==eout[j],"height_inout");}
  }}
 printf("SUMMARY suite2 checks=%d failures=%d\n",checks,fails); return fails?1:0;
}
