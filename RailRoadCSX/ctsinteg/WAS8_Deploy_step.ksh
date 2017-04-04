########################################################################################
# Editable variables section
########################################################################################

EAR_NAME=wo_mrt
CSX_MODULE_ROOT=""
PROJECT_TO_BUILD=MrtEAR
BAMBOO_PROJECT=MRT
BAMBOO_PLAN=MRT_TEMPLATE

########################################################################################
# Non-editable variables section
########################################################################################

PYTHON_SCRIPT_LOC=/opt/shared/atlassian/bamboo/buildfiles/buildforge/leapfrog
CSX_PROJECT_BASEDIR=${bamboo.build.working.directory}
WAS_DIR=/opt/local/scripts
# last 2 for dev(dev) build is 'ev', for qa(uat) is 'qa' and for master(prod) is 'er'

BUILD_VERSION=`echo ${bamboo_planRepository_branch} | grep -o '..$'`

if [ ${BUILD_VERSION} == ev ]
    then
        EAR_TO_DEPLOY=${EAR_NAME}_dev_${bamboo_buildNumber}.ear
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/${BUILD_VERSION}/DEV/BUILD_${bamboo_buildNumber}
	 EAR_DIR=${BUILD_RESULTS}/${PROJECT_TO_BUILD}
fi


if [ ${BUILD_VERSION} == qa ]
    then
        EAR_TO_DEPLOY=${EAR_NAME}_uat_${bamboo_buildNumber}.ear
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/${BUILD_VERSION}/UAT/BUILD_${bamboo_buildNumber}
	 EAR_DIR=${BUILD_RESULTS}/${PROJECT_TO_BUILD}
fi

if [ ${BUILD_VERSION} == er ]
    then
        EAR_TO_DEPLOY=${EAR_NAME}_prod_${bamboo_buildNumber}.ear
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/${BUILD_VERSION}/PROD/BUILD_${bamboo_buildNumber}
	 EAR_DIR=${BUILD_RESULTS}/${PROJECT_TO_BUILD}
fi


########################################################################################
########################################################################################


echo ---------------------------------------------------------------
echo ---------------------------------------------------------------
echo ---------------------------------------------------------------
echo The deploy version is: ${bamboo.DEPLOY_TO}
echo ---------------------------------------------------------------
echo The ear directory is: ${EAR_DIR}
echo ---------------------------------------------------------------

# Renaming ear file and copying to csxinstallableApps before WAS deployment
        echo ------- RENAMING AND COPYING EAR FILE TO csxinstallableApps --------
        cd ${EAR_DIR}
        mv ${EAR_NAME}_${bamboo_buildNumber}.ear ${EAR_TO_DEPLOY} 
        cp ./${EAR_TO_DEPLOY} /opt/softdepot/csxinst/installableApps/${EAR_NAME}/${EAR_TO_DEPLOY}


# Deploying if deploy_to is dev or uat
if [ ${bamboo.DEPLOY_TO} == dev -o ${bamboo.DEPLOY_TO} == uat ]
    then
    
        # WAS8 Deploy
        cd ${WAS_DIR}
        ./ws8_addjob ${EAR_DIR}/${EAR_TO_DEPLOY} ${bamboo.DEPLOY_TO} Paul_Brown@csx.com
    else
        
        echo ----------------------------------------------------------------------------------------------------
        echo ------- NOT DEPLOYING SINCE NEITHER dev NOR uat WAS SPECIFIED AS THE 'DEPLOY_TO' ENVIRONMENT. --------
        echo ----------------------------------------------------------------------------------------------------
fi