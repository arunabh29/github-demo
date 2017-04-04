for ucmvob in `cat /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/LOC_2016/pvob_list_2016.txt` ;
do
for stream in `cleartool lsstream -invob vob:/vob/"$ucmvob" | grep "01_int" | awk '{print $2}'` ;
do
vobname="`echo "$stream" | cut -c4- | rev | cut -c 7- | rev`"
echo $vobname $stream  $ucmvob >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/LOC_2016/List_by_CC_Command_04262016.txt
done
done
