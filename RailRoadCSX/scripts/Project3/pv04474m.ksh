
# Input for User Trans ZT 

# Set Environment Variables
. pvsetenv.sh

# Remove Previous Runs Output

rm -r $PSDATOUT/csxpy113.l*

# Executes the SQR for the run control PV04474M

payall2.sh pv04474m.sh csxpy113 ceh.in
RC=$?
#
if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv04474m.sh, ReturnCode: $RC"
        echo $ERRTXT
fi

# Check Report files to prevent ftp from bombing

#
if [ -a $PSDATOUT/csxpy113.lis ]
then
   echo " Report 1 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.lis
fi
#
if [ -a $PSDATOUT/csxpy113.l01 ]
then
   echo " Report 2 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l01
fi
#
if [ -a $PSDATOUT/csxpy113.l02 ]
then
   echo " Report 3 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l02
fi
#
if [ -a $PSDATOUT/csxpy113.l03 ]
then
   echo " Report 4 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l03
fi
#
if [ -a $PSDATOUT/csxpy113.l04 ]
then
   echo " Report 5 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l04
fi
#
if [ -a $PSDATOUT/csxpy113.l05 ]
then
   echo " Report 6 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l05
fi
#
if [ -a $PSDATOUT/csxpy113.l06 ]
then
   echo " Report 7 was Created"
else
   echo " **** No Data ****" > $PSDATOUT/csxpy113.l06
fi
#
##################################################
#
exit $RC
