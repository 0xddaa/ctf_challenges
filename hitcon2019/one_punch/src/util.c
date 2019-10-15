#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#include "sandbox.h"

int puts(const char *s)
{
    write(1, s, strlen(s));
    write(1, "\n", 1);
}

void print(const char *s)
{
    write(1, s, strlen(s));
}

void handler()
{
    puts("timeout");
    exit(0);
}

void error(const char *s)
{
    puts(s);
    exit(1);
}

__attribute__((constructor))
void setup()
{
    signal(SIGALRM, handler);
    alarm(30);

#ifndef SANDBOX_DISABLE
    sandbox();
#endif
}

uint32_t get_int()
{
    char buf[16];

    if (read(0, buf, 8) <= 0) {
        error("io");
    }

    return atoi(buf);
}
