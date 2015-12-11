import csv
import MySQLdb
import pickle

with open('/usr/ALSServer/dbfiles/top5StylesPerUser.txt','rb') as f:
	pickle_data = pickle.load(f)

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

for user in pickle_data:
    #print user[0]
    count=0
    for style in user[1]:
	count+=1
        row = (user[0],style.encode('utf-8'),user[1][style][0])
        cursor.execute("INSERT INTO topStyles(user_id,style_name,avg_score) VALUES(%s, %s, %s)", row)

mydb.commit()
cursor.close()
print "updated topStyles table"

