import sys

#-------------------------------------------------------------
#Approved Jar files 
#-------------------------------------------------------------
def getApprovedjars(jarFile,jarFiles):
    approvedProjectJars = []
    notApprovedJars = []
    try:
        approvedJarList = [line.strip() for line in open(jarFile)]
    except:
        print
        print 'Approved jar file was not found'
        print 'approvedJars.txt should be in CSX_SCRIPTS_HOME directory'
        sys.exit(1)
    for jars in jarFiles:
        for approvedJars in approvedJarList:
            if jars.startswith(approvedJars):
                approvedProjectJars.append(jars)
    notApprovedJars = [x for x in jarFiles if x not in approvedProjectJars]
    print "Non-Approved Jar Files: ", notApprovedJars
    return notApprovedJars
