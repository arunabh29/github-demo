import os.path
import shutil
import sys
import xml.etree.ElementTree as xml



#---------------------------------------------------
#Find Compiler Version Method
#---------------------------------------------------
def findCompilerVersion(currentLoc, root):    
    projectCompileVersion = []
    compileFile = os.path.join(root, 'org.eclipse.jdt.core.prefs') 
    lines = open(compileFile, 'r').read().splitlines()
    for line in lines:
        for word in line.splitlines():
            if word.startswith('org.eclipse.jdt.core.compiler.compliance='):
                compiler = word.split('=')[1].strip()
                projectCompileVersion.append(compiler)
    return projectCompileVersion


def compileVer(workingLoc,projectNames):
    compileVersion = []
    found = False
    for project in projectNames:
            currentLoc = os.path.join(workingLoc, project)
            for root, dirs, files in os.walk(currentLoc):
                for fname in files :
                    if fname == 'org.eclipse.jdt.core.prefs':
                        found = True
                        compileVersion.append(findCompilerVersion(currentLoc, root))       

    return compileVersion        