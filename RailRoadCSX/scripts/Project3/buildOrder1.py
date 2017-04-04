#--------------------------------------------------------
#buildOrder.py
#Print out list of project and its dependencies
#Print out build order in which projects should be built
#Marks the EAR project with a "*"
#
#--------------------------------------------------------

import os.path
import shutil
import sys
import xml.etree.ElementTree as xml



#----------------------------------------------------------
#Read in Directories 
#----------------------------------------------------------
workingLoc = sys.argv[1]
jarFileName = sys.argv[2]
buildDir = sys.argv[3]
distDir = sys.argv[4]

#---------------------------------------------------
#CONSTANTS
#---------------------------------------------------
antRunLoc = os.path.normpath('C:/prog/apache-ant-1.8.4/bin/ant.bat')
ejbFileDir = os.path.normpath('C:/CCSTG/s9161_bf_P0002638_dev/buildforge/leapfrog/ejbBuild.xml')
warFileDir = os.path.normpath('C:/CCSTG/s9161_bf_P0002638_dev/buildforge/leapfrog/warBuild.xml')
ejbTempFile = os.path.normpath('C:/prog/testBuild/ejbBuildtemp.xml')
warTempFile = os.path.normpath('C:/prog/testBuild/warBuildtemp.xml')
earFileDir = os.path.normpath('C:/CCSTG/s9161_bf_P0002638_dev/buildforge/leapfrog/earBuild.xml')
earTempFile = os.path.normpath('C:/prog/testBuild/earBuildtemp.xml')
compileLibDir = os.path.normpath('C:/Rational/IBM/WebSphere/AppServer')

#---------------------------------------- 
#Get all the project name if not provided
#----------------------------------------
projectNames = os.listdir(workingLoc)

#------------------------------------------------
#Find Dependencies method
#------------------------------------------------
def findDependecy(currentLoc):
    projectChildren = []
    project_file = os.path.join(currentLoc, ".project")  
    root = xml.parse(project_file).getroot() 
    progs = [projects for projects in root.findall('projects')]                    
    for Project in progs:
        for child in Project.getchildren():
            projectChildren.append(child.text)
            if not Project.getchildren():
                projectChildren = []
    return projectChildren

#------------------------------------------------
#Find Project type method
#------------------------------------------------
def findProjectType(currentLoc):
    projType = {}
    web = []
    ejb = []
    project_file = os.path.join(currentLoc, "application.xml")  
    root = xml.parse(project_file).getroot() 
    projects = root.getiterator()
    for proj in projects:
        if proj.tag.endswith('web-uri'):
            web.append(proj.text.rstrip('.war'))
        if proj.tag.endswith('ejb'):
            ejb.append(proj.text.rstrip('.jar'))
        if proj.tag.endswith('display-name'):
            projType['ear'] = proj.text  
    projType['web'] = web
    projType['ejb'] = ejb
    return projType 

#--------------------------------------------------
#Find Classpath Method
#--------------------------------------------------
def findClasspath(currentLoc):    
    classpath_file = os.path.join(currentLoc, ".classpath")
    root = xml.parse(classpath_file).getroot()
    projectPath = []
    for classpathentry in root.findall('classpathentry'):
        if classpathentry.get('kind') == 'src':
            src = classpathentry.get('path')
            projectPath.append(src)
    return projectPath

#---------------------------------------------------
#Find Compiler Version Method
#---------------------------------------------------
def findCompilerVersion(currentLoc):    
    projectCompileVersion = []
    compileFile = os.path.join(root, 'org.eclipse.jdt.core.prefs') 
    lines = open(compileFile, 'r').read().splitlines()
    for line in lines:
        for word in line.splitlines():
            if word.startswith('org.eclipse.jdt.core.compiler.compliance='):
                compiler = word.split('=')[1].strip()
                projectCompileVersion.append(compiler)
    return projectCompileVersion

#---------------------------------------------------------
#Get source 
#---------------------------------------------------------
def getSource(project):
    for key, keylist in srcPath.iteritems():
        if key == project:     
            src = keylist[0]
    return src  
    
#---------------------------------------------
#Searches for .project file 
#in the <projects> tag contains all the projects
# that that project depends on 
#From that a dependencies list will be created 
#Projects that have an "application.xml file is 
# the ear project, this will be denoted in the dependencies 
# list by a asterisk '*'
#Searches for .classpath file
# in the <classpathentry> tag contains the src path 
# for that project 
# srcPath Dictionary is create with projects and their 
# source path distination 
#----------------------------------------------

projectDependency = {} 
srcPath = {}
compileVersion = []
jarFiles = []
tests = []
projectTypes = {}
for project in projectNames:
        print project
        children = [] 
        currentLoc = os.path.join(workingLoc, project)
        for root, dirs, files in os.walk(currentLoc):
            for fname in files :
                if fname.endswith('.project'):    
                    children = findDependecy(currentLoc)
                    projectDependency[project] = children             
                if fname.endswith('application.xml'):
                    projectTypes = findProjectType(root)
                    children.append('*')
                    earDir = project 
                    projectDependency[project] = children
                if fname.endswith('.classpath'):
                    path = findClasspath(currentLoc)
                    srcPath[project] = path
                if fname.endswith('org.eclipse.jdt.core.prefs'):
                    compileVersion.append(findCompilerVersion(currentLoc))
                if fname.endswith('.jar'):
                    if fname.startswith(project) == False:
                        jarFiles.append(fname)

#-----------------------------------------------------
#Order projects in the order that they should be built 
#-----------------------------------------------------
buildOrder= []
tempDict = {}
templist = []
for key, keylist in projectDependency.iteritems():
    searchKey = key
    if not keylist:
        buildOrder.append(key)
        tempDict[key] = keylist
    else:
        for keyNext, keylistNext in projectDependency.iteritems():
            if searchKey in keylistNext:
                if searchKey not in buildOrder:
                    buildOrder.append(searchKey)
                    tempDict[keyNext] = keylistNext
                else:
                    for tempKey, tempList in tempDict.iteritems():
                        if searchKey in tempList:
                            tempIndex = buildOrder.index(tempKey)
                            buildOrder.insert(tempIndex, searchKey)
for key, keylist in projectDependency.iteritems():
    searchKey = key
    searchKeyList = keylist
    dictlist = projectDependency.values()
    for element in dictlist:
        for elementitems in element:
            templist.append(elementitems)
    for keyNext, keylistNext in projectDependency.iteritems():
        if searchKey not in keylistNext:
            if searchKey not in buildOrder:
                buildOrder.append(searchKey)


#-------------------------------------------------------------
#Approved Jar files 
#-------------------------------------------------------------
approvedProjectJars = []
approvedJarList = [line.strip() for line in open(jarFileName)]
for jars in jarFiles:
    for approvedJars in approvedJarList:
        if jars.startswith(approvedJars):
            approvedProjectJars.append(jars)

#---------------------------------------------------------------
#Set up Directories 
#---------------------------------------------------------------
shutil.rmtree(buildDir, ignore_errors=True)
shutil.rmtree(distDir, ignore_errors=True)
os.mkdir(buildDir)
os.mkdir(distDir)
for project in buildOrder:
    for key, keylist in projectTypes.iteritems():
        if key == 'ejb':
            if project in projectTypes['ejb']:
                ejbDir = os.path.join(workingLoc, project)
                ejbSrc = os.path.join(ejbDir, getSource(project))
                f1 = open(ejbFileDir, 'r') 
                f2 = open(ejbTempFile, 'w') 
                for line in f1:     
                    if line.find('***ejbdir***') > -1:
                        f2.write(line.replace('***ejbdir***', ejbDir))
                    elif line.find('***buildDir***') > -1:
                        f2.write(line.replace('***buildDir***', buildDir))
                    elif line.find ('***src***') > -1:
                        f2.write(line.replace('***src***', ejbSrc)) 
                    elif line.find ('***earDir***') > -1:
                        earDir = os.path.join(workingLoc, earDir)
                        f2.write(line.replace('***earDir***', earDir)) 
                    else:
                        f2.write(line)
                f1.close() 
                f2.close() 
                os.system(antRunLoc +' -f '+ ejbTempFile+ ' -Dcompile.lib.dir='+ compileLibDir)
        if key == 'web':
            if project in projectTypes['web']:
                webDir = os.path.join(workingLoc, project)
                webSrc = os.path.join(webDir, getSource(project))
                f1 = open(warFileDir, 'r')
                f2 = open(warTempFile, 'w')
                for line in f1:     
                    if line.find('***webdir***') > -1:
                        f2.write(line.replace('***webdir***', webDir))
                    elif line.find('***buildDir***') > -1:
                        f2.write(line.replace('***buildDir***', buildDir))
                    elif line.find ('***src***') > -1:
                        f2.write(line.replace('***src***', webSrc)) 
                    else:
                        f2.write(line)
                f1.close() 
                f2.close() 
                os.system(antRunLoc +' -f '+ warTempFile+ ' -Dcompile.lib.dir='+ compileLibDir) 
    if project == projectTypes['ear']:
        earDir = os.path.join(workingLoc, project)
        f1 = open(earFileDir, 'r')
        f2 = open(earTempFile, 'w')
        for line in f1:     
            if line.find('***earDir***') > -1:
                f2.write(line.replace('***earDir***', earDir))
            elif line.find('***buildDir***') > -1:
                f2.write(line.replace('***buildDir***', buildDir))
            elif line.find ('***dist***') > -1:
                f2.write(line.replace('***dist***', distDir)) 
            else:
                f2.write(line)
        f1.close() 
        f2.close() 
        os.system(antRunLoc +' -f '+ earTempFile+ ' -Dcompile.lib.dir='+ compileLibDir)
        
        
        
print
print 'Project Dependency: ', projectDependency
print 
print 'Source Path: ', srcPath
print 
print 'Compiler Version: ', max(compileVersion)    
print
print 'Builder Order: ', buildOrder
print
print 'Jar Files: ', jarFiles    
print
print 'Not approved Jars: ', [x for x in jarFiles if x not in approvedProjectJars]

