// Synthetic source-only integration. Engine callback slots are installed ONLY by ObjectObjects.
#if !(PSX_VERSION && PSXPC_TEST)
#error RE788 is restricted to the attributed backend
#endif
#include "GETSTUFF.H"
#include "CONTROL.H"
#include "ROOMLOAD.H"
#include "COLLIDE_S.H"
#include "LARA.H"
#include "SETUP.H"
#include "OBJECTS.H"
#include "BRIDGE_CALLBACKS.H"
#include <cstdio>
#include <cstring>
#include <cstdint>
static_assert(sizeof(void*)==4 && sizeof(long)==4 && sizeof(int)==4 && sizeof(FLOOR_INFO)==8,"i386 ABI required");
room_info rooms[1]; room_info* room=rooms;
short data[16]; short* floor_data=data;
ITEM_INFO storage[4]; ITEM_INFO* items=storage; ITEM_INFO* lara_item=storage;
lara_info lara; unsigned char InItemControlLoop; short ItemNewRoomNo; short ItemNewRooms[256][2];
extern object_info* objects; object_info object_storage[NUMBER_OBJECTS];
long bone_storage[4]; long* bones=bone_storage;
int height_type,tiltxoff,tiltyoff,OnObject; short* trigger_index;
FLOOR_INFO cells[16];
void InitialiseLaraLoad(short){__builtin_trap();}
static void poisoned_slot(ITEM_INFO*,int,int,int,int*){__builtin_trap();}
static bool observing;
static int family, query_x,query_y,query_z,seen,body_seen,adapter_calls,body_calls,adapter_out,body_out,events,hook_bad;
static const int ids[3]={BRIDGE_FLAT,BRIDGE_TILT1,BRIDGE_TILT2};
static void (*const adapters[3])(ITEM_INFO*,int,int,int,int*)={BridgeCallbackFlatCeiling,BridgeCallbackTilt1Ceiling,BridgeCallbackTilt2Ceiling};
static void (*const bodies[3])(ITEM_INFO*,long,long,long,long*)={BridgeFlatCeiling,BridgeTilt1Ceiling,BridgeTilt2Ceiling};
// Compiler observation hooks, NOT callback adapters. Only real callback TUs are instrumented.
// -O0/-fno-omit-frame-pointer/-m32 fixes the cdecl argument frame. The pointers remain real.
extern "C" void __cyg_profile_func_enter(void* fn,void*){
    if(!observing)return;
    bool adapter=fn==reinterpret_cast<void*>(adapters[family]);
    bool body=fn==reinterpret_cast<void*>(bodies[family]);
    if(!adapter&&!body)return;
    auto frame=static_cast<std::uintptr_t*>(__builtin_frame_address(1));
    auto out=reinterpret_cast<int*>(frame[6]);
    if(frame[2]!=reinterpret_cast<std::uintptr_t>(&storage[1]) || static_cast<int>(frame[3])!=query_x ||
       static_cast<int>(frame[4])!=query_y || static_cast<int>(frame[5])!=query_z || !out){++hook_bad;return;}
    if(adapter){seen=*out;++adapter_calls;events=events*10+1;}
    else {body_seen=*out;++body_calls;events=events*10+2;}
}
extern "C" void __cyg_profile_func_exit(void* fn,void*){
    if(!observing)return;
    bool adapter=fn==reinterpret_cast<void*>(adapters[family]);
    bool body=fn==reinterpret_cast<void*>(bodies[family]);
    if(!adapter&&!body)return;
    auto frame=static_cast<std::uintptr_t*>(__builtin_frame_address(1));
    auto out=reinterpret_cast<int*>(frame[6]);
    if(!out){++hook_bad;return;}
    if(body){body_out=*out;events=events*10+3;}
    else {adapter_out=*out;events=events*10+4;}
}
static int roof(int type,int low,int high,int x,int z){
    bool reverse=type==9||type==15||type==16;
    bool first=reverse?x+z>1024:z<x;
    int offset=first?low:high;
    int dz=first?-6:-2,dx=first?(reverse?1:-3):(reverse?-3:1);
    return 3072+(offset<16?offset:offset-32)*256+(z*dz>>2)+
           (dx<0?((1023-x)*dx>>2):-(x*dx>>2));
}
int main(){
    setvbuf(stdout,nullptr,_IONBF,0);
    int cases=0,diffs=0,result_diffs=0,state_fails=0;
    const int types[]={9,10,15,16,17,18}; const int coords[][2]={{200,100},{300,900}};
    for(int loaded=0;loaded<2;++loaded){
        objects=object_storage; memset(object_storage,0,sizeof object_storage);
        memset(bone_storage,0x5A,sizeof bone_storage);
        // Poison the seven-record neighborhood including all six slots. Loaded is varied independently.
        for(int o=BRIDGE_FLAT-1;o<=BRIDGE_TILT2+1;++o){
            memset(&objects[o],0xA5,sizeof(object_info));
            objects[o].floor=poisoned_slot; objects[o].ceiling=poisoned_slot;
            objects[o].object_mip=-123;
        }
        for(int id:ids)objects[id].loaded=loaded;
        object_info expected[NUMBER_OBJECTS]; memcpy(expected,objects,sizeof expected);
        // Expected records only, never substituted into the actual objects table.
        expected[LARA].shadow_size=160;expected[LARA].initialise=InitialiseLaraLoad;
        expected[LARA].hit_points=1000;expected[LARA].draw_routine=nullptr;expected[LARA].bite_offset&=0xFDFF;
        expected[LARA].save_hitpoints=1;expected[LARA].save_position=1;expected[LARA].save_flags=1;expected[LARA].save_anim=1;
        expected[BRIDGE_FLAT].floor=BridgeCallbackFlatFloor;expected[BRIDGE_FLAT].ceiling=BridgeCallbackFlatCeiling;
        expected[BRIDGE_TILT1].floor=BridgeCallbackTilt1Floor;expected[BRIDGE_TILT1].ceiling=BridgeCallbackTilt1Ceiling;
        expected[BRIDGE_TILT2].floor=BridgeCallbackTilt2Floor;expected[BRIDGE_TILT2].ceiling=BridgeCallbackTilt2Ceiling;
        for(int id:ids)expected[id].object_mip=3072;
        long expected_bones[4];memcpy(expected_bones,bone_storage,sizeof expected_bones);expected_bones[0]=10;
        unsigned char other_before[sizeof rooms+sizeof data+sizeof storage+sizeof cells+sizeof lara+sizeof ItemNewRooms];
        auto snapshot=[&](unsigned char* p){
#define SNAP(v) memcpy(p,&v,sizeof v);p+=sizeof v
            SNAP(rooms);SNAP(data);SNAP(storage);SNAP(cells);SNAP(lara);SNAP(ItemNewRooms);
#undef SNAP
        };
        height_type=101;tiltxoff=102;tiltyoff=103;OnObject=104;trigger_index=data+9;
        InItemControlLoop=1;ItemNewRoomNo=17;
        snapshot(other_before);ObjectObjects();
        bool globals=height_type==101&&tiltxoff==102&&tiltyoff==103&&OnObject==104&&trigger_index==data+9&&
            objects==object_storage&&items==storage&&room==rooms&&floor_data==data&&bones==bone_storage&&
            lara_item==storage&&InItemControlLoop==1&&ItemNewRoomNo==17;
        unsigned char other_after[sizeof other_before];snapshot(other_after);
        bool records=true,neighbors=true;
        for(int id:ids)records=records&&!memcmp(&expected[id],&objects[id],sizeof(object_info));
        for(int id=BRIDGE_FLAT-1;id<=BRIDGE_TILT2+1;++id)
            if(id!=BRIDGE_FLAT&&id!=BRIDGE_TILT1&&id!=BRIDGE_TILT2)
                neighbors=neighbors&&!memcmp(&expected[id],&objects[id],sizeof(object_info));
        bool full=!memcmp(expected,objects,sizeof expected),bs=!memcmp(expected_bones,bone_storage,sizeof expected_bones);
        bool other=!memcmp(other_before,other_after,sizeof other_before);
        printf("REG %d %d %d %d %d %d %d\n",loaded,records,neighbors,full,bs,other,globals);
        if(!records||!neighbors||!full||!bs||!other||!globals)++state_fails;
        for(int type:types)for(int low=0;low<32;++low)for(const auto& c:coords)
        for(int fam=0;fam<3;++fam)for(int q=-1;q<=1;++q)for(int inhibited=0;inhibited<2;++inhibited){
            int high=(low+17)%32,x=c[0],z=c[1]; family=fam;
            int level=4096+(fam==0?0:(((-x)&1023)>>(fam==1?2:1)));
            query_x=x;query_z=z;query_y=level+q;
            memset(cells,0,sizeof cells);memset(rooms,0,sizeof rooms);
            rooms[0].floor=cells;rooms[0].x_size=4;rooms[0].y_size=4;
            for(auto& cell:cells){cell.ceiling=12;cell.floor=32;cell.pit_room=cell.sky_room=255;}
            cells[5].index=1;
            memset(data,0,sizeof data);data[1]=static_cast<short>(type|(low<<5)|(high<<10));data[2]=0x7421;
            data[3]=static_cast<short>(32768|4);data[4]=0;data[5]=static_cast<short>(32768|1);
            memset(storage,0x3C,sizeof storage);storage[1].object_number=ids[fam];
            storage[1].flags=static_cast<short>(inhibited?32768:0);
            storage[1].pos.x_pos=-3000;storage[1].pos.y_pos=4096;storage[1].pos.z_pos=7000;storage[1].pos.y_rot=0;
            height_type=101;tiltxoff=102;tiltyoff=103;OnObject=104;trigger_index=data+9;
            InItemControlLoop=1;ItemNewRoomNo=17;
            // Entire fixture-owned records, not only touched fields; pointer globals are checked below.
            object_info ob[NUMBER_OBJECTS];memcpy(ob,objects,sizeof ob);
            long bb[4];memcpy(bb,bone_storage,sizeof bb);snapshot(other_before);
            seen=body_seen=adapter_out=body_out=123456;adapter_calls=body_calls=events=hook_bad=0;
            observing=true;int got=GetCeiling(&cells[5],x,query_y,z);observing=false;
            snapshot(other_after);
            bool unchanged=!memcmp(other_before,other_after,sizeof other_before)&&!memcmp(ob,objects,sizeof ob)&&!memcmp(bb,bone_storage,sizeof bb);
            bool state=height_type==101&&tiltxoff==102&&tiltyoff==103&&OnObject==104&&trigger_index==data+9&&
                objects==object_storage&&items==storage&&room==rooms&&floor_data==data&&bones==bone_storage&&lara_item==storage&&
                InItemControlLoop==1&&ItemNewRoomNo==17&&hook_bad==0&&adapter_calls==!inhibited&&body_calls==!inhibited&&events==(inhibited?0:1234);
            int incoming=roof(type,low,high,x,z);
            int target=(q==1&&!inhibited)?level+256:incoming;
            diffs+=!inhibited&&(seen!=incoming||body_seen!=incoming);
            result_diffs+=got!=static_cast<short>(target);state_fails+=!state||!unchanged;++cases;
            printf("ROW %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d\n",
                loaded,type,low,high,x,z,fam,q,inhibited,incoming,seen,body_seen,adapter_calls,body_calls,adapter_out,body_out,got,state,unchanged,events,query_y);
        }
    }
    printf("SUMMARY %d %d %d %d\n",cases,diffs,result_diffs,state_fails);
    return diffs||result_diffs||state_fails?1:0;
}
