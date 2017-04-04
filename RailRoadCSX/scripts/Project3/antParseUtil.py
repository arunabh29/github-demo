import shutil
import sys
import os
import os.path
import srcPath
import buildUtilityFunctions
import time

import inspect

#---------------------------------------------------------
#Get source 
#---------------------------------------------------------
def getSource(project, srcPath):
    src = ''
    for key, keylist in srcPath.iteritems():
        if key == project:
            for dir in keylist:     
                src+='./'+dir+':'
    return src  

#---------------------------------------------------------------
#Build ant Scripts 
#---------------------------------------------------------------
def parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, projectTypes, projectDependency, buildDir, earDirName, jarFileName, 
          buildSequence):
    #shutil.rmtree(buildDir, ignore_errors=True)
    
    try:
       os.makedirs(buildDir)
    except: #catch all exceptions
       pass

    parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir))
    print 'parentDir ' + parentDir

    curDir = os.path.dirname(os.path.abspath(__file__))
    curWorkingDir = os.getcwd()
    utilBuild = os.path.join(curDir, 'jarBuild.xml')
    copyJarBuild = os.path.join(parentDir, 'copyJarBuild.xml')

    # Set the value of antRunLoc with ANT_HOME environment variable
    #os.environ['ANT_HOME'] = 'C:\Utilities\Ant'
    antRunLoc = os.environ['ANT_HOME']
    
    # JSF version should be determined within the loop - as it can be different for different modules within the EAR
    
    # Parse, aka load the location of websphere lib folder from the environment variable
    # os.environ will throw an exception and blow up the whole process if the variable doesn't exist
    #     websphereLocFromEnv = os.environ['WAS' + str(wasVersion) + '_DIRECTORY']

    # set /tmp as current python directory to avoid message about 'getcwd does not exist'
    os.chdir(os.environ['BF_ROOT'])
    
#===============================================================================
# #     Determine JDK Version
# #     
# #     wasJDKVersion = buildUtilityFunctions.getJDKVersionForWebsphere(wasVersion)
# #     os.environ['JAVA_HOME'] = os.environ['JAVA_' + str(wasJDKVersion) + '_HOME']
# #     os.environ['PATH'] = os.environ['JAVA_' + str(wasJDKVersion) + '_BIN'] + os.pathsep + os.environ['PATH']
#===============================================================================

#     print '1 : ' + inspect.getfile(inspect.currentframe()) # script filename (usually with path)
#     print '2 : ' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
#     print '3 : ' + os.path.basename(inspect.getfile(inspect.currentframe())) # script name

    # Command Arguments
    # Keys build.dir, compile.lib.dir, and ear.libs.dir remain the same for each build
    currentBuildModule = os.path.basename(inspect.getfile(inspect.currentframe()))
    print 'currentBuildModule = ' + currentBuildModule
    commandArguments = buildUtilityFunctions.createCommonCommandArgs(currentBuildModule, buildDir, projectTypes, projectDependency, '')

    antFlags = buildUtilityFunctions.setAntFlags(commandArguments)

    parasoftAntJarPath = os.environ['PARASOFT_ANT_JAR_PATH'] 
    
    for project in buildSequence:
        build = [k for k, v in projectTypes.items() for prj in v if prj == project][0]
        classpathSequence = '0' # Set to default
        
        commandArguments['proj.type'] = '-Dproj.type=' + build + ' '
        commandArguments['project.name'] = '-Dproject.name=' + project + ' ' 
        
        if len(projectDependency[project]) != 0:
            commandArguments['proj.dep'] = '-Dproj.dep="' + '|'.join(set(projectDependency[project])) + '" '
        else:
            commandArguments['proj.dep'] = ''
        
        if build == 'util':
            utilDir = os.path.join(workingLoc, project)
            utilSrc = getSource(project,sourcePath)
            
            commandArguments['buildxml'] = '-f ' + utilBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + utilDir + ' '
            commandArguments['src.paths'] = '-Dsrc.paths=' + utilSrc + ' '

        commandArguments['classpath.sequence'] = '-Dclasspath.sequence=' + classpathSequence + ' '

        printMsg = build.upper() + ' ANT COMMAND FOR ' + project + ' --------'
        antCommand = buildUtilityFunctions.formulateAntCommand(commandArguments, antFlags, parasoftAntJarPath, printMsg)

        run = os.system(antCommand)
        print 'run after ' + build + ' build ' + str(run) + ' project ' + project

        if run != 0:
            print project
            print 'BUILD FAILED'
            sys.exit(1)
        continue

    # Run this step to copy the jar to appropriate location
    # copyJarBuild.xml
    # This ANT build adds a version to the artefact and 
    # copies it to the target distribution directory
    commandArguments = buildUtilityFunctions.createCopyCommandArgs(copyJarBuild, buildDir, jarFileName, earDirName, 'utilityJar', '', project, projectTypes, 'util')
    antFlags = buildUtilityFunctions.setAntFlags(commandArguments)

    print('commandArguments ' + str(commandArguments))

    printMsg = 'RUNNING ANT TO VERSION THE ARTEFACTS --------'
    antCommand = buildUtilityFunctions.formulateAntCommand(commandArguments, antFlags, '', printMsg)
    
    run = os.system(antCommand)
    print 'run after versioning artefacts build ' + str(run) + ' project ' + project

    if run != 0:
        print project
        print 'ARTIFACT VERSIONING FAILED'
        sys.exit(1)

