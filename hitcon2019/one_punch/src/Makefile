BIN=one_punch
CFLAGS= -Wno-int-conversion -g
CPPFLAGS=-D_FORTIFY_SOURCE=2

.PHONY: all clean one_punch

all: $(BIN)
	strip $(BIN)

$(BIN):
	gcc $(CFLAGS) $(CPPFLAGS) main.c util.c bpf-helper.c -o $(BIN)

test:
	gcc -D SANDBOX_DISABLE $(CFLAGS) $(CPPFLAGS) -g main.c util.c bpf-helper.c -o $(BIN)

clean:
	rm -f one_punch
