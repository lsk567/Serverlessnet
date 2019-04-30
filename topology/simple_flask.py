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
                  #  ip='10.0.0.251',
                   dimage="lsk567/lambda_proxy",
                   ports=[5000], # docker host ports to be opened
                   port_bindings={5000:5000}, # { docker host port : machine port }
                   dcmd="python -u proxy.py",
                   publish_all_ports=True)

d2 = net.addDocker('d2',
                  #  ip='10.0.0.252',
                   dimage="lsk567/lambda_proxy",
                   ports=[5000],
                   port_bindings={5000:5001},
                   dcmd="python -u proxy.py",
                   publish_all_ports=True)
            
d3 = net.addDocker('d3',
                  #  ip='10.0.0.253',
                   dimage="lsk567/lambda_proxy",
                   ports=[5000],
                   port_bindings={5000:5002},
                   dcmd="python -u proxy.py",
                   publish_all_ports=True)

info('*** Adding switches\n')
s1 = net.addSwitch('s1')
info('*** Creating links\n')
net.addLink(d1, s1)
net.addLink(d2, s1)
net.addLink(d3, s1)
info('*** Starting network\n')
net.start()
# info('*** Testing connectivity\n')
# net.ping([d1, d2, d3])
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()