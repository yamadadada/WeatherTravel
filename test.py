import pymysql

db = pymysql.connect("localhost", "root", "jerry75911", "gzweather")
con = db.cursor()

sql = "insert into weather(rain, windSpeed) VALUES ('%s', '%s')" % ("123", "9816")
con.execute(sql)
db.commit()
db.close()
