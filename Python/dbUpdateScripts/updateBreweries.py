import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

csv_data = csv.reader(file('BreweryTable.csv'))
for row in csv_data:
    #rowOut=(int(row[0]),row[1])
    cursor.execute("INSERT INTO  breweries(brewery_id,brewery_name,brewery_location) VALUES(%s, %s, %s)", row)

mydb.commit()
cursor.close()
print "updated brewery table"

