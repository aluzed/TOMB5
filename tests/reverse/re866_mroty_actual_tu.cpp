// Synthetic state; actual MATHS.C and LIBGTE.C, no replacement rotation body.
#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
MATRIX3D MatrixStack[32], iMatrixStack[32];
MATRIX3D *Matrix=MatrixStack, *iMatrix=iMatrixStack;
unsigned short MatrixSP;
long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
int main(int argc,char **argv) {
 static_assert(sizeof(MATRIX3D)>=32,"minimum matrix extent");
 if(argc!=3)return 79;
 setbuf(stdout,NULL);
 FILE *f=fopen(argv[1],"rb");if(!f)return 80;
 if(fread(rcossin_tbl,2,8192,f)!=8192)return 81;fclose(f);
 f=fopen(argv[2],"rb");if(!f)return 82;
 int angle,id=0;short m[9];
 while(fread(&angle,4,1,f)==1) {
  if(fread(m,2,9,f)!=9)return 83;
  memset(&gteRegs,0,sizeof(gteRegs));
  memset(MatrixStack,0,sizeof(MatrixStack));
  memset(iMatrixStack,0,sizeof(iMatrixStack));
  Matrix=MatrixStack; iMatrix=iMatrixStack; MatrixSP=0;
  memcpy(MatrixStack,m,18);
  for(int i=0;i<4;i++)memcpy(&gteRegs.CP2C.r[i],m+2*i,4);
  gteRegs.CP2C.r[4]=(uint16_t)m[8];
  mRotY(angle);
  // Fixed reviewed 608-word projection plus explicit complete native tail checks.
  for(size_t j=1024;j<sizeof(MatrixStack);j++)if(((unsigned char*)MatrixStack)[j])return 84;
  for(size_t j=1024;j<sizeof(iMatrixStack);j++)if(((unsigned char*)iMatrixStack)[j])return 85;
  if(iMatrix!=iMatrixStack)return 86;
  printf("%d",id++);
  for(int bank=0;bank<2;bank++)for(int j=0;j<256;j++) {
   uint32_t w;memcpy(&w,(char*)(bank?iMatrixStack:MatrixStack)+j*4,4);printf(" %u",w);
  }
  for(int bank=0;bank<3;bank++)for(int j=0;j<32;j++)
   printf(" %u",bank==0?gteRegs.CP2D.r[j]:bank==1?gteRegs.CP2C.r[j]:gteRegs.CP0.r[j]);
  printf(" %u %td\n",MatrixSP,Matrix-MatrixStack);
 }
 fclose(f);return 0;
}
