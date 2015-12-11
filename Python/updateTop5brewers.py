import csv
import MySQLdb
import pickle

with open('/usr/ALSServer/dbfiles/top5BrewersPerUser.txt','rb') as f:
	pickle_data = pickle.load(f)

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

for user in pickle_data:
    #print user[0]
    count=0
    for brewer in user[1]:
	count+=1
        row = (user[0],brewer.encode('utf-8'),user[1][brewer][0])
        cursor.execute("INSERT INTO topBrewers(user_id,brewer_name,avg_score) VALUES(%s, %s, %s)", row)

mydb.commit()
cursor.close()
print "updated topBrewers table"

