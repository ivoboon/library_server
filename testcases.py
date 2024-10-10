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
url_b = f"http://{ip}:{port}"

# Add a user
url = url_b + '/users'
data = {"name": "Test User"}
response = requests.post(url, json=data)
if response.status_code == 201:
	print("User created:", response.json())
else:
	print("Error:", response.json())

# Get a user
user_id = response.json()['id']
url = url_b + '/users/' + user_id
response = requests.get(url)
if response.status_code == 200:
	print("User retrieved:", response.json())
else:
	print("Error:", response.json())

# Update a user
url = url_b + '/users/' + user_id
data = {"name": "Test User 123"}
response = requests.put(url, json=data)
if response.status_code == 200:
	print("User updated:", response.json())
else:
	print("Error:", response.json())

# Delete a user
url = url_b + '/users/' + user_id
response = requests.delete(url)
if response.status_code == 204:
	print("User deleted successfully")
else:
	print("Error:", response.json())

# Add a book
url = url_b + '/books'
data = {"author": "Test Author", "title": "Test Title"}
response = requests.post(url, json=data)
if response.status_code == 201:
	print("Book created:", response.json())
else:
	print("Error:", response.json())

# Get a book
book_id = response.json()['id']
url = url_b + '/books/' + book_id
response = requests.get(url)
if response.status_code == 200:
	print("Book retrieved:", response.json())
else:
	print("Error:", response.json())

# Update a book's author
url = url_b + '/books/' + book_id
data = {"column": "AUTHOR", "value": "Test Author 123"}
response = requests.put(url, json=data)
if response.status_code == 200:
	print("Book updated:", response.json())
else:
	print("Error:", response.json())

# Update a book's title
url = url_b + '/books/' + book_id
data = {"column": "TITLE", "value": "Test Title 123"}
response = requests.put(url, json=data)
if response.status_code == 200:
	print("Book updated:", response.json())
else:
	print("Error:", response.json())

# Delete a book
url = url_b + '/books/' + book_id
response = requests.delete(url)
if response.status_code == 204:
	print("Book deleted successfully")
else:
	print("Error:", response.json())