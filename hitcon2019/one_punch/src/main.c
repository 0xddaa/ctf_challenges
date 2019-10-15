#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#include "util.h"

#define MAX_OBJECT          2
#define TCACHE_MAX_BINS     64
#define TCACHE_0x220        32

typedef struct tcache_entry
{
    struct tcache_entry *next;
} tcache_entry;

typedef struct tcache_perthread_struct
{
    char counts[TCACHE_MAX_BINS];
    tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;

static tcache_perthread_struct *tcache = NULL;

void *tps; // tcache_perthread_struct

void menu()
{
    print("############################\n");
    print("👼     One Punch Man      👼\n");
    print("############################\n");
    print("#   1. debut               #\n");
    print("#   2. rename              #\n");
    print("#   3. show                #\n");
    print("#   4. retire              #\n");
    print("#   5. Exit                #\n");
    print("############################\n");
    print("> ");
}

typedef struct {
    char *buf;
    size_t size;
} hero;

hero heroes[MAX_OBJECT];

void debut()
{
    uint32_t idx;

    print("idx: ");
    if (idx = get_int(), idx > MAX_OBJECT) {
        error("invalid");
    }

    char buf[0x400];
    int size;

    print("hero name: ");
    memset(buf, 0, 0x400);
    if (size = read(0, buf, 0x400), size <= 0) {
        error("io");
    }
    buf[size - 1] = '\0';

    if (size < 0x80 || size > 0x400) {
        error("poor hero name");
    }

    heroes[idx].buf = (char *) calloc(1, size);
    heroes[idx].size = size;

    strncpy(heroes[idx].buf, buf, size);
    memset(buf, 0, 0x400);
}

void rename()
{
    uint32_t idx;

    print("idx: ");
    if (idx = get_int(), idx > MAX_OBJECT) {
        error("invalid");
    }

    if (!heroes[idx].buf) {
        error("err");
    }

    print("hero name: ");
    if (read(0, heroes[idx].buf, heroes[idx].size) <= 0) {
        error("io");
    }
}

void show()
{
    uint32_t idx;

    print("idx: ");
    if (idx = get_int(), idx > MAX_OBJECT) {
        error("invalid");
    }

    if (heroes[idx].buf) {
        print("hero name: ");
        puts(heroes[idx].buf);
    }
}

void retire()
{
    uint32_t idx;

    print("idx: ");
    if (idx = get_int(), idx > MAX_OBJECT) {
        error("invalid");
    }

    free(heroes[idx].buf); // uaf
}

void one_punch()
{
    char *buf;

    if (tcache->counts[TCACHE_0x220] < 7) {
        error("gg");
    }

    if (buf = malloc(0x217), !buf) {
        error("err");
    }

    if (read(0, buf, 0x217) <= 0) {
        error("io");
    }

    puts("Serious Punch!!!");
    puts("( ﾟДﾟ)σ弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌弌⊃");
    puts(buf);
}

int main()
{
    void *p = malloc(0x1000);

    if (!p) {
        error("err");
    }
    free(p);

    tcache = ((uint64_t) p & 0xfffffffffffff000) + 0x10;

    while (1) {
        menu();
        int c = get_int();

        switch (c) {
            case 1:
                debut();
                break;
            case 2:
                rename();
                break;
            case 3:
                show();
                break;
            case 4:
                retire();
                break;
            case 0xc388:
                one_punch();
            case 5:
            default:
                puts("bye!");
                break;
                
        }
    }
    return 0;
}
