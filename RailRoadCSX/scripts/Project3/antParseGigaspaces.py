import shutil
import sys
import os
import os.path
import srcPath
import buildUtilityFunctions
import time

import inspect

#---------------------------------------------------------
# Get source 
#---------------------------------------------------------
def getSource(project, srcPath):
    src = ''
    for key, keylist in srcPath.iteritems():
        if key == project:
            for dir in keylist:     
                src += './' + dir + ':'
    return src  

#---------------------------------------------------------------
# Build ant Scripts 
#---------------------------------------------------------------
def parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, projectTypes, projectDependency, buildDir, earDirName, appPrefix, gigaspacesVersion, gsModuleName, jarFileName,
          buildSequence):
    
    try:
       os.makedirs(buildDir)
    except:  # catch all exceptions
       pass

    curDir = os.path.dirname(os.path.abspath(__file__))
    curWorkingDir = os.getcwd()
    parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir))
    
    print 'parentDir ' + parentDir
    
    gsUtilBuild = os.path.join(curDir, 'gigaJarBuild.xml')
    copyJarBuild = os.path.join(parentDir, 'copyJarBuild.xml')

    # Set the value of antRunLoc with ANT_HOME environment variable
    # os.environ['ANT_HOME'] = 'C:\Utilities\Ant'
    antRunLoc = os.environ['ANT_HOME']
    
    #######################websphereLocFromEnv = os.environ['WAS' + str(wasVersion) + '_DIRECTORY']

    os.chdir(os.environ['BF_ROOT'])
    
#===============================================================================
# #     Determine JDK Version
# #     javaVersion = buildUtilityFunctions.parseJDKVersion(jdkVersion)
# #     print 'JDK Version : ' + str(javaVersion)
# #     
# #     os.environ['JAVA_HOME'] = os.environ['JAVA_' + str(javaVersion) + '_HOME']
# #     os.environ['PATH'] = os.environ['JAVA_' + str(javaVersion) + '_BIN'] + os.pathsep + os.environ['PATH']
#===============================================================================

    os.environ['GIGASPACES_LIB_PATH'] = os.environ['GIGASPACES_LIB_PATH'] + '/' + buildUtilityFunctions.parseGSVersion(str(gigaspacesVersion))

    print 'parent dir ' + os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir))
    
    # Command Arguments
    # Keys build.dir, compile.lib.dir, and ear.libs.dir remain the same for each build
    currentBuildModule = os.path.basename(inspect.getfile(inspect.currentframe()))
    print 'currentBuildModule = ' + currentBuildModule
    commandArguments = buildUtilityFunctions.createCommonCommandArgs(currentBuildModule, buildDir, projectTypes, projectDependency, gsModuleName)
    antFlags = buildUtilityFunctions.setAntFlags(commandArguments)

    parasoftAntJarPath = os.environ['PARASOFT_ANT_JAR_PATH'] 
    
    for project in buildSequence:
        build = [k for k, v in projectTypes.items() for prj in v if prj == project][0]
        classpathSequence = '0'  # Set to default
        
        commandArguments['proj.type'] = '-Dproj.type=' + build + ' '
        commandArguments['project.name'] = '-Dproject.name=' + project + ' ' 
        
        if len(projectDependency[project]) != 0:
            commandArguments['proj.dep'] = '-Dproj.dep="' + '|'.join(set(projectDependency[project])) + '" '
        else:
            commandArguments['proj.dep'] = ''

        if build == 'util':
            gsUtilDir = os.path.join(workingLoc, project)
            gsUtilSrc = getSource(project, sourcePath)
            
            commandArguments['buildxml'] = '-f ' + gsUtilBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + gsUtilDir + ' '
            commandArguments['src.paths'] = '-Dsrc.paths=' + gsUtilSrc + ' '
            
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

    commandArguments = buildUtilityFunctions.createCopyCommandArgs(copyJarBuild, buildDir, jarFileName, earDirName, 'gigajar', appPrefix, project, projectTypes, 'util')
    antFlags = buildUtilityFunctions.setAntFlags(commandArguments)

    print('commandArguments ' + str(commandArguments))

    printMsg = 'RUNNING ANT TO VERSION THE ARTEFACTS --------'
    antCommand = buildUtilityFunctions.formulateAntCommand(commandArguments, antFlags, '', printMsg)

    run = os.system(antCommand)
    print 'run after versioning artefacts build ' + str(run) + ' project ' + project

    if run != 0:
        print project
        print 'ARTEFACT VERSIONING FAILED'
        sys.exit(1)

