# Author: Arunabh Chowdhury #
for eachucmvob in `cat /home/t8054/Arunabh_sandbox/Clearcase_Utils/pvob_list.txt` ;
do
for eachvob in `cleartool desc vob:/vob/"$eachucmvob" | grep "AdminVOB <-" | cut -c26-` ;
do
ucmproj=`cleartool lsproj -invob vob:/vob/"$eachucmvob" | grep "$eachvob"01 | cut -d' ' -f3`
if [ ! -z "$ucmproj" ]; then
echo $ucmproj"_int" $eachucmvob $eachvob >> /home/t8054/Arunabh_sandbox/Clearcase_Utils/LIST_OF_ALL-STREAMS.txt
fi
done
done