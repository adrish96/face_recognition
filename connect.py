import pymssql
import base64
import os

con=pymssql.connect(user='sa',password='sa@1234',database='easebizNZ',host='10.21.59.17')

cur=con.cursor()
cur.execute("SELECT PHOTOGRAPH_IMG FROM IHHL_DETAIL_IMG WHERE APPLICATION_ID='KA1500000002';")
result=cur.fetchall()
result=list(result)
print result[0]
#cur.execute("insert into TEST values (001, %s);", result[0])
cur.close()
con.close()

#fh=open("img.jpeg","wb")
#fh.write(result[0].decode('base64'))
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decode(result[0]))
fh.close()

