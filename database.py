import sqlite3

def initialise_database():
	conn = sqlite3.connect('library.db')
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS users (
		   ID TEXT PRIMARY KEY NOT NULL,
		   NAME TEXT NOT NULL
		)
	''')
	conn.commit()
	conn.close()