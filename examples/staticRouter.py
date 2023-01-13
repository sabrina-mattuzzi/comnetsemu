#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
"""
TOPOLOGY:

    r1----------------------r2
    |                       |
    s1                      |
   /   \                    |
 h1     h2                  h3
"""

from mininet.topo import Topo
from mininet.node import Node, Controller, OVSBridge
from mininet.log import setLogLevel, info
from mininet.link import TCLink

from comnetsemu.net import Containernet
from comnetsemu.node import DockerHost

from mininet.cli import CLI

PING_COUNT = 15

class staticRouter( Node ):
    def config( self, **params ):
        super( staticRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( staticRouter, self ).terminate()
    
    def newAddr(self, ip, link):
        self.cmd("ip addr add '%s' dev '%s'"%(ip, link))

    def newRoute(self, ip, link):
        self.cmd("ip route add '%s' dev '%s'"%(ip, link))

class TestTopo(Topo):
    def build(self):
        #add hosts
        host1 = self.addHost(
                "h1",
                cls=DockerHost,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
                ip='192.0.0.1/24'
            )
        host2 = self.addHost(
                "h2",
                cls=DockerHost,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
                ip='192.0.0.2/24',
            )
        host3 = self.addHost(
                "h3",
                cls=DockerHost,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
                ip='192.10.0.3/24'
            )
        #add routers
        router1 = self.addHost(
                "r1",
                cls=staticRouter,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
                ip='10.0.1.1'
            )
        router2 = self.addHost(
                "r2",
                cls=staticRouter,
                dimage="dev_test",
                docker_args={"cpuset_cpus": "0", "nano_cpus": int(1e8)},
                ip='10.0.2.1'
            )
        #add switch
        switch1 = self.addSwitch("s1", cls=OVSBridge)
        
        #add links
        self.addLink( router1, router2, cls=TCLink, intfName1='eth2', intfName2='eth2')
        self.addLink( router2, host3, cls=TCLink, intfName1='eth3', intfName2='eth3', params1={ 'ip' :'192.10.0.5/24'})
        self.addLink( router1, switch1, cls=TCLink, intfName1='eth1', intfName2='eth1', params1={ 'ip' :'192.0.0.0/24'})
        self.addLink( host1, switch1, cls=TCLink, intfName1='eth1', intfName2='h1')
        self.addLink( host2, switch1, cls=TCLink, intfName1='eth1', intfName2='h2')
       
        
def run_topo():
    net = Containernet(
        controller=Controller, link=TCLink, switch=OVSBridge, topo=TestTopo()
    )

    info("*** Starting network\n")
    net.start()
   
    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")
    r1 = net.get("r1")
    r2 = net.get("r2")

    r1.newAddr('192.0.0.1', 'eth1')
    r1.newAddr('192.0.0.2', 'eth1')
    r1.newRoute('192.10.0.0/24', 'eth2')

    r2.newAddr('192.10.0.3', 'eth3')    
    r2.newRoute('192.0.0.0/24', 'eth2')

    h1.cmd("ip addr add 10.0.1.1 dev eth1")
    h1.cmd("ip addr add 10.0.2.1 dev eth1")
    h1.cmd("ip addr add 192.10.0.3 dev eth1")
    
    h2.cmd("ip addr add 10.0.1.1 dev eth1")
    h2.cmd("ip addr add 10.0.2.1 dev eth1")
    h2.cmd("ip addr add 192.10.0.3 dev eth1")

    h3.cmd("ip addr add 10.0.2.1 dev eth3")
    h3.cmd("ip addr add 10.0.1.1 dev eth3")
    h3.cmd("ip addr add 192.0.0.1 dev eth3")
    h3.cmd("ip addr add 192.0.0.2 dev eth3")
    
    info( '\n*** Routing Table on Router r1:\n' )
    info( r1.cmd( 'route' ) )
    info( '\n*** Routing Table on Router r2:\n' )
    info( r2.cmd( 'route' ) )

    net.pingAll()
    #net.pingAllFull()
    CLI( net )

    info("*** Stopping network")
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run_topo()