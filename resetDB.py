import sqlite3

connection = sqlite3.connect('database.db')

with open('resetDB.sql') as f:
    connection.executescript(f.read())