########################################################################################
# Editable variables section
########################################################################################

TAR_NAME=tcismobile
CSX_MODULE_ROOT=""
PROJECT_TO_BUILD=
BAMBOO_PROJECT=TCIS
BAMBOO_PLAN=TCISMOBILE

########################################################################################
# Non-editable variables section
########################################################################################

BUILD_TIMESTAMP=$(echo `date +%y%m%d%H%M%S`)

echo BUILD_TIMESTAMP is:  ${BUILD_TIMESTAMP}

USER_EMAIL=`python /home/t8054/Arunabh_sandbox/python_scripts/getEmail.py ${bamboo_ManualBuildTriggerReason_userName}`
if [ ${USER_EMAIL} == "" ]
    then
     USER_EMAIL=Jacob_Daubendiek@csx.com
     echo The user ${bamboo_ManualBuildTriggerReason_userName} does not have a JIRA account. Please provide him/her access to JIRA.
fi


BUILD_BRANCH=`echo ${bamboo_planRepository_branch} | grep -o '..$'`


if [ ${BUILD_BRANCH} == op ]
    then
        BUILD_VERSION=dev
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/DEV/BUILD_${bamboo_buildNumber}
fi


if [ ${BUILD_BRANCH} == st ]
    then
        BUILD_VERSION=uat
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/UAT/BUILD_${bamboo_buildNumber}
fi


if [ ${BUILD_BRANCH} == er ]
    then
        BUILD_VERSION=prod
	 BUILD_RESULTS=/opt/local/software/smappsController/BAMBOO_BUILDS/${BAMBOO_PROJECT}/${BAMBOO_PLAN}/PROD/BUILD_${bamboo_buildNumber}
fi


TAR_TO_DEPLOY=${TAR_NAME}_${BUILD_VERSION}_${BUILD_TIMESTAMP}.tar

# Copy TAR_TO_DEPLOY to cfinstallableApps

cd ${BUILD_RESULTS}/dist
cp ./${TAR_NAME}.tar  /opt/softdepot/csxinst/cfinstallableApps/${TAR_NAME}/${TAR_TO_DEPLOY}


if [ ${bamboo.DEPLOY_TO} == dev -o ${bamboo.DEPLOY_TO} == uat ]
    then
    
        # # CF deploy
        /opt/local/scripts/cf_addjob ${TAR_TO_DEPLOY} ${bamboo.DEPLOY_TO} ${USER_EMAIL}
    else
        
        echo ----------------------------------------------------------------------------------------------------
        echo ------- NOT DEPLOYING SINCE NEITHER dev NOR uat WAS SPECIFIED AS THE 'DEPLOY_TO' ENVIRONMENT. --------
        echo ----------------------------------------------------------------------------------------------------
fi

