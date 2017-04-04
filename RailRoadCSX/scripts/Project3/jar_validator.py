#!/usr/bin/python

import hashlib
import os

import j2ee_utils
import email_manager
import blacklisted_jar

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    
    return hash.hexdigest()

class JarValidator(object):

    # EMAIL Configurations
    SENDER = 'Dev_Ops@csx.com'
    SUBJECT = 'Security Vulnerability Detected in Recent Build'
    BODY = """****** IMPORTANT SECURITY NOTICE *********
    
        There is a security vulnerability in the following JAR file identified in your recent build:
                %s
            
        To protect our environment and your application, please make plans to update this JAR to the following version:
                %s
            
        CSX will track risks related to this vulnerability and may restrict future builds unless this component is updated. Please update to the version suggested above to ensure a secure deployment.
        
        Please contact the Information Security department if you have any questions.
    
****** IMPORTANT SECURITY NOTICE *********
    """
    
    # Error messages
    MISSING_EAR_ERR = 'JAR Validator Error: Failed to identify the application EAR project.'
    BLACKLISTED_JAR_ERR = 'JAR Validator Error: Identified blacklisted JAR file in the application.'

    # Blacklisted JAR information
    BLACKLISTED_JAR_NAMES = ['commons-collections-3.2.1.jar', 'commons-collections4-4.0.jar']
    BLACKLISTED_JAR_MD5_CHKSUMS = ['13bc641afd7fd95e09b260f69c1e4c91', 'a18f2d0153b5607dff8c5becbdd76dd1']
    BLACKLISTED_JARS = [blacklisted_jar.BlacklistedJar('commons-collections-3.2.1.jar', '13bc641afd7fd95e09b260f69c1e4c91',
        'http://repo.csx.com/service/local/repositories/central/content/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar'),
        blacklisted_jar.BlacklistedJar('commons-collections4-4.0.jar', 'a18f2d0153b5607dff8c5becbdd76dd1',
        'http://repo.csx.com/service/local/repositories/central/content/org/apache/commons/commons-collections4/4.1/commons-collections4-4.1.jar')]

    def __init__(self, source_location, ear_project, build_user_email, fail_build=None, send_fail_email=None):
        self.__source_location = source_location
        self.__ear_project = ear_project if not j2ee_utils.is_empty_ear_project(ear_project) \
            else j2ee_utils.get_application_ear_project(self.get_source_location())
        
        if not self.get_ear_project():
            print(self.MISSING_EAR_ERR)
            sys.exit(-1)
        
        self.__projects = j2ee_utils.get_all_projects_in_application(\
            self.get_source_location(), self.get_ear_project())
        self.__ear_library = j2ee_utils.get_library_directory(self.get_ear_project(), \
            self.get_source_location())
        self.__project_jar_files = j2ee_utils.get_project_jar_files(self.get_source_location(), \
            self.get_projects())
        self.__build_user_email = build_user_email
        self.__fail_build = fail_build
        self.__send_fail_email = send_fail_email
    
    def get_source_location(self):
        return self.__source_location
        
    def get_ear_project(self):
        return self.__ear_project
        
    def get_projects(self):
        return self.__projects
        
    def get_ear_library(self):
        return self.__ear_library
        
    def get_project_jar_files(self):
        return self.__project_jar_files
        
    def get_build_user_email(self):
        return self.__build_user_email
        
    def should_fail_build(self):
        return self.__fail_build
        
    def should_send_fail_email(self):
        return self.__send_fail_email
        
    # Send email to person who invoked build if send_fail_email=True
    def conditionally_send_email(self, jar, updated_jar):
        if self.should_send_fail_email():
            e_mgr = email_manager.EmailManager(self.SENDER, self.get_build_user_email(), \
                self.SUBJECT, self.BODY % (jar, updated_jar))
            e_mgr.send_email()
    
    # Return -1 to fail buildforge build if fail_build=True.
    # Else, return 0 and allow build to continue.
    def get_blacklisted_jar_found_error_code(self):
        return -1 if self.should_fail_build() else 0
    
    def __print_blacklisted_jar_err(self, jar):
        print (self.BLACKLISTED_JAR_ERR)
        print ('\t' + jar)
    
    def __find_blacklisted_jar(self, jar):
        for blacklisted_jar in self.BLACKLISTED_JARS:
            if jar[jar.rfind(os.path.sep)+1:] in blacklisted_jar or md5sum(jar) in blacklisted_jar:
                return blacklisted_jar
        return None
    
    def run(self):
        # Check if blacklisted jars exist in application by name or if md5 checksum matches
        for jar in self.get_project_jar_files():
            blacklisted_jar = self.__find_blacklisted_jar(jar)
            
            if blacklisted_jar:
                self.__print_blacklisted_jar_err(jar)
                self.conditionally_send_email(jar, blacklisted_jar.get_suggested_jar_name())
                return self.get_blacklisted_jar_found_error_code()
        return 0
