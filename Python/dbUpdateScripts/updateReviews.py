import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

csv_data = csv.reader(file('ReviewTable.csv'))
for row in csv_data:
    #print row
    if len(row)!=12:
        print "row is %d long" % len(row)
        a= raw_input()
    cursor.execute("INSERT INTO  reviews(review_id,beer_id,score,aroma,appearance,taste,palate,overall,user_id, review_location, review_date, review_content) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

mydb.commit()
cursor.close()
print "updated reviews table"

