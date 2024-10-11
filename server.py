from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket

import database

class Handler(BaseHTTPRequestHandler):
	def get_path_parts(self):
		path_parts = self.path.strip('/').split('/')
		return path_parts


	def do_GET(self):
		path_parts = self.get_path_parts()
		resource = path_parts[0]

		if resource == 'users' and len(path_parts) > 1:
			record_id = path_parts[1]
			user = database.get_user(record_id)
			if user:
				self.send_response(200)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(json.dumps(user).encode())
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')
		
		elif resource == 'books' and len(path_parts) > 1:
			record_id = path_parts[1]
			book = database.get_book(record_id)
			if book:
				self.send_response(200)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(json.dumps(book).encode())
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "Book not found"}')
		

	def do_POST(self):
		path_parts = self.get_path_parts()
		resource = path_parts[0]

		content_length = int(self.headers['Content-Length'])
		post_data = self.rfile.read(content_length)
		data = json.loads(post_data)

		if resource == 'users':
			user_id = database.add_user(data)
			self.send_response(201)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			self.wfile.write(json.dumps({"id": user_id}).encode())

		elif resource == 'books':
			book_id = database.add_book(data)
			self.send_response(201)
			self.send_header("Content-type", "application/json")
			self.end_headers()
			self.wfile.write(json.dumps({"id": book_id}).encode())
		
		elif resource == 'transactions':
			if not database.get_user(data['user_id']):
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')
				return
			
			if not database.get_book(data['book_id']):
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "Book not found"}')
				return

			if data['direction'] == 'out' and not bool(database.get_book(data['book_id'])['available']):
				self.send_response(400)
				self.end_headers()
				self.wfile.write(b'{"error": "Book is not available"}')
				return
			
			if data['direction'] == 'in' and bool(database.get_book(data['book_id'])['available']):
				self.send_response(400)
				self.end_headers()
				self.wfile.write(b'{"error": "Book is already checked in"}')
				return
			
			transaction_id = database.transaction(data)
			if transaction_id:
				self.send_response(201)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(json.dumps({"id": transaction_id}).encode())
			else:
				self.send_response(422)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(b'{"error": "Unprocessable content"}')

	
	def do_PUT(self):
		path_parts = self.get_path_parts()
		resource = path_parts[0]

		content_length = int(self.headers['Content-length'])
		put_data = self.rfile.read(content_length)
		updated_data = json.loads(put_data)

		if resource == 'users' and len(path_parts) > 1:
			record_id = path_parts[1]
			if database.get_user(record_id):
				database.update_user(record_id, updated_data)
				self.send_response(200)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(json.dumps({"message:": "User updated"}).encode())
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')
		
		elif resource == 'books' and len(path_parts) > 1:
			record_id = path_parts[1]
			if database.get_book(record_id):
				database.update_book(record_id, updated_data)
				self.send_response(200)
				self.send_header("Content-type", "application/json")
				self.end_headers()
				self.wfile.write(json.dumps({"message:": "Book updated"}).encode())
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "Book not found"}')


	def do_DELETE(self):
		path_parts = self.get_path_parts()
		resource = path_parts[0]
		print(resource)

		if resource == 'users' and len(path_parts) > 1:
			record_id = path_parts[1]
			if database.get_user(record_id):
				database.delete_user(record_id)
				self.send_response(204)
				self.end_headers()
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')
		
		elif resource == 'books' and len(path_parts) > 1:
			record_id = path_parts[1]
			if database.get_book(record_id):
				database.delete_book(record_id)
				self.send_response(204)
				self.end_headers()
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')


def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip


def main():
	port = 8080
	ip = get_ip_address()
	print(ip)
	print('Initialising database...')
	database.initialise_database()
	print('Database initialised')
	server_address = (ip, port)
	httpd = HTTPServer(server_address, Handler)
	print(f'Serving on port {ip}:{port}...')
	httpd.serve_forever()


if __name__ == "__main__":
	main()