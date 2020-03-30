*Based on:
  https://ewen.mcneill.gen.nz/blog/entry/2014-10-07-ryu-and-openvswitch-on-docker/
and  https://naos.co.nz/talks/seize-control-with-ryu/seize-control-with-ryu.pdf*

  
# Build Instructions

  **Building the Ryu base:**

    docker build -t ryu312 .

 **Building the Ryu docker layer1**

    docker build -t ryu-flowrider .

 **Starting the Ryu container:**

    docker run -i -t -p 6633:6633 -p 6653:6653 ryu-kiwipycon

### Test with the Ryu application "flowrider3.py"

    docker attach kiwipycon_h1
    ping -c 5 -W 1 172.31.1.2         # Observe timeouts
    dig @172.31.1.2 +time=1 +tries=1 +short xyzzy.example.com
    ping -c 5 -W 1 172.31.1.2         # Observe it now works


### Cleanup
    ./cleanup.sh
