APP_NAME=SOX

TAG_TS=`date +%y%m%d%H%M%S`
TAG_NAME=${APP_NAME}_${TAG_TS}_PROD_BUILD-${bamboo.buildNumber}
LAST_PROD_COMMIT_FILE=abc.txt
CHANGESET_FILE=efg.txt
LAST_PROD_COMMIT=`cat abc.txt`
LAST_COMMIT=`git log | grep commit | head -n +1 | awk '{print $2}'`


echo The current working directory is `pwd`
echo Executing git status command in: `pwd`
COMMIT_STATUS=`git status | grep "nothing to commit, working directory clean"`

if [ "${COMMIT_STATUS}" == "nothing to commit, working directory clean" ]
    then
     echo "No new commits required. Comparing current commit with last (prod) commit."
     git diff ${LAST_COMMIT} ${LAST_PROD_COMMIT} --name-only > ${CHANGESET_FILE}
     
     echo "Saving current commit as last prod commit for next prod build"
     echo ${LAST_COMMIT} > ${LAST_PROD_COMMIT_FILE}
     
    else
     # Commit here
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
echo BF_ROOT is: "/opt/local/software/smappsController/BAMBOO_BUILDS/${bamboo.buildResultKey}/BUILD_${bamboo.buildNumber}"



curl --version
python --version


echo Displaying all commits
git log | grep commit

echo "Displaying difference between last two commits (file name only)"
git diff HEAD HEAD^ --name-only

git commit -m "Commit for PROD build"

echo "Creating PROD tag: " ${TAG_NAME}

git tag ${TAG_NAME}

echo "Displaying tags"
git tag --list

echo "Displaying differences between last two tags"
# git diff tag1 tag2 --name-only

echo --------------------------------------------------------------------------------------
echo --------------------------------------------------------------------------------------
# echo ---------------------- Creating issue from Bamboo ------------------------------------

echo --------------------------------------------------------------------------------------
# echo ---------------------- Done creating issue from Bamboo -------------------------------
echo --------------------------------------------------------------------------------------