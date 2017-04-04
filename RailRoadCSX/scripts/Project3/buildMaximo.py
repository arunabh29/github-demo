import sys
import os.path
import platform
import os
import inspect

import logging 

try:
     # realpath() with make your script run, even if you symlink it :)
    thisFolder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
    if thisFolder not in sys.path:
         sys.path.insert(0, thisFolder)
    
    # use this if you want to include modules from a subforder
    childFolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "subfolder")))
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
     
    import findDependency
    import srcPath
    import jarFiles
    import buildOrder
    import approvedJars
    import projectTypes
    import antParseMaximo
    import findUtil
    import libraryDirectory
    import datetime
    
    import buildUtilityFunctionsMaximo
    
    # These are only for command line parameters
    # not environment variables
    projectNamesFound= False
    earFileNameSet = False
    workingLocSet = False
    buildDirSet = False
    scriptsHomeSet = False
    includesJUnitProprtySet = False
    
    classpathSequence = ''
    
    print 'Start : ' + str(datetime.datetime.now())
    
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
    
    #------------------------------------------------------
    # Handle classpath sequencing - Custom or default
    #-------------------------------------------------------
    
    # Determine if the run requires a custom classpath build sequence
    # Key Terms:
    #    EXT = shared.lib.classpath + ext.classpath
    #    COMMON = common.classpath
    #    MODULE = module.compile.classpath
    #    EAR = ear.lib.classpath
    
    #libsDict = buildUtilityFunctionsMaximo.buildRefIds()
    customSeqSet = True
    if classpathSequence == '':
        customSeqSet = False
        print ("No custom classpath build sequence entered. Using the default.")
        classpathSequence = "WEBSPHERE, COMMON, MODULE, EAR"

    timeAtCount = 0;

    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' : '  + str(datetime.datetime.now())

    buildUtilityFunctionsMaximo.customCPSeq = classpathSequence
    
    # cpCount = 0
    # cpOrder = ''
    # print (classpathSequence.replace(' ', '').split(','))
    # for path in classpathSequence.replace(' ', '').split(','):
    #     cpOrder += libsDict[path]
    #     cpOrder += ' '
    #     cpCount += 1
    # 
    # if cpCount != 4:
    #     print ("Invalid amount of entries for the custom classpath sequence.")
    #     print ("Enter each of the following keys once to define the custom classpath sequence")
    #     print ("\t KEY     | VALUE")
    #     print ("---------------------------------------------------")
    #     print ("\t WEBSPHERE     | shared.lib.classpath + ext.classpath")
    # #         print ("\t SHARED  | shared.lib.classpath")
    #     print ("\t COMMON  | common.classpath")
    #     print ("\t MODULE  | module.compile.classpath")
    #     print ("\t EAR     | ear.lib.classpath")
    #     sys.exit(1)
    
    cpOrder = buildUtilityFunctionsMaximo.parseClasspathSeq(classpathSequence)

    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' : '  + str(datetime.datetime.now())
        
    cpOrder = cpOrder.strip(' ')
    cpOrder = '' + cpOrder + ''
    
    if (customSeqSet == True):
        print ("Custom classpath build sequence " + cpOrder + " has been entered.")
    else :
        print ("Default classpath build sequence " + cpOrder + " has been assigned.")
    
    #------------------------------------------------------
    
    
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
    
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' before projectTypes.getProjectTypes : '  + str(datetime.datetime.now())
    # Assign the types (ear, war, ejb, util) for each project
    projectType = projectTypes.getProjectTypes(workingLoc, projectNames)
    
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after projectTypes.getProjectTypes : '  + str(datetime.datetime.now())

    projectTypesAllDict = dict(projectType)
    print 'ProjectTypesAllDict before : ' + str(projectTypesAllDict)
    print 'projectType before : ' + str(projectType)
    projectType = buildUtilityFunctionsMaximo.cleanUpProjectList(workingLoc, projectTypesAllDict)
    print 'ProjectTypesAllDict After : ' + str(projectTypesAllDict)
    print 'projectType After : ' + str(projectType)
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' : '  + str(datetime.datetime.now())
    
    # Determine the library directory
    libDir = libraryDirectory.determineLibraryDirectory(projectType['ear'][0], workingLoc)
    print ('Library directory for the EAR file: ' + libDir)
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after libraryDirectory.determineLibraryDirectory : '  + str(datetime.datetime.now())
    
    # Determine the websphere and JSF version of the project
    websphereVersion = srcPath.findWebsphereVersion(workingLoc, projectNames)
    print ("Project Names: " + str(projectNames))
    print ("websphereVersion found ======== " + websphereVersion + " ========")
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after srcPath.findWebsphereVersion : '  + str(datetime.datetime.now())
    
    # Use this list in future leapfrog fixpack
    # Compare approved jar file list with the jar files used in this project
    approvedJarFile = os.path.join(CSX_SCRIPTS_HOME, 'approvedJars.txt')
    jarFiles = jarFiles.getJars(workingLoc, projectNames)
    print 'Jar Files: ', jarFiles
    notApprovedJars = approvedJars.getApprovedjars(approvedJarFile, jarFiles)
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after jarFiles.getJars and approvedJars.getApprovedjars : '  + str(datetime.datetime.now())
    
    # Determine the dependencies among the projects
    projectDependency = findDependency.Dependency(workingLoc, projectNames)
    
    # If the project is old (WAS 7) then dynamically remove the circular dependency
    # If the project is new (WAS 8) then print that there is a circular dependency and fail the build
    if websphereVersion == '7':
        projectDependency = findDependency.removeCircularDependency(projectDependency, projectType)
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after findDependency.removeCircularDependency : '  + str(datetime.datetime.now())
        
    print 'projectDependency: ', projectDependency
    
    buildSequence = buildOrder.getBuildOrder(projectType['ear'][0], projectDependency[projectType['ear'][0]], projectDependency)
    buildSequence = buildSequence.split(' ')
    buildSequence = buildOrder.createSet(buildSequence)
    buildSequence = buildOrder.buildUtilsFirst(buildSequence, projectType)
    print ("PROJECT BUILD ORDER = " + str(buildSequence))
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after buildSequence set-up : '  + str(datetime.datetime.now())
    
    # Now that project build order has been determined, we can remove duplicate projects in the dependency dictionary
    # to avoid copying duplicate files into the EAR
    projectDependency = findDependency.removeDependencyDuplicates(projectDependency, projectType)
    print ("OUTPUT EAR FILE STRUCTURE: " + str(projectDependency))
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after findDependency.removeDependencyDuplicates : '  + str(datetime.datetime.now())
    
    # Determine the source folders within each project
    sourcePath = srcPath.source(workingLoc, projectNames)
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after srcPath.source : '  + str(datetime.datetime.now())
    
    # Check if the project requires an <EJB>.jar to be copied into <WEB>.war/WEB-INF/lib/
    ejbCopyDict = buildUtilityFunctionsMaximo.copyEJBForREST(workingLoc, projectType["web"], projectType["ejb"])
    print ("EJBs THAT NEED TO BE COPIED INTO <WEB PROJECT>.WAR/WEB-INF/lib: " + str(ejbCopyDict))
    timeAtCount += 1
    print 'Step ' + str(timeAtCount) +' after buildUtilityFunctionsMaximo.copyEJBForREST : '  + str(datetime.datetime.now())
    
    antParseMaximo.parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, str(includesJUnitClasses), 
                   projectType, projectDependency, buildDir, earFileName, websphereVersion, 
                   buildSequence, cpOrder, customSeqSet, libDir, ejbCopyDict)
    print 'Step ' + str(timeAtCount) +' after antParseMaximo.parse : '  + str(datetime.datetime.now())

except:
    print 'All encompassing Exception'
    logging.exception('')
    exit(1)