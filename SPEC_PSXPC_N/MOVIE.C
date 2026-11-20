#include <stdio.h>
#include <stdlib.h>
#include "MOVIE.H"

#include "CONTROL.H"
#include <LIBETC.H>

static int FMV_FileExists(const char* path)
{
	FILE* f = fopen(path, "rb");

	if (f == NULL)
	{
		return 0;
	}

	fclose(f);
	return 1;
}

int S_PlayFMV(int sequence, int flag)//*, (<)5E7A0
{
	DISPENV disp;//interp@var_50
	//s1 = fmv_index
	//s2 = a1; //maybe skippable?
	//v0 = 7;

	if (getenv("TOMB5_FMVDBG") != NULL)
	{
		fprintf(stderr, "[FMVREQ] seq=%d flag=%d triggered=%08x\n",
		        sequence, flag, (unsigned)FmvSceneTriggered);
	}

	if (sequence != 7)
	{
		//v0 = 1
		if (FmvSceneTriggered & (1 << sequence))
		{
			return 1;
		}

		FmvSceneTriggered |= (1 << sequence);
	}


#if 0

	lui	$v1, 0x5555
		lh	$a2, 0x60 + var_44($sp)
		li	$v1, 0x55555556
		sll	$a2, 1
		mult	$a2, $v1
		addiu	$a0, $sp, 0x60 + var_48
		addiu	$a1, $s0, 0x5EE0//A3BF0 (db)
		lhu	$a3, 0xFA($a1)
		lhu	$t0, 0xFE($a1)
		li	$v0, 1
		sb	$v0, 0x60 + var_37($sp)
		sra	$a2, 31
		sh	$a3, 0x60 + var_3E($sp)
		sh	$t0, 0x60 + var_3A($sp)
		mfhi	$v1
		subu	$v1, $a2
		//PutDispEnv();//PutDispEnv(DISPENV *env);
		sh	$v1, 0x60 + var_44($sp)
		sll	$v1, $s1, 2
		addiu	$v0, $gp, 0x2E4C
		addu	$v1, $v0
		li	$a0, 0xFFFFFFFF
		lw	$v1, 0($v1)
		nop
		bne	$v1, $a0, loc_5E894
		move	$s5, $s0
		j	loc_5EBBC
		move	$v0, $zero
#endif

	/*
	 * Le lecteur MDEC/STR n'est pas porte. Deux modes :
	 *  - par defaut : comportement historique (retourne -1, la cinematique
	 *    n'est pas jouee et le jeu continue) ;
	 *  - TOMB5_FMV_DIR=<repertoire> : les FMV ont ete converties hors ligne
	 *    (jpsxdec) en FMV<n>.avi (ou FMV<n>.STR[0].avi) ; on les joue avec
	 *    ffplay avant de rendre la main au jeu.
	 */
	{
		const char* dir = getenv("TOMB5_FMV_DIR");
		if (dir != NULL)
		{
			char path[1024];
			char alt[1030];
			char cmd[1280];
			const char* maxSeconds;
			int rc;

			snprintf(path, sizeof(path), "%s/FMV%d.avi", dir, sequence);

			/* ffplay retourne 0 meme quand le fichier n'existe pas : on
			 * verifie donc explicitement avant de lancer le lecteur. */
			if (!FMV_FileExists(path))
			{
				snprintf(alt, sizeof(alt), "%s/FMV%d.STR[0].avi", dir, sequence);
				if (!FMV_FileExists(alt))
				{
					fprintf(stderr,
					        "[FMV] FMV%d introuvable dans %s, cinematique ignoree\n",
					        sequence, dir);
					fflush(stderr);
					return -1;
				}
				snprintf(path, sizeof(path), "%s", alt);
			}

			maxSeconds = getenv("TOMB5_FMV_SECONDS");
			if (maxSeconds != NULL && atoi(maxSeconds) > 0)
			{
				snprintf(cmd, sizeof(cmd),
				         "ffplay -autoexit -loglevel quiet -x 640 -y 480 -t %d '%s'"
				         " >/dev/null 2>&1", atoi(maxSeconds), path);
			}
			else
			{
				snprintf(cmd, sizeof(cmd),
				         "ffplay -autoexit -loglevel quiet -x 640 -y 480 '%s'"
				         " >/dev/null 2>&1", path);
			}

			/* La VRAM n'est touchee que si la video est effectivement jouee.
			 * Sans TOMB5_FMV_DIR (ou si le fichier manque), S_PlayFMV ne doit
			 * pas modifier l'etat PSX : l'ancien FMV_InitialiseVRAM()
			 * s'executait avant le test et changeait le rendu du niveau
			 * charge ensuite (icone d'arme, reference 63041e5c). */
			FMV_InitialiseVRAM();
			VSync(0);
			disp.screen.x = 0xF0;
			SetDefDispEnv(&disp, 0, 0, 480, 0);//BUG: v0 (0xF0, 240) is not written to $sp+0x10, $sp+0x10 gets 0 written to it, maybe custom sdk is used.

			fprintf(stderr, "[FMV] lecture de FMV%d (%s)\n", sequence, path);
			fflush(stderr);
			rc = system(cmd);
			fprintf(stderr, "[FMV] fin de FMV%d (rc=%d)\n", sequence, rc);
			fflush(stderr);
			return 0;
		}
	}

	return -1;//TODO
}


void FMV_InitialiseVRAM()//*, 5F160(<) (F)
{
	RECT16 rect;

	rect.x = 0;
	rect.y = 0;
	rect.w = 512;
	rect.h = 256;

	ClearImage(&rect, 0, 0, 0);

	rect.y = 240;
	ClearImage(&rect, 0, 0, 0);

	DrawSync(0);

	return;
}