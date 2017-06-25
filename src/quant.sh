#!/bin/bash

rm -rf data
mkdir data
python main.py

# FIXME Remove the following line, this was used when the data was quantized for
# the discrete model
# HQuant -T 1 -C HQuant.conf -s 1 -n 1 256 -S trainlist.txt linvq
