#!/bin/bash

./configure CFLAGS='-lgmp -O2'
make
make install
