import sys
import time
import socket
import json
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mqtt_gen")

def simulate_mqtt(target_ip, port=1883):
    logger.info(f"Starting simulated MQTT traffic to {target_ip}:{port}")
    while True:
        try:
            # Create a simple TCP socket simulating an MQTT connect/publish payload
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5.0)
                s.connect((target_ip, port))
                
                # MQTT Connect packet structure (mock)
                connect_packet = b"\x10\x12\x00\x04MQTT\x04\x02\x00\x3c\x00\x06device"
                s.sendall(connect_packet)
                time.sleep(1)
                
                # MQTT Publish packet structure (mock JSON payload)
                topic = "iot/sensors/env"
                payload = json.dumps({"temp": random.uniform(20.0, 30.0), "humidity": random.uniform(30.0, 50.0)})
                # Very rough raw construction of publish packet for honeypot triggering
                pub_packet = b"\x30" + bytes([len(topic) + len(payload) + 2]) + bytes([0, len(topic)]) + topic.encode() + payload.encode()
                
                s.sendall(pub_packet)
                logger.info(f"Published payload: {payload}")
                
        except (socket.timeout, ConnectionRefusedError) as e:
            logger.warning(f"Connection failed: {e}. Retrying in 5s...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mqtt_gen.py <target_ip>")
        sys.exit(1)
        
    target = sys.argv[1]
    simulate_mqtt(target)
