import os


def parseManifest(path, projectNames, projectType):
    utility = []
    for util in trimProjectNames:
        for line in open(path):
            for jar in line.split(':'):
                jar = jar.rstrip("\r\n").lstrip(" ").rstrip()
                if jar.rstrip('.jar').strip() == util:
                    utility.append(util)
                    projectType['util'] = utility
                    
    return projectType                

#def getUtil(projectType, projectNames, workingLoc):
def getUtil(projectType, projectNames):
    utilityList = []
    
    for project in projectNames:
        if not project in projectType['ear'] and not project in projectType['web'] and not project in projectType['ejb']:
            if not project in utilityList:
                utilityList.append(project)
                
    '''
    for project in projectNames:
        currentLoc = os.path.join(workingLoc, project)
        for root, dirs, files in os.walk(currentLoc):
            for f in files:
                if f == 'MANIFEST.MF':
                    path = os.path.join(root, f)  
                    parseManifest(path, projectNames, projectType)
    '''
    return utilityList
