// Independent synthetic list oracle; no target assets or captured memory.
#include "CONTROL.H"
#include "ITEMS.H"
#include <algorithm>
#include <cstdio>
#include <cstring>
ITEM_INFO* items;
extern short next_item_active;
static_assert(sizeof(void*)==4 && sizeof(ITEM_INFO)==144,"i386 fixture");
static int cases=0, failures=0;
static void check(const int* order,int length,int victim,bool active) {
 ITEM_INFO arena[6], expected[6];
 std::memset(arena,53,sizeof(arena));
 for(int i=0;i<6;i++){arena[i].active=0;arena[i].next_active=-1;}
 for(int i=0;i<length;i++){arena[order[i]].active=1;arena[order[i]].next_active=i+1<length?order[i+1]:-1;}
 arena[victim].active=active;
 std::memcpy(expected,arena,sizeof(arena));
 short head=length?order[0]:-1, wanted=head;
 // Oracle filters the logical sequence, not the production predecessor walk.
 if(active){
  expected[victim].active=0;
  int remaining[6], n=0;
  for(int i=0;i<length;i++)if(order[i]!=victim)remaining[n++]=order[i];
  wanted=n?remaining[0]:-1;
  for(int i=0;i<n;i++)expected[remaining[i]].next_active=i+1<n?remaining[i+1]:-1;
 }
 items=arena;next_item_active=head;
 RemoveActiveItem(victim);
 bool ok=items==arena && next_item_active==wanted && !std::memcmp(arena,expected,sizeof(arena));
 cases++;if(!ok){failures++;if(failures<5)std::printf("FAIL case=%d length=%d victim=%d\n",cases,length,victim);}
}
int main(){
 int p[]={0,1,2,3};
 do{for(int v=0;v<4;v++)check(p,4,v,true);}while(std::next_permutation(p,p+4));
 int q[]={0,1,2,3};
 check(q,0,0,false);check(q,0,0,true);check(q,1,0,true);check(q,1,0,false);
 check(q,2,0,true);check(q,3,1,true);check(q,3,2,true);
 check(q,3,4,true);check(q,3,1,false);check(q,3,4,false);
 std::printf("SUMMARY cases=%d failures=%d\n",cases,failures);
 return failures?1:0;
}
