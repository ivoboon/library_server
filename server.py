from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket

import database

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(b"Hello world!")

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