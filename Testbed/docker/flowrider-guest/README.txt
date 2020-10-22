Source: https://defuse.ca/gnutls-psk-client-server-example.htm

PSK:

server: gcc -Wall -Werror -c psk-server.c -o psk-server.o `pkg-config gnutls --cflags` \
        gcc psk-server.o -o psk-server `pkg-config gnutls --libs`

client: gcc -Wall -Werror -c psk-client.c -o psk-client.o `pkg-config gnutls --cflags`
        gcc psk-client.o -o psk-client `pkg-config gnutls --libs`



PEM:

server: gcc -Wall -Werror -c gnu-pem-server.c -o pem-server.o `pkg-config gnutls --cflags`
        gcc pem-server.o -o pem-server `pkg-config gnutls --libs`

client: gcc -Wall -Werror -c gnu-pem-client.c -o pem-client.o `pkg-config gnutls --cflags`
        gcc pem-client.o -o pem-client `pkg-config gnutls --libs`
