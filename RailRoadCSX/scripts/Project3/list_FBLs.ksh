# Lists foundation baselines for all integration streams in the PVOB csx_shipcsx

echo "" > /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
count=0

for int_stream in `cleartool lsstream -invob vob:/vob/csx_shipcsx | grep "01_int" | awk '{print $2}'` ;
do

rec=`cleartool lsstream -l stream:$int_stream@/vob/csx_shipcsx | sed -n '/foundation/,/recommended/p' | grep -v baselines`
check=`echo $rec | grep "(non-modifiable)"`
if [ ! -z "$check"  ]
 then
    count=$(($count+1))
    echo "########################## STREAM: $int_stream ######################################" >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
    echo "COMPONENT/S:" >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
    echo $rec >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
    echo "#####################################################################################" >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
    echo " " >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt

 
 else
    echo
    
fi



done

echo " " >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt
echo $count "applications have the common component" >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/list_common_comp-streams.txt