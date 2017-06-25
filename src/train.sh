#!/bin/bash

train_steps=3
num_subjects=8
activities=(1 2 3 4 5 6 Other)

for s in $(seq 1 $num_subjects)
do
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
    HInit -A -D -w 1.0 -T 1 -S subject10$s.dat-data/trainlist_act_$i.txt -M model/hmm0 model/proto/Activity$i

    echo "Training HMMS..."
    for j in $(seq 1 $train_steps)
    do
      HRest -A -D -T 1 -S subject10$s.dat-data/trainlist_act_$i.txt -M model/hmm$j -H model/hmm$((j-1))/Activity$i Activity$i
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
        #touch $hmm_file
        cp $filename $hmm_file
      else
        awk '/Activity/,/ENDHMM/' $filename >> $hmm_file
      fi
      let counter+=1
    fi
  done

  echo 'Training complete!'

  # Classify
  HVite -A -D -T 1 -w net.slf -H model/hmm$train_steps/all -i reco.mlf -S subject10$s.dat-data/classifylist.txt def/dict.txt hmmlist.txt
  awk 'NR%3==0' reco.mlf | awk '{print $3}' > results.txt
  #sed -n 's/^.*\(act_[0-9]*\).*$/\1/p' testtargetlist.txt | sed -e 's/act_/Activity/g' > original.txt
  #sed -n 's/^.*_act_\([0-9]*\).*$/\1/p' testtargetlist.txt | grep --color=never -o '[0-9]\+' | awk '$1>6{$1="Other"}1' | awk '{print "Activity"$0}' > original.txt
  sed -n 's/^.*_act_\([0-9]*\).*$/\1/p' subject10$s.dat-data/testlist.txt | grep --color=never -o '[0-9]\+' | awk '$1>6{$1="Other"}1' | awk '{print "Activity"$0}' > original.txt
  python accuracy.py >> accgaus.txt
done

