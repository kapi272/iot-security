import subprocess
import logging
from mininet.net import Containernet
from mininet.node import Controller
from mininet.link import Intf

logger = logging.getLogger(__name__)

def build_simulation_topology(node_count: int) -> Containernet:
    """
    Builds the Containernet topology for the simulated IoT network.
    """
    logger.info("Initializing Containernet network...")
    net = Containernet(controller=Controller)
    
    logger.info("Adding default controller (c0)...")
    net.addController('c0')
    
    logger.info("Adding OpenFlow virtual switch (s1)...")
    s1 = net.addSwitch('s1')
    
    nodes = []
    base_ip_prefix = "10.0.0."
    
    # 1. Create Virtual IoT Nodes
    for i in range(1, node_count + 1):
        node_name = f'd{i}'
        ip_addr = f'{base_ip_prefix}{i}/24'
        logger.info(f"Adding lightweight Docker node {node_name} with IP {ip_addr}...")
        
        # Containernet uses Docker images. Alpine is lightweight.
        node = net.addDocker(node_name, ip=ip_addr, dimage="alpine:latest")
        nodes.append(node)
        
        logger.info(f"Connecting {node_name} to s1...")
        net.addLink(node, s1)
        
    logger.info("Starting Mininet/Containernet network...")
    net.start()
    
    # 2. Establish the T-Pot Virtual Bridge
    bridge_interface = "br-74cf9d0e3e6d"
    tpot_honeypot_ip = "172.18.0.6"
    
    veth_name_host = "veth-tpot-h"
    veth_name_mn = "veth-tpot-mn"
    
    logger.info(f"Creating veth pair to link s1 to T-Pot bridge '{bridge_interface}'...")
    try:
        # Create veth pair
        subprocess.run(["ip", "link", "add", veth_name_host, "type", "veth", "peer", "name", veth_name_mn], check=True, capture_output=True)
        # Bring interfaces up
        subprocess.run(["ip", "link", "set", veth_name_host, "up"], check=True, capture_output=True)
        subprocess.run(["ip", "link", "set", veth_name_mn, "up"], check=True, capture_output=True)
        
        # Attach the host end to the Docker bridge (using iproute2)
        subprocess.run(["ip", "link", "set", veth_name_host, "master", bridge_interface], check=True, capture_output=True)
        
        # Attach the mininet end to the s1 switch
        Intf(veth_name_mn, node=s1)
        logger.info("Successfully established veth bridge to T-Pot.")
        
    except Exception as e:
        logger.error(f"Failed to setup veth bridge (expected if not running on Linux as root): {e}")
        
    # 3. Configure Default Routes
    logger.info("Configuring default routes on virtual nodes to point to T-Pot honeypot...")
    for node in nodes:
        node.cmd(f"ip route add default via {tpot_honeypot_ip}")
        
    logger.info("Topology setup complete.")
    return net
