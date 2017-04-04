filecount=0
gloc=0
diskspace=`du -sh`
for file in `find . -type f` ;
do
loc=`cat "$file" | wc -l`
## echo LINES OF CODE = "$loc"
gloc=$(($gloc+$loc))
filecount=$(($filecount+1))
done
echo "Total lines of code in the view " $gloc
echo "Total files in the view " $filecount
echo "Total diskspace used by view is " $diskspace