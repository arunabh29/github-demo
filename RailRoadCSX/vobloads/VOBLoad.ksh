#!/bin/ksh
#**************************************************************************************************
#
#    VOBLoad.sh      Korn Shell script to set environment for Rational VOB Load.
#    Author:          Keith Garrett
#    version:         1.0
#    Abstract:
#         Usage VOBLoad.sh <arg1 arg2 arg3...>
#                arg1: OPT=GO
#                arg2: DISP=Y/N
#                arg3: DEBUG=ON/OFF
#                arg4: VOB=<xxxxx> VOB Name
#                arg5: APPNM=<application name> i.e. peoplesoft, cops etc...
#                arg6: ACODE=<xx> Two Char code for application
#                arg7: FSYS=<xxx..> File System
#                arg8: FOLDER=<xxx..> Folder Name
#
#**************************************************************************************************

export PATH=$PATH:/opt/local/software/clearquest/clearquest/bin
export PATH=$PATH:/usr/bin:/etc:/usr/sbin
export PATH=$PATH:/usr/ucb
export PATH=$PATH:/usr/bin/X11
export PATH=$PATH:/sbin
export PATH=$PATH:/usr/java131/jre/bin
export PATH=$PATH:/usr/java131/bin
export PATH=$PATH:/opt/rational/clearcase/etc
export PATH=$PATH:/usr/local/bin
export PATH=$PATH:/usr/atria/bin
export PATH=$PATH:/home/z_vobadm

#cd `pwd`
#pwd
#/opt/rational/clearquest/bin/cqperl VOBLoad.pl $@

/opt/rational/clearquest/bin/cqperl VOBLoad.pl opt=config disp=y debug=off


#**************************************************************************************************
# End Of Source
#**************************************************************************************************
#
#
#  Documentation
#------------------------------------------------------------------------------------------------
#
# Owner           : Monitoring and Automation Group
# Copy Rights     : Copyright (c) 2006 CSX Technology
#
# Program Details -
# ~~~~~~~~~~~~~~~~~
# Input Parms     : see abstract above
# Variables       : see abstract above
#   Global        :
#   Local         :
# Calling Scripts : CI02214M.pl
# Timers Set      :
# Timers Purges   :
#
#
# History:
# Date          User/Inits  Description
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 07/20/2005    B8322/keg   Installation
#
#
#***********************************************************************************************

