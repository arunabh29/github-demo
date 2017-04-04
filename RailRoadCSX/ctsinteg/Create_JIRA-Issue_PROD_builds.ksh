########################################################################################
########################################################################################
# Setting build specific variables in this section.

EAR_NAME=wo_mrt

########################################################################################
########################################################################################

if [ ${bamboo_planRepository_branchName} == master ]
 then
    echo "Creating a JIRA issue for this production build."
    curl --version
    python --version
    python /home/t8054/Arunabh_sandbox/python_scripts/python_jira/python_jira_new/createJiraIssue_latest.py ${EAR_NAME} ${EAR_NAME}_prod_${bamboo.buildNumber}.ear ${bamboo.buildTimeStamp} ${bamboo.buildNumber}
    
    # Sleep 5 seconds for xml payload to be created and used by Curl
    sleep 5
    
    # Changing to directory that contains xml payload.
    cd /home/t8054/Arunabh_sandbox/python_scripts/python_jira/python_jira_new

    echo ----------------------------------------------
    echo ------  Calling Webservice now --------------
    echo ---------------------------------------------

    # calling prod webservice
    curl --header "Content-Type: text/xml;charset=UTF-8" --header "SOAPAction: http://www.csx.com/SmartService/Update" --data @SM_Input_new.xml http://webservices/MZ_LOC_UpdateSmartService_V1

    echo
    echo ---------------------------------------------
    echo ------- Done calling Webservice -------------
    echo ---------------------------------------------

 
 else
    echo "Skipping this step for Non-Prod builds."
    
fi