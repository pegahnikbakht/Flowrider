
# Ryu SDN Guest for the FlowRider2020 demonstrator
#


FROM occlum/occlum:0.18.1-ubuntu18.04

RUN apt-get update
Run apt-get install -qy  dnsutils iputils-ping netcat ipython
RUN apt-get install -qy  gnutls-bin libgnutls28-dev

# Add application and data into container
COPY . /endpoint

#RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 8082
