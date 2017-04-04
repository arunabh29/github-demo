
for each in `ls -ld * | awk '{print $9}'` ;
do

cd /vob/dispatch/$each

for dir in `find . -type d | sort -r` ;
do
echo "All files inside this directory will be removed: " $dir
cd /vob/dispatch/$each/$dir/
# ls -al | awk '{print $9}'
cleartool rmelem -f *
done

done