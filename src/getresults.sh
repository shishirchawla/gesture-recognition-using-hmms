#!/bin/bash

HVite -A -D -T 1 -w net.slf -H model/hmm3/all -i reco.mlf -S classifylist.txt def/dict.txt hmmlist.txt
awk 'NR%3==0' reco.mlf | awk '{print $3}' > results.txt
#sed -n 's/^.*\(act_[0-9]*\).*$/\1/p' testtargetlist.txt | sed -e 's/act_/Activity/g' > original.txt
sed -n 's/^.*_act_\([0-9]*\).*$/\1/p' testtargetlist.txt | grep --color=never -o '[0-9]\+' | awk '$1>6{$1="Other"}1' | awk '{print "Activity"$0}' > original.txt
python accuracy.py
