#include <iostream>

using namespace std;

class MSBoard {
public:
    MSBoard(int, int, int);
    ~MSBoard();
    void print_board();
    void get_ans();
    int check();

private:
    int w;
    int h;
    int c_mines;
    int **board;
    int **ans;

    void init_mine();
    void init_info();
};

