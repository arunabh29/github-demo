for each in `cleartool lsvob | grep -v "(ucmvob)" | awk '{print $2}'` ;
do
c1=`cleartool lshis -l vob:/$each | head -1`
str=$c1"   "$each
echo $str >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/VOB_Modify_Hist/VOBs_Last_Update_Dates_list.txt
done