#!/bin/bash

activities=(0 406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)


for i in ${activities[@]}
do
  echo "Activity$i" && find ../htkdata -iname *_act_$i\* | wc -l
done
