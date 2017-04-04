################################################################################################
################################################################################################

# Script Name    : getEmail-ID.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 02/17/2016
# Description    : This python script uses the Jira Rest API to get user details from Jira as a JSON object and processes it. (currently displays the email-id)
# Usage          : Pass RACF as a parameter to this python script.
# Modifications  :
# Ver	Name	   : 1.0

################################################################################################
################################################################################################

# test case user - s0854 - not a Jira user returns null

# To get the JSON response you must be logged in.

import json
import requests
import sys
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

racf_id=sys.argv[1]
username = "z_devops"
password = "N2t92en$"
url = 'https://jira.csx.com/rest/api/latest/user/search?username=%s' %racf_id
user_info=requests.get(url, auth=(username, password)).content
str = (user_info[1:-1])
# Converting this string into a dictionary
my_dict=json.loads(str)

if (str==""):
	print ("Arunabh_Chowdhury@csx.com")
else:
	print (my_dict['emailAddress'])
