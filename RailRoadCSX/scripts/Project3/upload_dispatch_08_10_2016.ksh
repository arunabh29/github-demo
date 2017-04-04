cd /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/Dispatch_Kit_Upload/dispatch_2015
for each in `ls -ld * | awk '{print $9}'` ;
do

blname=$each

echo "Processing this kit now: "$blname

clearfsimport -recurse $each /vob/dispatch/ > /home/t8054/Arunabh_sandbox/dispatch/dispatch_upload_logs_VC15_P000_2015_09012016.txt
# clearfsimport -preview -recurse $each /vob/dispatch/

sleep 2

cleartool mkbl -identical -view zz2_dp_P000_2015_dev -full $blname
echo "Baseline: "$blname "created"

sleep 2

done