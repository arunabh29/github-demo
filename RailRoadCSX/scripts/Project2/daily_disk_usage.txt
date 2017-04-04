cd /opt/shared/atlassian/bamboo/
echo "Disk space used by each file/folder under /opt/shared/atlassian/bamboo/: " > /home/t8054/Arunabh_sandbox/mail_tests/daily_disk_usage_EmailBody.txt
echo " " >> /home/t8054/Arunabh_sandbox/mail_tests/daily_disk_usage_EmailBody.txt
ls -al | awk '{print $9}' | tail -n +4 | xargs du -sh >> /home/t8054/Arunabh_sandbox/mail_tests/daily_disk_usage_EmailBody.txt
sleep 5
mail -s "Daily disk usage report from Bamboo prod: lnx21261" Arunabh_Chowdhury@csx.com < /home/t8054/Arunabh_sandbox/mail_tests/daily_disk_usage_EmailBody.txt