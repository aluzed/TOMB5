// Constructed asymmetric roof records with the real traps consumer; i386 ABI.
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "OBJECTS.H"
#include "TRAPS.H"
#include <cstdio>
#include <cstring>
static_assert(sizeof(void*)==4 && sizeof(long)==4 && sizeof(FLOOR_INFO)==8,"i386 ABI");
room_info rooms[1]; room_info* room=rooms;
short data[16]; short* floor_data=data;
ITEM_INFO item_storage[1]; ITEM_INFO* items=item_storage;
object_info object_storage[1]; object_info* objects=object_storage;
int height_type,tiltxoff,tiltyoff,OnObject; short* trigger_index;
static int seen,calls;
static void consumer(ITEM_INFO* i,int x,int y,int z,int* out){
    seen=*out; ++calls;
    long value=*out;
    TwoBlockPlatformCeiling(i,x,y,z,&value);
    *out=static_cast<int>(value);
}
static int roof(int type,int low,int high,int x,int z){
    bool reverse=type==9||type==15||type==16;
    bool first=reverse?x+z>1024:z<x;
    int offset=first?low:high;
    int dz=first?-6:-2,dx=first?(reverse?1:-3):(reverse?-3:1);
    int value=3072+(offset<16?offset:offset-32)*256;
    value+=z*dz>>2;
    value+=dx<0?((1023-x)*dx>>2):-(x*dx>>2);
    return value;
}
int main(){
    int cases=0,fails=0,input_diffs=0,result_diffs=0;
    const int coords[][2]={{100,200},{200,100},{512,512},{900,200},{200,900},{824,200},{825,200},{823,200}};
    const int types[]={9,10,15,16,17,18};
    for(int type:types) for(int low=0;low<32;++low) for(const auto& c:coords) for(int mode=0;mode<5;++mode){
        int high=(low+17)%32,x=c[0],z=c[1],y=mode==1?32:33;
        FLOOR_INFO cell; memset(&cell,0,sizeof cell); cell.index=1; cell.ceiling=12; cell.pit_room=cell.sky_room=255;
        memset(data,0,sizeof data); data[1]=static_cast<short>(type|(low<<5)|(high<<10)); data[2]=0x7421;
        data[3]=static_cast<short>(32768|4); data[4]=0; data[5]=static_cast<short>(32768);
        memset(items,0,sizeof item_storage); items[0].mesh_bits=mode==3?0:1; items[0].flags=mode==4?static_cast<short>(32768):0;
        memset(objects,0,sizeof object_storage); objects[0].ceiling=mode==0?nullptr:consumer;
        FLOOR_INFO cb=cell; short db[16]; memcpy(db,data,sizeof db); ITEM_INFO ib[1]; memcpy(ib,items,sizeof ib);
        object_info ob[1]; memcpy(ob,objects,sizeof ob); room_info rb[1]; memcpy(rb,rooms,sizeof rb);
        height_type=101;tiltxoff=102;tiltyoff=103;OnObject=104;trigger_index=data+9;
        calls=0;seen=123456;
        int expected_input=roof(type,low,high,x,z);
        int expected_calls=mode==0||mode==4?0:1;
        int value=(mode==2 && expected_input<0)?256:expected_input;
        int expected=static_cast<short>(value);
        int result=GetCeiling(&cell,x,y,z);
        bool state=height_type==101&&tiltxoff==102&&tiltyoff==103&&OnObject==104&&trigger_index==data+9;
        bool unchanged=!memcmp(&cb,&cell,sizeof cell)&&!memcmp(db,data,sizeof db)&&!memcmp(ib,items,sizeof ib)&&!memcmp(ob,objects,sizeof ob)&&!memcmp(rb,rooms,sizeof rb);
        bool bad_input=expected_calls && seen!=expected_input;
        bool bad_result=result!=expected;
        ++cases;input_diffs+=bad_input;result_diffs+=bad_result;
        if(bad_input||bad_result||calls!=expected_calls||!state||!unchanged)++fails;
        printf("ROW type=%d low=%d high=%d x=%d z=%d mode=%d seen=%d input=%d calls=%d result=%d expected=%d state=%d unchanged=%d\n",type,low,high,x,z,mode,seen,expected_input,calls,result,expected,state,unchanged);
    }
    printf("SUMMARY cases=%d failures=%d input_diffs=%d result_diffs=%d\n",cases,fails,input_diffs,result_diffs);
    return fails?1:0;
}
