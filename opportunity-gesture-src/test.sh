#!/bin/bash

train_steps=3
activities=(406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)

# Classify
#HVite -A -D -T 1 -w net.slf -H model/hmm$((train_steps))/all -i reco.mlf -S $subject_prefix$s-data/classifylist.txt def/dict.txt hmmlist.txt
HVite -A -D -T 1 -w wdnet -H model/hmm$((train_steps))/all -i hvite.mlf -S test-data/classifylist.txt def/dict.txt hmmlist.txt > reco.mlf
#awk 'NR%3==0' reco.mlf | awk '{print $3}' > $subject_prefix$s-results-simple.txt
awk '/mfcc$/{nr[NR+1]}; NR in nr' reco.mlf | awk '{print $1}' > results-simple.txt
sed -n 's/^.*_act_\([0-9]*\).*$/\1/p' test-data/testlist.txt | grep --color=never -o '[0-9]\+' | awk '{print "Activity"$0}' > original-simple.txt
echo "Simple training results" >> testing.txt

#simple_empty_lines=$(grep -cv -P '\S' $subject_prefix$s-results-simple.txt)
#simple_acc=$(python accuracy.py $subject_prefix$s-results-simple.txt $subject_prefix$s-original-simple.txt)
#simple_confusion=$(python confusion_matrix.py $subject_prefix$s-results-simple.txt $subject_prefix$s-original-simple.txt)
#echo $simple_acc >> testing.txt
#echo "$simple_confusion" >> testing.txt
#echo >> testing.txt
#
#simple_acc_msg="Simple training accuracy for $subject_prefix$s is $simple_acc . Number of instances that could not be classified: $simple_empty_lines ."
#echo $simple_acc_msg  | mail -s "Simple training complete for $subject_prefix$s" schawla32@gatech.edu
#
#echo 'Independent model training complete!'

