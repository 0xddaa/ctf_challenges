#!/bin/bash

echo $$
[ $$ -ge 1024 ] || while true; do  sleep 3; done
