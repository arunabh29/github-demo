#!/usr/bin/python

import sys

import jar_validator

SOURCE_LOCATION_ARG = '-srcLoc'
EAR_PROJECT_ARG = '-earProj'
BUILD_USER_EMAIL_ARG = '-userEmail'
CMD_ARG_SEP = '='

MISSING_SRC_LOC_ARG_ERR = 'JAR Validation Error: srcLoc is a mandatory argument.'
MISSING_EMAIL_ARG_ERR = 'JAR Validation Error: userEmail is a mandatory argument.'
  
def main():
    # Get the arguments passed via the command line
    source_location, ear_project, build_user_email = parse_cmd_args()
    
    # Verify source location was passed via the command line
    if not source_location:
        print(MISSING_SRC_LOC_ARG_ERR)
        return -1
    
    # Verifiy build user email was passed via the command line
    if not build_user_email:
        print(MISSING_EMAIL_ARG_ERR)
        return -1
    
    validator = jar_validator.JarValidator(source_location, ear_project, \
        build_user_email, send_fail_email=True)
    return validator.run()
    
def parse_cmd_args():
    src_loc = ear_proj = build_user_email = None
    
    if (1 < len(sys.argv)):
        for arg in sys.argv[1:]:
            key, value = arg.split(CMD_ARG_SEP)
            
            if SOURCE_LOCATION_ARG == key:
                src_loc = value
            elif EAR_PROJECT_ARG == key:
                ear_proj = value
            elif BUILD_USER_EMAIL_ARG == key:
                build_user_email = value
        
    return src_loc, ear_proj, build_user_email
    
if __name__ == '__main__':
    sys.exit(main())