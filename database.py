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


def update_user(user_id, user):
	conn, cursor = connect()

	cursor.execute('UPDATE USERS SET NAME = ? WHERE ID = ?', (user['name'], user_id))

	conn.commit()
	conn.close()


def delete_user(user_id):
	conn, cursor = connect()

	cursor.execute('DELETE FROM USERS WHERE ID = ?', (user_id,))

	conn.commit()
	conn.close()

def add_book(book):
	conn, cursor = connect()

	book_id = str(uuid.uuid4())
	cursor.execute('INSERT INTO BOOKS (ID, AUTHOR, TITLE) VALUES (?, ?, ?)', (book_id, book['author'], book['title']))

	conn.commit()
	conn.close()

	return book_id

def get_book(book_id):
	conn, cursor = connect()

	cursor.execute('SELECT ID, AUTHOR, TITLE FROM BOOKS WHERE ID = ?', (book_id,))
	book = cursor.fetchone()
	conn.close()

	return book

def update_book(book_id, book):
	conn, cursor = connect()
	

	cursor.execute(f"UPDATE BOOKS SET {book['column']} = ? WHERE ID = ?", (book['value'], book_id))

	conn.commit()
	conn.close()

def delete_book(book_id):
	conn, cursor = connect()

	cursor.execute('DELETE FROM BOOKS WHERE ID = ?', (book_id,))

	conn.commit()
	conn.close()