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

# Add a user
url_r = url + '/users'
data = {"name": "Test User"}
response = requests.post(url_r, json=data)
if response.status_code == 201:
	print("User created:", response.json())
else:
	print("Error:", response.json())

# Get a user
user_id = response.json()['id']
url_r = url + '/users/' + user_id
response = requests.get(url_r)
if response.status_code == 200:
	print("User retrieved:", response.json())
else:
	print("Error:", response.json())

# Update a user
url_r = url + '/users/' + user_id
data = {"name": "Test User 123"}
response = requests.put(url_r, json=data)
if response.status_code == 200:
	print("User updated:", response.json())
else:
	print("Error:", response.json())

# Delete a user
print('Press enter to delete the user')
input()
url_r = url + '/users/' + user_id
response = requests.delete(url_r)
if response.status_code == 204:
	print("User deleted successfully")
else:
	print("Error:", response.json())