#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import collections
import sqlite3 as lite
import sys

#
#This code gets all rows of the DB and copies the data to 
#a .txt file '/var/www/html/buoy/buoy.txt', that can be accessed
#from outside

con = lite.connect('buoy.db')  
    
cursor = con.cursor()    
cursor.execute("SELECT DateTime,Depth,TempC,TempF FROM buoy")
rows = cursor.fetchall()


rowarray_list = []
for row in rows:
    t = (row[0], row[1], row[2], row[3])
    rowarray_list.append(t)
 
j = json.dumps(rowarray_list)
rowarrays_file = '/var/www/html/buoy/buoy.txt'
f = open(rowarrays_file,'w')
print >> f, j
con.close()
