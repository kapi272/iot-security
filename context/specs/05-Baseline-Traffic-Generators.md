# Spec: Unit 5 - Baseline Traffic Generators

## Objective
Develop the lightweight Python scripts responsible for generating synthetic baseline IoT traffic, including MQTT sensor payloads, UDP video frame streams, and periodic HTTP telemetry requests[cite: 7]. Integrate these scripts with the backend orchestrator so they execute as continuous, asynchronous background processes directly inside the virtual nodes spawned in Unit 4[cite: 6].

## System Boundary
- **Target:** `/traffic_generators` directory[cite: 6].
- **Protected:** Do not alter the network topology definitions (`/topology`) or write offensive attack logic (`/attacks`)[cite: 6]. This unit is strictly dedicated to benign, simulated IoT operations.

## Implementation Steps

### 1. Create Protocol-Specific Traffic Scripts
- Inside the `/traffic_generators` directory, write standalone Python scripts that require minimal dependencies[cite: 6]:
  - **MQTT Script:** Connects to a designated broker IP and continuously publishes dummy sensor data (e.g., temperature, humidity) in a loop[cite: 7].
  - **HTTP Script:** Sends periodic `GET` or `POST` requests to mimic device heartbeats or telemetry syncs[cite: 7].
  - **UDP Script:** Streams raw dummy packets to simulate continuous video or audio feeds[cite: 7].

### 2. Orchestrate Container Execution
- Update the backend's network initialization sequence (from Unit 4) to assign roles to the spawned virtual nodes (e.g., Node 1-4 are cameras, Node 5-8 are temp sensors).
- Use Containernet/Mininet's subprocess execution methods (like `node.popen()`) to launch the corresponding traffic scripts *inside* the isolated network namespace of each virtual node[cite: 6].

### 3. Track Background Processes
- Capture the Process IDs (PIDs) returned when launching the traffic generator scripts.
- Append these PIDs to the backend's global, in-memory `active_pids` state array so the orchestrator can track their lifecycles[cite: 6].

### 4. Integrate with Teardown Manager
- Ensure that the Teardown Manager created in Unit 3 iterates over these specific traffic generation PIDs.
- The teardown block must explicitly send `SIGTERM` or `SIGKILL` to these loops before wiping the network interfaces to prevent zombie processes[cite: 6].

## Verification & Success Criteria
1. **Script Execution:** Clicking "Start Network" initializes the nodes and successfully starts the traffic scripts in the background without raising Python execution errors.
2. **Dashboard Visibility:** Normal network traffic and protocol breakdowns (MQTT, UDP, HTTP) begin appearing in the embedded Kibana dashboard telemetry[cite: 7].
3. **Clean Process Lifecycle:** Clicking "Stop System" successfully halts the continuous traffic generation loops, leaving no orphaned Python processes running on the host machine[cite: 7].