#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "ms.h"

#ifndef FLAG
#define FLAG "flag{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}"
#endif

using namespace std;

MSBoard::MSBoard(int w, int h, int c_mines)
{
    this->w = w;
    this->h = h;
    this->c_mines = c_mines;

    FILE *fp = fopen("/dev/urandom", "r");
    int seed;
    fread(&seed, sizeof(int), 1, fp);
    fclose(fp);
    srand(seed);

    init_mine();
    init_info();
}

/* 0 = unknown, 1 ~ 8 = num, -1 = bomb */
void MSBoard::init_mine()
{
    board = new int*[h];
    for (int i = 0; i < w; i++)
        board[i] = new int[w]();

    for (int i = 0; i < c_mines;) {
        int x = rand() % w;
        int y = rand() % h;
        
        if (board[y][x] == 0) {
            board[y][x] = -1;
            i++;
        }
    }
}

MSBoard::~MSBoard()
{
    for (int i = 0; i < w; i++) {
        delete [] board[i];
        delete [] ans[i];
    }
    delete [] board;
    delete [] ans;
}

void MSBoard::init_info()
{
    for (int j = 0; j < h; j++) {
        for (int i = 0; i < w; i++) {
            if (board[j][i] == -1)
                continue;

            // corner
            if (j > 0 && i > 0 && board[j-1][i-1] == -1)        board[j][i]++;
            if (j > 0 && i < w-1 && board[j-1][i+1] == -1)      board[j][i]++;
            if (j < h-1 && i > 0 && board[j+1][i-1] == -1)      board[j][i]++;
            if (j < h-1 && i < w-1 && board[j+1][i+1] == -1)    board[j][i]++;

            // direction
            if (j > 0 && board[j-1][i] == -1)                   board[j][i]++;
            if (j < h-1 && board[j+1][i] == -1)                 board[j][i]++;
            if (i > 0 && board[j][i-1] == -1)                   board[j][i]++;
            if (i < w-1 && board[j][i+1] == -1)                 board[j][i]++;
        }
    }
}

void MSBoard::print_board()
{
    printf("      ");
    for (int i = 0; i < w; i++)
        printf("%2d  ", i);
    printf("\n\n");

    for (int j = 0; j < h; j++) {
        printf("%2d    ", j);
        for (int i = 0; i < w; i++) {
#ifndef DEBUG
            if (board[j][i] > 0)
#else
            if (board[j][i] >= 0)
#endif
                printf("%2d  ", board[j][i]);
#ifdef DEBUG
            else if (board[j][i] == -1)
                printf("%2c  ", '*');
#endif
            else
                printf("%2c  ", '-');
        }
        printf("\n");
    }
}

void MSBoard::get_ans()
{
    ans = new int*[h];
    for (int i = 0; i < w; i++)
        ans[i] = new int[w]();

    for (int j = 0; j < h; j++) {
        for (int i = 0; i < w; i++) {
            cin >> ans[j][i];
        }
    }
}

int MSBoard::check()
{
    /* check ans is legal */
    for (int j = 0; j < h; j++) {
        for (int i = 0; i < w; i++) {
            if (ans[j][i] < -1 || ans[j][i] >= 9)
                return 1;
            else if (board[j][i] > 0 && board[j][i] != ans[j][i])
                return 2;
        }
    }

    /* check ans is correct */
    for (int j = 0; j < h; j++) {
        for (int i = 0; i < w; i++) {
            if (ans[j][i] == -1)
                continue;

            int count = 0;
            // corner
            if (j > 0 && i > 0 && ans[j-1][i-1] == -1)          count++;
            if (j > 0 && i < w-1 && ans[j-1][i+1] == -1)        count++;
            if (j < h-1 && i > 0 && ans[j+1][i-1] == -1)        count++;
            if (j < h-1 && i < w-1 && ans[j+1][i+1] == -1)      count++;

            // direction
            if (j > 0 && ans[j-1][i] == -1)                     count++;
            if (j < h-1 && ans[j+1][i] == -1)                   count++;
            if (i > 0 && ans[j][i-1] == -1)                     count++;
            if (i < w-1 && ans[j][i+1] == -1)                   count++;

            if (count != ans[j][i])
                return 3;
        }
    }
    return 0;
}

int main()
{
#ifndef DEBUG
    alarm(30);
#endif
    setvbuf(stdout, 0, _IONBF, 0);
    setvbuf(stdin, 0, _IONBF, 0);

    for (int level = 1; level <= 9; level++) {
        MSBoard board = MSBoard(level*10, level*10, level*10*level*10/5);
        board.print_board();
        board.get_ans();
#ifndef DEBUG
        if (board.check()) {
            puts("ggwp");
            exit(1);
        }
#else
        switch (board.check()) {
            case 1:
                puts("not in range");
                break;
            case 2:
                puts("not the same");
                break;
            case 3:
                puts("not correct ans");
                break;
            default:
                continue;
        }
        exit(1);
#endif
    }
    printf("Congraz! here is your flag: %s\n", FLAG);
    return 0;
}
