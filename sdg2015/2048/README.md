# 2048
## Description
2048 這題是 CTF 中 pwn 題型的簡化版  
由於本學期課程中不包括如何去利用程式中的漏洞  
因此在設計題目時，在外面包了一層 wrapper  
只要程式發生 crash ，wrapper 就會將 flag (token) 送給使用者  

## Write-up
這題一共有 6 種造成程式 crash 的方法  
還有 1 個不能直接造成 crash  
但是方便觸發 crash 的後門  

(1) Out of Bound  
在 `main` 中  
func 是用來儲存各個功能的陣列，大小為 4  
對應到選單的各種功能  
但是在判斷選單的邊界值卻到 5  
執行到第 10 行時會使程式跳到未知的地方  
造成 crash  
```
 1 void* func[] = { start, set_mapsize, show_bestscore, set_name };
 2 void (*ptr)();
 3 while (1) {
 4     uint8_t c = menu() - 1;
 5     if (c == 5)
 6         exit(0);
 7     else if (c > 5)
 8         continue;
 9     ptr = func[c];
10    (*ptr)();
11 }
```

(2) Stack Overflow  
在 `print_board` 裡面  
宣告了兩個大小為 16 的字串陣列  
第 153 & 154 行利用 `sprintf` 產生遊戲資訊的字串  
將會發生 buffer overflow 的問題  
" goal: %u score: %u " 字串長度已經超過 16 byte  
但由於後面還有 `info_fmt` 這個變數  
所以 153 行並不會 crash  
要到 154 行將字串複製到 `info_fmt` 才會使程式 crash  
由於這題編譯時 gcc 有做優化對齊 stack 長度  
因此字串長度總共要到 28 以上才會造成程式 crash  
只要選最大的地圖使 goal 到達最大值  
並且將分數玩到 6 位數以上即可達到觸發條件  

```
149     char info[16];
150     char info_fmt[16];
151
152     myprintf("|");
153     sprintf(info, " goal: %u score: %u ", count_goal(), SCORE);
154     sprintf(info_fmt, "%%-%ds", SIZE * 6 - 1);
```

(3) Command Injection  
這題的漏洞在 share.c 的 `set_scoreboard` 裡面  
在利用 `set username` 的功能設定名字以後  
只要創下最高紀錄 就會以 "名字 + 分數" 的格式將紀錄寫到檔案中  
由於名字沒有做任何過濾  
且直接利用 `system` 去執行指令  
只要名字包含 shell 中的特殊字元  
將會把原先 echo 的指令截斷且可以在後面執行其他指令  

```
 65     if (SCORE > score) {
 66         bzero(buf, 100);
 67         sprintf(buf, "echo \"%-20s    %-12d\" > score/%d", NAME, SCORE, getpid() % TEAM);
 68         system(buf);
 69     }
```

(4) Divide Zero  
在 C 語言中只要有除以 0 的程式碼被執行  
就會跳出 SIGFPE 的 signal 且中斷程式執行  
在宣告地圖大小時 邊界值使用 `int8_t` 的型態  
但是卻以 `atoi` 取得輸入整數  
因此只要輸入數字是 256 的倍數  
將等同輸入 0  
在 `new_item` 中將會對 size * size 取餘數  
此時如果 size 為 0 就會觸發 SIGFPE  

```
 18 struct game {
 19     uint16_t **board;
 20     uint8_t size;
 21     uint32_t space;
 22     uint32_t score;
 23     char name[20];
 24     uint8_t seed;
 25     uint8_t cheat;
 26 } typedef Game;
```

(5) Format String Vulnerability  
一樣因為在 `set username` 的功能中  
並沒有對字元做過濾  
因此使用者名稱可以包涵 `%` 的符號  
在 `print_score` 中  
98 行直接將 buffer 動態的作為 printf 的第一個參數  
此時如果使用者名稱包含 `%s`, `%n` 等格式化字串  
將可能因為對記憶體的不當存取  
導致程式 crash  

```
 95 void print_score(const char* buf)
 96 {
 97     myprintf("Best score:\n");
 98     myprintf(buf);
 99 }
```

(6) Heap Overflow  
程式雖然時做了 `clear_map` 去對棋盤做釋放  
但是在遊戲結束後，並不會正確的呼叫 `clear_map`  
加上在 `init_map` 中，如果發現 BOARD 並非 NULL  
就不會再次分配空間  
因此只要在成功破關後 將地圖 SIZE 增加  
再次進行遊戲  
在下次 `init_map` 的時候就會導致 heap overflow  

```
 23     if (!BOARD)
 24         BOARD = (uint16_t**) malloc(SIZE * sizeof(uint16_t*));
```

(7) Off-By-One  
在 `set_name` 的功能中  
最多將會讀取 20 byte 的字串加上 1 byte 的 NULL 作為字串結尾  
但是用來存名稱的 name 陣列只有 20 byte  
多出來的 1 byte 將會把用來產生隨機的 seed 變數給覆蓋  
這樣每次遊戲過程所生成的數字就會固定下來  
可以方便觸發後面的漏洞  

```
 78 void set_name()
 79 {
 80     myprintf("current name: %s\n", NAME);
 81     myprintf("username: ");
 82     scanf("%20s", NAME);
 83 }
```
