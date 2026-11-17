#ifndef THREEDEE_OBJ_H
#define THREEDEE_OBJ_H

#include "STYPES.H"

#if defined(__LP64__)
extern struct TSV* tsv_buffer;
#else
extern struct TSV tsv_buffer[1024];
#endif

extern void CreateMonoScreen();

#endif