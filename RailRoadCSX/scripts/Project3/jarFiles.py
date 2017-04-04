import os.path

def getJars(workingLoc, projectNames):
    jarFiles = []
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname.endswith('.jar'):
                        if fname.startswith(project) == False:
                            jarFiles.append(fname)
    return jarFiles                  