## Run the emulation

The emulation script can be executed with:

```
cd comnetsemu

$ sudo make dinamic-router
```

This command runs the "run.sh" file, which builds the docker image. Quagga is installed in the docker image which allows, through the use of its daemons, the use of various routing protocols.
The quagga's configuration files are created in the file "confQuagga.sh".
At the beginning of each example is the topology of the network.
After the used daemons are restarted, the CLI mode is entered.

list of useful commands:

-telnet localhost 'name-daemon'         To connect to a daemon. The password to access it is always 'zebra'.
-'name-router' vtysh                    To enter vtysh mode
--in vtysh mode:
    -write                              See used configuration files
    -show ip route                      see the routing table of the router.
    -traceroute 'IP address'            see the path of packets to the chosen IP address.
    -tcpdump                            sniff packets.

# RIP router #
This example shows how to build and use a dynamic router with RIP protocol.

# OSPF router #
This example shows how to build and use a dynamic router with OSPF protocol.
