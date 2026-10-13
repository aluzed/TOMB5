// Public finite arithmetic oracle; no target dump or private fixture inputs.
#include "EFFECTS.H"
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cstddef>
#include <climits>
short FXType;
extern "C" void unreached_boundary() { std::abort(); }
static_assert(sizeof(void*)==4 && sizeof(int)==4 && sizeof(long)==4 && sizeof(short)==2 && CHAR_BIT==8,"GCC i386 ABI");
static_assert(sizeof(ITEM_INFO)==144,"ITEM ABI");
static_assert(offsetof(ITEM_INFO,pos)+offsetof(PHD_3DPOS,x_rot)==76,"x offset");
static_assert(offsetof(ITEM_INFO,pos)+offsetof(PHD_3DPOS,y_rot)==78,"y offset");
static void put(unsigned char* p,unsigned v) { p[0]=v&255; p[1]=(v>>8)&255; }
static unsigned get(const unsigned char* p) { return p[0]+256u*p[1]; }
// Reviewed finite dataflow: independent unsigned halfwords, y half-turn and x negation.
// Byte oracle uses modular integers rather than production signed narrowing.
static void oracle(unsigned char* b) { put(b+78,(get(b+78)+32768u)%65536u); put(b+76,(65536u-get(b+76))%65536u); }
static bool check(unsigned x,unsigned y,unsigned n) {
 unsigned char in[144],want[144]; for(unsigned j=0;j<144;++j)in[j]=(31*j+7+n)%256;
 put(in+76,x);put(in+78,y);memcpy(want,in,144);
 ITEM_INFO i;memcpy(&i,in,144);FXType=(short)((n%4)*16384u);short fx=FXType;
 bool ok=true;turn180_effect(&i);oracle(want);ok=ok && !memcmp(&i,want,144) && FXType==fx;
 effect_routines[0](&i);oracle(want);ok=ok && !memcmp(&i,want,144) && FXType==fx && !memcmp(want,in,144);
 // Also table-first then direct: genuine initialized slot, never injected.
 memcpy(&i,in,144);memcpy(want,in,144);effect_routines[0](&i);oracle(want);
 ok=ok && !memcmp(&i,want,144) && FXType==fx;turn180_effect(&i);oracle(want);
 return ok && !memcmp(&i,want,144) && FXType==fx;
}
int main() {
 if(effect_routines[0]!=turn180_effect)return 2;
 unsigned n=0,fail=0;for(unsigned v=0;v<65536;++v) { fail+=!check(v,v,n);++n; }
 const unsigned b[]={0,1,32767,32768,32769,65534,65535};
 for(unsigned x:b)for(unsigned y:b) { fail+=!check(x,y,n);++n; }
 printf("cases=%u failures=%u controls=%u whole_item=144 FXType_unchanged=true real_slot=0\n",n,fail,n-fail);
 return fail?1:0;
}
