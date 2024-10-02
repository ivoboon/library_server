import requests
import socket

def get_ip_address():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip

ip = get_ip_address()
port = 8080
url = f"http://{ip}:{port}"
response = requests.get(url)

print(response.status_code)
print(response.text)