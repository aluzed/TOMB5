#include "MALLOC.H"

#include "GAMEFLOW.H"
#include "SPECIFIC.H"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define GAME_MALLOC_BUFFER_SIZE (1024*1060)

#if defined(__LP64__)
/* En LP64 les structures hotes sont plus grosses qu'en 32 bits : les
 * ITEM_INFO/ANIM_STRUCT/room_info contiennent des pointeurs de 8 octets et
 * les conversions du format fichier immobilisent des tampons
 * supplementaires. Le niveau titre consomme ~1 061 000 octets contre
 * ~922 000 en 32 bits, ce qui depassait l'arene d'origine. On garde une
 * arene separee, toujours allouee sous 4 Gio (MAP_32BIT). */
#undef GAME_MALLOC_BUFFER_SIZE
#define GAME_MALLOC_BUFFER_SIZE (4*1024*1024)
#endif

char* malloc_ptr = NULL;
int malloc_used = 0;
int malloc_free = GAME_MALLOC_BUFFER_SIZE;
int script_malloc_size = 0;
#if defined(__LP64__)
/* L'arene du jeu doit rester sous 4 Gio : le moteur stocke des adresses
 * 32 bits dans les blocs reloges depuis le fichier de niveau, et certains
 * chemins additionnent la valeur basse d'un pointeur a un offset.
 * MAP_32BIT garantit cette contrainte sur x86-64 (RMIG-005). */
#include <sys/mman.h>
char* malloc_buffer = NULL;

static void port_alloc_game_arena(void)
{
	void* p = mmap(NULL, GAME_MALLOC_BUFFER_SIZE, PROT_READ | PROT_WRITE,
	               MAP_PRIVATE | MAP_ANONYMOUS | MAP_32BIT, -1, 0);

	if (p == MAP_FAILED)
	{
		perror("game arena mmap(MAP_32BIT)");
		exit(1);
	}

	malloc_buffer = (char*)p;
}
#else
char malloc_buffer[GAME_MALLOC_BUFFER_SIZE];
#endif

/*
 * [FUNCTIONALITY] - init_game_malloc.
 * Resets malloc_buffer and all allocation stats back to their default values.
 * Note: The entire malloc_buffer is zero initialised.
 * Note: Once the gameflow script is loaded it's always in malloc_buffer regardless.
 */

#if defined(__LP64__)
/* Petit pool bas (< 4 Gio) pour les buffers de travail qui stockent des
 * pointeurs tronques sur 32 bits dans le code PSX (scratchpads de rendu).
 * Il ne doit jamais etre libere par init_game_malloc(). */
char* PORT_LowAlloc(int size)
{
	static char* pool = NULL;
	static int used = 0;
	const int POOL_SIZE = 16 * 1024 * 1024;

	if (pool == NULL)
	{
		void* p = mmap(NULL, POOL_SIZE, PROT_READ | PROT_WRITE,
		               MAP_PRIVATE | MAP_ANONYMOUS | MAP_32BIT, -1, 0);

		if (p == MAP_FAILED)
		{
			perror("PORT_LowAlloc mmap(MAP_32BIT)");
			exit(1);
		}

		pool = (char*)p;
	}

	size = (size + 15) & ~15;

	if (used + size > POOL_SIZE)
	{
		fprintf(stderr, "PORT_LowAlloc: pool exhausted (%d + %d > %d)\n",
		        used, size, POOL_SIZE);
		exit(1);
	}

	{
		char* ptr = &pool[used];
		used += size;
		return ptr;
	}
}
#endif

void init_game_malloc()//5E79C(<), 5F4F8(<) (F) (*) (D) (ND)
{
#if defined(__LP64__)
	if (malloc_buffer == NULL)
	{
		port_alloc_game_arena();
	}
#endif

	malloc_used = gfScriptLen;
	malloc_free = GAME_MALLOC_BUFFER_SIZE - gfScriptLen;
	malloc_ptr = &malloc_buffer[gfScriptLen];
	memset(&malloc_ptr[0], 0, GAME_MALLOC_BUFFER_SIZE - gfScriptLen);
}

/*
 * [FUNCTIONALITY] - game_malloc.
 * "Allocates" memory from our malloc_buffer declared on the stack.
 * Note: Memory that is "allocated" is not zero initialised.
 * Note: If you run out of memory the application will exit.
 * Note: Usage should be seen as stack functionality, always free the last block of memory you allocated (LIFO).
 * [USAGE]
 * @PARAM - [size] The amount of memory you wish to "allocate".
 * @RETURN - [ptr] Pointer to the memory block you just "allocated".
 */

char* game_malloc(int size)//5E7E8(<), 5F544(<) (F) (*) (?) (D) (ND)
{
#if DEBUG_VERSION
	char buf[80];
#endif

	char* ptr = NULL;

	size = (size + 3) & -4;

	if (size <= malloc_free)
	{
		ptr = malloc_ptr;
		malloc_free -= size;
		malloc_used += size;
		malloc_ptr += size;
	}
#if DEBUG_VERSION
	else
	{
		sprintf(buf, "game_malloc() out of space (needs %d only got %d)\n", size, malloc_free);
		S_ExitSystem(buf);
		return NULL;
	}
#endif
	return ptr;
}

/*
 * [FUNCTIONALITY] - game_free.
 * "Frees" memory from malloc_buffer.
 * Note: Memory that is freed is not zero initialised.
 * Note: There is no error checking so ensure you do not free more memory than the buffer can hold.
 * Note: Usage should be seen as stack functionality, always free the last block of memory you allocated (LIFO).
 * [USAGE]
 * @PARAM - [size] The amount of memory you wish to "free".
 */

void game_free(int size)//5E85C(<), 5F590(<) (F) (*) (D) (ND)
{
	size = (size + 3) & -4;

	malloc_ptr -= size;
	malloc_free += size;
	malloc_used -= size;
}

/*
 * [FUNCTIONALITY] - show_game_malloc_totals.
 * Prints the amount of free/used malloc_buffer memory to stdio in Kilobytes.
 */
#if DEBUG_VERSION
void show_game_malloc_totals()//5E894(<), * (F) (*)
{
	printf("---->Total Memory Used %dK of %dK<----\n", ((malloc_used + 1023) / 1024) - 10, ((malloc_used + malloc_free) / 1024) - 10);
}
#endif