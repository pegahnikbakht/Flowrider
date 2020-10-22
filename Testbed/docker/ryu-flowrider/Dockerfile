# Ryu SDN Container
#
# Loosely based on https://registry.hub.docker.com/u/osrg/ryu/dockerfile/
# and http://ewen.mcneill.gen.nz/blog/entry/2014-08-31-ryu-on-ubuntu-14-04/
#
# Built based on separate Ryu build container, to increase the amount of
# useful caching that we get; see "two Dockerfile" approach here:
#
# http://jpetazzo.github.io/2013/12/01/docker-python-pip-requirements/
#
# (in particular there is no caching beyond "ADD", because it could change
# on any run.)
#
# For syntax, see: http://docs.docker.com/reference/builder/
# Based on https://ewen.mcneill.gen.nz/blog/entry/2014-10-07-ryu-and-openvswitch-on-docker/
# VERSION 0.0.1

FROM ryu312
MAINTAINER Nicolae Paladi <nicolae.paladi@eit.lth.se>

# OpenFlow ports -- de facto (6633) and IANA assigned (6653)
EXPOSE 6633 6653

# Port for the OOB communication
EXPOSE 5000

# Add Ryu user account
RUN groupadd --system ryu
RUN useradd  --system -d /home/ryu -m -s /bin/bash -g ryu ryu

# Add application into container
ADD flowrider4.py /home/ryu/flowrider4.py

# Default command is to run Ryu against that application
CMD ["/bin/su", "-c", "/usr/local/bin/ryu-manager", "/home/ryu/flowrider4.py"]
