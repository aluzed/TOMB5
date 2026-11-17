#include "3D_GEN.H"

#include "CAMERA.H"
#include "GPU.H"

#include <LIBGTE.H>

long phd_left;
long phd_right;
long phd_top;
long phd_bottom;
long phd_persp;
#if defined(__LP64__)
/* La matrice monde->vue est un tableau de 12 mots 32 bits (format GTE).
 * En LP64, `long` fait 8 octets : les ecritures (matrix_stack[9]) et les
 * lectures (phd_mxptr[3]) n'utilisaient plus le meme pas et la projection
 * 3D etait completement fausse. */
int w2v_matrix[12];
int* phd_mxptr;
int matrix_stack[24];
#else
long w2v_matrix[12];
long* phd_mxptr;
long matrix_stack[24];
#endif
struct PHD_3DPOS viewer;
struct VECTOR3D CamPos;
struct VECTOR3D CamTgt;

void phd_InitWindow(int view_angle)//5D74C(<), 5DBC8(<) (F)
{
	phd_right = SCREEN_WIDTH - 1;
	phd_persp = COS((((((view_angle << 1) + view_angle) << 3) - view_angle) << 2) - view_angle) << 8 / SIN((((((view_angle << 1) + view_angle) << 3) - view_angle) << 2) - view_angle);
	phd_left = 0;
	phd_top = 0;
	phd_bottom = SCREEN_HEIGHT - 1;
	phd_mxptr = &matrix_stack[0];
	SetGeomOffset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2);
	SetGeomScreen(phd_persp);
}