#!/bin/bash

rm -rf data
mkdir data
python main.py
#&& HQuant -T 1 -C HQuant.conf -s 1 -n 1 256 -S trainlist.txt linvq
