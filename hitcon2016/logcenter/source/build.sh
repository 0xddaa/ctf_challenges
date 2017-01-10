#!/bin/sh

../configure --enable-debug --prefix=/home/logcenter/syslog-ng \
#../configure  \
	--enable-java=no \
	--enable-java-modules=no \
	--enable-amqp=no \
	--enable-sql=no \
	--enable-sun-streams=no \
	--enable-mongodb=no \
	--enable-json=no \
	--enable-geoip=no \
	--enable-pacct=no \
	--enable-stomp=no \
	--enable-systemd=no
