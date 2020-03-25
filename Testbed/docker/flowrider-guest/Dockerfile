# Ryu SDN Example Guest -- for the FlowRider2020 example
#


FROM python:alpine3.7

RUN apk update
RUN apk add  bind-tools
RUN apk add  iputils net-tools
RUN apk add --no-cache bash


# Add Endpoint user account
RUN groupadd --system endpoint
RUN useradd  --system -d /home/endpoint -m -s /bin/bash -g endpoint endpoint


# Add clientTLS application and data into container
ADD tls-keyclient.py /home/endpoint/tls-keyclient.py
ADD certs/client.crt /home/endpoint/client.crt
ADD certs/client.key /home/endpoint/client.key


# Add serverTLS application into container
ADD tls-keyserver.py /home/endpoint/tls-keysever.py
ADD certs/server.crt /home/endpoint/server.crt
ADD certs/server.key /home/endpoint/server.key


RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8082
