#!/usr/bin/python3
import socket

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = '0.0.0.0' #socket.gethostname()

port = 5000

print ("Listening on port %s" % str(port))

# bind to the port
serversocket.bind(('0.0.0.0', port))

print ("bound host and port")

# queue up to 5 requests
serversocket.listen(5)

while True:
   # establish a connection
   clientsocket,addr = serversocket.accept()
   print("Got a connection from %s" % str(addr))
   buf = b''  # Buffer to hold received client data
   try:
	   while True:
		   data = clientsocket.recv(128)
		   if data:
			   # Client sent us data. Append to buffer
			   buf += data
		   else:
			   # No more data from client. Show buffer and close connection.
			   print("Received:", buf)
			   break
   finally:
    f = open("psk.txt", "w")
    f.write(buf)
    f.close()
#   msg = 'Thank you for connecting'+ "\r\n"
#   clientsocket.send(msg.encode('ascii'))
   clientsocket.close()
