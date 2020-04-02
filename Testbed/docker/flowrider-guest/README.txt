server: gcc -Wall -o server c-tls-server.c -L/usr/lib -lssl -lcrypto
client: gcc -Wall -o client  c-tls-client.c -L/usr/lib -lssl -lcrypto 
