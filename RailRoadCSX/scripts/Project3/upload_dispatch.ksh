cd /opt/local/software/ccimport/dispatch/
for each in `ls -altr | grep "kit.VC" | awk '{print $9}'` ;
do
tempdir=`echo $each | grep -o -P '(?<=kit.).*(?=.gz)'`
mkdir $tempdir
chmod 777 $tempdir
tar -xvzf $each -C /opt/local/software/ccimport/dispatch/$tempdir/
chmod -R 777 /opt/local/software/ccimport/dispatch/$tempdir/*

str1=`echo $each | grep -o -P '(?<=kit.).*(?=.tar)'`
str2=`echo $each | grep -o -P '(?<=.tar).*(?=.gz)'`
blname=$str1$str2
echo $blname
cd /opt/local/software/ccimport/dispatch/$tempdir/
clearfsimport -recurse * /vob/dispatch/ >> /home/t8054/Arunabh_sandbox/dispatch/dispatch_upload_logs.txt
cleartool mkbl -identical -view zz2_dp_P0006483b_dev -full $blname
cd /opt/local/software/ccimport/dispatch/
rm -rf $tempdir
done