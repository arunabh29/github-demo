import sys
import os.path
import platform
import os

#These are Joe's files
import findDependency
import srcPath
import jarFiles
import buildOrder
import approvedJars
import projectTypes
import antParse
import findUtil
import libraryDirectory

import buildUtilityFunctions

# These are only for command line parameters
# not environment variables
projectNamesFound= False
earFileNameSet = False
workingLocSet = False
buildDirSet = False
scriptsHomeSet = False
includesJUnitProprtySet = False

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
    elif keys[0] == 'projectNames':
        projectNames = keys[1].split(',')
        projectNamesFound = True
        continue
    elif keys[0] == 'scriptsHome':
        CSX_SCRIPTS_HOME = keys[1]
        scriptsHomeSet = True
        continue
    elif keys[0] == 'earFileName':
        earFileName = keys[1]
        earFileNameSet = True
        continue
    elif keys[0] == 'classpathSequence':
        classpathSequence = keys[1]
        continue
    elif keys[0] == 'includesJUnitClasses':
        includesJUnitProprtySet = True
        includesJUnitClasses = keys[1]

# Verify that the workingLoc command argument is a path that exists
os.chdir(workingLoc)

# build.py script requires a "projectNames" command argument
# The value of projectNames can be an empty string or a specific project name
# Determine the appropriate projects to build according to this input
if projectNamesFound == False:
    print "projectNames is required"
    print "Please enter projectNames="
    sys.exit(1)
elif projectNamesFound == True and projectNames == ['']:
    projectNames = os.listdir(workingLoc)   
    print "projectNames was passed in as blank, make it based on directories: " + str(projectNames)
elif projectNamesFound == True and projectNames == ['PROJECT_TO_BUILD']:
    projectNames = os.listdir(workingLoc)   
    print "projectNames was passed in as PROJECT_TO_BUILD, make it based on directories: " + str(projectNames)
else:
    projectNames = projectTypes.findAllProjectNames(workingLoc, projectNames)

# Determine if the run requires a custom classpath build sequence
# Key Terms:
#    EXT = shared.lib.classpath + ext.classpath
#    COMMON = common.classpath
#    MODULE = module.compile.classpath
#    EAR = ear.lib.classpath

# Static lists for purpose of illustration 
# libTypes = ["WEBSPHERE", "COMMON", "MODULE", "EAR"] 
# libRefIds = ["ext.classpath", "common.classpath", "module.compile.classpath", "ear.lib.classpath"] 
# 
# libsDict = dict(zip(libType, libRefIds)) 
# for key,val in libsDict.items():
#     print key, "=>", val

cpOrder = '0'
# if classpathSequence == '':
#     print ("No custom classpath build sequence entered. Using the default.")
#     classpathSequence = "WEBSPHERE, COMMON, MODULE, EAR"
# else:
#     cpCount = 0
#     cpOrder = ''
#     print (classpathSequence.replace(' ', '').split(','))
#     for path in classpathSequence.replace(' ', '').split(','):
#         if path == 'WEBSPHERE':
#             cpOrder += 'ext.classpath'
# #         elif path == 'SHARED':
# #             cpOrder += 'shared.lib.classpath'
#         elif path == 'COMMON':
#             cpOrder += 'common.classpath'
#         elif path == 'MODULE':
#             cpOrder += 'module.compile.classpath'
#         elif path == 'EAR':
#             cpOrder += 'ear.lib.classpath'
#         else:
#             print (path + " is an invalid key for specifying the classpath sequence.")
#             print ("The keys that you must use are WEBSPHERE, COMMON, MODULE and EAR (values defined below).")
#             print ("\t KEY     | VALUE")
#             print ("\t -------------------------------------------------")
#             print ("\t WEBSPHERE     | ext.classpath")
# #             print ("\t SHARED  | shared.lib.classpath")
#             print ("\t COMMON  | common.classpath")
#             print ("\t MODULE  | module.compile.classpath")
#             print ("\t EAR     | ear.lib.classpath")
#             sys.exit()
#             
#         cpOrder += ' '
#         cpCount += 1
#     
#     if cpCount != 4:
#         print ("Invalid amount of entries for the custom classpath sequence.")
#         print ("Enter each of the following keys once to define the custom classpath sequence")
#         print ("\t KEY     | VALUE")
#         print ("---------------------------------------------------")
#         print ("\t WEBSPHERE     | shared.lib.classpath + ext.classpath")
# #         print ("\t SHARED  | shared.lib.classpath")
#         print ("\t COMMON  | common.classpath")
#         print ("\t MODULE  | module.compile.classpath")
#         print ("\t EAR     | ear.lib.classpath")
#         sys.exit()
#         
#     cpOrder = cpOrder.strip(' ')
#     cpOrder = '' + cpOrder + ''
#     print ("Custom classpath build sequence " + cpOrder + " has been entered.")

libsDict = buildUtilityFunctions.buildRefIds()
customSeqSet = True
if classpathSequence == '':
    customSeqSet = False
    print ("No custom classpath build sequence entered. Using the default.")
    classpathSequence = "WEBSPHERE, COMMON, MODULE, EAR"

cpCount = 0
cpOrder = ''
print (classpathSequence.replace(' ', '').split(','))
for path in classpathSequence.replace(' ', '').split(','):
    cpOrder += libsDict[path]
    cpOrder += ' '
    cpCount += 1

if cpCount != 4:
    print ("Invalid amount of entries for the custom classpath sequence.")
    print ("Enter each of the following keys once to define the custom classpath sequence")
    print ("\t KEY     | VALUE")
    print ("---------------------------------------------------")
    print ("\t WEBSPHERE     | shared.lib.classpath + ext.classpath")
#         print ("\t SHARED  | shared.lib.classpath")
    print ("\t COMMON  | common.classpath")
    print ("\t MODULE  | module.compile.classpath")
    print ("\t EAR     | ear.lib.classpath")
    sys.exit()
    
cpOrder = cpOrder.strip(' ')
cpOrder = '' + cpOrder + ''

if (customSeqSet == True):
    print ("Custom classpath build sequence " + cpOrder + " has been entered.")
else :
    print ("Default classpath build sequence " + cpOrder + " has been assigned.")

# Check for the required environment variables
if earFileNameSet == False:
    print "Output EAR file name not entered"
    print "Please enter EAR file name as earFileName="
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

if includesJUnitProprtySet == False:
    includesJUnitClasses = True

# Assign the types (ear, war, ejb, util) for each project
projectType = projectTypes.getProjectTypes(workingLoc, projectNames)

# Determine the library directory
libDir = libraryDirectory.determineLibraryDirectory(projectType['ear'][0], workingLoc)
print ('Library directory for the EAR file: ' + libDir)

# Determine the websphere and JSF version of the project
websphereVersion = srcPath.findWebsphereVersion(workingLoc, projectNames)
print ("Project Names: " + str(projectNames))
print ("websphereVersion found ======== " + websphereVersion + " ========")

# Use this list in future leapfrog fixpack
# Compare approved jar file list with the jar files used in this project
approvedJarFile = os.path.join(CSX_SCRIPTS_HOME, 'approvedJars.txt')
jarFiles = jarFiles.getJars(workingLoc, projectNames)
print 'Jar Files: ', jarFiles
notApprovedJars = approvedJars.getApprovedjars(approvedJarFile, jarFiles)

# Determine the dependencies among the projects
projectDependency = findDependency.Dependency(workingLoc, projectNames)

# If the project is old (WAS 7) then dynamically remove the circular dependency
# If the project is new (WAS 8) then print that there is a circular dependency and fail the build
if websphereVersion == '7':
    projectDependency = findDependency.removeCircularDependency(projectDependency, projectType)
    
print 'projectDependency: ', projectDependency

buildSequence = buildOrder.getBuildOrder(projectType['ear'][0], projectDependency[projectType['ear'][0]], projectDependency)
buildSequence = buildSequence.split(' ')
buildSequence = buildOrder.createSet(buildSequence)
buildSequence = buildOrder.buildUtilsFirst(buildSequence, projectType)
print ("PROJECT BUILD ORDER = " + str(buildSequence))

# Now that project build order has been determined, we can remove duplicate projects in the dependency dictionary
# to avoid copying duplicate files into the EAR
projectDependency = findDependency.removeDependencyDuplicates(projectDependency, projectType)
print ("OUTPUT EAR FILE STRUCTURE: " + str(projectDependency))

# Determine the source folders within each project
sourcePath = srcPath.source(workingLoc, projectNames)

# Check if the project requires an <EJB>.jar to be copied into <WEB>.war/WEB-INF/lib/
ejbCopyDict = buildUtilityFunctions.copyEJBForREST(workingLoc, projectType["web"], projectType["ejb"])
print ("EJBs THAT NEED TO BE COPIED INTO <WEB PROJECT>.WAR/WEB-INF/lib: " + str(ejbCopyDict))

antParse.parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, str(includesJUnitClasses), 
               projectType, projectDependency, buildDir, earFileName, websphereVersion, 
               buildSequence, cpOrder, customSeqSet, libDir, ejbCopyDict)
