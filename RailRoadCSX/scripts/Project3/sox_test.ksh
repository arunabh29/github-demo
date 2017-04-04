cgh_str=""
# for each in `ls -al | awk '{print $9}' | tail -n +4` ;
for each in `find /home/t8054/Arunabh_sandbox/python_scripts/SOX -type f` ; 
do
cgh_str="\"${cgh_str}\", \"$each"
# echo $cgh_str
done

chg_set="\""`echo $cgh_str | cut -c10-`"\""

echo ------------------------------------------
echo -- Below output is from the korn script --
echo ------------------------------------------

echo $chg_set
echo ------------------------------------------
echo ------------------------------------------

echo ----- Calling python now ------
python /home/t8054/Arunabh_sandbox/python_scripts/SOX/pytest.py $chg_set