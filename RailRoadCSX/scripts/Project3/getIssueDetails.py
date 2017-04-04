from jira.client import JIRA
import sys
import pprint

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

def print_issue(issue):
    '''
    Print out formatted jira issue
    '''
    print "Issue:       %s" % issue.key
    print "Description: %s" % issue.fields.description
    print "Summary:     %s" % issue.fields.summary
   # print "Assignee:    %s" % issue.fields.assignee.displayName
    print "Environment: %s" % issue.fields.environment
    print "Status:      %s" % issue.fields.status.name
  # print "Link:        %s/browse/%s" % (server, issue.key)

server = 'http://lnx21256:8080'
jira = connect_jira(server, 'admin', 'admin123')

# issue = jira.issue('PRCC-15')

try:
    issue = jira.issue(sys.argv[1])
except Exception,e:
    print "Can't find that Issue"

issue = jira.issue(sys.argv[1])
print_issue(issue)

