import sqlite3
import uuid

def connect():
	database = 'library.db'
	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	return conn, cursor

def initialise_database():
	conn, cursor = connect()
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS USERS (
		   ID TEXT PRIMARY KEY NOT NULL,
		   NAME TEXT NOT NULL
		)
	''')
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS BOOKS (
		   ID TEXT PRIMARY KEY NOT NULL,
		   AUTHOR TEXT NOT NULL,
		   TITLE TEXT NOT NULL
		)
	''')
	conn.commit()
	conn.close()

def add_user(user):
	conn, cursor = connect()

	user_id = str(uuid.uuid4())
	cursor.execute('INSERT INTO USERS (ID, NAME) VALUES (?, ?)', (user_id, user['name']))

	conn.commit()
	conn.close()

	return user_id

def get_user(user_id):
	conn, cursor = connect()

	cursor.execute('SELECT ID, NAME FROM USERS WHERE ID = ?', (user_id,))
	user = cursor.fetchone()
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