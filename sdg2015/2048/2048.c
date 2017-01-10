#include "2048.h"

void up();
void down();
void left();
void right();
void new_item();
void print_edge(char*, char*, char*);
void print_board();
int reach_goal(uint32_t goal);
char get_move();
void cheat();

/* public */
void init_map()
{
    int i, j;

    SPACE = SIZE * SIZE;
    SCORE = 0;
    srand(SEED);

    if (!BOARD)
        BOARD = (uint16_t**) malloc(SIZE * sizeof(uint16_t*));

    for (i = 0; i < SIZE; i++)
        BOARD[i] = (uint16_t*) malloc(SIZE * sizeof(uint16_t));
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++)
            BOARD[i][j] = 0;
    }

    new_item();
    new_item();
}

void clear_map()
{
    int i;
    for (i = 0; i < SIZE; i++)
        free(BOARD[i]);
    free(BOARD);
    BOARD = NULL;
}

int play(uint32_t goal)
{
    while (!reach_goal(goal)) {
        print_board();
        if (!SPACE)
            return 0;

        switch (get_move()) {
            case 'W':
            case 'w':
                up();
                new_item();
                break;
            case 'S':
            case 's':
                down();
                new_item();
                break;
            case 'A':
            case 'a':
                left();
                new_item();
                break;
            case 'D':
            case 'd':
                right();
                new_item();
                break;
            case 'C':
            case 'c':
                if (CHEAT)
                    cheat();
                break;
            case 'G':
            case 'g':
                if (CHEAT)
                    return 0;
                break;
        }
    }

    return 1;
}

uint32_t count_goal()
{
    return pow(2, SIZE * 2 + 3);
}

void print_score(const char* buf)
{
    myprintf("Best score:\n");
    myprintf(buf);
}

/* private */
void cheat()
{
    int i, j;
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            BOARD[i][j] = (BOARD[i][j] < 16384)? BOARD[i][j] * 2 : 0;
        }
    }
}

void new_item()
{
    while (1) {
        uint32_t loc = rand() % (SIZE * SIZE);
        int x = loc % SIZE;
        int y = loc / SIZE;
        
        if (!BOARD[y][x]) {
            BOARD[y][x] = (rand() % 3)? 2 : 4;
            SPACE--;
            return;
        }
    }
}

void print_edge(char* start, char* end, char* split)
{
    int i;
    const char edge[] = "-----";

    myprintf(start);
    for (i = 0; i < SIZE; i++) {
        if (i != 0)
            myprintf(split);
        myprintf(edge);
    }
    myprintf("%s\n", end);
}

void print_board()
{
    int i, j;
        
    clear();
    print_edge("┌", "┐", "-");

    /* print info bar */
    char info[16];
    char info_fmt[16];

    myprintf("|");
    sprintf(info, " goal: %u score: %u ", count_goal(), SCORE);
    sprintf(info_fmt, "%%-%ds", SIZE * 6 - 1);
    myprintf(info_fmt, info);
    myprintf("|\n");

    /* print map */
    for (i = 0; i < SIZE; i++) {
        if (!i)
            print_edge("├", "┤", "┬");
        else
            print_edge("├", "┤", "┼");
        for (j = 0; j < SIZE; j++)
            myprintf("|%5d", BOARD[i][j]);
        myprintf("|\n");
    }
    print_edge("└", "┘", "┴");
}

int reach_goal(uint32_t goal)
{
    int i, j;
    
    for (i = 0; i < SIZE; i++) {
        for (j = 0; j < SIZE; j++) {
            if (BOARD[i][j] == goal)
                return 1;
        }
    }
    return 0;
}

char get_move()
{
    myprintf("w: up, s: down, a: left, d: right\n");
    myprintf("Action: ");
    char buf[4];
    fgets(buf, 4, stdin);
    return buf[0];
}

void up()
{
    int x, y;
    for (y = 1; y < SIZE; y++) {
        for (x = 0; x < SIZE; x++) {
            int i;
            uint16_t *cur = &BOARD[y][x];
            uint16_t *last = &BOARD[y - 1][x];

            if (*cur == 0)
                continue;

            for (i = 0; i < y;) {
                if (*last == 0) {
                    *last = *cur;
                    *cur = 0; 
                } else if (*last == *cur){
                    *last = *cur * 2;
                    SCORE += *last;
                    *cur = 0;
                    SPACE++;
                    break;
                }
                i++;
                cur = last;
                last = &BOARD[y - 1 - i][x];
            }
        }
    }
}

void down()
{
    int x, y;
    for (y = SIZE - 2; y >= 0; y--) {
        for (x = 0; x < SIZE; x++) {
            int i;
            uint16_t *cur = &BOARD[y][x];
            uint16_t *last = &BOARD[y + 1][x];

            if (*cur == 0)
                continue;

            for (i = SIZE - 1; i > y;) {
                if (*last == 0) {
                    *last = *cur;
                    *cur = 0; 
                } else if (*last == *cur){
                    *last = *cur * 2;
                    SCORE += *last;
                    *cur = 0;
                    SPACE++;
                    break;
                }
                i--;
                cur = last;
                last = &BOARD[y + (SIZE - i)][x];
            }
        }
    }

}

void left()
{
    int x, y;
    for (x = 1; x < SIZE; x++) {
        for (y = 0; y < SIZE; y++) {
            int i;
            uint16_t *cur = &BOARD[y][x];
            uint16_t *last = &BOARD[y][x - 1];

            if (*cur == 0)
                continue;

            for (i = 0; i < x;) {
                if (*last == 0) {
                    *last = *cur;
                    *cur = 0; 
                } else if (*last == *cur){
                    *last = *cur * 2;
                    *cur = 0;
                    SCORE += *last;
                    SPACE++;
                    break;
                }
                i++;
                cur = last;
                last = &BOARD[y][x - 1 - i];
            }
        }
    }
}

void right()
{
    int x, y;
    for (x = SIZE - 2; x >= 0; x--) {
        for (y = 0; y < SIZE; y++) {
            int i;
            uint16_t *cur = &BOARD[y][x];
            uint16_t *last = &BOARD[y][x + 1];

            if (*cur == 0)
                continue;

            for (i = SIZE - 1; i > x;) {
                if (*last == 0) {
                    *last = *cur;
                    *cur = 0; 
                } else if (*last == *cur){
                    *last = *cur * 2;
                    *cur = 0;
                    SCORE += *last;
                    SPACE++;
                    break;
                }
                i--;
                cur = last;
                last = &BOARD[y][x + (SIZE - i)];
            }
        }
    }
}
