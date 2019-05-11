"""
Simple topology to simulate three containers (d1, d2, d3),
1 switch, and one controller:

            (c0)
             |
        -- (s1) -------
        |    |        |
      (d1)  (d2)     (d3)
    sender relayer receiver
"""
import sys
from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
setLogLevel('info')

# Get node count from commandline
if len(sys.argv) != 2:
  raise Exception('Invalid number of command line arguments. Expected 1 but ' + str(len(sys.argv) - 1) + ' given.')
hostCount = int(sys.argv[1])
if hostCount < 1:
  raise Exception('Host count must be greater than 0.')

net = Containernet(controller=Controller)
info('*** Adding controller\n')
net.addController('c0')
info('*** Adding docker containers using ubuntu:trusty images\n')

# Add relayer
r0 = net.addDocker('r0',
                   dimage="lsk567/lambda_relayer",
                   ports=[5000],
                   port_bindings={5000:4999},
                   dcmd="python -u relayer.py",
                   publish_all_ports=True)
# Add switch and actuator                  
nodes = {'switch': [],
        'actuator': []}
for i in range(hostCount):
  nodes['switch'].append(net.addDocker('sw' + str(i),
                        dimage='lsk567/lambda_switch',
                        ports=[5000], # docker host ports to be opened
                        port_bindings={5000: (5000 + i)}, # { docker host port : machine port }
                        dcmd='python -u switch.py ' + str(5000 + hostCount + i), # pass in target actuator's port
                        publish_all_ports=True))
                  
  nodes['actuator'].append(net.addDocker('a' + str(i),
                        dimage='lsk567/lambda_actuator',
                        ports=[5000], # docker host ports to be opened
                        port_bindings={5000: (5000 + hostCount + i)}, # { docker host port : machine port }
                        dcmd='python -u actuator.py',
                        publish_all_ports=True))

info('*** Adding mininet switches\n')
s1 = net.addSwitch('s1')

# Link all hosts to switch
info('*** Creating links\n')
net.addLink(r0, s1)
for i in range(hostCount):
  net.addLink(nodes['switch'][i], s1)
  net.addLink(nodes['actuator'][i], s1)

info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()