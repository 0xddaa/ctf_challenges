all:
	g++ caitlyn.cpp -o caitlyn -DFLAG='"CTF{ZZZ_zzz_zZZ_Zzz_ZzZ_zZz_ZZz_zzZ}"'
	strip caitlyn

problem:
	g++ caitlyn.cpp -o caitlyn -DFLAG='"CTF{THIS_IS_NOT_REAL_FLAG}"'
	strip caitlyn

debug:
	g++ -DDEBUG -g caitlyn.cpp -o caitlyn

clean:
	rm -f caitlyn
