#!/bin/bash

awk '{print $NF}' ../htkdata/S2-ADL4.dat_completesession.rec > pred-s2adl4.txt
for i in `seq 1 5`;
do
  tail pred-s2adl4.txt -n 1 >> pred-s2adl4.txt
done
awk '{print $NF}' ../htkdata/S2-ADL5.dat_completesession.rec > pred-s2adl5.txt
for i in `seq 1 4`;
do
  tail pred-s2adl5.txt -n 1 >> pred-s2adl5.txt
done
awk '{print $NF}' ../htkdata/S3-ADL4.dat_completesession.rec > pred-s3adl4.txt
for i in `seq 1 5`;
do
  tail pred-s3adl4.txt -n 1 >> pred-s3adl4.txt
done
awk '{print $NF}' ../htkdata/S3-ADL5.dat_completesession.rec > pred-s3adl5.txt
for i in `seq 1 4`;
do
  tail pred-s3adl5.txt -n 1 >> pred-s3adl5.txt
done

#printf "Activity0\nActivity0\nActivity0\nActivity0\nActivity0\n" >> pred-s2adl4.txt
#printf "Activity0\nActivity0\nActivity0\nActivity0\n" >> pred-s2adl5.txt
#printf "Activity0\nActivity0\nActivity0\nActivity0\nActivity0\n" >> pred-s3adl4.txt
#printf "Activity0\nActivity0\nActivity0\nActivity0\n" >> pred-s3adl5.txt

cat pred-s2adl4.txt > pred.txt
cat pred-s2adl5.txt >> pred.txt
cat pred-s3adl4.txt >> pred.txt
cat pred-s3adl5.txt >> pred.txt
