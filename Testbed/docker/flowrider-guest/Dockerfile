# Ryu SDN Example Guest -- for the FlowRider2020 example
#


FROM python:alpine3.7

RUN apk update
RUN apk add  bind-tools
RUN apk add  iputils net-tools
RUN apk add --no-cache bash


# Add clientTLS application and data into container
COPY tls-keyclient.py
COPY certs/client.crt
COPY certs/client.key


# Add serverTLS application into container
COPY tls-keyserver.py
COPY certs/server.crt
COPY certs/server.key


RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8082
