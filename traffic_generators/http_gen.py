import sys
import time
import urllib.request
import urllib.error
import random
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("http_gen")

def simulate_http(target_ip, port=80):
    logger.info(f"Starting simulated HTTP telemetry traffic to {target_ip}:{port}")
    endpoints = ["/api/v1/status", "/metrics", "/health", "/update"]
    
    while True:
        endpoint = random.choice(endpoints)
        url = f"http://{target_ip}:{port}{endpoint}"
        try:
            # We don't care about the response, just that we are hitting the honeypot
            logger.info(f"Sending GET request to {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'IoT-Device/1.0'})
            with urllib.request.urlopen(req, timeout=5.0) as response:
                response.read()
        except urllib.error.URLError as e:
            logger.warning(f"Request to {url} failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            
        # Random sleep between 2 to 10 seconds
        time.sleep(random.uniform(2, 10))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python http_gen.py <target_ip>")
        sys.exit(1)
        
    target = sys.argv[1]
    simulate_http(target)
