
# Executes the SQR for the run control PY00144M

. pvsetenv.sh

payall2.sh py00144m.sh cehpypy3 ceh.in 
RC=$?

if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv00144m.ksh cehpypy3, ReturnCode: $RC"
        echo $ERRTXT
fi

exit $RC
