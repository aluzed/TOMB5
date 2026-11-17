#ifndef THREED_GEN_H
#define THREED_GEN_H

#include "STYPES.H"

extern long phd_left;
extern long phd_right;
extern long phd_top;
extern long phd_bottom;
extern long phd_persp;
#if defined(__LP64__)
extern int w2v_matrix[12];
extern int* phd_mxptr;
extern int matrix_stack[24];
#else
extern long w2v_matrix[12];
extern long* phd_mxptr;
extern long matrix_stack[24];
#endif
extern struct PHD_3DPOS viewer;
extern struct VECTOR3D CamPos;
extern struct VECTOR3D CamTgt;

extern void phd_InitWindow(int view_angle);


#endif