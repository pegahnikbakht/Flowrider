*Original setup based on:
  https://ewen.mcneill.gen.nz/blog/entry/2014-10-07-ryu-and-openvswitch-on-docker/
and  https://naos.co.nz/talks/seize-control-with-ryu/seize-control-with-ryu.pdf*

Author: Nicolae Paladi <nicolae.paladi@eit.lth.se>

# Build Instructions
Assuming you start from the "Testbed" folder.

## Build Instructions (Docker images)


  **Building the Ryu base:**

    cd docker/ryubase/
    docker build -t ryu312 .

 **Building the Ryu docker layer1**

    cd docker/ryu-flowrider/
    docker build -t ryu-flowrider .

 **Building the flowrider guest container images**

    cd docker/flowrider-guest/
    docker build -t flowrider-guest .

**Building the PSK client-server applications**

    cd docker/flowrider-guest/

  * server:

        gcc -Wall -Werror -c psk-server.c -o psk-server.o `pkg-config gnutls --cflags`
        gcc psk-server.o -o psk-server `pkg-config gnutls --libs`

  * client:

        gcc -Wall -Werror -c psk-client.c -o psk-client.o `pkg-config gnutls --cflags`
        gcc psk-client.o -o psk-client `pkg-config gnutls --libs`


**Building the PKI client-server applications**

    cd docker/flowrider-guest/

  * server:

        gcc -Wall -Werror -c psk-server.c -o psk-server.o `pkg-config gnutls --cflags`
        gcc psk-server.o -o psk-server `pkg-config gnutls --libs`

  * client:

        gcc -Wall -Werror -c psk-client.c -o psk-client.o `pkg-config gnutls --cflags`
        gcc psk-client.o -o psk-client `pkg-config gnutls --libs`


# Launching the setup:
    ./flowrider-example

### Testing with the Ryu application "flowrider4.py".
You will need several terminals:

  * flowrider_h2 - terminal 1

        docker attach flowrider_h1
        cd /endpoint
        python keyserver.py

* flowrider_h2 - terminal 2
        docker exec -it flowrider_h2 /bin/bash
        cd /endpoint
        ./psk-server

* flowrider_h1 - terminal 1
        docker attach flowrider_h1
        cd /endpoint
        python keyserver.py

* flowrider_h1 - terminal 2
        docker exec -it flowrider_h2 /bin/bash
        cd /endpoint
        ./psk-client

**Note that to switch between the psk and pki approaches you  need to modify flowrider4.py and rebuild the ryu-flowrider image**

### Cleanup
    ./cleanup.sh


## Runnning multiple tests in the container:
    for run in {1..10}; do (time ./psk-client); done
