#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>

#define CHUNKNUM 0x400

#define SIZE_SZ (sizeof(size_t))
#define MALLOC_ALIGN_MASK (2*SIZE_SZ - 1)
#define MIN_CHUNK_SIZE 12
#define MINSIZE  \
    (unsigned long)(((MIN_CHUNK_SIZE+MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK))

#define request2size(req)                                         \
  (((req) + SIZE_SZ + MALLOC_ALIGN_MASK < MINSIZE)  ?             \
   MINSIZE :                                                      \
   ((req) + SIZE_SZ + MALLOC_ALIGN_MASK) & ~MALLOC_ALIGN_MASK)


const char chars[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_";
size_t size[CHUNKNUM];

void gen(char *chunk)
{
    int i;

    memset(chunk, '\x00', malloc_usable_size(chunk));
    for (i = 0; i < 0x10; i++)
	    chunk[i] = chars[rand() % strlen(chars)];

#ifdef DEBUG
    printf("size: %ld, content: %s\n", malloc_usable_size(chunk), chunk);
#endif
}

int is_dup(int i, size_t s)
{
    int j;

    for (j = 0; j < i; j++) {
        if (size[j] == s)
            return 1;
    }
    return 0;
}

void create_heap()
{
    int i;
    char *chunk;

    srand(0);
    memset(size, '\xff', sizeof(size));
    for (i = 0; i < CHUNKNUM; i++) {
        while (1) {
            size[i] = request2size(rand() % 56746);
            if (!is_dup(i, size[i]))
                break;
        }
        chunk = (char*) malloc(size[i]);
        gen(chunk);
    }
}

void main()
{
    puts("I splited the secrets and hide the slice in each chunk.");
    puts("secrets = ''.join(chunks[i] for i in sorted(chunks)) # sorted by chunk size");
    puts("\
flag = \"CTF{%s}\" % secrets[24] + secrets[37] + secrets[52] + secrets[62] + secrets[79] + secrets[94] + \
+ secrets[95] + secrets[129] + secrets[208] + secrets[292] + secrets[364] + secrets[601] \
+ secrets[663] + secrets[764] + secrets[897] + secrets[955] + secrets[1057] + secrets[1179] \
+ secrets[1186] + secrets[1224] + secrets[1324] + secrets[1448] + secrets[1496] \
+ secrets[1545] + secrets[1548] + secrets[1552] + secrets[1674] + secrets[1927] \
+ secrets[1933] + secrets[2019] + secrets[2172] + secrets[2222] + secrets[2271] \
+ secrets[2287] + secrets[2350] + secrets[2360] + secrets[2413] + secrets[2430]");
    create_heap();
}
