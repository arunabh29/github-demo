import xml.etree.ElementTree as xml
import os

#------------------------------------------------------------------------
# Determine the library directory based on the <library-directory>
# tag in the application.xml within the EAR project folder/META-INF/.
# The default value is 'lib'.
# Parameter(s): earFileName - name of the applications EAR project folder
#               workingLoc - path to the application's working location
#------------------------------------------------------------------------
def determineLibraryDirectory(earFileName, workingLoc):
    libraryDirectory = 'lib'
    applicationPath = os.path.join(workingLoc, earFileName + '/META-INF/application.xml')
    xmlTags = xml.parse(applicationPath).getroot().getiterator()
    for t in xmlTags:
        if (t.tag.endswith('library-directory')):
            libraryDirectory = t.text
    return libraryDirectory