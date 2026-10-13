// RE945 SOURCE-only harness. Real globals, complete production MISC.C linked separately.
#include "MISC.H"
#include "CONTROL.H"
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stdint.h>
static_assert(sizeof(long)==4 && sizeof(int)==4 && sizeof(void*)==4,"GCC ILP32 required");
long rand_1=0, rand_2=0;
static int isolation() {
    SeedRandomControl(1); SeedRandomDraw(0);
    if (rand_1!=1 || rand_2!=0) return 1;
    if (GetRandomControl()!=16838 || rand_1!=1103527590 || rand_2!=0) return 1;
    if (GetRandomDraw()!=0 || rand_1!=1103527590 || rand_2!=12345) return 1;
    SeedRandomControl(0);
    if (rand_1!=0 || rand_2!=12345) return 1;
    SeedRandomDraw(1);
    if (rand_1!=0 || rand_2!=1) return 1;
    if (GetRandomDraw()!=551730746 || rand_1!=0 || rand_2!=1103527590) return 1;
    if (GetRandomControl()!=0 || rand_1!=12345 || rand_2!=1103527590) return 1;
    puts("isolation PASS"); return 0;
}
int main(int argc, char** argv) {
    if (argc!=2) return 2;
    if (!strcmp(argv[1],"--isolation")) return isolation();
    // Reject whitespace/signs; decimal or explicit hexadecimal uint32 only.
    if (!argv[1][0] || argv[1][0]=='-' || argv[1][0]=='+' || argv[1][0]==' ') return 2;
    int base=10; const char* digits=argv[1];
    if (digits[0]=='0' && (digits[1]=='x' || digits[1]=='X')) { base=16; digits+=2; }
    if (!*digits) return 2;
    for (const char* p=digits; *p; ++p) {
        if (!((*p>='0' && *p<='9') || (base==16 && ((*p>='a' && *p<='f') || (*p>='A' && *p<='F'))))) return 2;
    }
    errno=0; char* end=0; unsigned long seed=strtoul(digits,&end,base);
    if (errno==ERANGE || !end || *end || seed>UINT32_MAX) return 2;
    SeedRandomControl((long)seed); SeedRandomDraw((long)seed);
    printf("seed %ld %ld\n",rand_1,rand_2);
    long c=GetRandomControl(); printf("control %ld %ld %ld\n",c,rand_1,rand_2);
    long d=GetRandomDraw(); printf("draw %ld %ld %ld\n",d,rand_1,rand_2);
    return 0;
}
