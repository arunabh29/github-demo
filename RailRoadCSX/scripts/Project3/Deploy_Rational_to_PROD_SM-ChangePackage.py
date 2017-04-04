################################################################################################
################################################################################################

# Script Name    : Deploy_Rational_to_PROD_SM-ChangePackage.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 05/25/2016
# Description    : This python script scans the SM database for any INPRG Rational deploy prod jobs and starts the actual PRODUCTION deployment using the SM Change record
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


# Query for all Rational INPRG deploys
c.execute("select wochange.wonum ||',', pmchgwoswimgrln.releaseitemnum ||',', releaseitem.description ||',', classstructure.description ||',', pmchgwoswimgrln.sequence ||'#' from wochange, classstructure, pmchgwoswimgrln, releaseitem where wochange.classstructureid = '3094' and wochange.classstructureid=classstructure.classstructureid and pmchgwoswimgrln.wonum=wochange.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and wochange.status in ('INPRG') and wochange.schedstart <= sysdate and wochange.deployed = 0")
os.system('clear')


print (" ")
print ("****************************************************************************************************************************************************************************************************************************")
print ("****************************************************************************************************************************************************************************************************************************")
print (" ")

for row in c:
  # print row[0], "-", row[1]
    print ("Deploy Record: " + str(row))
    Change_Num=row[0][:-1]
    Issue_ID=row[1][:-1]
    ChangeSet_Path=row[2][:-1]
    Deploy_Type=row[3][:-1]	


    print("Change_Num: %s" % Change_Num)
    print("Issue_ID: %s" % Issue_ID)
    print("ChangeSet_Path: %s" % ChangeSet_Path)
    print("Deploy_Type: %s" % Deploy_Type)
    # print type(row)


    if (Deploy_Type == "Rational Deploy"):
        command_str= "/home/t8054/Arunabh_sandbox/python_scripts/SOX/PeopleSoft_SOX_Deployment.ksh " + str(git_work_dir) + " " + str(ChangeSet_Path)
        print ("Command String: %s" % command_str)



    print (" ")
    print ("****************************************************************************************************************************************************************************************************************************")
    print (" ")
    

    os.system('echo "Scheduling prod deploy: "')
    os.system(command_str)

    
c.close()
conn.close()