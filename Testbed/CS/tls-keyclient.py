#!/usr/bin/env python3

import socket

HOST = '0.0.0.0'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Sending key information to %s" % HOST)
s.sendall(b'Hello, world')
data = s.recv(1024)
print("Received back data %s" % data)
print('Received', data.decode('ascii'))



