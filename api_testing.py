import socket

server = socket.socket()

server.bind(("localhost",5678))
server.listen()

client, address = server.accept()

request = client.recv(1024)
print(request)
print("#"*20)
print(request.decode())


