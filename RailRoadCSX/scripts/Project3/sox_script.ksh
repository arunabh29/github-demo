arr=`ls -al | awk '{print $9}' | tail -n +4`
cgh_set=""
for k in "${arr[@]}" ;
do
echo "$k"
cgh_set=${cgh_set}"$k";
done

echo $cgh_set