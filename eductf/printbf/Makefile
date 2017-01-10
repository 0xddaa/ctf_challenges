# Slight cheating during instruction execute but runs faster
FLAGS=-W -Wall -Wextra -Wpedantic -O3 -U_FORTIFY_SOURCE

all:
	python genbf.py
	python toker.py -t tpl.c -bf bf > printbf.c
	gcc $(FLAGS) printbf.c -o printbf
	strip printbf

.PHONY=clean
clean:
	rm -f printbf printbf.c
