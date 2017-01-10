#!/bin/bash

pid=$$
conf="/home/logcenter/tmp/$pid"
persist="/home/logcenter/tmp/$pid-persist"
pidfile="/home/logcenter/tmp/$pid-pidfile"
if [ $pid -le 1024 ] || [ $pid -eq 22222 ]; then
  echo "something error happened, plz try againg."
  exit 0
fi

rm -f "$conf"
sed "s/PORT/$$/" /home/logcenter/conf.tpl > $conf
if [ -f "$conf" ]; then
  timeout 90 /home/logcenter/syslog-ng/sbin/syslog-ng -f $conf -R $persist -p $pidfile -d 2>&1
else
  echo "something error happened, plz try againg."
  exit 1
fi
