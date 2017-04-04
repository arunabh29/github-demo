#!/bin/sh
# ratmenu.ksh
#
#=============================================================================
# Modification History
#=============================================================================
#
# CRnumber      Date            Author          Description
#-----------------------------------------------------------------------------
#
# Set the terminal to vt100 to enable "bold" and "underline"  of text
TERM=vt100
LINES=24
export TERM LINES
MENUHOME=/opt/software/batch/smssutil/RatTools/VOBLoad
#
# Setup traps so no shell access occurs
# see kill man page for further info
# 
#trap 'echo " ";exit' 0 1 2 3 9 15 24 25
#trap ". `cat $MENUHOME/ratmenu.ksh" 2
#
# Set Custom Prompt
PS3='Select an option and press Enter: '
#
# Setup consistent terminal settings so no shell escapes occur!
# See stty man page for further info
/usr/bin/stty erase "^H" intr "^C" kill "^U" eof "^D" susp "^Z" dsusp "^Y"
/usr/bin/stty -ignbrk -parenb -istrip imaxbel icanon

menutitle(){
 clear
 tput cup 1 1
 echo "\n\n\n\n"
 echo "\t\t`tput smso` CSX Rational Utilities Menu - `uname -n` `tput rmso`\n\n"
}
# Main Program
menutitle
select x in VOB_Load_Prompt VOB_Load_Config VOB_Load_Logs Create_PVOB exit
do
case $x in
VOB_Load_Prompt) 
	logger -p daemon.notice "VOB Load ran by `whoami`" 
	cd /opt/software/batch/smssutil/RatTools/VOBLoad/Prod 
	./VOBLoad.sh opt=prompt disp=y debug=on
	sleep 10 
	menutitle;;
VOB_Load_Config) 
	logger -p daemon.notice "VOB Load ran by `whoami`" 
	cd /opt/software/batch/smssutil/RatTools/VOBLoad/Prod  
	./VOBLoad.sh opt=config disp=y debug=on
	sleep 10 
	menutitle;;
VOB_Load_Logs) 
	logger -p daemon.notice "VOB Load Logs ran by `whoami`" 
	cd /opt/software/batch/smssutil/RatTools/VOBLoad/Prod  
	more MessageLog.txt
	menutitle ;;
Create_PVOB) 
	logger -p daemon.notice "Create_PVOB ran by `whoami`" 
	cd /opt/software/batch/smssutil/RatTools/VOBLoad/Prod
 	./cr_pvob.ksh
        sleep 2
	menutitle ;;
exit) 
	echo "\n\t Goodbye Fellow Rat Pack!"
	break;;
esac
done
# End Program
