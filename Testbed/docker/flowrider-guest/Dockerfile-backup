# Ryu SDN Example Guest -- for the FlowRider2020 example
#


FROM python:alpine3.7

RUN apk update
RUN apk add  bind-tools
RUN apk add  iputils net-tools
RUN apk add --no-cache bash

# Add application and data into container
COPY . /endpoint

#RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8082
