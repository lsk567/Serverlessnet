"""
Simple topology to simulate three containers (d1, d2, d3),
1 switch, and one controller:

            (c)
             |
          - (s1)-
         |   |   |
       (d1) (d2) (d3)
     sender open receiver
           lambda
"""
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers using ubuntu:trusty images\n')
d1 = net.addDocker('d1',
                   dimage="lsk567/lambda_switch",
                   ports=[4999], # docker host ports to be opened
                   port_bindings={4999:4999}, # { docker host port : machine port }
                   dcmd="python -u switch.py",
                   publish_all_ports=True)

d2 = net.addDocker('d2',
                   dimage="lsk567/lambda_relayer",
                   ports=[4997],
                   port_bindings={4997:4997},
                   dcmd="python -u relayer.py",
                   publish_all_ports=True)
            
d3 = net.addDocker('d3',
                   dimage="lsk567/lambda_actuator",
                   ports=[4998],
                   port_bindings={4998:4998},
                   dcmd="python -u actuator.py",
                   publish_all_ports=True)

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d2, s1)
net.addLink(d3, s1)
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()