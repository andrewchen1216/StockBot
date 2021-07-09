import sqlite3
con = sqlite3.connect("../stock.db")
cur = con.cursor()
cur.execute('''CREATE TABLE stocks
               (date text, trans text, symbol text, qty real, price real)''')

cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
con.commit()
for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)
con.close()