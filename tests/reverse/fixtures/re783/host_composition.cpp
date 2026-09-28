// BLOCKED-001 lot23 v4 — suite1 non instrumentee: records bridges structures (loaded0/1),
// voisins, buffers complets GetHeight ET GetCeiling. Memes attentes baseline/candidate.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "COLLIDE_S.H"
#include "LARA.H"
#include "SETUP.H"
#include "OBJECTS.H"
#include "BRIDGE_CALLBACKS.H"
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
static void poison_floor(ITEM_INFO*,int,int,int,int*){}
static void poison_ceiling(ITEM_INFO*,int,int,int,int*){}
static const int X=1131,Z=1757,IY=4096,ACC=8192;
static int off0(){return (-X)&1023;}
static int level_of(int o){return o==BRIDGE_TILT1?IY+(off0()>>2):o==BRIDGE_TILT2?IY+(off0()>>1):IY;}
static int checks=0,fails=0;
static void check(bool ok,const char* w){++checks; if(!ok){++fails;printf("FAIL %s\n",w);}}
static void cc(){memset(cells,0,sizeof cells);rooms[0].floor=cells;rooms[0].x_size=4;rooms[0].y_size=4;
 for(auto&c:cells){c.ceiling=32;c.floor=32;c.pit_room=0xFF;c.sky_room=0xFF;} cells[5].index=1;
 memset(&lara,0,sizeof lara);InItemControlLoop=1;ItemNewRoomNo=0;memset(ItemNewRooms,0,sizeof ItemNewRooms);lara_item=storage;}

static void compose(){
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
    room_info rb=rooms[0]; ITEM_INFO ib[4]; memcpy(ib,storage,sizeof ib); short db[64]; memcpy(db,data,sizeof db);
    FLOOR_INFO cb[16]; memcpy(cb,cells,sizeof cb); object_info ob[NUMBER_OBJECTS]; memcpy(ob,object_storage,sizeof ob);
    short got=GetCeiling(&cells[5],X,query,Z);
    int prior=ACC; for(int i=1;i<=2;++i) if(!(mask>>(i-1)&1)){int lv=level_of(objs[i-1]); prior=(query>lv)?lv+256:prior;}
    check(got==prior,"ceil_return");
    check(!memcmp(&rb,&rooms[0],sizeof rb)&&!memcmp(ib,storage,sizeof ib)&&!memcmp(db,data,sizeof db)
          &&!memcmp(cb,cells,sizeof cb)&&!memcmp(ob,object_storage,sizeof ob),"ceil_buffers");
   }}}
 for(int fam=0;fam<3;++fam){ int obj=fam==0?BRIDGE_FLAT:fam==1?BRIDGE_TILT1:BRIDGE_TILT2;
  for(int q=0;q<2;++q){ int query=q==0?level_of(obj):level_of(obj)+1;
   cc(); memset(data,0,sizeof data);
   data[1]=(short)(0x8000|TRIGGER_TYPE);data[2]=0;data[3]=1;data[4]=(short)(0x8000|2);
   for(int k=1;k<=2;++k){storage[k].object_number=(short)obj;storage[k].flags=0;
    storage[k].pos.x_pos=-3000;storage[k].pos.y_pos=IY;storage[k].pos.z_pos=7000;storage[k].pos.y_rot=0;}
   room_info rb=rooms[0]; ITEM_INFO ib[4]; memcpy(ib,storage,sizeof ib); short db[64]; memcpy(db,data,sizeof db);
   FLOOR_INFO cb[16]; memcpy(cb,cells,sizeof cb); object_info ob[NUMBER_OBJECTS]; memcpy(ob,object_storage,sizeof ob);
   short got=GetHeight(&cells[5],X,query,Z);
   check(got==((q==0)?level_of(obj):ACC),"height_return");
   check(!memcmp(&rb,&rooms[0],sizeof rb)&&!memcmp(ib,storage,sizeof ib)&&!memcmp(db,data,sizeof db)
         &&!memcmp(cb,cells,sizeof cb)&&!memcmp(ob,object_storage,sizeof ob),"height_buffers");
  }}
}

int main(){
 setvbuf(stdout,NULL,_IONBF,0);
 bool inst=true;
 for(int loaded=0;loaded<2;++loaded){
  objects=object_storage; memset(object_storage,0,sizeof object_storage); memset(bone_storage,0,sizeof bone_storage);
  for(int o=447;o<=453;++o){ memset(&object_storage[o],0xA5,sizeof(object_info));
   object_storage[o].floor=poison_floor; object_storage[o].ceiling=poison_ceiling; object_storage[o].object_mip=-123; }
  for(int o=448;o<=452;o+=2){ object_storage[o].loaded=loaded; }
  object_info bef[7], exp[7]; for(int k=0;k<7;++k) memcpy(&bef[k],&object_storage[447+k],sizeof(object_info));
  for(int k=0;k<7;++k){ memcpy(&exp[k],&bef[k],sizeof(object_info));
   int o=447+k; if(o==BRIDGE_FLAT){exp[k].floor=BridgeCallbackFlatFloor;exp[k].ceiling=BridgeCallbackFlatCeiling;exp[k].object_mip=0x0c00;}
   else if(o==BRIDGE_TILT1){exp[k].floor=BridgeCallbackTilt1Floor;exp[k].ceiling=BridgeCallbackTilt1Ceiling;exp[k].object_mip=0x0c00;}
   else if(o==BRIDGE_TILT2){exp[k].floor=BridgeCallbackTilt2Floor;exp[k].ceiling=BridgeCallbackTilt2Ceiling;exp[k].object_mip=0x0c00;}
   if(o==BRIDGE_FLAT||o==BRIDGE_TILT1||o==BRIDGE_TILT2) exp[k].loaded=loaded; }
  ObjectObjects();
  for(int k=0;k<7;++k){ int o=447+k; bool bridge=(o==448||o==450||o==452);
   if(bridge) check(!memcmp(&exp[k],&object_storage[o],sizeof(object_info)),"bridge_record_matches_expected");
   else check(!memcmp(&bef[k],&object_storage[o],sizeof(object_info)),"neighbor_preserved"); }
  check(object_storage[BRIDGE_FLAT].loaded==loaded && object_storage[BRIDGE_TILT1].loaded==loaded
        && object_storage[BRIDGE_TILT2].loaded==loaded,"loaded_reread");
  if(object_storage[BRIDGE_FLAT].floor!=BridgeCallbackFlatFloor) inst=false;
  compose();   // composition sous CHAQUE etat loaded
 }
 if(!inst){ printf("SUMMARY suite1v4 checks=%d failures=%d SKIP_calls=1\n",checks,fails); return 1; }
 printf("SUMMARY suite1v4 checks=%d failures=%d\n",checks,fails); return fails?1:0;
}
