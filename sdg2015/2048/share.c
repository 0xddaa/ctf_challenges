#include <unistd.h>
#include "share.h"

extern Game g;

void myprintf(const char* fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    __vprintf_chk(100, fmt, ap);
    fflush(stdout);
    va_end(ap);
}

void clear()
{
    system("clear");
}

void init()
{
    signal(SIGALRM, handler);
    alarm(300);
    SIZE = 4;
    CHEAT = 0;
    SEED = time(NULL);
    sprintf(NAME, "Player");
    
    char buf[100];
    sprintf(buf, "score/%d", getpid() % TEAM);
    
    if (access(buf, F_OK) == -1) {
        bzero(buf, 100);
        sprintf(buf, "echo \"%-20s    %-12d\" > score/%d", "ddaa", 5566, getpid() % TEAM);
        system(buf);
    }
}

void handler()
{
    myprintf("time out!\n");
    exit(1);
}

void set_bestscore()
{
    char buf[100];
    sprintf(buf, "score/%d", getpid() % TEAM);
    
    if (access(buf, F_OK) == -1) {
        myprintf("Something error!\n");
        exit(1);
    }

    FILE *f = fopen(buf, "r");
    bzero(buf, 100);
    fgets(buf, 100, f);
    fclose(f);

    /* get current best */
    int score;
    strtok(buf, " ");
    sprintf(buf, "%s", strtok(NULL, " "));
    sscanf(buf, "%d", &score);
    if (SCORE > score) {
        bzero(buf, 100);
        sprintf(buf, "echo \"%-20s    %-12d\" > score/%d", NAME, SCORE, getpid() % TEAM);
        system(buf);
    }
}


