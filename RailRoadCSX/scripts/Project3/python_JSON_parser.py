################################################################################################
################################################################################################

# Script Name    : python_JSON_parser.py
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

racf_id=sys.argv[1]

username = "z_devops"
password = "N2t92en$"
# url = 'https://jira.csx.com/rest/api/latest/user/search?username=b3601'
url = 'https://jira.csx.com/rest/api/latest/user/search?username=%s' %racf_id

user_info=requests.get(url, auth=(username, password)).content

print ("\n")
print ("****************  PRINTING JSON OBJECT *************************************")
print (user_info)

# user_info is a JSON object ( a string enclosed within []) so removing first and last chars.
str = (user_info[1:-1])
print ("\n")
print ("****************  PRINTING STRING *************************************")
print (str)

# Converting this string into a dictionary
my_dict=json.loads(str)


print ("\n")
print ("****************  PRINTING ENTIRE DICTIONARY IN THIS SECTION *************************************")
print (my_dict)
print ("****************  PRINTING ENTIRE DICTIONARY IN THIS SECTION *************************************")

print ("\n")
print ("****************  EMAIL ADDRESS *************************************")
print (my_dict['emailAddress'])
print ("***********************************************************************\n")

print ("****************  DISPLAY NAME *************************************")
print (my_dict['displayName'])
print ("***********************************************************************\n")

print ("****************  TIME ZONE *************************************")
print (my_dict['timeZone'])
print ("***********************************************************************\n")

print ("****************  ACTIVE ? *************************************")
print (my_dict['active'])
print ("***********************************************************************\n")

print ("****************  LOCALE *************************************")
print (my_dict['locale'])
