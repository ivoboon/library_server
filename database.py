import sqlite3
import uuid

def initialise_database():
	conn = sqlite3.connect('library.db')
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS USERS (
		   ID TEXT PRIMARY KEY NOT NULL,
		   NAME TEXT NOT NULL
		)
	''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS BOOKS (
		   ID TEXT PRIMARY KEY NOT NULL,
		   AUTHOR TEXT NOT NULL,
		   TITLE TEXT NOT NULL
		)
	''')
	conn.commit()
	conn.close()

def add_user():
	pass

def get_user(user_id):
	conn = sqlite3.connect('library.db')
	c = conn.cursor()

	c.execute('SELECT ID, NAME FROM USERS WHERE ID = ?', (user_id))
	user = c.fetchone()
	conn.close()

	return user


def update_user():
	pass

def delete_user():
	pass

def add_book():
	pass

def get_book():
	pass

def update_book():
	pass

def delete_book():
	pass