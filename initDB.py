import sqlite3

connection = sqlite3.connect('database.db')

with open('initDB.sql') as f:
    connection.executescript(f.read())