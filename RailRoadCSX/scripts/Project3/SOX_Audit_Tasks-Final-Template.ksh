echo The current working directory is `pwd`

APP_NAME=SOX

TAG_TS=`date +%y%m%d%H%M%S`
DATE_STR=`date`
TAG_NAME=${APP_NAME}_${TAG_TS}_PROD_BUILD-${bamboo.buildNumber}
TAG_MESSAGE="Tagging production build: BUILD-${bamboo.buildNumber} on ${DATE_STR}"
LAST_PROD_COMMIT_FILE=/home/t8054/Arunabh_sandbox/python_scripts/SOX/last_prod_commit.txt
CHANGESET_FILE=/home/t8054/Arunabh_sandbox/python_scripts/SOX/jira_attachment.txt
LAST_PROD_COMMIT=`cat ${LAST_PROD_COMMIT_FILE}`
LAST_COMMIT=`git log | grep commit | head -n +1 | awk '{print $2}'`

echo Executing git status command in: `pwd`
COMMIT_STATUS=`git status | grep "nothing to commit, working directory clean"`



if [ "${COMMIT_STATUS}" == "nothing to commit, working directory clean" ]
    then
     
     echo "Tagging current commit as a prod build"
     git tag -a ${TAG_NAME} -m "${TAG_MESSAGE}"
     sleep 2
     
     echo "No new commits required. Comparing current commit with last (prod) commit."
     git diff ${LAST_COMMIT} ${LAST_PROD_COMMIT} --name-only > ${CHANGESET_FILE}
     
     sleep 2
     echo "Saving current commit as last prod commit for next prod build"
     echo ${LAST_COMMIT} > ${LAST_PROD_COMMIT_FILE}
     
    else
     # Commit here
     git commit -m "Tagging this prod commit with: ${TAG_NAME}"
     sleep 2
     
     git tag -a ${TAG_NAME} -m "${TAG_MESSAGE}"
     sleep 2
     
     # Updating LAST_COMMIT because a commit was required and done
     LAST_COMMIT=`git log | grep commit | head -n +1 | awk '{print $2}'`
     git diff ${LAST_COMMIT} ${LAST_PROD_COMMIT} --name-only > ${CHANGESET_FILE}
     sleep 2
     
     echo "Saving current commit as last prod commit for next prod build"
     echo ${LAST_COMMIT} > ${LAST_PROD_COMMIT_FILE}
     
fi

echo the build number is: ${bamboo.buildNumber}
echo The bamboo build working dir is: ${bamboo.build.working.directory}
echo The bamboo plan name is: ${bamboo.planName}
echo User that executed this plan: ${bamboo.ManualBuildTriggerReason.userName}
echo Bamboo Agent ID: ${bamboo.agentId}
echo Build Result Key: ${bamboo.buildResultKey}
echo Build Timestamp is: ${bamboo.buildTimeStamp}
echo Build Plan name is: ${bamboo.buildPlanName}
echo Plan name is: ${bamboo.planName}
echo Short Plan name is: ${bamboo.shortPlanName}
echo Short Job name is: ${bamboo.shortJobName}



echo "Displaying tags"
git tag --list

echo "Displaying commits"
git log | grep commit

echo --------------------------------------------------------------------------------------
echo --------------------------------------------------------------------------------------
echo --------------------------------------------------------------------------------------
echo --------------------------------------------------------------------------------------

# Calling python to upload Change-Set in a Jira issue.
echo "Calling python to upload Change-Set in a Jira issue."
python /home/t8054/Arunabh_sandbox/python_scripts/SOX/create-sox_issue.py ${APP_NAME} ${TAG_NAME} ${TAG_TS} BUILD-${bamboo.buildNumber}
