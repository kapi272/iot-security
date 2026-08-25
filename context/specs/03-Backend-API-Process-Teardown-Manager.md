# Spec: Unit 3 - Backend API & Process Teardown Manager

## Objective
Establish the Python backend server (using FastAPI or Flask) to serve as the system orchestrator. This unit focuses on binding the server strictly to `127.0.0.1`, setting up the in-memory state tracking for active processes, and implementing the critical teardown manager to ensure network namespaces and background processes are safely cleaned up (`mn -c`) when a simulation ends or crashes.

## System Boundary
- **Target:** `/backend` directory (Python server files).
- **Protected:** Do not implement the actual Containernet topology logic (`/topology`) or offensive scripts (`/attacks`) in this unit. Mock the subprocess executions for starting the network and attacks.

## Implementation Steps

### 1. Initialize the Python Backend
- Create a new Python application (e.g., `main.py` using FastAPI or Flask).
- Configure the web server (e.g., Uvicorn for FastAPI) to bind strictly and exclusively to `127.0.0.1` (localhost) to prevent external access.
- Configure CORS (Cross-Origin Resource Sharing) middleware to allow requests only from the local frontend origin.

### 2. Implement In-Memory State Management
- Define a global, in-memory state object (e.g., a Python dictionary or dataclass) to track:
  - `status`: Current system state (e.g., `idle`, `simulating`, `attacking`).
  - `active_pids`: A list or dictionary of active subprocess IDs (for tracking Mininet, background traffic generators, and attack scripts).
- Ensure no databases (SQLite, etc.) are initialized. State must be purely ephemeral.

### 3. Create Core API Endpoints
- **POST `/api/network/start`:** Accept payload parameters (mode, node count, interface). Update state to `simulating`. (Log a mock message instead of actually launching Mininet for now).
- **POST `/api/attacks/trigger`:** Accept payload (attack type). Update state to `attacking`. (Log a mock message instead of actually launching Hydra/Nmap).
- **POST `/api/system/stop`:** The critical endpoint that triggers the Teardown Manager and resets the in-memory state to `idle`.

### 4. Implement the Teardown Manager
- Write a dedicated cleanup function (`teardown_environment()`).
- Implement subprocess calls to explicitly execute `mn -c` (Mininet clean) to wipe virtual network interfaces and switches.
- Iterate through the `active_pids` list and send `SIGTERM`/`SIGKILL` to forcefully terminate orphaned attack or traffic generation processes.
- Ensure any future long-running orchestrator tasks are wrapped in a `try...finally` block, where the `finally` clause strictly calls `teardown_environment()`.

## Verification & Success Criteria
1. **Root Execution & Binding:** The backend successfully launches using `sudo`/root privileges and strictly listens on `127.0.0.1`.
2. **Frontend Integration:** Clicking the "Stop System" button on the frontend successfully hits the `/api/system/stop` backend endpoint (verified via network tab or backend logs).
3. **Cleanup Execution:** When the stop endpoint is triggered, the backend console logs explicitly show the execution of `mn -c` and the clearing of tracked PIDs.
4. **Statelessness:** Restarting the Python backend completely flushes the `active_pids` and resets the status to `idle`.