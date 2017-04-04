

########################################################################################
# Editable variables section
########################################################################################

APPLICATION_NAME=tcis
BAMBOO_PROJECT=DevOps
BAMBOO_PLAN=COLDFUSION_TEMPLATE_WAS8

########################################################################################
# Non-editable variables section
########################################################################################

BUILD_TIMESTAMP = `date +%y%m%d%H%M%S`

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


TAR_TO_DEPLOY=${APPLICATION_NAME}_${BUILD_VERSION}_${BUILD_TIMESTAMP}.tar

# Copy TAR_TO_DEPLOY to cfinstallableApps

TAR_BUILT = `cd ${BUILD_RESULTS}/dist && find . -name '*.tar'`
cp ${BUILD_RESULTS}/dist/${TAR_BUILT}  /opt/softdepot/csxinst/cfinstallableApps/${APPLICATION_NAME}/${TAR_TO_DEPLOY}

# deploy
sleep 5
/opt/local/scripts/cf_addjob ${TAR_TO_DEPLOY} ${bamboo.DEPLOY_TO} ${USER_EMAIL}