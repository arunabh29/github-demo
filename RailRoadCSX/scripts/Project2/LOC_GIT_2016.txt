# find all files recursively that do NOT have the below extensions
# find . -type f ! -regex  '.*\.\(git\|png\|jpg\|swf\|gif\|pdf\|swf\|log\)'

filecount=0
gloc=0
for file in `find . -type f ! -regex  '.*\.\(git\|png\|jpg\|swf\|gif\|pdf\|swf\|log\)'` ;
do
loc=`cat "$file" | wc -l`
## echo LINES OF CODE = "$loc"
gloc=$(($gloc+$loc))
filecount=$(($filecount+1))
done
echo "Total lines of code in the repo: " $gloc
echo "Total files in the repo excluding .git, .png, .jpg, .swf, .gif, .pdf, .swf and .log files: " $filecount
echo "**************************************************************************************************"
echo "**************************************************************************************************"