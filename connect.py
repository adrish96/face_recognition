import pymssql
import base64
import os
import cv2

con=pymssql.connect(user='sa',password='sa@1234',database='easebizNZ',host='10.21.59.17')

cur=con.cursor()
cur.execute(" SELECT APPLICATION_ID, PHOTOGRAPH_IMG_CTYPE, PHOTOGRAPH_IMG FROM IHHL_DETAIL_IMG WHERE APPLICATION_ID='KA1500000027';")
result=cur.fetchall()
#result=list(result)
ext=result[0][1]
name=result[0][0]
ext=ext[6:]
fn=name + "." + ext
print fn
cur.close()
con.close()

#fh=open("img.jpeg","wb")
#fh.write(result[0].decode('base64'))

with open(fn, "wb") as fh:
    fh.write(bytearray(result[0][2]))
fh.close()

img=cv2.imread(fn)
cv2.imshow(fn,img)
cv2.waitKey(0)
cv2.destroyAllWindows()



