
# Executes the SQR for the run control PV06244M

. pvsetenv.sh

payall2.sh pv06244m.ksh csxpy89v ceh.in

RC=$?

if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv06244m.ksh csxpy89v, ReturnCode: $RC"
        echo $ERRTXT
fi

exit $RC
