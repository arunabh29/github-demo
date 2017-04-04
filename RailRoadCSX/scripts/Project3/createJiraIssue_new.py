import sys
from jira.client import JIRA


def connect_jira(jira_server, jira_user, jira_password):
    '''
    Connect to JIRA. Return None on error
    '''
    try:
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options,
                    # Note the tuple
                    basic_auth=(jira_user,
                                jira_password))
        return jira
    except Exception,e:
        print "Failed to connect to JIRA: %s" % e
        return None


root_dict = {

'project' : { 'key': 'PRCC' },

'summary' : 'Test summary for auto created issue from putty',

'description' : 'Test desc for auto created issue from putty',

'issuetype' : { 'name' : 'ChangePackage' },

}

server = 'http://lnx21256:8080'
jira = connect_jira(server, 'admin', 'admin123')

my_issue= jira.create_issue(fields=root_dict)

print "Issue:       %s" % my_issue.key
print "Description: %s" % my_issue.fields.description
print "Summary:     %s" % my_issue.fields.summary