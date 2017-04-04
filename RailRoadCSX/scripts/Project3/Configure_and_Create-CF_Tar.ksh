########################################################################################
# DO NOT edit this section
########################################################################################

CSX_SCRIPTS_HOME=/opt/shared/atlassian/bamboo/buildfiles/buildforge
CSX_ANT_BASEDIR=${bamboo.build.working.directory}
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


# Create distribution directory for copying tar file
CSX_DISTDIR=$BUILD_RESULTS/dist
mkdir -p ${CSX_DISTDIR}

########################################################################################
########################################################################################


echo The deploy version is: ${bamboo.DEPLOY_TO}

echo "########################################################################################"
echo "########################################################################################"

echo Current value of CSX_PROJECT_BASEDIR is ${CSX_PROJECT_BASEDIR}
echo Current value of BUILD_RESULTS is ${BUILD_RESULTS}
echo Current value of EAR_NAME is ${EAR_NAME}
echo Current value of CSX_MODULE_ROOT is ${CSX_MODULE_ROOT}
echo Current value of PROJECT_TO_BUILD is ${PROJECT_TO_BUILD}
echo Current value of bamboo_ANT_HOME is ${bamboo_ANT_HOME}

echo "########################################################################################"
echo "########################################################################################"

echo "########################################################################################"
echo "########################### STARTING BUILD NOW #########################################"
echo "########################################################################################"

echo "Ant Base Dir is ${CSX_ANT_BASEDIR}"
${bamboo_ANT_HOME}/ant -f ${CSX_SCRIPTS_HOME}/generic.tar.build.script/cfbuild.xml ${bamboo_CSX_ANT_VERBOSE_ON} ${bamboo_CSX_ANT_EMACS_ON} ${bamboo_CSX_ANT_ARGUMENTS} -Dbasedir=${CSX_ANT_BASEDIR} -Dbuild.root.dir=${BUILD_RESULTS} -Ddist.dir=${CSX_DISTDIR}


echo "########################################################################################"
echo "#################  COMPLETED EXECUTION OF ANT BUILD SCRIPT  #########################"
echo "########################################################################################"

echo "#################  REMOVING BUILD WORKING DIRECTORY NOW  #########################"
# rm -rf ${CSX_PROJECT_BASEDIR}
echo "###############  DONE REMOVING BUILD WORKING DIRECTORY  ######################"