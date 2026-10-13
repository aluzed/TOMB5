// Authored synthetic fixtures only; the complete current CONTROL.C is linked.
#include "CONTROL.H"
#include "DRAW.H"
#include "CAMERA.H"
#include <cstdio>
#include <cstring>
#include <cstddef>
#include <cstdint>
ANIM_STRUCT* anims;
CHANGE_STRUCT* changes;
RANGE_STRUCT* ranges;
short* commands;
static_assert(sizeof(void*)==4 && sizeof(long)==4 && sizeof(ITEM_INFO)==144 && sizeof(ANIM_STRUCT)==40 && sizeof(CHANGE_STRUCT)==6 && sizeof(RANGE_STRUCT)==8,"i386 fixture ABI required");
static_assert(offsetof(ITEM_INFO,pos)==64 && offsetof(ITEM_INFO,speed)==30,"projection ABI");
struct Fixture { int frame,velocity,acceleration,lateral,lateral_acceleration,angle; };
static const Fixture fixtures[8] = {
 {3,327680,131072,-458752,196608,0},
 {4,-589824,-65536,524288,-131072,8192},
 {5,65535,1,-65537,1,-16384},
 {6,1114112,0,-1245184,0,12345},
 {7,2147483640,2147483640,-2147483640,-2147483640,-12345},
 {8,2147418112,65536,65536,65536,16384},
 {9,INT32_MIN,-65536,-65536,-65536,-32768},
 {10,196608,-65536,-131072,65536,4096}
};
template<class T> static void put(unsigned char* p,int off,T value) { std::memcpy(p+off,&value,sizeof value); }
static void snapshot(unsigned char* out,const ITEM_INFO& item,const ANIM_STRUCT* a,const CHANGE_STRUCT* ch,const RANGE_STRUCT* r,const short* q) {
 std::memcpy(out,&item,144); std::memcpy(out+144,a,80); std::memcpy(out+224,ch,12);
 std::memcpy(out+236,r,32); std::memcpy(out+268,q,64); std::memcpy(out+332,rcossin_tbl,16384);
}
static void hex(const unsigned char* p) { for(int j=0;j<16716;++j) std::printf("%02x",unsigned(p[j])); }
static unsigned char approved_item[144],approved_animation[80];
static int active_case=-1;
bool re940_fixture_domain(const ITEM_INFO* item) {
 return item && anims && active_case>=0 && active_case<8 &&
  !std::memcmp(item,approved_item,144) && !std::memcmp(anims,approved_animation,80);
}
int main() {
 for(int c=0;c<8;++c) {
  const Fixture& f=fixtures[c]; unsigned char b[16716]={},out[16716];
  for(int j=0;j<144;++j) b[j]=(23+31*j+c)%256;
  put<uint32_t>(b,4,0xfedc1234u); put<uint32_t>(b,60,0u); put<uint32_t>(b,132,0xabcdefa7u & ~8u);
  const short fields[6]={1,7,2,0,short(f.frame),0}; std::memcpy(b+14,fields,12);
  put<short>(b,30,17); put<short>(b,32,23); put<short>(b,34,0);
  put<int>(b,64,100+c); put<int>(b,68,-200-c); put<int>(b,72,300+c); put<short>(b,78,short(f.angle));
  put<short>(b,150,1); put<int>(b,152,f.velocity); put<int>(b,156,f.acceleration);
  put<int>(b,160,f.lateral); put<int>(b,164,f.lateral_acceleration);
  const short bounds[4]={2,100,1,2}; std::memcpy(b+168,bounds,8); std::memcpy(b+332,rcossin_tbl,16384);
  ITEM_INFO item; ANIM_STRUCT a[2]; CHANGE_STRUCT ch[2]; RANGE_STRUCT r[4]; short q[32];
  std::memcpy(&item,b,144); std::memcpy(a,b+144,80); std::memcpy(ch,b+224,12); std::memcpy(r,b+236,32); std::memcpy(q,b+268,64);
  anims=a; changes=ch; ranges=r; commands=q;
  active_case=c; std::memcpy(approved_item,b,144); std::memcpy(approved_animation,b+144,80);
  AnimateItem(&item);
  if(anims!=a || changes!=ch || ranges!=r || commands!=q) return 2;
  snapshot(out,item,a,ch,r,q);
  std::printf("ROW %d ",c); hex(b); std::printf(" "); hex(out); std::printf("\n");
 }
 return std::ferror(stdout) ? 3 : 0;
}
