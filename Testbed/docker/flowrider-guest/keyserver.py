#!/usr/bin/python3 
import socket                                         

# create a socket object
serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = '0.0.0.0' #socket.gethostname()                           

port = 5000                                           

print ("Listienign on port %s" % str(port)) 

# bind to the port
serversocket.bind(('0.0.0.0', port))                                  

print ("bound host and port")

# queue up to 5 requests
serversocket.listen(5)                                           

while True:
   # establish a connection
   clientsocket,addr = serversocket.accept()      

   print("Got a connection from %s" % str(addr))
    
   msg = 'Thank you for connecting'+ "\r\n"
   clientsocket.send(msg.encode('ascii'))
   clientsocket.close()

