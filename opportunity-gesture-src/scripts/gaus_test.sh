#!/bin/bash

### CONFIG
# try all values in the range gaus_start to gaus_end
gaus_start=20
gaus_end=50

# currently only 3, 5, and 7 are the supported number of states
num_states=5

# feature vector size
vector_size=308
### CONFIG END

### DO NOT CHANGE ANYTHING BEYOND THIS POINT

# create prototype for the defined config
cd ..

for gaus in `seq $gaus_start $gaus_end`;
do
  echo "Testing with states=${num_states} gaus=${gaus}"
  echo "Testing with states=${num_states} gaus=${gaus}" >> scripts/gaus_test.txt

  cd model/proto

  python generate_hmm_prototype.py $num_states $gaus $vector_size

  # replace proto file with the newly generated definition
  sed "s/hmmproto.*\'/hmmproto_${num_states}_${gaus}_${vector_size}\'/" -i createhmmprototypes.sh
  ./createhmmprototypes.sh

  cd ../../

  # train
  ./train.sh

  # test
  ./session-test.sh

  cd pred && ./pred.sh

  cd ..

  python results.py pred/pred.txt groundtruth/truth_withoutnull.txt >> scripts/gaus_test.txt
  echo >> scripts/gaus_test.txt
  echo >> scripts/gaus_test.txt
done

