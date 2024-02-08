import sqlite3

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

