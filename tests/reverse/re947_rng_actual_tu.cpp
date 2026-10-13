#include "MISC.H"
#include "CONTROL.H"
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
static_assert(sizeof(long)==4,"ILP32");
static_assert(sizeof(uint32_t)==4,"uint32");
long rand_1=0x11223344,rand_2=-1430532899;
static long signed_state(uint32_t x){return x<=UINT32_C(2147483647)?(long)x:(long)((int64_t)x-INT64_C(4294967296));}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 unsigned ops[26],seeds[26],op,seed; int count=0;
 while(scanf("%u %x",&op,&seed)==2){if(count==26)return 2;ops[count]=op;seeds[count++]=seed;}
 if(!feof(stdin))return 2;
 const uint32_t pairs[8][2]={{0,1},{0x7fffffff,0x80000000},{0xffffffff,0xfffffffe},{0x80000001,0x7ffffffe},{0xffff,0xffff0000},{0x10000,0x8000},{0xd371f947,0xaabbccdd},{0x55555555,0xaaaaaaaa}};
 const unsigned pattern[26]={0,1,2,3,3,2,0,3,2,1,2,3,3,2,2,3,3,2,2,3,3,2,2,3,3,2};
 bool first=!strcmp(argv[1],"--first-control")||!strcmp(argv[1],"--first-draw");
 if(first){if(count!=3||ops[0]!=0||ops[1]!=1||seeds[0]!=0xd371f947||seeds[1]!=0xd371f947||seeds[2]!=0||ops[2]!=(unsigned)(!strcmp(argv[1],"--first-control")?2:3))return 2;}
 else {if(strlen(argv[1])!=1||argv[1][0]<'0'||argv[1][0]>'7'||count!=26)return 2;unsigned c=argv[1][0]-'0';for(int j=0;j<26;j++){unsigned want=j==0||j==9?pairs[c][0]:j==1||j==6?pairs[c][1]:0;if(ops[j]!=pattern[j]||seeds[j]!=want)return 2;}}
 for(int j=0;j<count;j++){long r=0;op=ops[j];seed=seeds[j];if(op==0)SeedRandomControl(signed_state(seed));if(op==1)SeedRandomDraw(signed_state(seed));if(op==2)r=GetRandomControl();if(op==3)r=GetRandomDraw();printf("%u %u %u\n",(unsigned)r,(unsigned)rand_1,(unsigned)rand_2);}return 0;
}
