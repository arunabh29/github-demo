import os.path
import shutil
import sys
import xml.etree.ElementTree as xml




#------------------------------------------------------
#Find util dependencies 
#-------------------------------------------------------

def parseManifest(path, projectNames, dependents):
    for util in projectNames:
        for line in open(path):
            for jar in line.split(':'):
                jar = jar.rstrip("\r\n").lstrip(" ").rstrip()
                if jar.rstrip('.jar').strip() == util:
                    dependents.append(util)
    return dependents                




#------------------------------------------------
#Find Dependencies method
#------------------------------------------------
def findDependency(currentLoc, dependents):
    project_file = os.path.join(currentLoc, ".project")  
    root = xml.parse(project_file).getroot() 
    progs = [projects for projects in root.findall('projects')]                    
    for Project in progs:
        for child in Project.getchildren():
            if not child.text in dependents:
                dependents.append(child.text)
    return dependents

#---------------------------------------------
#Searches for .project file 
#in the <projects> tag & contains all 
#projects this project depends on 
#----------------------------------------------
# projectNames = ['NBCConsole', 'NBCEar', 'NBCConsoleEJB']
def Dependency(workingLoc, projectNames):
    projectDependency = {}
    found = False
    for project in projectNames:
        #print project
        dependents = [] 
        currentLoc = os.path.join(workingLoc, project)
        for root, dirs, files in os.walk(currentLoc):
            for fname in files :
                if fname == '.project':
                    found = True    
                    dependents = findDependency(currentLoc, dependents)
                if fname == 'MANIFEST.MF':
                    path = os.path.join(root, fname)  
                    dependents = parseManifest(path, projectNames, dependents)
        projectDependency[project] = dependents
         
    if found == False:
        print '.project file was not found'
        print 'Make sure that your project contains a .project file'
        sys.exit(1)
    
    return projectDependency

#-------------------------------------------------------
# Detects if a dependency exists in the projects such that
# an EJB project depends on a WEB project or vice versa.
#
# Returns True if such a dependency exists.  Else, None.
#-------------------------------------------------------
def detectIrregularDependency(projectDependency, projectTypes):
    for ejbProj in projectTypes['ejb']:
        for webProj in projectTypes['web']:
            if ejbProj in projectDependency[webProj] or webProj in projectDependency[ejbProj]:
                print ('Irregular project dependency detected between ' + ejbProj + ' and ' + webProj + '.')
                return True
    
    return None

#-------------------------------------------------------
# Remove circular dependency from the project dependency dictionary
#-------------------------------------------------------
def removeCircularDependency(projectDependency, projectTypes):
    previousType = 'ear'
    types = ['web', 'ejb', 'util']
    while types:
        for type in types:
            for project in projectTypes[type]: # If projectDependency[project] contains projectTypes[previousType]
                for previousProject in projectTypes[previousType]:
                    if previousProject in projectDependency[project]:
                        print ("This application contains a circular dependency:")
                        print ("\t" + project + " is dependent upon " + str(projectDependency[project]))
                        print ("\t" + previousProject + " is dependent upon " + str(projectDependency[previousProject]))
                        projectDependency[project].remove(previousProject)
        
        previousType = types[0]
        types.remove(previousType)
        
    return projectDependency

#-------------------------------------------------------
# Remove duplicates within the project dependency dictionary
#-------------------------------------------------------
def removeDependencyDuplicates(projectDependency, projectTypes):
    earProject = projectTypes['ear'][0]
    earProjectDependency = projectDependency[earProject]
    
    for earDependentProject in earProjectDependency:
        for project in projectDependency:
            if project != earProject:
                if earDependentProject in projectDependency[project]:
                    projectDependency[project].remove(earDependentProject)
                    
    return projectDependency