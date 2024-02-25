import sqlite3

connection = sqlite3.connect('database.db')

cur = connection.cursor()

data = cur.execute("SELECT * FROM addresses").fetchall()
print(data)

connection.close()