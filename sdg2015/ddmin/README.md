# ddmin
## Description
`ddmin` 這題是呼應本學期課程中的作業  
全稱是 delta debugging minimize  
情境是已經在測試階段發現某個測資會導致程式 crash  
目標是寫一個自動化的 ddmin script  
找出測資中能觸發程式 crash 的最小子集合  
要除錯的程式是 **Defcon 23 Qual** 的其中一題 -- `hackercalc`  
`hackercalc` 是一個可編程的計算機  
使用者定義計算函式後，計算機就會算出結果  
EX:  

```
// Define the behavior  
func GG(a)
    return a + 10

// Calculate
run GG(1)
RESULT: 11 (B)
```

## Write-up
### Principle
雖然說這題是參考自課程作業  
但是解法並不限制一定要寫出完整的 ddmin script  
只要能找出 minimal crash input 就可以  
大部分同學是利用半自動的方式找出答案  
刪去大部分的 input 以後再人工刪除不合規定的 input  

要對 `hackercalc` 寫出完整的 ddmin script 其實並不容易  
ddmin 的原理是利用不斷的分割得到 input 的子集  
再以分割後的子集作為測資測試程式  
如果程式執行後保持 crash  
則再分割子集 直到沒有更小的子集為止  
但 `hackercalc` 與範例與作業並不相同  
範例單純的去分割一個字串，精細度可以到每個字元  
作業稍微複雜，解析一個 xml 檔案，精細度則可以到每個單字  
至於這題的精細度該如何決定呢?  
由於 `hackercalc` 是一個類似 interpreter 的程式  
我認為應該以 *每行代碼* 做為最小單位  
如果更分得更細，很可能執行的過程就與原先的測資不同  
會失去 ddmin 原本的意義  
此外，由於 interpreter 的特性  
會使代碼的順序有相依性  
沒辦法如範例或作業中，透過 binary search 的方式去分割子集  
如果用逐行分割  
時間複雜度將會是 O(2^N)  
在以每行為單位的分割方式已經要執行數分鐘才能得到結果  
如果分得更細，執行時間將會成指數成長  

### Implementation
在出這題的時候其實我沒有料到會這麼難...XD  
最早在實作的分割時候只是很直覺的將每一行代碼從刪除  
這樣的做法在應付 part1 的測資是 OK 的  
但是如果測資包含 if 陳述句滿足某些條件可能會找出錯誤的結果  
底下是一個例子:  

```
func MOD(a, b)
    if (a < 1)
        if (a > 2)
            return 1
        return b % 0
    return 1
```

當 `a = -1` 時會執行到 `return b % 0` 這行  
導致程式發生 **Floating point exception**  
因此在 `MOD` 裡面只需要包含該行即可  
其他都是多餘的 input  
但是如果分割時一次只刪除一行  
在刪除 `if (a < 1)` 這行以後  
程式將改變 control flow 變成執行到 `return 1`  
不會如原先一樣執行 `return b % 0`  
因此在判斷時，會認為 `if (a < 1)` 會造成 crash 而必須被保留  
實際上，這行並非造成程式 crash 的原因  
BTW，在一開始進行 kof 時沒有馬上開放的原因  
是因為比賽前一天才發現自己的作法不是正解 囧rz  

第一個改良方式是用排列組合的方式窮舉出所有可能  
但是這樣跑不出結果......  
以 50 行的測資來說，C(1, 50) + C(2, 50) + ... + C(50, 50)  
測試的數量等同於 `O(2^50)`  
稍微改進將目標從全部測資縮小為每個 function  
可以把結果變成 `O(n * 2^m)` (n = function 數量, m = function 的最大行數)  
但是對單一 function 很複雜這種 worst case 來說一樣跑不出結果  

於是我又換了一種改良方式  

1. 先以 function 為單位去分割子集，過濾沒被使用的 function  
2. 以 if/while 敘述的 block 為單位去分割子集，過濾不必要的 if/while block  
3. 靜態分析代碼以建立 `hackercalc` 計算時的 control flow  
4. 以行為單位，並且根據執行順序動態分割子集  

如此一來效率上就好上太多   
時間複雜度降到 O(N) 就可以找出結果  
這樣找出來的結果已經幾乎是正確結果  
但是還是有例外.....  

例外是處理 function 之間相依性的問題  
舉例來說：  
如果 if/while 的條件判斷  
倚賴其他 function 的回傳結果  
由於刪減後可能會讓回傳值與原先不同  
將會導致 if/while 分割時得到錯誤的結果  
如果將處理 if/while 敘述的分割也根據執行順序執行應該可以避免此問題  
不過我用了另一個偷懶的做法  
用迴圈去重複執行 ddmin 數次  
這樣 fucntion 之間執行順序的問題就可以因為執行數次而解決  
最後得到的結果就是 minimal crash input  
