// Constructed finite raw-bank transport; no hardware sign-extension claim.
#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <cstddef>
#include <initializer_list>
MATRIX3D MatrixStack[32],iMatrixStack[32];
MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP;
long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
static struct { unsigned char pre[16]; MATRIX3D m; unsigned char post[16]; } fixture;
static unsigned char *input=(unsigned char*)&fixture;
static unsigned char saved[64];
static void dump(int id,int stage){
 printf("%d %d",id,stage);
 for(int b=0;b<3;b++)for(int j=0;j<32;j++)printf(" %u",b==0?gteRegs.CP0.r[j]:b==1?gteRegs.CP2D.r[j]:gteRegs.CP2C.r[j]);
 for(int b=0;b<2;b++)for(int j=0;j<256;j++){uint32_t w;memcpy(&w,(char*)(b?iMatrixStack:MatrixStack)+j*4,4);printf(" %u",w);}
 for(int j=0;j<16;j++){uint32_t w;memcpy(&w,input+j*4,4);printf(" %u",w);}
 printf(" %ld %ld %u\n",long(Matrix-MatrixStack),long(iMatrix-iMatrixStack),MatrixSP);
}
int main(){
 static_assert(sizeof(long)==4 && sizeof(MATRIX3D)==32 && sizeof(gteRegs)==384,"ABI32");
 static_assert(offsetof(MATRIX3D,m22)==16 && offsetof(MATRIX3D,pad)==18 && offsetof(MATRIX3D,tx)==20,"layout");
 int id=0;
 for(unsigned hi: {0u,0x1234u,0x8000u,0xffffu})for(unsigned lo: {0u,0x1000u,0x8000u,0xffffu})for(int d: {0,29})for(int mode: {0,1,2}){
  for(int j=0;j<96;j++)((unsigned char*)&gteRegs)[j*4]=0; // full initialization below
  uint32_t bank[96];for(int j=0;j<96;j++)bank[j]=(uint32_t(j)*0x1020301u)^0xa5c39b27u;memcpy(&gteRegs,bank,384);
  gteRegs.CP2C.r[4]=(hi<<16)|lo;
  memset(MatrixStack,0x39,1024);memset(iMatrixStack,0x75,1024);
  memset(input,0x6b,16);memset(input+48,0x5a,16);
  uint32_t words[8]={0x01020304u,0x81234567u,0xffff0101u,0x80001234u,(hi<<16)|lo,0x12345678u,0x80000001u,0xffffffffu};
  memcpy(input+16,words,32);memcpy(saved,input,64);
  Matrix=MatrixStack+d;iMatrix=iMatrixStack+7;MatrixSP=23;
  if(mode==0){mPushMatrix();dump(id,0);}
  else if(mode==1){mLoadMatrix(&fixture.m);dump(id,0);}
  else {
   mPushMatrix();dump(id,0);
   for(int j=0;j<8;j++)gteRegs.CP2C.r[j]^=0xdeadbeefu;
   mLoadMatrix(Matrix);dump(id,1);
   mPushMatrix();dump(id,2);
   for(int j=0;j<8;j++)gteRegs.CP2C.r[j]^=0xabcdef12u;
   mPopMatrix();dump(id,3);
  }
  if(memcmp(input,saved,64))return 91;
  id++;
 }
 return 0;
}
