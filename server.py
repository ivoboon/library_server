from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket

import database

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		path_parts = self.path.split('/')
		resource = path_parts[1]
		record_id = path_parts[-1]

		if resource == 'users':
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

		if resource == 'hello':
			response = f"Hello, {record_id}"
			byte_string = response.encode('utf-8')
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.wfile.write(byte_string)


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