import subprocess
import logging
from mininet.net import Containernet
from mininet.node import Controller
from mininet.link import Intf
from typing import Tuple, List
import os

logger = logging.getLogger(__name__)

def build_simulation_topology(node_count: int) -> Tuple[Containernet, List[int]]:
    """
    Builds the Containernet topology for the simulated IoT network and launches baseline traffic.
    Returns:
        tuple containing the Mininet network object and a list of host-side PIDs of the traffic generators.
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
        
        # Mount traffic generators
        tg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'traffic_generators'))
        
        # Containernet uses Docker images. python:3.9-alpine has python pre-installed.
        node = net.addDocker(node_name, ip=ip_addr, dimage="python:3.9-alpine", volumes=[f"{tg_dir}:/traffic_generators:ro"])
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
        
    # 3. Configure Default Routes and Launch Traffic Generators
    logger.info("Configuring default routes and launching baseline traffic on virtual nodes...")
    pids = []
    
    for i, node in enumerate(nodes):
        # Configure route to T-Pot
        node.cmd(f"ip route add default via {tpot_honeypot_ip}")
        
        # Assign traffic generation role based on node index
        if i % 3 == 0:
            script = "http_gen.py"
        elif i % 3 == 1:
            script = "mqtt_gen.py"
        else:
            script = "udp_gen.py"
            
        logger.info(f"Launching {script} on {node.name} targeting {tpot_honeypot_ip}...")
        try:
            proc = node.popen(["python", f"/traffic_generators/{script}", tpot_honeypot_ip])
            if proc and proc.pid:
                pids.append(proc.pid)
                logger.info(f"[{node.name}] Started {script} (Host PID: {proc.pid})")
        except Exception as e:
            logger.error(f"Failed to launch script on {node.name}: {e}")
            
    logger.info(f"Topology setup complete. Returning {len(pids)} traffic generator PIDs.")
    return net, pids


def build_live_topology(interface: str) -> Containernet:
    """
    Builds the Containernet topology for live traffic analysis by bridging a physical interface.
    Returns:
        The Mininet network object.
    """
    logger.info("Initializing Live Mode network...")
    net = Containernet(controller=Controller)
    
    logger.info("Adding default controller (c0)...")
    net.addController('c0')
    
    logger.info("Adding OpenFlow virtual switch (s1)...")
    s1 = net.addSwitch('s1')
    
    logger.info("Starting Mininet/Containernet network...")
    net.start()
    
    # 1. Establish the T-Pot Virtual Bridge
    bridge_interface = "br-74cf9d0e3e6d"
    
    veth_name_host = "veth-tpot-h"
    veth_name_mn = "veth-tpot-mn"
    
    logger.info(f"Creating veth pair to link s1 to T-Pot bridge '{bridge_interface}'...")
    try:
        # Create veth pair
        subprocess.run(["ip", "link", "add", veth_name_host, "type", "veth", "peer", "name", veth_name_mn], check=True, capture_output=True)
        # Bring interfaces up
        subprocess.run(["ip", "link", "set", veth_name_host, "up"], check=True, capture_output=True)
        subprocess.run(["ip", "link", "set", veth_name_mn, "up"], check=True, capture_output=True)
        
        # Attach the host end to the Docker bridge
        subprocess.run(["ip", "link", "set", veth_name_host, "master", bridge_interface], check=True, capture_output=True)
        
        # Attach the mininet end to the s1 switch
        Intf(veth_name_mn, node=s1)
        logger.info("Successfully established veth bridge to T-Pot.")
        
    except Exception as e:
        logger.error(f"Failed to setup veth bridge (expected if not running on Linux as root): {e}")
        
    # 2. Attach Physical Interface
    logger.info(f"Attaching physical interface '{interface}' to virtual switch...")
    try:
        # Attach interface to switch via Mininet Intf
        Intf(interface, node=s1)
        
        # Set promiscuous mode so all traffic flows into the switch for Suricata
        subprocess.run(["ip", "link", "set", interface, "promisc", "on"], check=True, capture_output=True)
        logger.info(f"Interface '{interface}' bound and promiscuous mode enabled.")
    except Exception as e:
        logger.error(f"Failed to attach physical interface '{interface}' (expected on macOS or non-root): {e}")
        
    logger.info("Live topology setup complete.")
    return net
