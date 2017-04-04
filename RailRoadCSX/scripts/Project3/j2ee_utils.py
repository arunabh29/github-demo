#!/usr/bin/python

import os
import xml.etree.ElementTree as xml

PROJECT_FILE = '.project'
PROJECTS_XML_TAG = 'projects'
APPLICATION_FILE = 'application.xml'

#-------------------------------------------------------------------------------------------
# Function: is_empty_ear_project
# Parameter(s): ear_project - ear project name
# Description: Returns True if ear_project is "", empty string, or None. Else, None.
#-------------------------------------------------------------------------------------------
def is_empty_ear_project(ear_project):
    return '""' == ear_project or '' == ear_project \
        or None == ear_project

#-------------------------------------------------------------------------------------------
# Function: get_application_ear_project
# Parameter(s): source_location - path to the application project files
# Description: Searches for the application's ear project.  Returns the name of the ear
#              project if found. Else, None.
#-------------------------------------------------------------------------------------------
def get_application_ear_project(source_location):
    project_names = os.listdir(source_location)
    
    for project in project_names:
        current_location = os.path.join(source_location, project)
        
        for root, dirs, files in os.walk(current_location):
                for file_name in files:
                    if file_name == APPLICATION_FILE:
                        return project
    
    return None

#-------------------------------------------------------------------------------------------
# Function: get_all_project_in_application
# Parameter(s): source_location - path to the application project files
#               ear_project_name - the ear project name
# Description: Parses the EAR's .project file.  Returns a list of all the projects in this
#              application if able.  Else, None.
#-------------------------------------------------------------------------------------------
def get_all_projects_in_application(source_location, ear_project_name):
    project_names = [__format_path(ear_project_name)]
    
    # Get the EAR file's root directory
    ear_project_root_dir = os.path.join(source_location, ear_project_name)
    
    # Get the EAR's .project file
    ear_project_file = __get_project_file(ear_project_root_dir)
    
    # .project file not found
    if (not ear_project_file):
        return None
    
    # Identify the projects associated with the EAR by reading the children of the
    # 'projects' tag in the .project file.
    parse_project_file = xml.parse(ear_project_file).getroot()
    projs = [projects for projects in parse_project_file.findall(PROJECTS_XML_TAG)]
    for p in projs:
        for child in p.getchildren():
            project_names.append(__format_path(child.text))

    return project_names

#-------------------------------------------------------------------------------------------
# Function: get_project_file
# Parameter(s): ear_project_root_dir - path to the EAR project root directory
# Description: Gets the EAR's .project file.  Returns the EAR's .project file location if
#              found.  Else, None.
#-------------------------------------------------------------------------------------------
def __get_project_file(ear_project_root_dir):
    for root, dirs, files in os.walk(ear_project_root_dir):
        for file in files:
            if file == PROJECT_FILE:
                return os.path.join(root, PROJECT_FILE)
    return None

#-------------------------------------------------------------------------------------------
# Function: format_path
# Parameter(s): path - path
# Description: Adds path separator to the end of the path if does not already exist.
#-------------------------------------------------------------------------------------------
def __format_path(path):
    if not path.endswith(os.path.sep):
        path += os.path.sep
    
    return path
    
#------------------------------------------------------------------------
# Determine the library directory based on the <library-directory>
# tag in the application.xml within the EAR project folder/META-INF/.
# The default value is 'lib'.
# Parameter(s): ear_file_name - name of the applications EAR project folder
#               working_loc - path to the application's working location
#------------------------------------------------------------------------
def get_library_directory(ear_file_name, working_loc):
    library_directory = 'lib'
    application_path = os.path.join(working_loc, ear_file_name + '/META-INF/application.xml')
    xml_tags = xml.parse(application_path).getroot().getiterator()
    for t in xml_tags:
        if (t.tag.endswith('library-directory')):
            library_directory = t.text
    return library_directory
    
#------------------------------------------------------------------------
# Determine the list of jar files being used within the application. The
# list contains the complete path to the jar file.
# Parameter(s): source_loc - path to the application's source location
#               project_names - list of project names in the application
#------------------------------------------------------------------------
def get_project_jar_files(source_loc, project_names):
    jar_files = []
    for project in project_names:
            current_loc = os.path.join(source_loc, project)
            for root, dirs, files in os.walk(current_loc):
                for fname in files :
                    if fname.endswith('.jar'):
                        jar_files.append(root + os.path.sep + fname)
    return jar_files