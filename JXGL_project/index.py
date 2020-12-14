import pymssql
conn = pymssql.connect(host='localhost',user='sa',password='000000',database='test',charset='GBK')
cursor = conn.cursor()
print(conn)
print(cursor)
cursor.execute('select * from student')
data = cursor.fetchall()
print(data)

cursor.close()
conn.close()

