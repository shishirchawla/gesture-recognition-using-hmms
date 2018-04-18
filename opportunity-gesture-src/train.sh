#!/bin/bash

train_data_dir='train-data'
train_steps=3
activities=(0 406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)
#activities=(0)

# Train
# Cleanup old hmms
rm -rf ./model/hmm*
for i in $(seq 0 $train_steps)
do
  mkdir ./model/hmm$i
done

# Init and train hmms
for i in ${activities[@]}
do
  echo "Initialize HMM..."
  HInit -A -D -w 1.0 -T 1 -S $train_data_dir/trainlist_act_$i.txt -M model/hmm0 model/proto/Activity$i

  echo "Training HMMS..."
  for j in $(seq 1 $train_steps)
  do
    HRest -A -D -T 1 -v 0.00000000001 -S $train_data_dir/trainlist_act_$i.txt -M model/hmm$j -H model/hmm$((j-1))/Activity$i Activity$i
  done
done

# Concat hmms into one file
echo 'Compiling hmms into one file..'
hmm_file=./model/hmm$train_steps/all
counter=0

rm -f $hmm_file
for filename in ./model/hmm$train_steps/*
do
  if [ $filename != $hmm_file ] && [ $filename != "./model/hmm$train_steps/*" ]; then
    if [ $counter -eq 0 ]; then
      cp $filename $hmm_file
    else
      awk '/Activity/,/ENDHMM/' $filename >> $hmm_file
    fi
    let counter+=1
  fi
done

# Embedded training
mkdir model/hmm4
mkdir model/hmm5

# 1st iter
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 1 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist2.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 2 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist3.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 3 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist4.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 4 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist5.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 5 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist6.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 6 hmmlist.txt
HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps))/all  -M model/hmm$((train_steps+1)) -p 0 hmmlist.txt model/hmm$((train_steps+1))/*.acc
# 2nd iter
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 1 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist2.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 2 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist3.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 3 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist4.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 4 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist5.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 5 hmmlist.txt
HERest -T 1 -v 0.00000000001  -S train-data/sessionlist6.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 6 hmmlist.txt
HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps+1))/all  -M model/hmm$((train_steps+2)) -p 0 hmmlist.txt model/hmm$((train_steps+2))/*.acc
