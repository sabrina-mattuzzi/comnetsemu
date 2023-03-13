#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
TOPOLOGY:

    r2----------r3
    |          / |
    |         /  |
    |        /   |
    |       /    |
    |      /     |
    |     /      |
    |    /       |
    |   /        |
    |  /         |
    | /          |
    r1-----------r4 
                 |
                 |
                 r5

"""

from mininet.topo import Topo 
from mininet.node import Node, Controller, OVSBridge
from mininet.log import setLogLevel, info
from mininet.link import TCLink

from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost

from comnetsemu.cli import CLI


PING_COUNT = 15

def run_topo():
    net = Containernet(
        controller=Controller, link=TCLink, switch=OVSBridge
    )

    #add routers
    r1 = net.addDockerHost(
                "r1",
                dimage= "dinamic_router",
                docker_args={ "hostname": "r1" }
            )
    r2 = net.addDockerHost(
                "r2",
                dimage="dinamic_router",
                docker_args={ "hostname": "r2" }
            )
    r3 = net.addDockerHost(
                "r3",
                dimage="dinamic_router",
                docker_args={ "hostname": "r3" }
            )
    r4 = net.addDockerHost(
                "r4",
                dimage="dinamic_router",
                docker_args={ "hostname": "r4" }
            )
    r5 = net.addDockerHost(
                "r5",
                dimage="dinamic_router",
                docker_args={ "hostname": "r5" }
            )
    #add links
    net.addLink( r1, r2, cls=TCLink, intfName1='eth1', intfName2='eth1', params1={ 'ip' :'100.0.0.1/30'}, params2={ 'ip' :'100.0.0.2/30'})
    net.addLink( r1, r3, cls=TCLink, intfName1='eth3', intfName2='eth3', params1={ 'ip' :'100.0.0.5/30'}, params2={ 'ip' :'100.0.0.6/30'})
    net.addLink( r2, r3, cls=TCLink, intfName1='eth2', intfName2='eth2', params1={ 'ip' :'100.0.0.13/30'}, params2={ 'ip' :'100.0.0.14/30'})  
    net.addLink( r3, r4, cls=TCLink, intfName1='eth1', intfName2='eth1', params1={ 'ip' :'100.0.0.17/30'}, params2={ 'ip' :'100.0.0.18/30'})
    net.addLink( r1, r4, cls=TCLink, intfName1='eth2', intfName2='eth2', params1={ 'ip' :'100.0.0.9/30'}, params2={ 'ip' :'100.0.0.10/30'})
    net.addLink( r4, r5, cls=TCLink, intfName1='eth3', intfName2='eth3', params1={ 'ip' :'100.0.0.21/30'}, params2={ 'ip' :'100.0.0.22/30'})
    
   
    info("*** Starting network\n")
    net.start()
    info('*** starting zebra and ripd\n')
    info('**r1\n')
    info(r1.cmd('/etc/init.d/zebra restart'))
    info(r1.cmd('/etc/init.d/ripd restart'))
    info('**r2\n')
    info(r2.cmd('/etc/init.d/zebra restart'))
    info(r2.cmd('/etc/init.d/ripd restart'))
    info('**r3\n')
    info(r3.cmd('/etc/init.d/zebra restart'))
    info(r3.cmd('/etc/init.d/ripd restart'))
    info('**r4\n')
    info(r4.cmd('/etc/init.d/zebra restart'))
    info(r4.cmd('/etc/init.d/ripd restart'))
    info('**r5\n')
    info(r5.cmd('/etc/init.d/zebra restart'))
    info(r5.cmd('/etc/init.d/ripd restart'))
    info('\n')

    info('\n**** wait for routers to build their own routing table\n\n')
    info('*** you can connect to the daemon using the "<hostname> telnet localhost <name-daemon>" command (password: "zebra")\n')
    info('*** use the command "<hostname> vtysh" to access the integrated user interface shell and then:\n')
    info('** "traceroute <IP>" to trace the paths of data packets from their origin to their destinations\n')
    info('** "show ip rip" to show RIP routes\n')
        
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run_topo()