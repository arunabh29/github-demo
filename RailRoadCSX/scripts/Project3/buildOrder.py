
import os.path
import sys

# -------------------------------------------------------------
# Determine the order in which the projects should be built by
# passing the ear project as the initial project parameter
# Parameter(s): project - the current project being evaluated
#               projectDependency - the projects which the current
#               project parameter is dependent upon
# -------------------------------------------------------------
def getBuildOrder(project, projectDependency, projectDependencyDict):
    for p in projectDependency:
        if project in projectDependencyDict[p]:
            print ("This application contains a circular dependency:")
            print ("\t" + project + " is dependent upon " + str(projectDependency))
            print ("\t" + p + " is dependent upon " + str(projectDependencyDict[p]))
            print 'BUILD FAILED'
            sys.exit(1)
    
    if len(projectDependency) == 0:
        return project
    
    return getBuildOrder(projectDependency[0], projectDependencyDict[projectDependency[0]], projectDependencyDict) + ' ' + getBuildOrder(project, projectDependency[1:], projectDependencyDict)
    
    
# -------------------------------------------------------------------
# creates a set and maintains the order of the list
# -------------------------------------------------------------------
def createSet(l):
    ret = []
    for x in l:
        if not x in ret:
            ret.append(x)
    return ret

# -------------------------------------------------------------------
# Swaps the positions in the list
# -------------------------------------------------------------------
def swap(index1, index2, l):
    temp = l[index1]
    l[index1] = l[index2]
    l[index2] = temp
    return l

# -------------------------------------------------------------------
# Utility projects need to be built first.  This reorders the project
# build order.
# Parameter(s): buildSequence - build order list
#               projectTypes - dictionary that designates a project as
#                              util, ear, web, or ejb
# -------------------------------------------------------------------
def buildUtilsFirst(buildSequence, projectTypes):
    for i in range(len(buildSequence)):
        if [k for k, v in projectTypes.items() for prj in v if prj == buildSequence[i]][0] == 'util':
            tempIndex = i
            while (tempIndex != 0 and [k for k, v in projectTypes.items() for prj in v if prj == buildSequence[tempIndex-1]][0] != 'util'):
                buildSequence = swap(tempIndex-1, tempIndex, buildSequence)
                tempIndex -= 1
    return buildSequence
                 