// Public constructed finite fixtures; full production TUs and real software GTE.
#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
MATRIX3D MatrixStack[32],iMatrixStack[32];
MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP;
long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
int main(int argc,char **argv){
 static_assert(sizeof(long)==4 && sizeof(MATRIX3D)==32,"ABI32 required");
 if(argc!=3)return 79;
 setbuf(stdout,NULL);
 FILE *f=fopen(argv[1],"rb");if(!f)return 80;
 if(fread(rcossin_tbl,2,8192,f)!=8192)return 81;fclose(f);
 f=fopen(argv[2],"rb");if(!f)return 82;
 int axis,angle,id=0;short m[9];
 while(fread(&axis,4,1,f)==1){
  if(fread(&angle,4,1,f)!=1 || fread(m,2,9,f)!=9)return 83;
  memset(&gteRegs,0,sizeof(gteRegs));
  memset(MatrixStack,0,sizeof(MatrixStack));memset(iMatrixStack,0,sizeof(iMatrixStack));
  Matrix=MatrixStack;iMatrix=iMatrixStack;MatrixSP=0;
  memcpy(axis?iMatrixStack:MatrixStack,m,18);
  for(int j=0;j<4;j++)memcpy(&gteRegs.CP2C.r[(axis?8:0)+j],m+2*j,4);
  gteRegs.CP2C.r[(axis?8:0)+4]=(uint16_t)m[8];
  gteRegs.CP2D.r[1]=0x12345678;gteRegs.CP2D.r[3]=0xabcd7654;
  if(axis)iRotZ(angle);else mRotZ(angle);
  if(Matrix!=MatrixStack || iMatrix!=iMatrixStack)return 84;
  printf("%d",id++);
  for(int b=0;b<2;b++)for(int j=0;j<256;j++){
   uint32_t w;memcpy(&w,(char*)(b?iMatrixStack:MatrixStack)+4*j,4);printf(" %u",w);
  }
  for(int b=0;b<3;b++)for(int j=0;j<32;j++)printf(" %u",b==0?gteRegs.CP2D.r[j]:b==1?gteRegs.CP2C.r[j]:gteRegs.CP0.r[j]);
  printf(" %u\n",MatrixSP);
 }
 fclose(f);return 0;
}
