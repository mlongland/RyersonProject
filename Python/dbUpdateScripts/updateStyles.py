import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='pythonconnector',
    passwd='python1029',
    db='BeerRatings')
cursor = mydb.cursor()

csv_data = csv.reader(file('StyleTable.csv'))
for row in csv_data:
    #rowOut=(int(row[0]),row[1])
    cursor.execute("INSERT INTO styles(style_id,style_name) VALUES(%s, %s)", row)

mydb.commit()
cursor.close()
print "updated %s table" % 'style'
