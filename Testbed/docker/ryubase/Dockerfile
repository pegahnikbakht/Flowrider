# Ryu SDN Container
# 
# Loosely based on https://registry.hub.docker.com/u/osrg/ryu/dockerfile/
# and http://ewen.mcneill.gen.nz/blog/entry/2014-08-31-ryu-on-ubuntu-14-04/
# and https://ewen.mcneill.gen.nz/blog/entry/2014-10-07-ryu-and-openvswitch-on-docker/
# VERSION 0.0.1

FROM ubuntu:14.04

MAINTAINER Nicolae Paladi <nicolae.paladi@eit.lth.se>

RUN apt-get update
RUN apt-get install -qy --no-install-recommends python-pbr python-py python-six python-oslo.config python-eventlet python-lxml python-netaddr python-paramiko python-routes python-webob python-sphinx python-pip

ENV HOME /root
WORKDIR /root

ADD requirements.txt /root/requirements.txt
RUN pip install python2-secrets
RUN pip install -r /root/requirements.txt
