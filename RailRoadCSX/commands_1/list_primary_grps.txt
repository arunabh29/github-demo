for eachvob in `cat /home/t8054/Arunabh_sandbox/Clearcase_Utils/vobincsx-coldfusion.txt` ;
do
pg=`cleartool desc vob:/vob/outplace | grep "group csxt.ad.csx.com" | cut -c27-`
echo $pg
done
