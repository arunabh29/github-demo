#################################################################################
#
#   script: vobload.pl
#   written by: McCoy Carter , 10/28/05
#   
#   Script requires these arguments:
#
#       -group -app -appcode -pvob -filesystem -folder
#
#################################################################################

id

newgrp $group

cleartool mkvob -public -pas rat -nc -tag /vob/$app -host rs113 -hpath /opt/local/software/clearcode/vobs/$filesystem/$app.vbs -gpath /net/rs113/opt/local/software/clearcode/vobs/$filesystem/$app.vbs /net/rs113/opt/local/software/clearcode/vobs/$filesystem/$app.vbs

cleartool mount /vob/$app

cleartool desc vob:/vob/$app

# run Region Synchronizer

cleartool mkview -tag view_$appcode_$app /opt/local/software/clearcase/view_$appcode_$app.vws

cleartool setview view_$appcode_$app
 
cleartool mkcomp -nc -root /vob/$app $app@/vob/$pvob

cleartool mkfolder -nc -in \RootFolder@$pvob $folder@$pvob

cleartool mkproject -nc -modcomp $app@/vob/$pvob -in $folder@/vob/$pvob $appcode.$app.01@/vob/$pvob

# cleartool mkstream

cleartool mkview -tag z_vobadm_$appcode_$app -stream $appcode_$app.01_Int@/vob/$pvob /opt/local/software/clearcase/z_vobadm_$appcode_$app.vws

cleartool setview z_vobadm_$appcode_$app

cleartool mkactivity "act_load_$app"

cleartool setactivity act_load_$app

cd /net/rs113/opt/local/software/clearcode/$app

umask 2

clearfsimport -preview -recurse * /vob/$app

clearfsimport -recurse * /vob/$app

cleartool mkbl -nc -identical -com $app@/vob/$pvob 

cleartool chstream -nc -rec -def $appcode_$app_Int@/vob/$pvob

