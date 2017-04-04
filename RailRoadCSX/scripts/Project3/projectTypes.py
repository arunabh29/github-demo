import os.path
import shutil
import sys
import xml.etree.ElementTree as xml
import findUtil
import re


#------------------------------------------------
#Find type method
#------------------------------------------------
def findProjectType(currentLoc, project):
    projType = {}
    web = []
    ejb = []
    ear = []
    
    warPattern = '\.war$'
    jarPattern = '\.jar$'
    extPattern = '\.[jw]ar$'
    EMPTY_STRING = ''

    project_file = os.path.join(currentLoc, "application.xml")  
    root = xml.parse(project_file).getroot() 
    projects = root.getiterator()
    for proj in projects:
        if proj.tag.endswith('web-uri'):
            #web.append(proj.text.rstrip('.war').strip())
            #web.append(proj.text[:-4])
            web.append(re.sub(extPattern, EMPTY_STRING, proj.text))
        if proj.tag.endswith('ejb'):
            #ejb.append(proj.text.rstrip('.jar').strip())
            #ejb.append(proj.text[:-4])
            ejb.append(re.sub(extPattern, EMPTY_STRING, proj.text))
    ear.append(project)        
    projType['ear'] = ear 
    projType['web'] = web
    projType['ejb'] = ejb
    return projType 


def getProjectTypes(workingLoc, projectNames):
    projectTypes = {}
    found = False
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            #print "current location is here " + currentLoc
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname == 'application.xml':
                        found = True
                        projectTypes = findProjectType(root, project)   
    if found == False:
        print 
        print "application.xml not found!"
        print "Please check your project and add application.xml file to project"
        sys.exit(1)
        
    projectTypes['util'] = findUtil.getUtil(projectTypes, projectNames)    
    
    return projectTypes
    

#-------------------------------------------------------------------------------------------
# Function: findAllProjectNames
# Parameter(s): workingLoc - path to the application project files
#               projectNames - the project names that were input by the user from cmd line
# Description: Parses through the .project files.  Returns a list of all the projects in this
#              application.
#-------------------------------------------------------------------------------------------
def findAllProjectNames(workingLoc, projectNames):
    for project in projectNames:
        currentLoc = os.path.join(workingLoc, project)
        for root, dirs, files in os.walk(currentLoc):
            for file in files:
                if file == '.project':
                    appFile = os.path.join(root, '.project')
                    parseAppFile = xml.parse(appFile).getroot()
                    projs = [projects for projects in parseAppFile.findall('projects')]
                    for p in projs:
                        for child in p.getchildren():
                            if not child.text in projectNames:
                                projectNames.append(child.text)
    return projectNames
