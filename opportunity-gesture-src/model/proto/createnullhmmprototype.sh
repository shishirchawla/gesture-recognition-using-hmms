protofile='hmmproto_3_30_308'

activities=(0)

hmm_prefix="Activity"

for i in "${activities[@]}"
do
  cp $protofile $hmm_prefix$i
  sed -i -e "s/proto/$hmm_prefix$i/g" $hmm_prefix$i
done
