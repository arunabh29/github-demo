# pv06694m.ksh  csxpy070  ProBusiness periodic interface

# Set Environment Variables

. pvsetenv.sh

# Executes the csxpy070.sqr program

payall2.sh pv06694m.sh csxpy070 csxpy070.in 

RC=$?

if [ $RC -eq 0 ]
then

#  get the current run id
   RUNID=SEA

#  copy csxpy070 output file to generic name
#  for FTP to rs017 by pv12504m.sh

   cp $PSDATOUT/PVP.CSXPY070.F01.$RUNID \
      $PSDATOUT/PVP.CSXPY070.F01

#  zip the periodic file

   rm $PSDATOUT/PVP.CSXPY070.F01.$RUNID.zip

   pkzip $PSDATOUT/PVP.CSXPY070.F01.$RUNID.zip \
         $PSDATOUT/PVP.CSXPY070.F01.$RUNID \
         $PSDATOUT/csxpy070.lis

   ###uuencode $PSDATOUT/PVP.CSXPY070.F01.$RUNID.zip PVP.CSXPY070.F01.$RUNID.zip |

   ###mailx -s "CSX periodic file for runid $RUNID" \
     ###    -r PayrollServices@csx.com \
      ###   taxfile@probusiness.com mroth@probusiness.com

   ###echo '' |
   ###mailx -s "CSX periodic file for runid $RUNID has been e-mailed to ProBusiness" \
   ###      PayrollServices@csx.com

#  remove the zip file

   ###rm $PSDATOUT/PVP.CSXPY070.F01.$RUNID.zip

else
   ERRTXT="ERROR IN PROGRAM pv06694m.sh csxpy070, ReturnCode: $RC"
   echo $ERRTXT |tee ${PSLOG}/pv06694m_$$.log
   echo "Return Code is $RC"| tee -a  ${PSLOG}/pv06694m_$$.log        
fi

exit $RC
