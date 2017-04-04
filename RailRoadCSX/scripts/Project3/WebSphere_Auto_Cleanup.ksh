########################################################################################
# Non-editable variables section
########################################################################################

PYTHON_SCRIPT_LOC=/opt/shared/atlassian/bamboo/buildfiles/buildforge/leapfrog
CSX_PROJECT_BASEDIR=${bamboo.build.working.directory}
WAS_DIR=/opt/local/scripts

BUILD_VERSION=`echo ${bamboo_planRepository_branch} | grep -o '..$'`

if [ ${BUILD_VERSION} == op ]
    then
        cd /opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/DEV
        echo Removing all but the last three build directories.
        echo Removing these directories: `ls -t | awk 'NR>3'`
        ls -t | awk 'NR>3' | xargs rm -rf
fi


if [ ${BUILD_VERSION} == st ]
    then
        cd /opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/UAT
        echo Removing all but the last three build directories.
        echo Removing these directories: `ls -t | awk 'NR>3'`
        ls -t | awk 'NR>3' | xargs rm -rf
fi

if [ ${BUILD_VERSION} == er ]
    then
        cd /opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/PROD
        echo Removing all but the last three build directories.
        echo Removing these directories: `ls -t | awk 'NR>3'`
        ls -t | awk 'NR>3' | xargs rm -rf
fi


# Cleanup the build working directory
echo Removing working directory: ${bamboo_build_working_directory}
rm -rf ${bamboo_build_working_directory}