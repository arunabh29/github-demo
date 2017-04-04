################################################################################################
################################################################################################

# Script Name    : CF-Auto_Deploy.py
# Author         : Arunabh Chowdhury (Service Management Team)
# Creation Date  : 05/05/2016
# Description    : This python script scans the SM database for any CF prod jobs that is currently in 'INPRG' state and immediately starts a PRODUCTION deployment using the SM Change record.
# Usage          : Gets called by a cron every 5 minutes
# Modifications  :
# Ver	Name	   : 1.0

################################################################################################
################################################################################################

import cx_Oracle
import os



conn_str = "MAXIMO/panther5@MZXP"
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()


# Query for all Coldfusion INPRG deploys
c.execute("select wochange.wonum ||',', pmchgwoswimgrln.releaseitemnum ||',', releaseitem.description ||',', classstructure.description ||',', pmchgwoswimgrln.sequence ||'#' from wochange, classstructure, pmchgwoswimgrln, releaseitem where wochange.classstructureid = '3093' and wochange.classstructureid=classstructure.classstructureid and pmchgwoswimgrln.wonum=wochange.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and wochange.status in ('INPRG') and wochange.schedstart <= sysdate and wochange.deployed = 0")


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
    Deployable_Artifact=row[2][:-1]
    Deploy_Type=row[3][:-1]
    

    print("Change_Num: %s" % Change_Num)
    print("ChangePackage/Issue ID: %s" % Issue_ID)
    print("Deployable_Artifact: %s" % Deployable_Artifact)    
    print("Deploy_Type: %s" % Deploy_Type)
    
   
    print type(row) 


    if ((Deploy_Type == "Coldfusion Deploy") and (Issue_ID[:2] == "CM")):
        command_str= "/opt/local/scripts/cf_prodjob " + str(Deployable_Artifact) + " " + str(Change_Num) + " now y"
        print ("Command String: %s" % command_str)
        os.system('echo Schduling CF production deploy now')        
        os.system(command_str)

    print (" ")
    print ("****************************************************************************************************************************************************************************************************************************")
    print ("****************************************************************************************************************************************************************************************************************************")    
    print (" ")
    

    
    
    

c.close()
# conn.commit()
conn.close()