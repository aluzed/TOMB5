// Synthetic inputs only; complete retained MATHS.C and LIBGTE.C, no GTE stubs.
#include "MATHS.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
struct MATRIX3D MatrixStack[32],iMatrixStack[32];
struct MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP;
long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
int main(int argc,char**argv){static_assert(sizeof(int)==4&&sizeof(short)==2,"register widths");setbuf(stdout,NULL);FILE*f=fopen(argv[1],"rb");if(!f)return 80;if(fread(rcossin_tbl,2,8192,f)!=8192)return 81;fclose(f);f=fopen(argv[2],"rb");if(!f)return 82;int a,id=0;short m[9];while(fread(&a,4,1,f)==1){if(fread(m,2,9,f)!=9)return 83;memset(&gteRegs,0,sizeof(gteRegs));memset(MatrixStack,0,sizeof(MatrixStack));memcpy(MatrixStack,m,18);for(int i=0;i<4;i++)memcpy(&gteRegs.CP2C.r[i],m+2*i,4);gteRegs.CP2C.r[4]=(uint16_t)m[8];mRotX(a);printf("%d",id++);for(int i=0;i<8;i++){uint32_t w;memcpy(&w,((char*)Matrix)+4*i,4);printf(" %u",w);}for(int c=0;c<2;c++)for(int r=0;r<32;r++)printf(" %u",c?gteRegs.CP2C.r[r]:gteRegs.CP2D.r[r]);puts("");}fclose(f);return 0;}
