
#####################################################################
##  This will connect to the database and download all the images  ##
##  from the database in a folder->'details_ph_ii\\' with file     ##
##  names according to their APPLICATION_ID                        ##
#####################################################################


import pymssql
import os
import cv2
import numpy as np

print "Connecting to databse....\n"

con=pymssql.connect(user='sa',password='Admin@123456789',database='IHHL_SBM',host='10.72.143.154')

print "Connected...\n"

cur=con.cursor()
cur.execute(" select APPLICATION_ID, TOILET_PHOTO_IMG_CType, TOILET_PHOTO_IMG from dbo.IHHl_Detail_ph_ii;")
result=cur.fetchall()

row=0

for results in result:
    if result[row][0] == None:
        print "\nApplication No not found!"
        break
    if  result[row][2] == None:
        print row,"\nphotograph image is missing"
        row=row+1
        continue
    ext=result[row][1]
    name=result[row][0]
    if ext is None:
        ext='png'
    else:
        ext=ext[6:]
    fn=name + "." + ext
    print row, fn
    filename='details_ph_ii\\' + fn
    with open(filename, "wb") as fh:
        fh.write(bytearray(result[row][2]))
    fh.close()
    row=row+1


cur.close()
con.close()

