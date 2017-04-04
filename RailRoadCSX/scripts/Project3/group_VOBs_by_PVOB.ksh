for eachucmvob in `cleartool lsvob | grep "ucmvob" | awk '{print $2}' | cut -c 6-` ;
do
for stream in `cleartool lsstream -invob vob:/vob/"$eachucmvob" | grep "01_int" | awk '{print $2}'` ;
do
vobname="`echo "$stream" | cut -c4- | rev | cut -c 7- | rev`"
echo $vobname ----- "$eachucmvob" >> /home/f8164/reports/application_by_pvob.txt
done
echo -----------------------------------
echo -----------------------------------
echo End of PVOB: $eachucmvob
echo -----------------------------------
echo -----------------------------------
done