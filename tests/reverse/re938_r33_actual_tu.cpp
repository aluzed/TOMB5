// RE938: finite constructed inputs, not natural gameplay or a hardware oracle.
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
int main() {
 static_assert(sizeof(int)==4 && sizeof(long)==4 && sizeof(MATRIX3D)==32 && sizeof(gteRegs)==384,"ABI32");
 static_assert(sizeof(gteRegs.CP2C.p[4].d)==4,"fullword");
 uint32_t le=1; if(*reinterpret_cast<unsigned char*>(&le)!=1) return 80;
 const int left[12]={120,-240,360,-480,600,-720,840,-960,1200,100,-200,300};
 const int right[12]={-41,82,-123,164,-205,246,-287,328,1601,-61,122,-183};
 const uint32_t poison[4]={0,0x12340000u,0,0xabcd0000u};
 for(int pair=0;pair<4;++pair) for(int fraction=1;fraction<4;++fraction) {
  std::memset(MatrixStack,0x39,sizeof MatrixStack); std::memset(iMatrixStack,0x75,sizeof iMatrixStack);
  Matrix=MatrixStack+1; iMatrix=iMatrixStack+1;
  for(int j=0;j<12;++j) {
   int x=left[j]+(pair%2)*17, y=right[j]+(pair%2)*29;
   if(j==8 && pair>=2) {x=-1201;y=-1602;}
   if(j<9) {short sx=x,sy=y;std::memcpy(reinterpret_cast<char*>(Matrix)+2*j,&sx,2);std::memcpy(reinterpret_cast<char*>(iMatrix)+2*j,&sy,2);}
   else {std::memcpy(reinterpret_cast<char*>(Matrix)+20+4*(j-9),&x,4);std::memcpy(reinterpret_cast<char*>(iMatrix)+20+4*(j-9),&y,4);}
  }
  unsigned char stacks[2048]; std::memcpy(stacks,MatrixStack,1024); std::memcpy(stacks+1024,iMatrixStack,1024);
  uint32_t initial[96]; for(unsigned j=0;j<96;++j) initial[j]=0xa5c39b27u^(j*0x1020301u);
  initial[68]=poison[pair];std::memcpy(&gteRegs,initial,sizeof initial);
  MatrixSP=7;iFrac=fraction;iRate=4;iAmbientR=31;iAmbientG=-47;iAmbientB=59;
  InterpolateMatrix();
  if(std::memcmp(stacks,MatrixStack,1024)||std::memcmp(stacks+1024,iMatrixStack,1024)) return 81;
  if(Matrix!=MatrixStack+1||iMatrix!=iMatrixStack+1||MatrixSP!=7||iFrac!=fraction||iRate!=4||iAmbientR!=31||iAmbientG!=-47||iAmbientB!=59) return 82;
  // All inactive stack entries and active padding are return-time byte canaries.
  std::printf("%d %d",pair,fraction);
  for(unsigned j=0;j<96;++j) {uint32_t w;std::memcpy(&w,reinterpret_cast<char*>(&gteRegs)+4*j,4);std::printf(" %u",w);} std::puts("");
 }
}
