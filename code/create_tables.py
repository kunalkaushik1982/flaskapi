from msilib.schema import ControlEvent
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (pname text, price real)"
cursor.execute(create_table)

insert_item = "INSERT INTO items VALUES ('test',10.99)"
cursor.execute(insert_item)

connection.commit()
connection.close()
