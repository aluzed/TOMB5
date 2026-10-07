// Entire actual TUs; synthetic field-assigned fixture, no target payload.
#include "SPHERES.H"
#include "MATHS.H"
#include "LOAD_LEV.H"
#include "CONTROL.H"
#include "CAMERA.H"
#include "GTEREG.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
object_info storage[2]; object_info* objects=storage;
ANIM_STRUCT* anims; long* bones;
MATRIX3D MatrixStack[32],iMatrixStack[32];
MATRIX3D *Matrix=MatrixStack,*iMatrix=iMatrixStack;
unsigned short MatrixSP; long iFrac,iRate,iAmbientR,iAmbientG,iAmbientB;
short rcossin_tbl[8192];
void bytes(const void*p,size_t n){auto b=(const unsigned char*)p;for(size_t i=0;i<n;i++)printf("%02x",b[i]);puts("");}
int main(int argc,char**argv){FILE*f=fopen(argv[1],"rb");if(!f)return 80;if(fread(rcossin_tbl,2,8192,f)!=8192)return 81;fclose(f);
ITEM_INFO item={}; ANIM_STRUCT anim={};short frame[24]={};long bone[4]={0,3,5,-2};
item.object_number=0;item.anim_number=0;item.frame_number=0;item.pos.x_pos=100;item.pos.y_pos=200;item.pos.z_pos=300;item.pos.z_rot=16384;
anim.frame_ptr=frame;anim.interpolation=(12<<8)|1;anim.frame_base=0;anim.frame_end=1;anims=&anim;bones=bone;
objects[0].nmeshes=2;objects[0].bone_index=0;objects[0].frame_base=frame;
frame[6]=8;frame[7]=-4;frame[8]=2;frame[9]=(short)0x4000;frame[10]=(short)0x4000;
ITEM_INFO saved=item;ANIM_STRUCT sa=anim;short sf[24];memcpy(sf,frame,sizeof frame);long sb[4];memcpy(sb,bone,sizeof bone);object_info so=objects[0];
for(int j=0;j<2;j++){memset(MatrixStack,0,sizeof MatrixStack);memset(iMatrixStack,0,sizeof iMatrixStack);memset(&gteRegs,0,sizeof gteRegs);Matrix=MatrixStack;iMatrix=iMatrixStack;MatrixSP=0;MatrixStack[0].m00=4096;MatrixStack[0].m11=4096;MatrixStack[0].m22=4096;
PHD_VECTOR p={1,2,3};GetJointAbsPosition(&item,&p,j);
// Independent scalar quarter-turn composition from versioned table.
long sn=rcossin_tbl[2048],cs=rcossin_tbl[2049];long fx=9+(j?3:0),fy=-2+(j?5:0);long x=100+(fx*cs-fy*sn)/4096,y=200+(fx*sn+fy*cs)/4096,z=j?303:305;
if(p.x!=x||p.y!=y||p.z!=z){fprintf(stderr,"oracle joint%d got %ld %ld %ld expected %ld %ld %ld\n",j,p.x,p.y,p.z,x,y,z);return 2;}
if(Matrix!=MatrixStack||iMatrix!=iMatrixStack||memcmp(&item,&saved,sizeof item)||memcmp(&anim,&sa,sizeof anim)||memcmp(frame,sf,sizeof frame)||memcmp(bone,sb,sizeof bone)||memcmp(objects,&so,sizeof so))return 3;
printf("joint%d %ld %ld %ld %u\n",j,p.x,p.y,p.z,MatrixSP);bytes(MatrixStack,sizeof MatrixStack);bytes(iMatrixStack,sizeof iMatrixStack);bytes(&gteRegs,sizeof gteRegs);
}return 0;}
