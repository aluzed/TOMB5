#include "CONTROL.H"
#include "CONTROL_S.H"
#include "CAMERA.H"
#include <cstdio>
#include <cstring>
extern int GetChange(ITEM_INFO*,ANIM_STRUCT*);
ANIM_STRUCT* anims; CHANGE_STRUCT* changes; RANGE_STRUCT* ranges; short* commands;
static ITEM_INFO* observed; static int events[100], count; static unsigned char domain[16770];
static void p16(int off,int value){unsigned short v=(unsigned short)value;memcpy(domain+off,&v,2);}
static void p32(int off,unsigned value){memcpy(domain+off,&value,4);}
static void literal_fixture(int c){
 memset(domain,0,sizeof domain);for(int j=0;j<144;j++)domain[j]=(19+c+j*31)%256;
 memcpy(domain+386,rcossin_tbl,16384);
 const int frames[16]={-11,-10,-9,-1,0,1,9,10,11,32766,-32768,0,0,0,0,0};int f=frames[c];
 p32(4,2882400018u);p32(132,2779096497u & ~8u);
 int fields[6]={5,c==14?5:7,(c==4||c==15)?9:(c==1||c==2)?8:-2,0,f==-32768?32767:f-1,0};for(int j=0;j<6;j++)p16(14+j*2,fields[j]);
 p16(30,17);p16(32,23);p16(34,0);p32(64,100);p32(68,(unsigned)-200);p32(72,300);p16(78,12345);
 for(int j=0;j<3;j++){p16(144+j*40+6,5+j+2*(j>0));p16(144+j*40+24,-32768);p16(144+j*40+26,32767);p16(144+j*40+32,j==0&&c!=11?3:0);}
 p16(144+40+6,8);p16(144+80+6,9);
 const int ch[9]={6,1,4,7,c==12?0:2,0,7,1,2};for(int j=0;j<9;j++)p16(264+j*2,ch[j]);
 if(c==13){p16(270,6);p16(276,6);}if(c==12)p16(276,6);
 const int rr[20]={-10,-1,1,-7,0,10,2,5,0,10,1,-3,20,30,1,21,100,110,2,101};for(int j=0;j<20;j++)p16(282+j*2,rr[j]);
}
bool re943_fixture_domain(ITEM_INFO* item) {
 return item && !memcmp(item,domain,144) && !memcmp(anims,domain+144,120) && !memcmp(changes,domain+264,18) && !memcmp(ranges,domain+282,40) && !memcmp(commands,domain+322,64) && !memcmp(rcossin_tbl,domain+386,16384);
}
static void snapshot(int phase) { events[count++]=phase;events[count++]=observed->current_anim_state;events[count++]=observed->goal_anim_state;events[count++]=observed->required_anim_state;events[count++]=observed->anim_number;events[count++]=observed->frame_number; }
extern "C" void __cyg_profile_func_enter(void* f,void*) __attribute__((no_instrument_function));
extern "C" void __cyg_profile_func_exit(void* f,void*) __attribute__((no_instrument_function));
extern "C" void __cyg_profile_func_enter(void* f,void*) {if(f==(void*)GetChange)snapshot(0);}
extern "C" void __cyg_profile_func_exit(void* f,void*) {if(f==(void*)GetChange)snapshot(1);}
static void save(const char* dir,const char* label,int c,const char* suffix,const void* data,size_t size) {char path[2048];snprintf(path,sizeof path,"%s/%s-case-%02d.%s",dir,label,c,suffix);FILE* f=fopen(path,"wb");if(!f) __builtin_abort();fwrite(data,1,size,f);fclose(f);}
int main(int argc,char** argv) {
 if(argc<3)return 2;static_assert(sizeof(ITEM_INFO)==144&&sizeof(ANIM_STRUCT)==40&&sizeof(CHANGE_STRUCT)==6&&sizeof(RANGE_STRUCT)==8&&sizeof(void*)==4,"i386 ABI");int fails=0;
 for(int c=0;c<16;c++) {
  unsigned char expected[16770],out[16770],ee[400];char path[2048];
  const char* suffixes[]={"input","expected","events"};void* dest[]={domain,expected,ee};size_t sizes[]={16770,16770,400};size_t en=0;
  for(int j=0;j<3;j++){snprintf(path,sizeof path,"%s/case-%02d.%s",argv[1],c,suffixes[j]);FILE*f=fopen(path,"rb");if(!f)return 3;size_t n=fread(dest[j],1,sizes[j],f);fclose(f);if(j<2&&n!=sizes[j])return 3;if(j==2)en=n;}
  unsigned char supplied[16770];memcpy(supplied,domain,sizeof domain);literal_fixture(c);if(memcmp(supplied,domain,sizeof domain))return 4;
  ITEM_INFO item;ANIM_STRUCT a[3];CHANGE_STRUCT ch[3];RANGE_STRUCT r[5];short q[32];
  memcpy(&item,domain,144);memcpy(a,domain+144,120);memcpy(ch,domain+264,18);memcpy(r,domain+282,40);memcpy(q,domain+322,64);
  anims=a;changes=ch;ranges=r;commands=q;observed=&item;count=0;
  if(argc==4)((unsigned char*)&item)[0]^=1;
  AnimateItem(&item);
  memcpy(out,&item,144);memcpy(out+144,a,120);memcpy(out+264,ch,18);memcpy(out+282,r,40);memcpy(out+322,q,64);memcpy(out+386,rcossin_tbl,16384);
  bool ok=!memcmp(out,expected,sizeof out)&&en==count*4&&!memcmp(ee,events,en)&&anims==a&&changes==ch&&ranges==r&&commands==q;fails+=!ok;
  save(argv[1],argv[2],c,"native",out,sizeof out);save(argv[1],argv[2],c,"events",events,count*4);printf("case=%d %s events=%d\n",c,ok?"PASS":"FAIL",count/6);
 }
 printf("cases=16 failures=%d\n",fails);return fails?1:0;
}
