// Authored synthetic exact finite16 command4 fixtures, never production.
#include "CONTROL.H"
#include "DRAW.H"
#include "CAMERA.H"
#include "SETUP.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <cstddef>
ANIM_STRUCT* anims; CHANGE_STRUCT* changes; RANGE_STRUCT* ranges; short* commands; object_info* objects;
static_assert(sizeof(void*)==4 && sizeof(long)==4 && sizeof(ITEM_INFO)==144 && sizeof(ANIM_STRUCT)==40 && sizeof(object_info)==64,"i386 fixture ABI");
static_assert(offsetof(ITEM_INFO,after_death)==48 && offsetof(ITEM_INFO,hit_points)==34,"distinct fields");
template<class T> static void put(unsigned char* b,int o,T v){std::memcpy(b+o,&v,sizeof(v));}
static void fixture(int c,unsigned char* b){
 std::memset(b,0,16908);for(int j=0;j<144;++j)b[j]=(19+31*j+c)%256;
 unsigned short fl[4]={0,1,2,65533};short death[3]={0,7,-7};int oid=1+c%2;
 put<uint32_t>(b,4,0xfedc1234u);put<uint32_t>(b,132,(0xa5a5a5a1u&~8u)|((c%4)<<1));put<short>(b,12,oid);
 short fields[6]={1,7,2,0,short(c>=12?9:10),0};std::memcpy(b+14,fields,12);
 put<short>(b,30,17);put<short>(b,32,23);put<short>(b,34,0);put<short>(b,48,death[c/4%3]);
 put<int>(b,64,100+c);put<int>(b,68,-200-c);put<int>(b,72,300+c);put<short>(b,78,12345);
 put<short>(b,150,1);short bounds[4]={2,10,1,2};std::memcpy(b+168,bounds,8);put<short>(b,180,2);
 put<short>(b,190,3);short next[4]={2,20,1,2};std::memcpy(b+208,next,8);put<short>(b,268,4);put<short>(b,270,4);
 std::memcpy(b+332,rcossin_tbl,16384);for(int j=0;j<192;++j)b[16716+j]=(71+j*7)%256;
 for(int j=0;j<3;++j)put<unsigned short>(b,16716+j*64+50,j==oid?fl[c%4]:fl[c%4]^2);
}
static void snapshot(unsigned char* b,const ITEM_INFO* item){
 std::memcpy(b,item,144);std::memcpy(b+144,anims,80);std::memcpy(b+224,changes,12);std::memcpy(b+236,ranges,32);std::memcpy(b+268,commands,64);std::memcpy(b+332,rcossin_tbl,16384);std::memcpy(b+16716,objects,192);
}
bool re941_fixture_domain(const ITEM_INFO* item){
 if(!item||!anims||!changes||!ranges||!commands||!objects)return false;
 unsigned char actual[16908],approved[16908];snapshot(actual,item);
 for(int c=0;c<16;++c){fixture(c,approved);if(!std::memcmp(actual,approved,16908))return true;}return false;
}
static void hex(const unsigned char* b){for(int j=0;j<16908;++j)std::printf("%02x",unsigned(b[j]));}
int main(int argc,char**){
 for(int c=0;c<16;++c){
 unsigned char b[16908],out[16908];fixture(c,b);ITEM_INFO item;ANIM_STRUCT a[2];CHANGE_STRUCT ch[2];RANGE_STRUCT r[4];short q[32];object_info ob[3];
 std::memcpy(&item,b,144);std::memcpy(a,b+144,80);std::memcpy(ch,b+224,12);std::memcpy(r,b+236,32);std::memcpy(q,b+268,64);std::memcpy(ob,b+16716,192);
 anims=a;changes=ch;ranges=r;commands=q;objects=ob;
 if(argc>1)item.pos.x_pos+=1;
 AnimateItem(&item);
 if(anims!=a||changes!=ch||ranges!=r||commands!=q||objects!=ob)return 2;
 snapshot(out,&item);std::printf("ROW %d ",c);hex(b);std::printf(" ");hex(out);std::printf("\n");
 }return std::ferror(stdout)?3:0;
}
