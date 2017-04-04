import shutil
import sys
import os.path
import srcPath
import time
import re

import datetime
import buildUtilityFunctionsMaximo

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
def parse(CSX_SCRIPTS_HOME, workingLoc, sourcePath, includesJUnitClasses, projectTypes,
          projectDependency, buildDir, earFileName, wasVersion, buildSequence,
          cpOrder, customSeqSet, libDir, ejbCopyDict):
    # shutil.rmtree(buildDir, ignore_errors=True)
    
    print 'Custome Seq Set : ' + str(customSeqSet) + '  Classpath Order : ' + cpOrder
    try:
       os.makedirs(buildDir)
    except:  # catch all exceptions
       pass

    #Use below line to generate error for test
    #os.chdir('C:\\RAD91_WS\\CMOR_Susan3_notExist')
    
    curDir = os.path.dirname(os.path.abspath(__file__))
    curWorkingDir = os.getcwd()
    parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir))

    print 'parentDir ' + parentDir
    
    #cleaup build directory 
    buildUtilityFunctionsMaximo.cleanupBuildDir( buildDir )

    ejbBuild = os.path.join(curDir, 'ejbBuildMaximo.xml')
    warBuild = os.path.join(curDir, 'warBuildMaximo.xml')
    earBuild = os.path.join(curDir, 'earBuildMaximo.xml')
    utilBuild = os.path.join(curDir, 'utilBuildMaximo.xml')
    copyEarBuild = os.path.join(parentDir, 'copyEarBuild.xml')

    earDir = projectTypes['ear']
    earDir = os.path.join(workingLoc, earDir[0])
    print 'projectTypes', projectTypes 

    # Determines the Classpath sequencing for the build
    # 0 is default - this is the sequence for WAS8, WAS7 with JSF 1.2, and WAS7 with JSP
    # 1 is for an application using WAS7 with JSF 2.0
    #cpCount = 0
    classpathSequence = '0'
    
    # Set the value of antRunLoc with ANT_HOME environment variable
    # os.environ['ANT_HOME'] = 'C:\Utilities\Ant'
    antRunLoc = os.environ['ANT_HOME']
    
    # JSF version should be determined within the loop - as it can be different for different modules within the EAR
    
    # Parse, aka load the location of websphere lib folder from the environment variable
    # os.environ will throw an exception and blow up the whole process if the variable doesn't exist
    websphereLocFromEnv = os.environ['WAS' + str(wasVersion) + '_DIRECTORY']
    # set /tmp as current python directory to avoid message about 'getcwd does not exist'
    os.chdir(os.environ['BF_ROOT'])
    if wasVersion == '7':  # if websphere version is 7, use java_6_home variable
        os.environ['JAVA_HOME'] = os.environ['JAVA_6_HOME']
        # used for debugging only print "JAVA_HOME for websphere 7 is: " + os.environ['JAVA_6_HOME']
        # prepend JAVA_6_BIN to the PATH
        os.environ['PATH'] = os.environ['JAVA_6_BIN'] + os.pathsep + os.environ['PATH']
        # used for debugging only print "PATH for websphere 7 is: " + os.environ['PATH']     
            
    elif wasVersion == '8':  # if webpshere version is 8, use java_7_home variable
        # os.putenv('JAVA_HOME', os.environ['JAVA_7_HOME'] )
        os.environ['JAVA_HOME'] = os.environ['JAVA_7_HOME']
        # used for debugging only print "JAVA_HOME for websphere 8 is: " + os.environ['JAVA_HOME']
        # prepend JAVA_7_BIN to the PATH
        os.environ['PATH'] = os.environ['JAVA_7_BIN'] + os.pathsep + os.environ['PATH']
        # used for debugging only print "PATH for websphere 8 is: " + os.environ['PATH']
        # Parse the location of the EAR Jar files and add them to the build of the utility
       
        path = "/usr/tmp"

        # Now that you have found the EAR lib files, take them
        # and move them to util's location
        # Now change the directory
    
    includesJUnitTestObj = re.search('(Y|Yes|T|True|1)', includesJUnitClasses, re.IGNORECASE)
    excludeStarTestJava = ('Y' if includesJUnitTestObj else 'N')
    print 'excludeStarTestJava ' + str(excludeStarTestJava)

    # Command Arguments
    # Keys build.dir, compile.lib.dir, and ear.libs.dir remain the same for each build
    currentBuildModule = os.path.basename(inspect.getfile(inspect.currentframe()))
    print 'currentBuildModule = ' + currentBuildModule

    utilDir = []
    for project in projectTypes['util']:
        utilDir = os.path.join(workingLoc, project)
        utilSrc = getSource(project, sourcePath)
        os.chdir(utilDir)
    
    # Command Arguments
    # Keys build.dir, compile.lib.dir, and ear.libs.dir remain the same for each build
    commandArguments = {}

    commandArguments = buildUtilityFunctionsMaximo.createFullBuildCommandArgs(currentBuildModule, buildDir, projectTypes, projectDependency, websphereLocFromEnv, earDir, earFileName, libDir, cpOrder, excludeStarTestJava)
    antFlags = buildUtilityFunctionsMaximo.setAntFlags(commandArguments)

    parasoftAntJarPath = os.environ['PARASOFT_ANT_JAR_PATH'] 
    
    for project in buildSequence:
        build = [k for k, v in projectTypes.items() for prj in v if prj == project][0]
        classpathSequence = cpOrder
        
        commandArguments['proj.type'] = '-Dproj.type=' + build + ' '
        commandArguments['project.name'] = '-Dproject.name=' + project + ' ' 
        commandArguments['build.seq'] = '-Ddynamic.build.seq=true' + ' '
        if(customSeqSet == True) :
            commandArguments['build.seq.msg'] = '-Ddynamic.build.seq.message="Selecting custom classpath sequence : Order ' + buildUtilityFunctionsMaximo.customCPSeq + ' Lib ref : ' + classpathSequence + '" '
        else:
            commandArguments['build.seq.msg'] = '-Ddynamic.build.seq.message="Selecting Default classpath sequence : Order ' + buildUtilityFunctionsMaximo.defaultCPSeq + ' Lib ref : ' + classpathSequence + '" '
        
        if len(projectDependency[project]) != 0:
            commandArguments['proj.dep'] = '-Dproj.dep="' + '|'.join(set(projectDependency[project])) + '" '
        else:
            commandArguments['proj.dep'] = ''

        # Reset copy.ejbs command argument to EMPTY_STRING 
        commandArguments['copy.ejbs'] = ''
        
        if build == 'util':
            utilDir = os.path.join(workingLoc, project)
            utilSrc = getSource(project, sourcePath)
            
            if (project == 'properties') :
                print('Properties project found')
                commandArguments['copy.properties'] = '-Dcopy.properties=True' + ' ' 

            commandArguments['buildxml'] = '-f ' + utilBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + utilDir + ' '
            commandArguments['src.paths'] = '-Dsrc.paths=' + utilSrc + ' '
            
        elif build == 'ejb':
            ejbDir = os.path.join(workingLoc, project)
            ejbSrc = getSource(project, sourcePath)
            
            commandArguments['buildxml'] = '-f ' + ejbBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + ejbDir + ' '
            commandArguments['src.paths'] = '-Dsrc.paths=' + ejbSrc + ' '
            
        elif build == 'web':
            webDir = os.path.join(workingLoc, project)
            webSrc = getSource(project, sourcePath)
            
            #WAS 7 / jsp / jsf 1.2 sequence 
            if (wasVersion == '7' and srcPath.findJSFVersion(workingLoc, project) == '2.0'):
                classpathSequence = buildUtilityFunctionsMaximo.jsf2WAS7CPSeq
                #"MODULE, WEBSPHERE, COMMON, EAR"
                commandArguments['build.seq.msg'] = '-Ddynamic.build.seq.message="Selecting was7jsf2 classpath sequence : Order ' + buildUtilityFunctionsMaximo.jsf2WAS7CPSeq + ' Lib ref : ' + classpathSequence + '" '
            else :
                if (customSeqSet == False) :
                    classpathSequence = buildUtilityFunctionsMaximo.defaultCPSeq 
                    #"WEBSPHERE, COMMON, MODULE, EAR"
                    commandArguments['build.seq.msg'] = '-Ddynamic.build.seq.message="Selecting Default classpath sequence : Order ' + buildUtilityFunctionsMaximo.defaultCPSeq + ' Lib ref : ' + classpathSequence + '" '
                else :
                    classpathSequence = buildUtilityFunctionsMaximo.customCPSeq
                    commandArguments['build.seq.msg'] = '-Ddynamic.build.seq.message="Selecting Custom classpath sequence : Order ' + buildUtilityFunctionsMaximo.customCPSeq + ' Lib ref : '  + classpathSequence + '" '

            print ('classpathSequence in web build ' + classpathSequence)
            commandArguments = buildUtilityFunctionsMaximo.resetClasspathSeq(commandArguments, classpathSequence)

            commandArguments['buildxml'] = '-f ' + warBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + webDir + ' '
            commandArguments['src.paths'] = '-Dsrc.paths=' + webSrc + ' '
            
            if len(ejbCopyDict[project]) > 0:
                commandArguments['copy.ejbs'] = '-Dcopy.ejbs="' + '|'.join(ejbCopyDict[project]) + '" ' 

        elif build == 'ear':
            earDir = os.path.join(workingLoc, project)

            commandArguments['buildxml'] = '-f ' + earBuild + ' '
            commandArguments['basedir'] = '-Dbasedir=' + earDir + ' '
            commandArguments['src.paths'] = ''

        #commandArguments['classpath.sequence'] = '-Dclasspath.sequence="' + classpathSequence + '" '
        #commandArguments['classpath.count'] = '-Dclasspath.count=' + str(cpCount) + ' '
        antCommand = 'ant ' + commandArguments['buildxml'] + ' ' + antFlags + '-lib ' + parasoftAntJarPath + ' '
        for arg in commandArguments:
            if arg != 'buildxml' and arg != 'CSX_ANT_VERBOSE_ON' and arg != 'CSX_ANT_EMACS_ON' and arg != 'CSX_ANT_ARGUMENTS':
                antCommand += commandArguments[arg]
        
        print 'Custom Build Sequence : ' + str(customSeqSet) + '  Classpath Order : ' + cpOrder
        print ''
        printMsg = build.upper() + ' ANT COMMAND FOR ' + project + ' --------'
        antCommand = buildUtilityFunctionsMaximo.formulateAntCommand(commandArguments, antFlags, parasoftAntJarPath, printMsg)

        run = os.system(antCommand)
        print 'run after ' + build + ' build ' + str(run) + ' project ' + project

        if run != 0:
            print project
            print 'BUILD FAILED'
            sys.exit(1)
        continue
        
        
    # Run EntArch Supplied Artifact Version Ant Buildforge step
    # copyEarBuild.xml
    # This ANT build adds a version to the artifact and copies it to the target distribution directory
    
    commandArguments = buildUtilityFunctionsMaximo.createCopyCommandArgs(copyEarBuild, buildDir, '', earFileName, '', '', project, projectTypes, 'ear')
    antFlags = buildUtilityFunctionsMaximo.setAntFlags(commandArguments)

    print('commandArguments ' + str(commandArguments))

    printMsg = 'RUNNING ANT TO VERSION THE ARTEFACTS --------'
    antCommand = buildUtilityFunctionsMaximo.formulateAntCommand(commandArguments, antFlags, '', printMsg)

    run = os.system(antCommand)
    print 'run after versioning artefacts build ' + str(run) + ' project ' + project

    print 'End : ' + str(datetime.datetime.now())
    
    if run != 0:
        print project
        print 'ARTIFACT VERSIONING FAILED'
        sys.exit(1)

    # Write Websphere version to file so it can be read by buildforge
    websphereVersionFile = open(buildDir + "/wsVersion.txt", "w")
    websphereVersionFile.write("Websphere Version:\nws" + str(wasVersion))
    
    # Must run Jtest when performing a production build
    # Optional to run Jtest when performing any other build
 #==============================================================================
 #    if os.environ['RUN_SECURITY_SCAN'] == 'Yes' or os.environ['CSX_CLEARCASE_BUILD_VERSION'] == 'prod':
 #        # Run Parasoft Jtest on each of the compiled projects
 #        dataPath = buildDir + '/JtestWorkspace/'
 #        jtestPath = os.path.join(os.environ['JTEST_HOME'], 'jtestcli')
 #         
 #        commandArguments.clear()
 #        commandArguments['config'] = '-config "builtin://Static Analysis" '
 #        commandArguments['data'] = '-data "' + dataPath + '" '
 #        commandArguments['localsettings'] = '-localsettings "' + os.environ['JTEST_LOCAL_SETTINGS_PATH'] + '" '
 #        #commandArguments['nobuild'] = '-nobuild '
 #        #commandArguments['showdetails'] = '-showdetails '
 #         
 #        for project in buildSequence:
 #            # Load the project modules into the Jtest workspace
 #            projectDir = os.path.join(workingLoc, project)
 #            commandArguments['import'] = '-import "' + projectDir + '" '
 #             
 #            jtestCommand = jtestPath + ' ' + commandArguments['data'] + ' ' + commandArguments['import'] + ' '
 # 
 #            print ('\n----------LOADING ' + project + ' INTO WORKSPACE FOR JTEST-------------')
 #            print (jtestCommand)
 #                             
 #            run = os.system(jtestCommand)
 #         
 #            if run != 0:
 #                print 'LOAD FAILED'
 #                sys.exit(1)
 # 
 #            print ('---------------------------LOADING COMPLETE------------------------------')
 #                 
 #     
 #        jtestReportDest = os.path.join(buildDir, 'JtestOutput' + '/')
 #        commandArguments['report'] = '-report "' + jtestReportDest + '" '
 #     
 #        jtestCommand = jtestPath + ' '
 #         
 #        for arg in commandArguments:
 #            if arg != 'import':
 #                jtestCommand += commandArguments[arg]
 #             
 #        print ('\n---------------------------RUNNING JTEST------------------------------')
 #        print (jtestCommand)
 #         
 #        startTime = time.time()                
 #        run = os.system(jtestCommand)
 #        endTime = time.time()
 #     
 #        if run != 0:
 #            print 'JTEST FAILED'
 #            sys.exit(1)
 #             
 #        print ('JTEST EXECUTION TIME: ' + str(endTime - startTime) + " SECONDS")
 #         
 #        print ('---------------------------JTEST COMPLETE------------------------------')
 #==============================================================================
        
