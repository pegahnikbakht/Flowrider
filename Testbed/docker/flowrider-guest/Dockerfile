# Ryu SDN Example Guest -- for the FlowRider2020 example
# 


FROM python:alpine3.7

RUN apk update
RUN apk add  bind-tools
RUN apk add  iputils net-tools
RUN apk add --no-cache bash

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python keyserver.py


