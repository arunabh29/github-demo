import os.path
import re
# import shutil
# import sys
import xml.etree.ElementTree as xml

defaultCPSeq  = "WEBSPHERE, COMMON, MODULE, EAR"
jsf2WAS7CPSeq = "MODULE, WEBSPHERE, COMMON, EAR"
#------------------------------------------------------
# Map library RefIds to Types 
#-------------------------------------------------------

def buildRefIds():
    libTypes = ["WEBSPHERE", "COMMON", "MODULE", "EAR"] 
    libRefIds = ["ext.classpath", "common.classpath", "module.compile.classpath", "ear.lib.classpath"] 
    
    libsDict = dict(zip(libTypes, libRefIds)) 
    for key,val in libsDict.items():
        print key, "=>", val

    return libsDict
    
#------------------------------------------------------------
# Reset the command arguments for special classpath sequence 
#------------------------------------------------------------

def resetClasspathSeq(commandArguments, classpathSequence):
    libsDict = buildRefIds()
    customClasspathSequence = ''
    cpCount = 0
    print (classpathSequence.replace(' ', '').split(','))
    for path in classpathSequence.replace(' ', '').split(','):
        customClasspathSequence += libsDict[path]
        customClasspathSequence += ' '
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
        
    customClasspathSequence = customClasspathSequence.strip(' ')
    customClasspathSequence = '' + customClasspathSequence + ''
    commandArguments = createClasspathSeq(commandArguments, customClasspathSequence)
    
    return commandArguments;

#------------------------------------------------------
# Find JDK version 
#-------------------------------------------------------

def parseJDKVersion(jdkVersion):
    jdkRegex = re.compile(r'^([-+]?)([0-9]*)(\.?)([0-9]+)$')
    matchObj = jdkRegex.search(jdkVersion)
    
    try:
        if not matchObj:
            print 'Invalid JDK version Provided : ' + jdkVersion + '- Using default version, 7'
            jdkVersion = '7'
            matchObj = jdkRegex.search(jdkVersion)
    except:
        print 'Unknown Error : ' + jdkVersion
        raise 

    if(len(jdkVersion)):
        if (float(jdkVersion) % 1 == 0):
            javaVersion = matchObj.group(2) if matchObj.group(2) else matchObj.group(4)
            javaVersion = int(float(jdkVersion))
        else:
            javaVersion = javaVersion = matchObj.group(4) if matchObj.group(4) else 7
    else:
        javaVersion = 7

    print 'jdkVersion from parseJDKVersion ' + str(javaVersion)
    return javaVersion

def createFullBuildCommandArgs (currentBuildModule, buildDir, projectTypes, projectDependency, websphereLocFromEnv, earDir, earFileName, libDir, customClasspathSequence, customSeqSet, excludeStarTestJava):
    commandArguments = createCommonCommandArgs(currentBuildModule, buildDir, projectTypes, projectDependency, '')
    commandArguments = createClasspathSeq(commandArguments, customClasspathSequence)
    commandArguments['custom.seq'] = '-Dcustom.seq.set=' + str(customSeqSet) + ' '

    commandArguments['compile.lib.dir'] = '-Dcompile.lib.dir=' + websphereLocFromEnv + ' '
    commandArguments['ear.libs.dir'] = '-Dear.libs.dir=' + earDir + ' '
    commandArguments['library.directory'] = '-Dlibrary.directory=' + libDir + ' '
    commandArguments['ear.name'] = '-Dear.name=' + earFileName + ' '
    commandArguments['custom.classpath.sequence'] = '-Dcustom.classpath.sequence="' + customClasspathSequence + '" '

    commandArguments['exclude.starTest.java'] = '-Dexclude.starTest.java=' + excludeStarTestJava + ' '

    return commandArguments

def createClasspathSeq(commandArguments, customClasspathSequence) :
    if(customClasspathSequence != '0') :
        print 'customClasspathSequence != 0 ' + customClasspathSequence
        classPaths = customClasspathSequence.split()
        for idx, val in enumerate(classPaths):
            print 'idx ' + str(idx) + ' val ' + str(val)
            v1 = 'seq.' + str(idx+1)
            print (v1)
            commandArguments["'" + v1 + "'"] = '-D' + v1 + '=' + val + ' '
    else :
        print 'customClasspathSequence == 0 ' + customClasspathSequence
    return commandArguments

def createCommonCommandArgs(currentBuildModule, buildDir, projectTypes, projectDependency, gsModuleName):
    commandArguments = getAntFlags()
    commandArguments['buildxml'] = ''
    commandArguments['basedir'] = ''
    commandArguments['build.dir'] = '-Dbuild.dir=' + buildDir + ' '
    commandArguments['src.paths'] = ''
    commandArguments['project.types'] = '-Dproject.types="' + str(projectTypes) + '" '
    commandArguments['project.dependency'] = '-Dproject.dependency="' + str(projectDependency) + '" '
    if (currentBuildModule == 'antParseUtil.py' or currentBuildModule == 'antParseGigaspaces.py'):
        commandArguments['jaronly.build'] = '-Djaronly.build=true '

        # Find the websphere location from the environment
        websphereLocFromEnv = os.environ[ os.environ['WAS_DEFAULT_VERSION'] + '_DIRECTORY']
        commandArguments['compile.lib.dir'] = '-Dcompile.lib.dir=' + str(websphereLocFromEnv) + ' '

        if (currentBuildModule == 'antParseGigaspaces.py'):
            commandArguments['gigaspace.build'] = '-Dgigaspace.build=true '
            commandArguments['gigaspace.module.name'] = '-Dgigaspace.module.name="' + str(gsModuleName) + '" '

    return commandArguments

def createCopyCommandArgs(copyBuild, buildDir, jarFileName, earDirName, subDirName, appPrefix, project, projectTypes, sourceType):

    commandArguments = getAntFlags()
    commandArguments['buildxml'] = '-f ' + copyBuild + ' '
    commandArguments['basedir'] = '-Dbasedir=' + buildDir + ' '
    commandArguments['targetDistDir'] = '-DtargetDistDir=' + os.environ['CSX_INSTALLABLEAPPS'] + '/' + earDirName + '/' + subDirName + ' '
    commandArguments['buildVersionNumber'] = '-DbuildVersionNumber=' + os.environ['B'] + ' '
    commandArguments['clearCaseVersion'] = '-DclearCaseVersion=' + os.environ['CSX_CLEARCASE_BUILD_VERSION'] + ' '
    commandArguments['sourceDistDir'] = '-DsourceDistDir=' + buildDir + '/' + projectTypes[sourceType][0] + ' '

    if len(appPrefix) > 0:
        commandArguments['app.name'] = '-Dapp.name=' + appPrefix + ' '
    else:
        commandArguments['app.name'] = '-Dapp.name=' + earDirName + ' '
    
    if len(jarFileName) > 0:
        commandArguments['jar.name'] = '-Djar.name=' + jarFileName + ' '
    else:
        commandArguments['jar.name'] = '-Djar.name=' + project + ' '

    print('commandArguments ' + str(commandArguments))
    return commandArguments

def getAntFlags():
    commandArguments = {}
    commandArguments['CSX_ANT_VERBOSE_ON'] = os.environ['CSX_ANT_VERBOSE_ON'] + ' '
    commandArguments['CSX_ANT_EMACS_ON'] = os.environ['CSX_ANT_EMACS_ON'] + ' '
    commandArguments['CSX_ANT_ARGUMENTS'] = os.environ['CSX_ANT_ARGUMENTS'] + ' '
    return commandArguments

def setAntFlags(commandArguments):    
    antFlags = (commandArguments['CSX_ANT_VERBOSE_ON'] + ' '
                + commandArguments['CSX_ANT_EMACS_ON'] + ' '
                + commandArguments['CSX_ANT_ARGUMENTS'] + ' ')
    return antFlags

def formulateAntCommand(commandArguments, antFlags, parasoftAntJarPath, printMsg):
    antCommand = 'ant ' + commandArguments['buildxml'] + ' ' + antFlags
    if(len(parasoftAntJarPath) > 0):
        antCommand += ' -lib ' + parasoftAntJarPath + ' '

    for arg in commandArguments:
        if arg != 'buildxml' and arg != 'CSX_ANT_VERBOSE_ON' and arg != 'CSX_ANT_EMACS_ON' and arg != 'CSX_ANT_ARGUMENTS':
            antCommand += commandArguments[arg]
    
    print '-------- START OF ' + printMsg
    print antCommand
    print '---------- END OF ' + printMsg
    
    return antCommand

def parseGSVersion(gsVersion):
    print 'gsVersion ' + gsVersion
    # This below works. Trying different versions
    # gsRegex = re.compile(r'^([-+]?)(([0-9]*)((\.?)([0-9]))*)$')
    
    # (.+(\..+)+) - Anything
    # (\w+(\.\w+)+) - Any alpha numeric
    gsRegex = re.compile(r'^(\d+(\.\d+)*)$')
    matchObj = gsRegex.search(gsVersion)
    
    try:
        if not matchObj:
            print 'Invalid Gigaspace version Provided : ' + gsVersion
            raise
        else:
            gigaspaceVersion = gsVersion
    except:
        print 'Unknown Error : ' + gsVersion
        raise 

    print 'gigaspaceVersion from parseGSVersion ' + str(gigaspaceVersion)
    return gigaspaceVersion

def getJDKVersionForWebsphere(websphereVersion):
    if websphereVersion == '7':  # if websphere version is 7, jdk version is 6
        jdkVersion = 6
    elif wasVersion == '8':  # if webpshere version is 8, jdk version is 6
        jdkVersion = 7
    else:  # if webpshere version is not 6 or 7, jdk version is 7
        jdkVersion = 7
    return jdkVersion

def miscTests():
    print '1 : ' + inspect.getfile(inspect.currentframe())  # script filename (usually with path)
    print '2 : ' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
    print '3 : ' + os.path.basename(inspect.getfile(inspect.currentframe()))  # script name
     
    scrDirs = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).split(os.sep)
    print 'scrDirs ' + str(scrDirs) + ' len of list ' + str(len(scrDirs))
 
    print os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).split(os.sep)[0]
    
    
#------------------------------------------------------
# Check <WEB Project(s)>/.settings/org.eclipse.wst.common.component
# If <dependent-module archiveName="<EJB>.jar" ... > exists
# Then indicate that we will need to copy <EJB>.jar(s) artifact to
# <WEB>.war(s)/WEB-INF/lib/
#-------------------------------------------------------
def copyEJBForREST(workingLoc, webProjects, ejbProjects):
    # Return a dictionary, where the WEB project name is the key
    # and the value is a list of EJBs that need to be copied
    # into <WEB>.war/WEB-INF/lib/
    DEPENDENT_MODULE_XML_PATH = "/.settings/org.eclipse.wst.common.component"
    DEPENDENT_MODULE_XML_TAG = "dependent-module"
    DEPENDENT_MODULE_ARCHIVE_NAME_TAG = "archiveName"
    extPattern = '\.[jw]ar$'
    EMPTY_STRING = ''
    ejbCopyDict = {}

    for project in webProjects:
        ejbCopyDict[project] = []
        dependentModuleXMLPath = os.path.join(workingLoc, project 
                                              + DEPENDENT_MODULE_XML_PATH)
        xmlRoot = xml.parse(dependentModuleXMLPath).getroot().getiterator()
                        
        for dependentModule in xmlRoot:
            if DEPENDENT_MODULE_XML_TAG == dependentModule.tag:
                archiveName = re.sub(extPattern,
                                     EMPTY_STRING,
                                     dependentModule.attrib[DEPENDENT_MODULE_ARCHIVE_NAME_TAG])
                if archiveName in ejbProjects:
                    ejbCopyDict[project].append(archiveName)
                    
    return ejbCopyDict
                
            
