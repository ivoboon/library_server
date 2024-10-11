import sqlite3
import uuid
import datetime

def connect():
	database = 'library.db'
	conn = sqlite3.connect(database)
	cursor = conn.cursor()
	return conn, cursor


def initialise_database():
	conn, cursor = connect()

	# Users table
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS USERS (
			ID TEXT PRIMARY KEY NOT NULL,
			NAME TEXT NOT NULL
		)
	''')

	# Books table
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS BOOKS (
			ID TEXT PRIMARY KEY NOT NULL,
			AUTHOR TEXT NOT NULL,
			TITLE TEXT NOT NULL,
			AVAILABLE BOOLEAN DEFAULT TRUE
		)
	''')

	# Transactions table
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS TRANSACTIONS (
			ID TEXT PRIMARY KEY NOT NULL,
			TIMESTAMP TEXT NOT NULL,
			USER_ID TEXT NOT NULL,
			BOOK_ID TEXT NOT NULL,
			DIRECTION TEXT NOT NULL
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

	if user:
		return {
			"id": user[0],
			"name": user[1]
		}

	return None


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

	cursor.execute('SELECT ID, AUTHOR, TITLE, AVAILABLE FROM BOOKS WHERE ID = ?', (book_id,))
	book = cursor.fetchone()
	conn.close()

	if book:
		return {
			"id": book[0],
			"author": book[1],
			"title": book[2],
			"available": book[3]
		}

	return None


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


def transaction(transaction):
	conn, cursor = connect()

	transaction_id = str(uuid.uuid4())
	transaction_timestamp = datetime.datetime.now().isoformat()

	available = ''
	if transaction['direction'] == 'in':
		available = True
	elif transaction['direction'] == 'out':
		available = False
	else:
		return

	try:
		conn.execute('BEGIN TRANSACTION')

		conn.execute('UPDATE BOOKS SET AVAILABLE = ? WHERE ID = ?', (available, transaction['book_id']))
		conn.execute("INSERT INTO TRANSACTIONS (ID, TIMESTAMP, USER_ID, BOOK_ID, DIRECTION) VALUES (?, ?, ?, ?, ?)", (transaction_id, transaction_timestamp, transaction['user_id'], transaction['book_id'], transaction['direction']))

		conn.commit()

		return transaction_id

	except sqlite3.Error as e:
		conn.rollback()

		return
	
	finally:
		conn.close()