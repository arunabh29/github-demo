#!/usr/bin/perl
#**************************************************************************************************
# Script Name    : VOBCICO_CQLogin.pl
# Author         : McCoy Carter
# Co-Author      : Keith Garrett
# Creation Date  : 01/04/2006
# Description    : Class file for VOBCICO to handle ClearQuest Login Commands.
# Program abstract
#-----------------------------------------------------------------------------------------------------
# The perl script is intended to run under ccperl or cqperl from the Rational software
#-----------------------------------------------------------------------------------------------------
# Note           : To view properly in Ultra Edit have the 'Tab Stop Value' set to 2.
#                  From Menu Bar Select 'Advanced-->Configuration-->Edit Tab-->Tab Stop Value'
#**************************************************************************************************
# Beginning Of Source
#**************************************************************************************************
return 1;


sub connectCQ($) #***** DB Connect *****************************************************************
{                                                                         #
  &Disp_Vars(910,"connectCQ",@_);                                         #
                                                                          #
  my ($CQCreds)=@_;                                                       #
  my $session = CQPerlExt::CQSession_Build();                             #
  my $username=$CQCreds->{"username"};                                    #
  my $password=$CQCreds->{"password"};                                    #
  my $database=$CQCreds->{"database"};                                    #
  my $rc;                                                                 #
                                                                          #
  &Log_Msg(260,"Connecting. [ID:$username DB:$database]");                #
                                                                          #
  $rc = $session->UserLogon($username, $password, $database, "");         #
                                                                          #
  if ($rc ne undef )                                                      #
  {                                                                       #
     &Exit_Pgm(260,"Failed. [ID:$username DB:$database]");                #
  }                                                                       #
  else                                                                    #
  {                                                                       #
    &Log_Msg(260,"Successful. [Session:$session]");                       #
  }                                                                       #
                                                                          #
  return $session;                                                        #
}                                                                         #
#***************************************************************************************************



sub readLoginConfiguration($) #***** Get configuration for Logon ***********************************
{                                                                         #
    &Disp_Vars(910,"readConfiguration",@_);                               #
                                                                          #
    my ($configurationFile)=@_;                                           #
                                                                          #
    &Log_Msg(260,"Reading:$configurationFile");                           #
                                                                          #
    my $fh=new IO::File->new($configurationFile);                         #
    my %preferences;                                                      #
    if (defined($fh)){                                                    #
    while (readline($fh)) {                                               #
      chomp;                  # no newline                                #
      s/#.*//;                # no comments                               #
      s/^\s+//;               # no leading white                          #
      s/\s+$//;               # no trailing white                         #
      next unless length;     # anything left?                            #
      my ($var, $value) = split(/\s*=\s*/, $_, 2);                        #
      $preferences{$var} = $value;                                        #
    }                                                                     #
    } else {                                                              #
      &Exit_Pgm(260,"Unable to Open Config File:$configurationFile");     #
    }                                                                     #
    return %preferences;                                                  #
}                                                                         #
#**************************************************************************************************

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
# Input Parms     :
# Variables       :
#   Global        :
#   Local         :
# Calling Scripts :
# Timers Set      :
# Timers Purges   :
#
#
# History:
# Date          User/Inits  Description
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 03/23/2006    F8164/mcc   Create Template
#***********************************************************************************************
