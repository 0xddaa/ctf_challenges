SRC = otp.c
BIN = otp
LIBS = $(shell libgcrypt-config --libs) $(shell pkg-config --libs libcrypto) $(shell pkg-config --libs openssl) $(shell pkg-config --libs gnutls)

all:
	gcc $(SRC) $(CFLAGS) $(LIBS) -o $(BIN)
clean:
	rm -rf $(BIN)
