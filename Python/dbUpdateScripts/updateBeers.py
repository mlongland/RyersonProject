import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

csv_data = csv.reader(file('BeerTable.csv'))
for row in csv_data:
    #print row
    if len(row)!=12:
        print "row is %d long" % len(row)
        a= raw_input()
    cursor.execute("INSERT INTO  beers(beer_id,beer_name,brewery_id,style_id,distribution_id,commercial_desc,ratings_count,ratings_mean, ratings_weighted, est_calories, abv, ibu) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

mydb.commit()
cursor.close()
print "updated brewery table"

