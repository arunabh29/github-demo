import sys
import os.path
import platform
import os
import inspect
 # realpath() with make your script run, even if you symlink it :)
thisFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if thisFolder not in sys.path:
     sys.path.insert(0, thisFolder)

# use this if you want to include modules from a subforder
childFolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if childFolder not in sys.path:
     sys.path.insert(0, childFolder)

parentFolder = os.path.dirname(thisFolder)
if parentFolder not in sys.path:
     sys.path.insert(0, parentFolder)

curDir = os.path.dirname(os.path.abspath(__file__))
print 'curdir : ' + str(curDir)
print 'current working directory : ' + os.getcwd()
 # Info:
 # cmd_folder = os.path.dirname(os.path.abspath(__file__)) # DO NOT USE __file__ !!!
 # __file__ fails if script is called in different ways on Windows
 # __file__ fails if someone does os.chdir() before
 # sys.argv[0] also fails because it doesn't not always contains the path
 
#These are Joe's files
import findDependency
import srcPath
import jarFiles
import buildOrder
import approvedJars
import projectTypes
import antParseUtil
import findUtil

# These are only for command line parameters
# not environment variables
projectNameFound= False
jarFileNameSet = False
workingLocSet = False
buildDirSet = False
scriptsHomeSet = False
earDirNameSet = False

classpathSequence = ''

#Assign identifiers 
for arg in sys.argv:
    keys = arg.split('=')
    if keys[0] == 'workingLoc':
        workingLoc = keys[1]
        workingLocSet = True
        continue
    elif keys[0] == 'buildDir':
        buildDir = keys[1]
        buildDirSet = True
        continue
    elif keys[0] == 'projectName':
        projectName = keys[1]
        projectNameFound = True
        continue
    elif keys[0] == 'scriptsHome':
        CSX_SCRIPTS_HOME = keys[1]
        scriptsHomeSet = True
        continue
    elif keys[0] == 'jarFileName':
        jarFileName = keys[1]
        jarFileNameSet = True
        continue
    elif keys[0] == 'earDirName':
        earDirName = keys[1]
        earDirNameSet = True
        continue
    elif keys[0] == 'classpathSequence':
        classpathSequence = keys[1]

# Verify that the workingLoc command argument is a path that exists
os.chdir(workingLoc)

# Check for the required environment variables

if projectNameFound == False or (projectNameFound == True and projectName == ['']) or (projectNameFound == True and projectName == ['PROJECT_TO_BUILD']):
    print "projectName is required"
    print "Please enter projectName="
    sys.exit(1)
else:
    projectNames = projectTypes.findAllProjectNames(workingLoc, projectName.split(","))

if jarFileNameSet == False:
    print "Output JAR file name not entered, setting as blank and will be set to project in the run"
    jarFileName=''

if earDirNameSet == False:
    print "Output directory name not entered - must be an EAR directory"
    print "Please enter directory name as earDirName="
    sys.exit(1)

if workingLocSet == False:
    print "workingLoc is required"
    print "Please enter workingLoc as workingLoc="
    sys.exit(1)
    
if buildDirSet == False:
    print "buildDir is required"
    print "Please enter buildDir as buildDir="
    sys.exit(1)

if scriptsHomeSet == False:
    print "scriptsHome is required"
    print "Please enter scriptsHome as scriptsHome="
    sys.exit(1) 

#projectType = projectTypes.getProjectTypes(workingLoc, projectNames)
# projectType = dict()
# projectType['util'] = projectName.split(",")

projectType = {}
projectType['ear'] = {}
projectType['web'] = {}
projectType['ejb'] = {}

projectType['util'] = findUtil.getUtil(projectType, projectNames)

# Determine the websphere and JSF version of the project
#websphereVersion = srcPath.findWebsphereVersion(workingLoc, projectName.split(","))
websphereVersion = srcPath.findWebsphereVersion(workingLoc, projectNames)
print ("Project Name: " + str(projectNames))
print ("websphereVersion found ======== " + websphereVersion + " ========")

# Use this list in future leapfrog fixpack
# Compare approved jar file list with the jar files used in this project
approvedJarFile = os.path.join(CSX_SCRIPTS_HOME, 'approvedJars.txt')
#jarFiles = jarFiles.getJars(workingLoc, projectName)
jarFiles = jarFiles.getJars(workingLoc, projectNames)
print 'Jar Files: ', jarFiles
notApprovedJars = approvedJars.getApprovedjars(approvedJarFile, jarFiles)

# Determine the dependencies among the projects
#projectDependency = findDependency.Dependency(workingLoc, projectName.split(","))
projectDependency = findDependency.Dependency(workingLoc, projectNames)

print 'projectDependency: ', projectDependency

buildSequence = buildOrder.getBuildOrder(projectType['util'][0], projectDependency[projectType['util'][0]], projectDependency)
buildSequence = buildSequence.split(' ')
buildSequence = buildOrder.createSet(buildSequence)
buildSequence = buildOrder.buildUtilsFirst(buildSequence, projectType)
print ("PROJECT BUILD ORDER = " + str(buildSequence))


# Determine the source folders within each project
#sourcePath = srcPath.source(workingLoc, projectName.split(","))
sourcePath = srcPath.source(workingLoc, projectNames)

antParseUtil.parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, projectType, projectDependency, buildDir, earDirName, jarFileName, buildSequence)
