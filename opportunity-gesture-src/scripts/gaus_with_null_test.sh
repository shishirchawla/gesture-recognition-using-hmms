#!/bin/bash

### CONFIG
# try all values in the range gaus_start to gaus_end
gaus_start=10
gaus_end=50
null_gaus_start=10
null_gaus_end=30

activity_gaus=49

# currently only 3, 5, and 7 are the supported number of states
num_states=5
null_num_states=3

# feature vector size
vector_size=308
### CONFIG END

### DO NOT CHANGE ANYTHING BEYOND THIS POINT

# create prototype for the defined config
cd ..

for null_gaus in `seq $null_gaus_start $null_gaus_end`;
do

  # create null hmm prototype
  cd model/proto

  python generate_hmm_prototype.py $null_num_states $null_gaus $vector_size

  # replace proto file with the newly generated definition
  sed "s/hmmproto.*\'/hmmproto_${null_num_states}_${null_gaus}_${vector_size}\'/" -i createnullhmmprototype.sh
  ./createnullhmmprototype.sh

  cd ../../

  for activity_gaus in `seq $gaus_start $gaus_end`;
  do
    echo "Testing with states=${num_states} activity_gaus=${activity_gaus} null_gaus=${null_gaus}"
    echo "Testing with states=${num_states} activity_gaus=${activity_gaus} null_gaus=${null_gaus}" >> scripts/gaus_test.txt

    # generate activity prototype
    cd model/proto

    python generate_hmm_prototype.py $num_states $activity_gaus $vector_size

    # replace proto file with the newly generated definition
    sed "s/hmmproto.*\'/hmmproto_${num_states}_${activity_gaus}_${vector_size}\'/" -i createhmmprototypes.sh
    ./createhmmprototypes.sh

    cd ../../

    # train
    ./train.sh

    # test
    ./session-test.sh

    cd pred && ./pred.sh

    cd ..

    python results.py pred/pred.txt groundtruth/truth.txt >> scripts/gaus_test.txt
    echo >> scripts/gaus_test.txt
    echo >> scripts/gaus_test.txt
  done
done

