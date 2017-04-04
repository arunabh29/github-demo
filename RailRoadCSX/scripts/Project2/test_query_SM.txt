cd /ora01/oracle/product/11.2.0/client/bin
./sqlplus /nolog<<!!
connect MAXIMO/panther5@MZXP
select wo.wonum, wo.ownerdisplayname owner, wo.owner racf, ct.description classfication_desciption, ct.classstructureid, releaseitem.releaseitemnum, case  pmchgwoswimgrln.releaseitemnum  when 'MANUAL DEPLOY' THEN PMCHGWOSWIMGRLN.ADHOC ELSE releaseitem.description END as sourceci, wo.status, wo.schedstart, wo.schedfinish from wochange wo, classstructure ct,pmchgwoswimgrln, releaseitem where WO.CLASSSTRUCTUREID = CT.CLASSSTRUCTUREID  and pmchgwoswimgrln.wonum=wo.wonum and releaseitem.releaseitemnum = pmchgwoswimgrln.releaseitemnum and ct.classstructureid in ('3091','3092', '3093', '3094', '3096', '3097', '4743', '5051', '5052' ) and wo.deployed = '0' and wo.status = 'SCHEDULED' and wo.schedstart >= to_date ((to_char(sysdate, 'MM/DD/YYYY') || '06:00:00PM'), 'MM/DD/YYYY:HH:MI:SSPM') and wo.schedfinish <= to_date ((to_char(sysdate + 1, 'MM/DD/YYYY') || '02:00:00AM'),'MM/DD/YYYY:HH:MI:SSAM')
;
!!
