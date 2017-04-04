vobname=$1
projid=$2
pvobname=`cleartool desc vob:/vob/$vobname | grep "AdminVOB ->" | cut -c26-`


for each in `cleartool lsstream -invob vob:/vob/$pvobname | grep -e $vobname -e $projid | awk '{print $2}'` ;
do
echo "Locking Stream $each now"
cleartool lock -nusers f8164 -nc stream:$each@/vob/$pvobname
# cleartool unlock -nusers f8164 -nc stream:$each@/vob/$pvobname
echo "Done locking stream $each"
echo "#####################################"
done


echo "Done locking all streams, now locking vob"

echo "Locking the vob: $vobname now"
cleartool lock -nc vob:/vob/$vobname/
# cleartool unlock -nc vob:/vob/$vobname/
echo "Done locking the vob: $vobname"