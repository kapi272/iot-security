import sys
import time
import socket
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udp_gen")

def simulate_udp(target_ip, port=5060):
    logger.info(f"Starting simulated UDP stream to {target_ip}:{port}")
    
    # UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        packet_count = 0
        while True:
            try:
                # Generate 256 bytes of random payload to mimic video/audio frames
                payload = os.urandom(256)
                s.sendto(payload, (target_ip, port))
                packet_count += 1
                
                if packet_count % 100 == 0:
                    logger.info(f"Sent {packet_count} UDP packets to {target_ip}:{port}")
                    
                # Stream at ~10 packets per second
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Unexpected error sending UDP packet: {e}")
                time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python udp_gen.py <target_ip>")
        sys.exit(1)
        
    target = sys.argv[1]
    simulate_udp(target)
