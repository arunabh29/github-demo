##############################################################
# Executes the SQR for the run control PV07764M
############################################################## 
##############################################################
. pvsetenv.sh
##############################################################
echo $PSCNTL
export DestFile1=$PSCNTL/tst1.in 
##############################################################
echo ''        > ${DestFile1}
read LINE < $PSCNTL1/off.in
echo $LINE | awk '{print $1}' | read RUN_ID
echo $RUN_ID >> ${DestFile1}
echo 'F'      >> ${DestFile1}
echo 'Y'      >> ${DestFile1}
echo ''       >> ${DestFile1}
echo ''       >> ${DestFile1}
echo ''       >> ${DestFile1}
echo ''       >> ${DestFile1}
echo ''       >> ${DestFile1}
echo ''       >> ${DestFile1}
