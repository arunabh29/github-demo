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

# test case user - s0854 - not a Jira user returns null

# To get the JSON response you must be logged in.

import json
import urllib2
import requests
import sys
import requests.packages.urllib3
import os
import commands

requests.packages.urllib3.disable_warnings()



username = "z_devops"
password = "N2t92en$"

url = 'https://git.csx.com/repos?visibility=public'
repo_info=requests.get(url, auth=(username, password)).content
str = (repo_info[1:-1])
print (repo_info)

'''
Converting this string into a dictionary
status1, str1 = commands.getstatusoutput('curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET  https://git.csx.com/users/z_devops/repos?per_page=5 > /home/t8054/Arunabh_sandbox/python_scripts/abc.txt ')
status1, str1 = commands.getstatusoutput('curl -s -u z_devops:N2t92en$ -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET https://bitbucket.csx.com/repos?visibility=public > /home/t8054/Arunabh_sandbox/python_scripts/abc.txt ')
status1, str1 = commands.getstatusoutput('curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET https://git.csx.com/repos?visibility=public > /home/t8054/Arunabh_sandbox/python_scripts/abc.txt ')
status2, str2 = commands.getstatusoutput(' cat /home/t8054/Arunabh_sandbox/python_scripts/abc.txt | tail -n +16 ')
print (str2)


my_repo_dict=json.loads(str)



print (my_repo_dict['isLastPage'])
print (my_repo_dict['limit'])
print (my_repo_dict['nextPageStart'])
print (my_repo_dict['size'])
print (my_repo_dict['start'])


# print (my_repo_dict['values'][3])

for e1 in my_repo_dict['values']:
    for e2 in e1['links']['clone']:
        if (e2['name'] == "ssh"):
            print (e2['href'])

'''