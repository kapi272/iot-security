# Spec: Unit 4 - Containernet Topology (Simulation Mode)

## Objective
Develop the core network virtualization script using Containernet (a Mininet fork) to generate the simulated IoT network. This unit is responsible for spinning up the configured number of lightweight virtual nodes, instantiating the virtual switch (`s1`), and critically, establishing the virtual ethernet (`veth`) bridge that connects the simulated network to the external T-Pot Docker environment (Defense Core)[cite: 6, 7].

## System Boundary
- **Target:** `/topology` directory (Python Containernet scripts)[cite: 6].
- **Protected:** Do not write backend API routing logic (`/backend`) or background traffic generation scripts (`/traffic_generators`) in this unit. Focus strictly on network infrastructure and node instantiation.

## Implementation Steps

### 1. Initialize the Topology Script
- Create a Python script (e.g., `simulated_network.py`) inside the `/topology` directory.
- Import the necessary Containernet/Mininet modules (`Containernet`, `node.Controller`, `link.TCLink`, `CLI`).
- Define a function `build_simulation_topology(node_count: int)` that accepts the dynamic number of nodes requested by the user from the UI.

### 2. Instantiate Virtual Switch and Nodes
- Initialize the Mininet network object with a default controller.
- Add a central OpenFlow virtual switch (e.g., `s1`) to the network.
- Loop `node_count` times to create lightweight Docker containers (e.g., using a base `alpine` image) that act as the virtual IoT devices[cite: 7].
- Connect each virtual IoT node to the `s1` switch using Mininet links. Assign IP addresses sequentially within the safe virtual subnet (e.g., `10.0.0.0/24`)[cite: 6, 7].

### 3. Establish the T-Pot Virtual Bridge
- Create a virtual ethernet (`veth`) pair to link the Mininet environment to the Docker network where T-Pot is running[cite: 7].
- Attach one end of the `veth` pair to the virtual switch (`s1`).
- Attach the other end to the Docker bridge network used by the T-Pot containers (often `docker0` or a custom T-Pot bridge network).
- Ensure routing tables within the virtual nodes are configured to route default traffic toward the T-Pot honeypot IP address.

### 4. Integrate with the Backend Orchestrator
- Modify the `/api/network/start` endpoint (created in Unit 3) to actually import and execute `build_simulation_topology()`.
- Ensure the network object (`net`) is preserved in the backend's memory state so that the Teardown Manager can cleanly execute `net.stop()` and `mn -c` when the session ends[cite: 6, 7].

## Verification & Success Criteria
1. **Topology Generation:** Clicking "Start Network (Simulation Mode)" in the frontend successfully triggers the backend to spawn the specified number of virtual nodes (verifiable via `docker ps` showing the lightweight Alpine containers)[cite: 7].
2. **Bridge Connectivity:** Executing a `ping` command from inside one of the newly created virtual nodes successfully reaches the IP address of the T-Pot Cowrie honeypot.
3. **Clean Console:** The backend console shows the Mininet network starting and bridging without physical interface binding errors or root permission denials[cite: 7].
4. **Lifecycle Enforcement:** Clicking "Stop System" successfully tears down the Containernet nodes and virtual switch, removing the containers from `docker ps`[cite: 7].