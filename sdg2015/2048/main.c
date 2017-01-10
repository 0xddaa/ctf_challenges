#include <stdint.h>

#include "2048.h"

extern Game g;

void level1()
{
    myprintf("Hey, 2048 is so difficult. Let's begin from 64. I think everyone can reach it...?\n");
    myprintf("Press any key to start...\n");
    getchar();
    init_map();
    if (play(64)) {
        myprintf("Congraz! You pass 64! XD\n");
        clear_map();
        CHEAT = 1;
    } else {
        myprintf("How can you lose? I can't believe it!\n");
        exit(0);
    }
}

int menu()
{
    myprintf("======MENU======\n");
    myprintf("1. start\n");
    myprintf("2. set map size\n");
    myprintf("3. best score\n");
    myprintf("4. set username\n");
    myprintf("5. exit\n");

    char buf[4];
    int c;

    while(1) {
        myprintf("> ");
        fgets(buf, 4, stdin);
        c = atoi(buf);
        return c;
    }
}

void start()
{
    if (!CHEAT) {
        level1();
        return;
    }

    init_map();
    int goal = count_goal();
    if (goal == 0) {
        myprintf("It's impossible to win the game.\n");
    } else if (play(goal)) {
        myprintf("Congraz! You pass %d! XD\n", goal);
        set_bestscore();
    } else
        myprintf("You lose. What a pity.\n");
    
}

void set_mapsize()
{
    if (!CHEAT) {
        myprintf("Locked.\n");
        return;
    }

    myprintf("map size: ");
    char buf[4];
    int size = atoi(fgets(buf, 4, stdin));
    if (size < 4)
        myprintf("Map too small!\n");
    else
        SIZE = size;
}

void set_name()
{
    myprintf("current name: %s\n", NAME);
    myprintf("username: ");
    scanf("%20s", NAME);
}

void show_bestscore()
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

    print_score(buf);
}

int main()
{
    void* func[] = { start, set_mapsize, show_bestscore, set_name };
    void (*ptr)();

    init();
    while (1) {
        uint8_t c = menu() - 1;
        if (c == 4)
            exit(0);
        else if (c > 4)
            continue;
        ptr = func[c];
        (*ptr)();
    }
    
    return 0;
}
