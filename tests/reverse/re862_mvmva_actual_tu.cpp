#include "GTEREG.H"
#include <cstdio>
#include <cstdint>
#include <cstring>
int main(int argc,char**argv){static_assert(sizeof(gteRegs.CP2C.p[5].sd)==4 && sizeof(long long)==8,"signed CV32 and accumulator64");FILE*f=fopen(argv[1],"rb");if(!f)return 80;uint32_t op,bank[64];int id=0;setbuf(stdout,NULL);while(fread(&op,4,1,f)==1){if(fread(bank,4,64,f)!=64)return 81;for(int i=0;i<32;i++){gteRegs.CP2D.r[i]=bank[i];gteRegs.CP2C.r[i]=bank[32+i];}if(docop2(op)!=1)return 82;printf("%d",id++);for(int i=0;i<32;i++)printf(" %u",gteRegs.CP2D.r[i]);for(int i=0;i<32;i++)printf(" %u",gteRegs.CP2C.r[i]);puts("");}fclose(f);return 0;}
