// Geometry service doubles only; compile the complete unchanged CAMERA.C TU.
#include "CAMERA.H"
#include "CONTROL.H"
#include "GETSTUFF.H"
#include <cstdio>
#include <cstring>
#include <cstddef>
#include <type_traits>
static_assert(sizeof(long)==4 && sizeof(void*)==4 && sizeof(GAME_VECTOR)==16,"i386");
static_assert(offsetof(GAME_VECTOR,room_number)==12 && offsetof(GAME_VECTOR,box_number)==14,"layout");
static_assert(std::is_same<decltype(&GetFloor),FLOOR_INFO*(*)(long,long,long,short*)>::value,"floor ABI");
static_assert(std::is_same<decltype(&GetHeight),short(*)(FLOOR_INFO*,int,int,int)>::value,"height ABI");
static_assert(std::is_same<decltype(&GetCeiling),short(*)(FLOOR_INFO*,int,int,int)>::value,"ceiling ABI");
static int hs[10],cs[10],rs[10],idx,fi,ei;static FLOOR_INFO f;
static void sep(){if(ei++)std::printf(",");}
FLOOR_INFO* GetFloor(long x,long y,long z,short* r){int old=*r;*r=rs[fi<10?fi:9];++fi;sep();std::printf("[\"F\",%ld,%ld,%ld,%d,%d]",x,y,z,old,*r);return &f;}
short GetHeight(FLOOR_INFO* p,int x,int y,int z){if(p!=&f)__builtin_trap();int v=hs[idx<10?idx:9];sep();std::printf("[\"H\",%d,%d,%d,%d]",x,y,z,v);return v;}
short GetCeiling(FLOOR_INFO* p,int x,int y,int z){if(p!=&f)__builtin_trap();int v=cs[idx<10?idx:9];++idx;sep();std::printf("[\"C\",%d,%d,%d,%d]",x,y,z,v);return v;}
int main(){GAME_VECTOR a,b;long push;while(std::scanf("%ld%ld%ld%hd%hd%ld%ld%ld%hd%hd%ld",&a.x,&a.y,&a.z,&a.room_number,&a.box_number,&b.x,&b.y,&b.z,&b.room_number,&b.box_number,&push)==11){
for(int i=0;i<10;i++)if(std::scanf("%d",&hs[i])!=1)return 2;
for(int i=0;i<10;i++)if(std::scanf("%d",&cs[i])!=1)return 2;
for(int i=0;i<10;i++)if(std::scanf("%d",&rs[i])!=1)return 2;
GAME_VECTOR before=a;idx=fi=ei=0;std::printf("{\"events\":[");long ret=mgLOS(&a,&b,push);
if(std::memcmp(&a,&before,sizeof a))return 3;
std::printf("],\"result\":%ld,\"dest\":[%ld,%ld,%ld,%d,%d]}\n",ret,b.x,b.y,b.z,b.room_number,b.box_number);
}return 0;}
