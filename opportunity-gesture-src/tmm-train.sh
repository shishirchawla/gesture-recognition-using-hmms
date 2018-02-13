#!/bin/bash

train_data_dir='train-data'
train_steps=3
activities=(0 406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)

cp hmmlist.txt ./model/hmm$train_steps/
cp tmm.hed ./model/hmm$train_steps/

mkdir ./model/hmm$((train_steps+1))

cd ./model/hmm$train_steps/
HHEd -M ../hmm$((train_steps+1)) -H Activity0 -H Activity406516 -H Activity406517 -H Activity404516 -H Activity404517 -H Activity406520 -H Activity404520 -H Activity406505 -H Activity404505 -H Activity406519 -H Activity404519 -H Activity406511 -H Activity404511 -H Activity406508 -H Activity404508 -H Activity408512 -H Activity407521 -H Activity405506 tmm.hed hmmlist.txt

cd ../../
mkdir ./model/hmm$((train_steps+2))
for i in ${activities[@]}
do
  HRest -A -D -T 1 -S $train_data_dir/trainlist_act_$i.txt -M model/hmm$((train_steps+2)) -H model/hmm$((train_steps+1))/Activity0 -H model/hmm$((train_steps+1))/Activity$i Activity$i
  if [ $i = 0 ]; then
    cp model/hmm$((train_steps+2))/Activity$i model/hmm$((train_steps+2))/BackActivity$i
  fi
done
mv -f model/hmm$((train_steps+2))/BackActivity0 model/hmm$((train_steps+2))/Activity0

# FIXME START
mkdir ./model/hmm$((train_steps+3))
for i in ${activities[@]}
do
  HRest -A -D -T 1 -S $train_data_dir/trainlist_act_$i.txt -M model/hmm$((train_steps+3)) -H model/hmm$((train_steps+2))/Activity0 -H model/hmm$((train_steps+2))/Activity$i Activity$i
  if [ $i = 0 ]; then
    cp model/hmm$((train_steps+3))/Activity$i model/hmm$((train_steps+3))/BackActivity$i
  fi
done
mv -f model/hmm$((train_steps+3))/BackActivity0 model/hmm$((train_steps+3))/Activity0

mkdir ./model/hmm$((train_steps+4))
for i in ${activities[@]}
do
  HRest -A -D -T 1 -S $train_data_dir/trainlist_act_$i.txt -M model/hmm$((train_steps+4)) -H model/hmm$((train_steps+3))/Activity0 -H model/hmm$((train_steps+3))/Activity$i Activity$i
  if [ $i = 0 ]; then
    cp model/hmm$((train_steps+4))/Activity$i model/hmm$((train_steps+4))/BackActivity$i
  fi
done
mv -f model/hmm$((train_steps+4))/BackActivity0 model/hmm$((train_steps+4))/Activity0
# FIXME END

echo 'Tied training complete!'

# Concat hmms into one file
echo 'Compiling hmms into one file..'
hmm_file=./model/hmm$((train_steps+4))/all

rm -f $hmm_file
counter=0
for filename in ./model/hmm$((train_steps+4))/*
do
  if [ $filename != $hmm_file ] && [ $filename != "./model/hmm$((train_steps+4))/*" ]; then
    if [ $counter -eq 0 ]; then
      #touch $hmm_file
      cp $filename $hmm_file
    else
      awk '/Activity/,/ENDHMM/' $filename >> $hmm_file
    fi
    let counter+=1
  fi
done

