for stream in `./cleartool lsstream -invob vob:/vob/csx_tsi_fmlm | grep "01_int" | awk '{print $2}'` ;
do

vobname="`echo "$stream" | cut -c4- | rev | cut -c 7- | rev`"
vobpath=`./cleartool desc vob:/vob/"$vobname" | grep "VOB storage global pathname" | awk '{print $5}' | cut -c2- | rev | cut -c 2- | rev`

echo "PROCESSING THE VOB " $vobname " NOW"
echo "THE VOBPATH is:  " $vobpath

for addlgroup in `./cleartool desc vob:/vob/"$vobname" | grep "group csxt.ad.csx.com" | tail -n +2 | cut -c27- | grep -v clearcas` ;
  do
   ./cleartool protectvob -f -delete_group "$addlgroup" "$vobpath"
  done

echo "DONE PROCESSING THE VOB " $vobname

echo "##############################################################################################"
echo "##############################################################################################"
echo "##############################################################################################"
echo "                                                                                              "
echo "                                                                                              "

done