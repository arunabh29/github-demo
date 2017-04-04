__author__ = 'a3577'
import sys
from shutil import copytree, rmtree, copyfile
import os
import stat
# this program copies the files from a view to a new directory,
# marks all the files as readwrite
# copies any file that ends with "." + the env variable passed in the command line to the base part of the file
# for example a.b.xml.dev is copied over a.b.xml in the same directory
# requires environment, source and target directories for input variables
# we may restrict it to only the adapter and apns directories which is why we capture those
envSet = False
rootDirSet = False
appRootDirSet = False
targetDirSet = False

env = ""
fileList = []
apnDir = ""
adapterDir = ""
#Assign identifiers
for arg in sys.argv:
    keys = arg.split('=')
    if keys[0] == 'env':
        envSet = True
        env = keys[1]
        continue
    if keys[0] == 'rootDir':
        rootDirSet = True
        rootDir = keys[1]
        continue
    if keys[0] == 'targetDir':
        targetDirSet = True
        targetDir = keys[1]
        continue
    if keys[0] == 'appRootDir':
        appRootDirSet = True
        appRootDir = keys[1]
        continue
#die if nothing set
if not envSet or not rootDirSet or not targetDirSet or not appRootDirSet:
    print 'Must set env, rootDir, targetDir and appRootDir variables e.g. copyfile env=dev rootDir=/a/b/c'
    sys.exit(1)

if os.path.isdir(targetDir):
    rmtree(targetDir)

copytree(rootDir,targetDir)

listOfSpecificDirs = []

for root, dirs, files in os.walk(targetDir):
    for fname in files:
        full_path = os.path.join(root, fname)
        os.chmod(full_path ,stat.S_IWRITE)
        if fname.__len__() > env.__len__():
            startPos = fname.__len__() - env.__len__() - 1
            if fname.find("."+env,startPos) > -1:
                fileList.append(full_path)

    for dirName in dirs:
        full_path = os.path.join(root, dirName)
        os.chmod(full_path,stat.S_IWRITE)
        if dirName == 'adapters':
            adapterDir = full_path
        if dirName == 'apns':
            apnDir = full_path



for file in fileList:
    baseFileName = file[0:file.__len__()-env.__len__()-1]
    copyfile(file,baseFileName)

if env <> "prod":
    copyfile(apnDir+os.sep+"apns-certificate-sandbox.p12", appRootDir+os.sep+"apns-certificate-sandbox.p12")
else:
    copyfile(apnDir+os.sep+"apns-certificate-production.p12", appRootDir+os.sep+"apns-certificate-production.p12")