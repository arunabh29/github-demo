/ora01/oracle/product/11.2.0/client/bin/sqlplus /nolog<<!!
connect MAXIMO/panther5@MZXP
select wonum, parent, status, statusdate from workorder where status='CANCELLED' and parent like 'C1462%' order by statusdate desc;
!!
