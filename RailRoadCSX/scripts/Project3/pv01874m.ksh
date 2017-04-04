. hrpd

echo "pv01874m.sh Monthly SeaLand L Run........"

DestFile="/home/psoft/tst.in"

DestFile1="/home/psoft/tst1.in"

DestFile2="/home/psoft/tst2.in"

DestFile3="/home/psoft/tst3.in"
DestFile4="/home/psoft/hdr.in"

DestFile5="/home/psoft/hold.in"

DestFile6="/home/psoft/cycle.in"

DestFile7="/home/psoft/yesno.in"

DestFile8="/home/psoft/direct.in"
DestFile9="/home/psoft/vendext.in"
DestFileV="/home/psoft/vendload.in"

PFIX='/home/psoft/A'
PREFIX='A'

export TempVar

echo "PREFIX IS: $PREFIX"

#echo "oracle_SID is " ${ORACLE_SID}

OutputFile=${PFIX}.in

#cp ${OutputFile} ${DestFile}
echo ${OutputFile} ${DestFile}...
echo > ${OutputFile}
cat  ${OutputFile}

print " just before get.... "
print 'prefix is ' $PREFIX

echo   ${ORACLE_UID}/${ORACLE_PID}@${ORACLE_SID} 

TempVar=`sqlplus -s ${ORACLE_UID}/${ORACLE_PID}@${ORACLE_SID} <<EndSQL_1

set heading off ;

spool ${OutputFile} ;

select 
	csx_run_prefix || LTRIM(TO_CHAR(csx_run_cycle,'00')) 
FROM
	sysadm.ps_csx_batch_run
WHERE
	csx_run_PREFIX = '${PREFIX}' ;

spool off;

quit;

EndSQL_1`

print 'temp var ' $TempVar

echo ${TempVar} > $DestFile5

cat  /home/psoft/hold.in |&

while read -p line
do
     RUN_NAME=`echo ${line} | awk -F, '{print ($1)}'`
     echo 'run name is ' $RUN_NAME
done


echo "Temp Var is1:["$TempVar"]"
print "run name ["$RUN_NAME"]"
   
Enddt=`sqlplus -s ${ORACLE_UID}/${ORACLE_PID}@${ORACLE_SID} <<EndSQL_2

set heading off ;

spool ${OutputFile} ;

select 
	DISTINCT(pay_end_dt) 
FROM
	sysadm.ps_pay_calendar
WHERE
	Run_ID = '${RUN_NAME}' ;

spool off;

quit;

EndSQL_2`

print $Enddt

Bngdt=`sqlplus -s ${ORACLE_UID}/${ORACLE_PID}@${ORACLE_SID} <<EndSQL_2

set heading off ;

spool ${OutputFile} ;

select 
	DISTINCT(pay_begin_dt)
FROM
	sysadm.ps_pay_calendar
WHERE
	Run_ID = '${RUN_NAME}' ;

spool off;

quit;


EndSQL_3`

### get Vendor run id

VendRunid=`sqlplus -s ${ORACLE_UID}/${ORACLE_PID}@${ORACLE_SID} <<EndSQL_4

set heading off ;

spool ${OutputFile} ;

select 
	csx_run_prefix || LTRIM(TO_CHAR(csx_run_cycle,'00')) 
FROM
	sysadm.ps_csx_batch_run
WHERE
	csx_run_PREFIX = 'V' ;

spool off;

quit;

EndSQL_4`

echo "Temp Var is: "${TempVar}
echo "Enddt Var is: "${Enddt}
echo "Bngdt Var is: "${Bngdt}
echo $PREFIX
echo "Vendor runid is: "${VendRunid}


# first format for calc/confirm
cp ${OutputFile} ${DestFile}
# second format for reports
#cp ${OutputFile} ${DestFile1}
#########################################
echo '' > ${DestFile1}
echo ${TempVar} >> ${DestFile1}
echo 'O' >> ${DestFile1}
echo 'Y' >> ${DestFile1}
echo '' >> ${DestFile1}
echo '' >> ${DestFile1}
echo 'x' >> ${DestFile1}
#########################################
echo '' > ${DestFile8}
echo ${TempVar} >> ${DestFile8}
echo 'O' >> ${DestFile8}
echo 'Y' >> ${DestFile8}
echo '' >> ${DestFile8}
echo '' >> ${DestFile8}
echo 'PSI' >> ${DestFile8}
echo '' >> ${DestFile8}
echo ${TempVar} > ${DestFile4}
#########################################
echo '' > ${DestFile6}
echo 'O' > ${DestFile6}

######    create parm file for Vendor Extract (csxpy004)

echo '' > ${DestFile9}
echo ${TempVar} >> ${DestFile9}
echo 'O' >> ${DestFile9}
echo 'Y' >> ${DestFile9}
echo ${VendRunid} >> ${DestFile9}
echo '' >> ${DestFile9}
echo '' >> ${DestFile9}
echo 'x' >> ${DestFile9}

######    create parm file for Vendor Load (csxpy04a)

echo '' > ${DestFileV}
echo ${VendRunid} >> ${DestFileV}
echo 'O' >> ${DestFileV}
echo 'Y' >> ${DestFileV}
echo '' >> ${DestFileV}
echo '' >> ${DestFileV}
echo 'x' >> ${DestFileV}

# echo "Run complete for prefix ${PREFIX}"

echo 'Y' > ${DestFile7}

exit 0
