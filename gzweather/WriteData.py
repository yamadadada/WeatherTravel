import sqlite3

mydb = sqlite3.connect("gzweather.sqlite")
cursor = mydb.cursor()
sql = "select * from weather"
results = cursor.execute(sql)
data = cursor.fetchall()
for a in data:
    print(a)