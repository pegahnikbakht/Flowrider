Source: https://defuse.ca/gnutls-psk-client-server-example.htm

server: gcc -Wall -o server pem-server.c -L/usr/lib -lssl -lcrypto
client: gcc -Wall -o client  pem-client.c -L/usr/lib -lssl -lcrypto

PSK:

server: gcc -Wall -Werror -c psk-server.c -o psk-server.o `pkg-config gnutls --cflags`
        gcc psk-server.o -o psk-server `pkg-config gnutls --libs`

client: gcc -Wall -Werror -c client.c -o client.o `pkg-config gnutls --cflags`
        gcc psk-client.o -o psk-client `pkg-config gnutls --libs`



PEM:

server: gcc -Wall -Werror -c pem-server.c -o pem-server.o `pkg-config gnutls --cflags`
        gcc psk-server.o -o pem-server `pkg-config gnutls --libs`

client: gcc -Wall -Werror -c pem-client.c -o pem-client.o `pkg-config gnutls --cflags`
        gcc pem-client.o -o pem-client `pkg-config gnutls --libs`
