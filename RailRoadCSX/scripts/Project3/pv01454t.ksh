
# Executes the SQR for the run control PY01454M

. pvsetenv.sh
payall2.sh py01454m.sh cehpy013 blank.in
RC=$?

if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv01454m.sh cehpy013, ReturnCode: $RC"
        echo $ERRTXT
fi

exit $RC
