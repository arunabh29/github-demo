import os.path
import sys
import xml.etree.ElementTree as xml
from httplib import PRECONDITION_FAILED

#--------------------------------------------------
# Find .classpath files in a project
# Tries to figure out the websphere version
#--------------------------------------------------
def findWebsphereVersion (workingLoc, projectNames):
    foundVersion = '7'
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname == '.classpath':
                        # root is the directory where the .classpath file loads from
                        classpath_file = os.path.join(root, ".classpath")
                        # classpath_file = "/opt/local/software/websphere"
                        root = xml.parse(classpath_file).getroot()
                        for classpathentry in root.findall('classpathentry'):
                            if classpathentry.get('kind') == 'con':
                                path = classpathentry.get('path')     
                                if "com.ibm.ws.ast.st.runtime.runtimeTarget.v70" in path:
                                    foundVersion = pickHighestVersion(foundVersion, '7')
                                elif "com.ibm.ws.ast.st.runtime.runtimeTarget.v85" in path:
                                    foundVersion = pickHighestVersion(foundVersion, '8')
                                # no need for an else because the path might not contain websphere info
    return foundVersion
   
def pickHighestVersion(previousFoundVersion, justFoundVersion ):
    if previousFoundVersion < justFoundVersion:
        return justFoundVersion
    else:
        return previousFoundVersion
    
#--------------------------------------------------
# Function: findJSFVersion
# Parameter(s): workingLoc - path to the project directories for this application
#               project - name of project for which to determine JSF version
# Description: This function determines the JSF version of the application by
#              checking the faces-config.xml file or determining if the javax.faces.*.jar
#              file exists in the ../WebContent/WEB-INF/lib/ directory
#--------------------------------------------------
def findJSFVersion(path, project):
    version = '1.2'
    facesConfigLoc = os.path.join(path, project + "/WebContent/WEB-INF")
    facesConfigDir = os.listdir(facesConfigLoc)
    javaxFacesLoc = os.path.join(facesConfigLoc, 'lib')
    javaxFacesDir = os.listdir(javaxFacesLoc)

    for file in javaxFacesDir:
        if 'javax.faces' in file:
            version = '2.0'
            return version
            
    if 'faces-config.xml' in facesConfigDir:
        xmlPath = os.path.join(facesConfigLoc, 'faces-config.xml')
        facesConfigFile = xml.parse(xmlPath).getroot()
        version = facesConfigFile.get('version')
    
    return version



#--------------------------------------------------
# Deal with .classpath file
# Gets called for each directory of a project
#--------------------------------------------------
def findClasspath(currentLoc):    
    # currentLOC is the directory where the .classpath file loads from
    # currentLoc = "/home/s9153/buildprojs/pse/ps_apps/spcc/spccEXT"
    classpath_file = os.path.join(currentLoc, ".classpath")
    # classpath_file = "/home/s9153/buildprojs/pse/ps_apps/spcc/spccEXT/.classpath"
    root = xml.parse(classpath_file).getroot()
    projectPath = []
    for classpathentry in root.findall('classpathentry'):
        if classpathentry.get('kind') == 'src':
            src = classpathentry.get('path').rstrip('/')
            # at this point src is a variable that holds the name of a directory
            # such as src .apt_whatever
            directoryToCheckIfExists = os.path.join(currentLoc, src)
            # find out if the directory exists
            if os.path.isdir(directoryToCheckIfExists):
                # the above checks to see if src & class path file exists. 
                # If they do, directory will be added to the list of directories 
                # to pass to ANT, if not, then move on and do not add to list of 
                # directories to ANT.
                projectPath.append(src)
    
    return projectPath

#--------------------------------------------------
# Find .classpath files in a project
# Tries to find lib entries of to add to the 
# classpath for build of utility
#--------------------------------------------------
def findClasspath2 (workingLoc, projectNames):
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname == '.classpath':
                        # root is the directory where the .classpath file loads from
                        classpath_file = os.path.join(root, ".classpath")
                        # classpath_file = "/opt/local/software/smappsController/leapfrog/whatever projec youre runnimg
                        root = xml.parse(classpath_file).getroot()
                        for classpathentry in root.findall('classpathentry'):
                            if classpathentry.get('kind') == 'lib':
                                path = classpathentry.get('path')
    return path 

#---------------------------------------------
#Searches for .project file 
#in the <projects> tag contains all the projects
# that that project depends on 
#----------------------------------------------
def source(workingLoc, projectNames):
    srcPath = {}
    found = False
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname == '.classpath':
                        found = True
                        path = findClasspath(currentLoc)
                        srcPath[project] = path         
                        

    return srcPath                         
