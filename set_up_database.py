import sqlite3
import os

'''

# Connect to your SQLite database
conn = sqlite3.connect("books.db")
columns = [
		"id INTEGER PRIMARY KEY",
		"isbn VARCHAR UNIQUE",
		"title VARCHAR",
		"authors VARCHAR",
]
create_table_cmd = f"CREATE TABLE book ({','.join(columns)})"
conn.execute(create_table_cmd)

'''
def reset_database():
	if os.path.exists("users.db"):
		os.remove("users.db")
	conn = sqlite3.connect("users.db")
	columns = [
			"id INTEGER PRIMARY KEY",
			"username VARCHAR UNIQUE",
			"password VARCHAR",
	]
	create_table_cmd = f"CREATE TABLE user ({','.join(columns)})"
	conn.execute(create_table_cmd)


if __name__ == '__main__':
	reset_database()
"""
to see database from command line
connect to database: % sqlite3 users.db
see tables: % .tables
"""