import cx_Oracle

conn_str = ""
conn = cx_Oracle.connect(conn_str)
c = conn.cursor()
c.execute("select wonum, parent, status, statusdate from workorder where status='CANCELLED' and parent like 'C1462%' order by statusdate desc")
for row in c:
    print row
c.close()
conn.close()