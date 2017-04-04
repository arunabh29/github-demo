################################################################################################
################################################################################################

# Script Name    : Deploy_to_PROD_SM-ChangePackage.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 05/05/2016
# Description    : This python script scans the SM database for any prod jobs and then schedules the actual PRODUCTION deployment using the SM Change record
# Usage          : Gets called by start_SM_AutoDeploy.sh
# Modifications  :
# Ver	Name	   : 1.0

################################################################################################
################################################################################################

import cx_Oracle
import os


conn_str = "MAXIMO/panther5@MZXP"
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()

git_work_dir="/home/t8054/Arunabh_sandbox/GIT_Local_Repositories/PeopleSoft/peoplesoft_test"
command_str=""

# The query returns all deployments scheduled through SM between 6 PM and 2 AM of next day.
c.execute("select wo.wonum, wo.ownerdisplayname owner, wo.owner racf, ct.description classfication_desciption, ct.classstructureid, releaseitem.releaseitemnum, case  pmchgwoswimgrln.releaseitemnum  when 'MANUAL DEPLOY' THEN PMCHGWOSWIMGRLN.ADHOC ELSE releaseitem.description END as sourceci, wo.status, wo.schedstart, wo.schedfinish from wochange wo, classstructure ct,pmchgwoswimgrln, releaseitem where WO.CLASSSTRUCTUREID = CT.CLASSSTRUCTUREID  and pmchgwoswimgrln.wonum=wo.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and ct.classstructureid in ('3091','3092', '3093', '3094', '3096', '3097', '4743', '5051', '5052' ) and wo.deployed = '0' and wo.status = 'SCHEDULED' and wo.schedstart >= to_date ((to_char(sysdate, 'MM/DD/YYYY') || '01:00:00PM'), 'MM/DD/YYYY:HH:MI:SSPM') and wo.schedfinish <= to_date ((to_char(sysdate + 1, 'MM/DD/YYYY') || '02:00:00AM'),'MM/DD/YYYY:HH:MI:SSAM')")


# Query for all Coldfusion INPRG deploys
#c.execute("select wochange.wonum ||',', pmchgwoswimgrln.releaseitemnum ||',',  case  pmchgwoswimgrln.releaseitemnum  when 'CUSTOM DEPLOY' THEN PMCHGWOSWIMGRLN.ADHOC ELSE releaseitem.description END ||',', classstructure.description ||',', pmchgwoswimgrln.sequence ||'#' from wochange, classstructure, pmchgwoswimgrln, releaseitem where wochange.classstructureid = '4743' and wochange.classstructureid=classstructure.classstructureid and pmchgwoswimgrln.wonum=wochange.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and wochange.status in ('INPRG') and wochange.schedstart <= sysdate and wochange.deployed = 0")


# Query for all Rational INPRG deploys
# c.execute("select wochange.wonum ||',', pmchgwoswimgrln.releaseitemnum ||',', releaseitem.description ||',', classstructure.description ||',', pmchgwoswimgrln.sequence ||'#' from wochange, classstructure, pmchgwoswimgrln, releaseitem where wochange.classstructureid = '3094' and wochange.classstructureid=classstructure.classstructureid and pmchgwoswimgrln.wonum=wochange.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and wochange.status in ('INPRG') and wochange.schedstart <= sysdate and wochange.deployed = 0")
os.system('clear')


print (" ")
print ("****************************************************************************************************************************************************************************************************************************")
print ("****************************************************************************************************************************************************************************************************************************")
print (" ")

for row in c:
  # print row[0], "-", row[1]
    print ("Deploy Record: " + str(row))
    Change_Num=row[0]
    Implementer_Name=row[1]
    ID=row[2]
    Deploy_Type=row[3]
    Deployable_Artifact=row[6]	
    ChangePackageID=row[5]
    Deploy_Time=row[8]

    print("Change_Num: %s" % Change_Num)
    print("Deploy_Type: %s" % Deploy_Type)
    print("Implementer_Name: %s" % Implementer_Name)
    print("Deployable_Artifact: %s" % Deployable_Artifact)
    print("ChangePackage/Issue ID: %s" % ChangePackageID)
    print("Deploy_Time: %s" % Deploy_Time)
    # print type(row) 


    # Formatting name to construct Email-ID
    Name_String= Implementer_Name.split(',')
    fn=Name_String[1][1::]
    ln= Name_String[0]
    mail_id= fn + "_" + ln + "@csx.com"
    print("Email: %s" % mail_id)


    # Formatting Deploy time
    deploy_string=str(Deploy_Time).split(' ')
    dep_day=deploy_string[0].replace("-","")
    dep_time=deploy_string[1].replace(":","")[:-2]
    Military_Deploy_Time=dep_day + "-" + dep_time
    print("Military Deploy Time: %s" % Military_Deploy_Time)

    
    if (Deploy_Type == "Websphere8 Deploy"):
       command_str= "/opt/local/scripts/ws8_prodjob " + str(Deployable_Artifact) + " " + str(Change_Num) + " " + Military_Deploy_Time + " y"
       print ("Command String: %s" % command_str)
      

    if (Deploy_Type == "Websphere7 Deploy"):
        command_str= "/opt/local/scripts/ws7_prodjob " + str(Deployable_Artifact) + " " + str(Change_Num) + " " + Military_Deploy_Time + " y"
        print ("Command String: %s" % command_str)


    if (Deploy_Type == "Coldfusion Deploy"):
        command_str= "/opt/local/scripts/cf_prodjob " + str(Deployable_Artifact) + " " + str(Change_Num) + " " + Military_Deploy_Time + " y"
        print ("Command String: %s" % command_str)


    # if (Deploy_Type == "Rational Deploy"):
      #  command_str= "/home/t8054/Arunabh_sandbox/python_scripts/SOX/PeopleSoft_SOX_Deployment.ksh " + str(git_work_dir) + " " + str(Deployable_Artifact)
      #  print ("Command String: %s" % command_str)



    print (" ")
    print ("****************************************************************************************************************************************************************************************************************************")
    print (" ")
    

    os.system('echo "Scheduling prod deploy: "')
    # os.system(command_str)
    # c.execute("update wochange set deployed = 1 where wonum = '%s' " %Change_Num)

    
# c.commit()
c.close()
conn.close()