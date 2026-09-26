#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "COLLIDE_S.H"
#include "LARA.H"
#include "SETUP.H"
#include "OBJECTS.H"
#include <cstdio>
#include <cstring>
#include <climits>
#include <type_traits>
#include <initializer_list>
static_assert(sizeof(void*)==4 && sizeof(long)==4 && sizeof(int)==4 && sizeof(FLOOR_INFO)==8,"i386 ABI");
room_info rooms[1]; room_info* room=rooms;
short data[16]; short* floor_data=data;
ITEM_INFO storage[3]; ITEM_INFO* items=storage; ITEM_INFO* lara_item;
lara_info lara; unsigned char InItemControlLoop; short ItemNewRoomNo; short ItemNewRooms[256][2];
object_info object_storage[1]; object_info* objects=object_storage;
int height_type,tiltxoff,tiltyoff,OnObject; short* trigger_index;
FLOOR_INFO cells[16];
static int calls;
// Explicit fixture adapter: real BridgeFlatFloor uses long*, slot uses int*.
// Never cast incompatible function or data pointers, never read baseline's uninitialized output.
static void bridge(ITEM_INFO* item,int x,int y,int z,int* output){
 ++calls; long h=LONG_MIN; BridgeFlatFloor(item,x,y,z,&h);
 if(h!=LONG_MIN)*output=(int)h;
}
static_assert(std::is_same<decltype(object_storage[0].floor),decltype(&bridge)>::value,"exact callback slot type");
int main(){int checks=0,failures=0;
 for(int base: {0,4,12})for(int first:{512,4096})for(int second:{512,4096})for(int y:{0,1024,5000})for(int mask=0;mask<4;mask++)for(int consumer=0;consumer<2;consumer++){
  memset(rooms,0,sizeof rooms);memset(cells,0,sizeof cells);memset(data,0,sizeof data);memset(storage,0,sizeof storage);memset(object_storage,0,sizeof object_storage);
  rooms[0].floor=cells;rooms[0].x_size=4;rooms[0].y_size=4;rooms[0].item_number=0;
  for(auto &c:cells){c.floor=base;c.ceiling=-32;c.pit_room=255;c.sky_room=255;}
  cells[5].index=1;
  data[1]=(short)(32768|TRIGGER_TYPE);data[2]=0;data[3]=1;data[4]=(short)(32768|2);
  storage[0].room_number=0;storage[0].next_item=-1;storage[0].floor=123456;storage[0].pos.x_pos=1131;storage[0].pos.z_pos=1757;storage[0].pos.y_pos=y-128;
  for(int i=1;i<=2;i++){storage[i].object_number=0;storage[i].flags=(mask>>(i-1)&1)?(short)32768:0;storage[i].pos.y_pos=i==1?first:second;}
  lara_item=storage;memset(&lara,0,sizeof lara);lara.item_number=0;InItemControlLoop=1;ItemNewRoomNo=0;memset(ItemNewRooms,0,sizeof ItemNewRooms);
  object_storage[0].floor=bridge;calls=0;
  ITEM_INFO expected_items[3];memcpy(expected_items,storage,sizeof storage);
  bool writes=false;int expected=base*256;int expected_calls=0;for(int i=1;i<=2;i++)if(!(mask>>(i-1)&1)){++expected_calls;int h=i==1?first:second;if(h>=y){expected=h;writes=true;}}
  int got;
  if(consumer){UpdateLaraRoom(storage,128);got=storage[0].floor;expected_items[0].floor=expected;}
  else got=GetHeight(&cells[5],1131,y,1757);
  bool ok=got==expected && !memcmp(storage,expected_items,sizeof storage) && calls==expected_calls && OnObject==(writes?1:0) && height_type==0 && tiltxoff==0 && tiltyoff==0 && trigger_index==data+1 && ItemNewRoomNo==0;
  ++checks;if(!ok)++failures;
  printf("%s base=%d first=%d second=%d y=%d mask=%d consumer=%d expected=%d actual=%d calls=%d\n",ok?"PASS":"FAIL",base,first,second,y,mask,consumer,expected,got,calls);
 }
 printf("SUMMARY checks=%d failures=%d\n",checks,failures);return failures?1:0;
}
