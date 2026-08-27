import subprocess
import os
import signal
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import logging
import sys

# Add parent directory to path to import topology
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from topology.simulated_network import build_simulation_topology, build_live_topology
except ImportError as e:
    # Handle environment without mininet/containernet gracefully for testing
    logging.warning(f"Failed to import topology module: {e}")
    build_simulation_topology = None
    build_live_topology = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Autonomous IoT Cyber Defense - Teardown Manager")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory State
class SystemState:
    status: str = "idle"
    active_pids: List[int] = []
    net: Optional[Any] = None
    promisc_interface: Optional[str] = None

state = SystemState()

# Request Models
class NetworkStartRequest(BaseModel):
    mode: str
    node_count: int
    device_type: str
    interface: Optional[str] = None

class AttackRequest(BaseModel):
    attack_type: str
    target: Optional[str] = None

def teardown_environment():
    logger.info("Initiating teardown manager...")
    # 1. Kill tracked PIDs
    for pid in state.active_pids:
        try:
            logger.info(f"Sending SIGTERM to PID {pid}")
            os.kill(pid, signal.SIGTERM)
        except OSError as e:
            logger.warning(f"Failed to kill PID {pid}: {e}")
    
    state.active_pids.clear()
    
    # 2. Cleanup Promiscuous Interface if Live Mode was used
    if state.promisc_interface:
        logger.info(f"Disabling promiscuous mode on {state.promisc_interface}...")
        try:
            subprocess.run(["sudo", "-n", "ip", "link", "set", state.promisc_interface, "promisc", "off"], check=True, capture_output=True)
        except Exception as e:
            logger.warning(f"Failed to disable promiscuous mode on {state.promisc_interface}: {e}")
        finally:
            state.promisc_interface = None
            
    # 3. Stop Mininet network
        logger.info("Stopping Containernet network...")
        try:
            state.net.stop()
        except Exception as e:
            logger.warning(f"Error stopping network gracefully: {e}")
        finally:
            state.net = None
            
    # 4. Cleanup Mininet
    logger.info("Running 'mn -c' to clean virtual network interfaces...")
    try:
        subprocess.run(["sudo", "-n", "mn", "-c"], check=True, capture_output=True)
        logger.info("Mininet cleanup successful.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Mininet cleanup failed: {e.stderr.decode()}")

@app.post("/api/network/start")
async def start_network(req: NetworkStartRequest):
    if state.status != "idle":
        raise HTTPException(status_code=400, detail="System is not idle.")
    
    state.status = "simulating"
    logger.info(f"Starting network with mode={req.mode}, nodes={req.node_count}, device={req.device_type}")
    
    if req.mode == "simulation":
        if build_simulation_topology:
            try:
                state.net, pids = build_simulation_topology(req.node_count)
                if pids:
                    state.active_pids.extend(pids)
                    logger.info(f"Tracking {len(pids)} traffic generator processes.")
            except Exception as e:
                logger.error(f"Failed to start simulation topology: {e}")
                state.status = "error"
                raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")
        else:
            logger.warning("Containernet module missing, running in dry-run mode.")
            
    elif req.mode == "live":
        if not req.interface:
            raise HTTPException(status_code=400, detail="An interface must be specified for live mode.")
            
        if build_live_topology:
            try:
                state.net = build_live_topology(req.interface)
                state.promisc_interface = req.interface
                logger.info(f"Live mode started on interface {req.interface}.")
            except Exception as e:
                logger.error(f"Failed to start live topology: {e}")
                state.status = "error"
                raise HTTPException(status_code=500, detail=f"Live simulation failed: {e}")
        else:
            logger.warning("Containernet module missing, running in dry-run mode.")
            state.promisc_interface = req.interface
    
    return {"status": "success", "message": f"Network started in {req.mode} mode"}

@app.post("/api/attacks/trigger")
async def trigger_attack(req: AttackRequest):
    if state.status != "simulating":
        raise HTTPException(status_code=400, detail="System must be simulating to launch attacks.")
    
    state.status = "attacking"
    logger.info(f"Triggering attack: {req.attack_type}")
    # TODO: In future units, we will launch attack scripts here and track their PIDs
    
    return {"status": "success", "message": f"Attack '{req.attack_type}' triggered"}

@app.post("/api/system/stop")
async def stop_system():
    logger.info("System stop requested.")
    teardown_environment()
    state.status = "idle"
    return {"status": "success", "message": "System stopped and environment cleaned."}

if __name__ == "__main__":
    logger.info("Starting Backend Server on 127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
