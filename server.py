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
				response = {
					"ID": user[0],
					"NAME": user[1]
				}
				self.wfile.write(json.dumps(response).encode())
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b'{"error": "User not found"}')
		


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

	
	def do_PUT(self):
		pass

	def do_DELETE(self):
		pass

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