import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

csv_data = csv.reader(file('DistributionTable.csv'))
for row in csv_data:
    #rowOut=(int(row[0]),row[1])
    cursor.execute("INSERT INTO distribution(distribution_id,distribution_desc) VALUES(%s, %s)", row)

mydb.commit()
cursor.close()
print "updated distribution table"

