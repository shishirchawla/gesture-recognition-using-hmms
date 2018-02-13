protofile='proto3s_10_847'
#protofile='proto5s_10_847'
#activities=(406516 406517 404516 404517 406520 404520 406505 404505 406519 404519 406511 404511 406508 404508 408512 407521 405506)
activities=(404520 404517 408512)
hmm_prefix="Activity"

for i in "${activities[@]}"
do
  cp $protofile $hmm_prefix$i
  sed -i -e "s/proto/$hmm_prefix$i/g" $hmm_prefix$i
done
