################################################################################################
################################################################################################

# Script Name    : createJiraIssue_latest.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 11/25/2015
# Description    : This script initiates the Jira-SM integration. It gets executed on every successful production build.
# Usage          : It is automatically triggered from inside a Bamboo build plan on a successful production build.
# Modifications  :
# Ver	Name	   : 1.0

################################################################################################
################################################################################################

import sys
import time
from jira.client import JIRA

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

################################################################################################
############  THIS SECTION CREATES JIRA ISSUE AFTER A SUCCESSFUL PRODUCTION BUILD  #############
################################################################################################


# JIRA NON-PROD LOGIN
# options={'server': 'http://lnx21256:8080'}
# jira=JIRA(options=options,basic_auth=('admin', 'admin123'))


# JIRA PROD LOGIN
# The additional login parameter " 'verify': False " is only for JIRA-PROD to get past the SSL3 certificate verification error.
# The Jira prod server's SSL certificate is probably signed by a non-standard CA.
# The python SSL library does not trust this non-standard CA.
options={'server': 'https://lnx21259.csxt.csx.com:8443', 'verify': False}
# options={'server': 'https://lnx21259.csxt.csx.com:8443'}

jira=JIRA(options=options,basic_auth=('z_devops', 'N2t92en$'))

summary_text=sys.argv[1]
description_text=sys.argv[2]
changedate_text=sys.argv[3]
build_number=sys.argv[4]

# Creating the dictionary and populating fields using command-line parameters

issue_dict = {

 'project' : { 'key': 'CM' },

 'summary' : summary_text,

 'description' : description_text,

 'issuetype' : { 'name' : 'ChangePackage' },

}

print "******************************************************"
print "Begin creating issue"
print "******************************************************"

# Creating issue using the dictionary
issue_obj= jira.create_issue(fields=issue_dict)

print "******************************************************"
print "Done creating issue: %s" % issue_obj.key
print "******************************************************"

# transitioning from Opened to Pre-Approved state
jira.transition_issue(issue_obj.key, '11')

# transitioning from Pre-Approved to Approved state
jira.transition_issue(issue_obj.key, '21')

print "******************************************************"
print "Done transitioning status for issue: %s" % issue_obj.key
print "******************************************************"

# Sleeping 5 seconds for the issue transitions to complete
time.sleep(5)


################################################################################################
###############  DONE CREATING JIRA ISSUE AFTER A SUCCESSFUL PRODUCTION BUILD  #################
################################################################################################


################################################################################################
##########  THIS SECTION CREATES THE SOAP-XML ELEMENT TREE AND POPULATES THE NODES  ############
################################################################################################

# Creating root

root=Element('soapenv:Envelope')
root.set('xmlns:max', 'http://www.ibm.com/maximo')
root.set('xmlns:soapenv', 'http://schemas.xmlsoap.org/soap/envelope/')
tree=ElementTree(root)

# Creating all child elements

soapenv_Header=Element('soapenv:Header')
soapenv_Body=Element('soapenv:Body')
max_SyncCSXRI=Element('max:SyncCSXRI')
max_CSXRISet=Element('max:CSXRISet')
max_RELEASEITEM=Element('max:RELEASEITEM')


max_MAXINTERRORMSG=Element('max:MAXINTERRORMSG')
max_CHANGEBY=Element('max:CHANGEBY')
max_CHANGEDATE=Element('max:CHANGEDATE')
max_CINUM=Element('max:CINUM')
max_CLASSSTRUCTUREID=Element('max:CLASSSTRUCTUREID')
max_CSXEXTERNALSYSTEM=Element('max:CSXEXTERNALSYSTEM')
max_DESCRIPTION=Element('max:DESCRIPTION')
max_OBJECTTYPE=Element('max:OBJECTTYPE')
max_PARENT=Element('max:PARENT')
max_RELEASEITEMID=Element('max:RELEASEITEMID')
max_RELEASEITEMNUM=Element('max:RELEASEITEMNUM')
max_RFCNUM=Element('max:RFCNUM')
max_STATUS=Element('max:STATUS')
max_STATUSDATE=Element('max:STATUSDATE')

# Setting Release Item attribute
max_RELEASEITEM.set('action', 'AddChange')

# Setting parent-child relationship

root.append(soapenv_Header)
root.append(soapenv_Body)

soapenv_Body.append(max_SyncCSXRI)

max_SyncCSXRI.append(max_CSXRISet)

max_CSXRISet.append(max_RELEASEITEM)

max_RELEASEITEM.append(max_MAXINTERRORMSG)
max_RELEASEITEM.append(max_CHANGEBY)
max_RELEASEITEM.append(max_CHANGEDATE)
max_RELEASEITEM.append(max_CINUM)
max_RELEASEITEM.append(max_CLASSSTRUCTUREID)
max_RELEASEITEM.append(max_CSXEXTERNALSYSTEM)
max_RELEASEITEM.append(max_DESCRIPTION)
max_RELEASEITEM.append(max_OBJECTTYPE)
max_RELEASEITEM.append(max_PARENT)
# max_RELEASEITEM.append(max_RELEASEITEMID)
max_RELEASEITEM.append(max_RELEASEITEMNUM)
max_RELEASEITEM.append(max_RFCNUM)
max_RELEASEITEM.append(max_STATUS)
max_RELEASEITEM.append(max_STATUSDATE)

# name.text='Arunabh Chowdhury'
# lastname.text='Chowdhury'
# firstname.text='Arunabh'

max_MAXINTERRORMSG.text='A'
max_CHANGEBY.text='admin'
max_CHANGEDATE.text=changedate_text
max_CSXEXTERNALSYSTEM.text='JIRA'
max_DESCRIPTION.text=description_text
max_OBJECTTYPE.text='CP'
# max_PARENT.text='CSXTEST123'
# max_RELEASEITEMID.text=issue_obj.key
# max_RELEASEITEMID.text=build_number

max_RELEASEITEMNUM.text=issue_obj.key
max_STATUS.text='PROD'
max_STATUSDATE.text=changedate_text


print etree.tostring(root)
tree.write(open(r'/home/t8054/Arunabh_sandbox/python_scripts/python_jira/python_jira_new/SM_Input_new.xml', 'w'))


################################################################################################
#############  DONE CREATING THE SOAP-XML ELEMENT TREE AND POPULATING THE NODES  ###############
################################################################################################
