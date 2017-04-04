

# Executes the SQR for the run control PV01324M

. pvsetenv.sh
payall2.sh pv01324m.sh csxpy007 ceh.in
RC=$?
#
if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv01324m.sh csxpy007, ReturnCode: $RC"
        echo $ERRTXT
fi

##############################################
exit $RC
