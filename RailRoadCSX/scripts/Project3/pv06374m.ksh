
#      CHECK PARM FILE NAMES IN BOTH PAYALL2

# Input for TTG combined T&E/Nonops Time Feed
#############################################
# Set Environment Variables
. pvsetenv.sh
#############################################
# Remove Previous Runs Output
#############################################
rm -r $PSDATOUT/csxpy2.l*
rm -r $PSDATOUT/csxpy2a.l*
#############################################
# Executes the csxpy2.sqr program

payall2.sh pv06374m.sh csxpy2 ceh.in 
RC=$?
#
if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv06374m.sh csxpy2, ReturnCode: $RC"
        echo $ERRTXT |tee ${PSLOG}/pv06374m_$$.log
        echo "Return Code is $RC"| tee -a  ${PSLOG}/pv06374m_$$.log        
        exit $RC
fi
##################################################
# Create " **** No Data ****" if files don't exist
##################################################
#
if [ ! -a $PSDATOUT/csxpy2.lis ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.lis
fi

if [ ! -a $PSDATOUT/csxpy2.l01 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l01
fi

if [ ! -a $PSDATOUT/csxpy2.l02 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l02
fi

if [ ! -a $PSDATOUT/csxpy2.l03 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l03
fi

if [ ! -a $PSDATOUT/csxpy2.l04 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l04
fi

if [ ! -a $PSDATOUT/csxpy2.l05 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l05
fi

if [ ! -a $PSDATOUT/csxpy2.l06 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l06
fi

if [ ! -a $PSDATOUT/csxpy2.l07 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l07
fi

if [ ! -a $PSDATOUT/csxpy2.l08 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l08
fi

if [ ! -a $PSDATOUT/csxpy2.l09 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l09
fi

if [ ! -a $PSDATOUT/csxpy2.l10 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2.l10
fi
#
#############################################
# Executes the csxpy2a.sqr program

payall2.sh pv063742.sh csxpy2a ceh.in 
RC=$?
#
if [ $RC -ne 0 ]
then
        ERRTXT="ERROR IN PROGRAM pv063742.sh csxpy2a, ReturnCode: $RC"
        echo $ERRTXT | tee ${PSLOG}/pv06374m_$$.log
        echo "Return Code is $RC " | tee -a ${PSLOG}/pv06374m_$$.log        
fi
##################################################
# Create " **** No Data ****" if files don't exist
##################################################
#
if [ ! -a $PSDATOUT/csxpy2a.lis ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.lis
fi

if [ ! -a $PSDATOUT/csxpy2a.l01 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l01
fi

if [ ! -a $PSDATOUT/csxpy2a.l02 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l02
fi

if [ ! -a $PSDATOUT/csxpy2a.l03 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l03
fi

if [ ! -a $PSDATOUT/csxpy2a.l04 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l04
fi

if [ ! -a $PSDATOUT/csxpy2a.l05 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l05
fi

if [ ! -a $PSDATOUT/csxpy2a.l06 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l06
fi

if [ ! -a $PSDATOUT/csxpy2a.l07 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l07
fi

if [ ! -a $PSDATOUT/csxpy2a.l08 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l08
fi

if [ ! -a $PSDATOUT/csxpy2a.l09 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l09
fi

if [ ! -a $PSDATOUT/csxpy2a.l10 ]
then
   echo " **** No Data ****" > $PSDATOUT/csxpy2a.l10
fi
#

lp -d hr01 $PSDATOUT/csxpy2a.lis
lp -d hr01 $PSDATOUT/csxpy2a.l01
lp -d hr01 $PSDATOUT/csxpy2a.l02
lp -d hr01 $PSDATOUT/csxpy2a.l03
lp -d hr01 $PSDATOUT/csxpy2a.l04
lp -d hr01 $PSDATOUT/csxpy2a.l05
lp -d hr01 $PSDATOUT/csxpy2a.l06
lp -d hr01 $PSDATOUT/csxpy2a.l07
lp -d hr01 $PSDATOUT/csxpy2a.l08
lp -d hr01 $PSDATOUT/csxpy2a.l09
lp -d hr01 $PSDATOUT/csxpy2a.l10
lp -d hr01 $PSDATOUT/csxpy2.lis
lp -d hr01 $PSDATOUT/csxpy2.l01
lp -d hr01 $PSDATOUT/csxpy2.l02
lp -d hr01 $PSDATOUT/csxpy2.l03
lp -d hr01 $PSDATOUT/csxpy2.l04
lp -d hr01 $PSDATOUT/csxpy2.l05
lp -d hr01 $PSDATOUT/csxpy2.l06
lp -d hr01 $PSDATOUT/csxpy2.l07
lp -d hr01 $PSDATOUT/csxpy2.l08
lp -d hr01 $PSDATOUT/csxpy2.l09
lp -d hr01 $PSDATOUT/csxpy2.l10
exit $RC
