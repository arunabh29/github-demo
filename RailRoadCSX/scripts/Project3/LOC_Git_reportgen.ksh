for each in `cat /home/t8054/Arunabh_sandbox/python_scripts/repo_list.txt` ;
do

repo_url=`echo $each`

echo "Cloning the repository: " $repo_url
echo "*********************************************************"

cd /home/t8054/Arunabh_sandbox/test_dir
git clone $repo_url
cd `ls`
echo "Inside the repo directory: " `pwd`

ts=`echo date +"%m%d%Y_%H%M%S"`

echo "Repository: " $repo_url >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/LOC_2016/LOC_GIT_$ts_Report.txt
/home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/LOC_2016/LOC_GIT_2016.ksh >> /home/t8054/Arunabh_sandbox/shell_scripts/Clearcase_Utils/LOC_2016/LOC_GIT_$ts_Report.txt

echo "Deleting the repo directory: " `pwd`
cd ../
rm -rf *

done