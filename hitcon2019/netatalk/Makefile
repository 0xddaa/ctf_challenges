SRC_DIR= ./netatalk-3.1.11

.PHONY: all build release clean


all: release

build:
	cd $(SRC_DIR) && ./configure
	make -C $(SRC_DIR)

release: clean
	cp -a afpd libatalk.so.18 conf/afp.conf netatalk/share/
	tar zcvf netatalk.tgz netatalk/

clean:
	rm -rf netatalk.tgz
