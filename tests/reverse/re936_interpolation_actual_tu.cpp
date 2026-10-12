#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
MATRIX3D MatrixStack[32],iMatrixStack[32]; MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP; long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB; short rcossin_tbl[8192];
int main(){static_assert(sizeof(long)==4 && sizeof(MATRIX3D)==32 && sizeof(gteRegs)==384,"ABI32");
int a[12]={120,-240,360,-480,600,-720,840,-960,1200,100,-200,300};int b[12]={-41,82,-123,164,-205,246,-287,328,1601,-61,122,-183};
for(int c=0;c<2;c++)for(int f=1;f<=3;f++){
memset(MatrixStack,0x39,sizeof(MatrixStack));memset(iMatrixStack,0x75,sizeof(iMatrixStack));
for(int j=0;j<9;j++){short av=a[j]+c*17,bv=b[j]+c*29;memcpy((char*)Matrix+j*2,&av,2);memcpy((char*)iMatrix+j*2,&bv,2);}
for(int j=9;j<12;j++){int av=a[j]+c*17,bv=b[j]+c*29;memcpy((char*)Matrix+20+(j-9)*4,&av,4);memcpy((char*)iMatrix+20+(j-9)*4,&bv,4);}
unsigned char saved[2048];memcpy(saved,MatrixStack,1024);memcpy(saved+1024,iMatrixStack,1024);
uint32_t bank[96];for(int j=0;j<96;j++)bank[j]=0xa5c39b27u^(uint32_t(j)*0x1020301u);bank[68]=0;memcpy(&gteRegs,bank,384);
iFrac=f;iRate=4;iAmbientR=31;iAmbientG=-47;iAmbientB=59;InterpolateMatrix();
if(memcmp(saved,MatrixStack,1024)||memcmp(saved+1024,iMatrixStack,1024))return 91;
if(Matrix!=MatrixStack||iMatrix!=iMatrixStack||iFrac!=f||iRate!=4||iAmbientR!=31||iAmbientG!=-47||iAmbientB!=59)return 92;
printf("%d %d",c,f);for(int j=0;j<96;j++){uint32_t w;memcpy(&w,(char*)&gteRegs+j*4,4);printf(" %u",w);}puts("");}
return 0;}
