protofile='hmmproto_5_50_308'

# 35
activities=(404520 404517 408512 406516 406517 404516 406520 406505 404505 406519 404519 406511 404511 406508 404508 407521 405506)
# 18
#activities=(406519 404519 406511 404511 406508 404508)
# 30
#activities=(406505 404505 405506)
# 25
#activities=(408512)
#activities=(0)

#activities=(406519 404519 406511 404511 406508 404508 408512)
#activities=(404520 404517 408512)
#404511 407521 
hmm_prefix="Activity"

for i in "${activities[@]}"
do
  cp $protofile $hmm_prefix$i
  sed -i -e "s/proto/$hmm_prefix$i/g" $hmm_prefix$i
done
