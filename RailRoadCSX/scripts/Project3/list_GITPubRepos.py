################################################################################################
################################################################################################

# Script Name    : list_GITPubRepos.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 07/05/2016
# Description    : This python script lists all public GIT repo-urls
# Usage          : Run standalone
# Modifications  :
# Ver	Name	   : 1.0

################################################################################################
################################################################################################


# To get the JSON response you must be logged in.

import json
import requests
import commands
import os

requests.packages.urllib3.disable_warnings()

status1, str1 = commands.getstatusoutput('curl -s -u z_devops:N2t92en$ -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET https://git.csx.com/repos?limit=1000 > /home/t8054/Arunabh_sandbox/python_scripts/abc.txt ')
# status1, str1 = commands.getstatusoutput('curl -s -u <racf>:<pwd> -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET https://git.csx.com/repos?limit=1000 > /home/t8054/Arunabh_sandbox/python_scripts/abc.txt ')
status2, str2 = commands.getstatusoutput(' cat /home/t8054/Arunabh_sandbox/python_scripts/abc.txt | tail -n +16 ')


# Converting this string into a dictionary
my_repo_dict=json.loads(str2)


'''
print (my_repo_dict['isLastPage'])
print (my_repo_dict['limit'])
# print (my_repo_dict['nextPageStart'])
print (my_repo_dict['size'])
print (my_repo_dict['start'])

'''


# print (my_repo_dict['values'][3])

for e1 in my_repo_dict['values']:
    # print (e1['name'].lower())
    for e2 in e1['links']['clone']:
        if (e2['name'] == "http"):
            # print (e1['name'].lower())            
            print (e2['href'])
	     # print ("*****************************************************")


