import glob
import os
import sys
import time
import inspect
from macpath import curdir

def getJarsInFolder(folderLocation):
	jarFiles = []    	
	for root, dirs, files in os.walk(folderLocation):
		for fname in files :
			if fname.endswith('.jar'):			
				jarFiles.append(root + '/' + fname)
	return jarFiles

def sourceArgument(sourceLocation, buildOutputLocation):
	validFolder = os.listdir(buildOutputLocation)
	validSource = ['src', 'ejbModule', 'WebContent']
	srcArgument = []
	for folder in validFolder:		
		for root, dirs, files in os.walk(sourceLocation + '/' + folder):
			for dir in dirs :
				if (dir in validSource):
					srcArgument.append('-source ' + root + '/' + dir)	
	return ' ' + ' '.join(srcArgument)
	
def isNoneOrEmptyOrBlankString (checkString):
    isNullEmptyBlank = True
    if checkString and checkString.strip() :
        isNullEmptyBlank = False
    return isNullEmptyBlank

def isPositiveNumber (inValue):
    isPosNumber = False
    if not isNoneOrEmptyOrBlankString(inValue):
	    num_format = re.compile(r'^[+]?([0-9]+(?:[\.][0-9]*)?|\.[0-9]+)$')
	    isNonNegativeNumber = re.match(num_format, inValue)
	    if isNonNegativeNumber and float(isPosNumber.group()) > 0.0:
	    	isPosNumber = True
    return isPosNumber

minSpaceHours = 24.0
jtestCliPath = '/opt/local/software/jtest/parasoft/jtest/9.5/jtestcli'

curDir = os.path.dirname(os.path.abspath(__file__))
curWorkingDir = os.getcwd()
parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), os.pardir))

print 'curDir : ' + curDir + ' parentDir : ' + parentDir

jtestSettingsLoc = os.path.join(curDir, 'csxjtest.settings')
jtestRulesProps = os.path.join(curDir, 'csxjtestRules.properties')

print 'jtestSettingsLoc ' + jtestSettingsLoc
print 'jtestRulesProps ' + jtestRulesProps

	
workingLocSet = False
buildDirSet = False
scriptsHomeSet = False
minSpaceHoursSet = False
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
	elif keys[0] == 'scriptsHome':
		CSX_SCRIPTS_HOME = keys[1]
		scriptsHomeSet = True
		continue
	elif keys[0] == 'jtestCliPath':
		jtestCliPath = keys[1]       
		continue
	elif keys[0] == 'minSpaceHours':
		rerunInterval = keys[1]
		if isPositiveNumber(rerunInterval) :
			minSpaceHours = float(rerunInterval)
			if(minSpaceHours > 24.0) :
				minSpaceHours = 24.0
			minSpaceHoursSet = True
			continue

if (not (workingLocSet and buildDirSet and scriptsHomeSet)):
	print "workingLoc, buildDir and scriptsHome all required. jtestCliPath, minSpaceHours optional."
	sys.exit(1)

# reportName
CSX_CLEARCASE_BUILD_VERSION = os.environ["CSX_CLEARCASE_BUILD_VERSION"]
reportFileName = 'reportParasoft-' + CSX_CLEARCASE_BUILD_VERSION + '.html'

# Find Last Execution to see if execution is needed
newestReport = 'No previous Parasoft report detected.'
newestTime = 0
higherLevel = os.path.dirname(buildDir)
for fullName in [os.path.join(higherLevel, f, reportFileName) for f in os.listdir(higherLevel) if os.path.exists(os.path.join(higherLevel, f, reportFileName))]:
	if (os.path.getmtime(fullName) > newestTime):
		newestTime = os.path.getmtime(fullName)
		newestReport = fullName
print 'MOST RECENT PREVIOUS PARASOFT REPORT FOR ' + CSX_CLEARCASE_BUILD_VERSION.upper() + ': ' + newestReport
if (newestTime > 0):
	deltaHours = (time.time() - newestTime) / 3600
	print ('==> Generated on: ' + time.ctime(newestTime)
	+ ", Delta: " + str(round(deltaHours, 1)) + " hours" + ' or ' + str(round(deltaHours / 24, 1)) + " days.")
	if (deltaHours > minSpaceHours):
		print "==> Parasoft execution needed since delta more than " + str(minSpaceHours) + " hours."
	else:
		print "==> Parasoft execution skipped at this time since less than " + str(minSpaceHours) + " hours. "
		sys.exit()
		
		
# We start with an empty Classpath
classpath = ''

# Source JARs
validFolder = os.listdir(buildDir)
for folder in validFolder:		
	jar_files = getJarsInFolder(workingLoc + '/' + folder)
	classpath = classpath + ':' + ':'.join(jar_files)

# Build distribution JARs
jar_files = getJarsInFolder(buildDir)
classpath = classpath + ':' + ':'.join(jar_files)

# Common compile JARs
commonCompileLibFolder = '/opt/local/software/bfviewstorage/BF_SOURCE/leapfrog/CompileLibs';
commonCompileLib_jar_files = getJarsInFolder(commonCompileLibFolder)
classpath = classpath + ':' + ':'.join(commonCompileLib_jar_files)
 
# WebSphere JARs
wsLibFolder = '/opt/local/software/websphere/v8/plugins'
ws_jar_files = getJarsInFolder(wsLibFolder)
classpath = classpath + ':' + ':'.join(ws_jar_files)

# Set the Classpath as environment variable for JTestCli consumption
os.environ["CLASSPATH"] = classpath


# Generate Command Line
jTestExecute = (jtestCliPath 
			+ ' -config ' + jtestRulesProps 
			+ sourceArgument(workingLoc, buildDir)
			+ ' -localsettings ' + jtestSettingsLoc
			+ ' -report ' + buildDir + '/' + reportFileName
			+ ' -publish'
			+ ' -data ' + buildDir + '/JTestWorkspace'
			)

# look for the presence of concurrent execution
os.system("ls -la /tmp | grep 'nexus-maven-repository'")
			
# Execute JTestCli
print jTestExecute
os.system(jTestExecute)

# Remove leftover nexus-maven-repository files
os.system("ls -la /tmp | grep 'nexus-maven-repository'")
os.system("du -hc /tmp/nexus-maven-repository* | grep 'total'")
os.system("rm -Rf /tmp/nexus-maven-repository*")
os.system("rm -Rf ~/.m2/repository/.cache/*")


