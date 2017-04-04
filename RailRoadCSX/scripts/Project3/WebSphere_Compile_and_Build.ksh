########################################################################################
# DO NOT edit this section
########################################################################################
PYTHON_SCRIPT_LOC=/opt/shared/atlassian/bamboo/buildfiles/buildforge/leapfrog
CSX_PROJECT_BASEDIR=${bamboo.build.working.directory}
BUILD_VERSION=`echo ${bamboo_planRepository_branch} | grep -o '..$'`

if [ ${BUILD_VERSION} == op ]
    then
        BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/DEV/BUILD_${bamboo_buildNumber}
fi


if [ ${BUILD_VERSION} == st ]
    then
        BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/UAT/BUILD_${bamboo_buildNumber}
fi

if [ ${BUILD_VERSION} == er ]
    then
        BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/PROD/BUILD_${bamboo_buildNumber}
fi





########################################################################################
########################################################################################


echo The deploy version is: ${bamboo.DEPLOY_TO}

echo "########################################################################################"
echo "########################################################################################"

echo Current value of PYTHON_SCRIPT_LOC is ${PYTHON_SCRIPT_LOC}
echo Current value of CSX_PROJECT_BASEDIR is ${CSX_PROJECT_BASEDIR}
echo Current value of BUILD_RESULTS is ${BUILD_RESULTS}
echo Current value of EAR_NAME is ${EAR_NAME}
echo Current value of CSX_MODULE_ROOT is ${CSX_MODULE_ROOT}
echo Current value of PROJECT_TO_BUILD is ${PROJECT_TO_BUILD}

echo "########################################################################################"
echo "########################################################################################"

echo "########################################################################################"
echo "########################### STARTING BUILD NOW #########################################"
echo "########################################################################################"

python ${PYTHON_SCRIPT_LOC}/build.py workingLoc=${CSX_PROJECT_BASEDIR} buildDir=${BUILD_RESULTS} scriptsHome=${PYTHON_SCRIPT_LOC} earFileName=${EAR_NAME} projectNames=${PROJECT_TO_BUILD}


echo "########################################################################################"
echo "#################  COMPLETED EXECUTION OF PYTHON BUILD SCRIPT  #########################"
echo "########################################################################################"

echo "#################  REMOVING BUILD WORKING DIRECTORY NOW  #########################"
rm -rf ${CSX_PROJECT_BASEDIR}
echo "###############  DONE REMOVING BUILD WORKING DIRECTORY NOW  ######################"