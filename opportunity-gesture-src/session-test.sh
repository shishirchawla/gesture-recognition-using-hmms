#!/bin/bash

train_steps=3
activities=(0 406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)

# Classify
HVite -A -D -T 1 -w wdnet -H model/hmm$((train_steps+2))/all -i hvite.mlf -S test-data/sessionlist.txt def/dict.txt hmmlist.txt > reco.mlf
#HVite -A -D -T 1 -m -f -s 40.0 -p -100.0 -w wdnet -H model/hmm$((train_steps))/all -i hvite.mlf -S test-data/sessionlist.txt def/dict.txt hmmlist.txt > reco.mlf
#awk '/mfcc$/{nr[NR+1]}; NR in nr' reco.mlf | awk '{print $1}' > results-session.txt
#/nethome/schawla32/test/htk/HTKLVRec/HDecode -H model/hmm$((train_steps))/all -S test-data/sessionlist.txt \
#          -t 220.0 220.0 \
#          -i hvite2.mlf -w wdnet \
#          -z lat \
#          -p -100.0 -s 40.0 def/dict.txt hmmlist.txt

# parse HTK to human
python parse_htk_to_human.py hvite.mlf


# NEW EMBEDDED TRAINING (TODO ERROR [+7031]  transition mat sum)
#HERest -S train-data/sessionlist.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) hmmlist.txt
# train in parts
# http://disfruta555.blogspot.ca/2015/04/trouble-shooting-htk-error-7031.html

#rm -rf model/hmm4/
#rm -rf model/hmm5/
#rm -rf model/hmm6/
#rm -rf model/hmm7/
#rm -rf model/hmm8/
#
## 1st iter
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 1 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist2.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 2 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist3.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 3 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist4.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 4 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist5.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 5 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist6.txt -H model/hmm$((train_steps))/all -M model/hmm$((train_steps+1)) -p 6 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps))/all  -M model/hmm$((train_steps+1)) -p 0 hmmlist.txt model/hmm$((train_steps+1))/*.acc
## 2nd iter
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 1 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist2.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 2 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist3.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 3 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist4.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 4 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist5.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 5 hmmlist.txt
#HERest -T 1 -v 0.00000000001  -S train-data/sessionlist6.txt -H model/hmm$((train_steps+1))/all -M model/hmm$((train_steps+2)) -p 6 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps+1))/all  -M model/hmm$((train_steps+2)) -p 0 hmmlist.txt model/hmm$((train_steps+2))/*.acc
## 3rd iter
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 1 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist2.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 2 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist3.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 3 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist4.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 4 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist5.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 5 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist6.txt -H model/hmm$((train_steps+2))/all -M model/hmm$((train_steps+3)) -p 6 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps+2))/all  -M model/hmm$((train_steps+3)) -p 0 hmmlist.txt model/hmm$((train_steps+3))/*.acc
## 4th iter
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist.txt  -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 1 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist2.txt -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 2 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist3.txt -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 3 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist4.txt -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 4 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist5.txt -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 5 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist6.txt -H model/hmm$((train_steps+3))/all -M model/hmm$((train_steps+4)) -p 6 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps+3))/all  -M model/hmm$((train_steps+4)) -p 0 hmmlist.txt model/hmm$((train_steps+4))/*.acc
## 5th iter
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist.txt  -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 1 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist2.txt -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 2 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist3.txt -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 3 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist4.txt -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 4 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist5.txt -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 5 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -t 120.0 60.0 240.0 -S train-data/sessionlist6.txt -H model/hmm$((train_steps+4))/all -M model/hmm$((train_steps+5)) -p 6 hmmlist.txt
#HERest -T 1 -v 0.00000000001 -H model/hmm$((train_steps+4))/all  -M model/hmm$((train_steps+5)) -p 0 hmmlist.txt model/hmm$((train_steps+5))/*.acc

# NEW END
