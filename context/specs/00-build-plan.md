### 1. Defense Core Initialization
*   **System Boundary:** Docker / T-Pot
*   **What it builds:** The T-Pot Docker environment (Suricata, Cowrie, ELK stack)[cite: 6]. It includes modifying the Nginx `X-Frame-Options` configuration to allow iframe embedding, fulfilling the Iframe Sandboxing invariant[cite: 6]. 
*   **Dependencies:** None.
*   **Visible Result:** The T-Pot Kibana dashboard is accessible directly in the host machine's browser.

### 2. Frontend UI Shell & Kibana Embedding
*   **System Boundary:** `/frontend`[cite: 6]
*   **What it builds:** The auth-free local web interface using HTML/JS/CSS[cite: 6]. This includes the dashboard layout, state toggles (Simulation vs. Live)[cite: 7], and embedding the Kibana dashboard inside an `<iframe>`[cite: 7].
*   **Dependencies:** Unit 1 (T-Pot must be running to embed the iframe).
*   **Visible Result:** The full visual layout of the application is rendered in the browser, showing the embedded telemetry dashboard.

### 3. Backend API & Process Teardown Manager
*   **System Boundary:** `/backend`[cite: 6]
*   **What it builds:** The Python server (FastAPI/Flask) bound strictly to `127.0.0.1` and running with `root` privileges[cite: 6]. It establishes the in-memory state tracking (PIDs, status flags)[cite: 6] and implements the mandatory `try...finally` teardown block to execute `mn -c` and aggressive PID cleanup[cite: 6, 7].
*   **Dependencies:** Unit 2 (Connects the UI buttons to the API).
*   **Visible Result:** Clicking the "Stop System" button on the UI successfully triggers the backend API and prints the teardown/cleanup logs in the backend console.

### 4. Containernet Topology (Simulation Mode)
*   **System Boundary:** `/topology`[cite: 6]
*   **What it builds:** The Python script to virtualize the IoT network using Containernet[cite: 6]. It spins up the configured number of lightweight host nodes, creates the virtual switch (`s1`), and establishes the virtual bridge (`veth`) to the T-Pot Docker environment[cite: 6, 7].
*   **Dependencies:** Unit 3 (Backend is required to execute the topology script as root) and Unit 1 (T-Pot bridge must exist).
*   **Visible Result:** Clicking "Start Network (Simulation Mode)" in the UI successfully initializes the Containernet nodes without interface binding errors in the console[cite: 7].

### 5. Baseline Traffic Generators
*   **System Boundary:** `/traffic_generators`[cite: 6]
*   **What it builds:** Lightweight Python scripts that generate synthetic sensor payloads (MQTT), video streams (UDP), and periodic telemetry requests (HTTP)[cite: 7]. The backend orchestrates these to run as detached background processes inside the virtual nodes[cite: 6].
*   **Dependencies:** Unit 4 (The virtual nodes must exist to run the scripts inside them).
*   **Visible Result:** Normal network traffic and protocol breakdowns begin appearing in the embedded Kibana dashboard[cite: 7].

### 6. Live Mode Physical Bridging
*   **System Boundary:** `/topology`[cite: 6]
*   **What it builds:** The conditional logic to bypass virtual node creation and instead bind a local hardware interface (e.g., `eth0`) directly to the virtual switch based on user UI selection[cite: 7].
*   **Dependencies:** Unit 4 (Relies on the foundational topology framework).
*   **Visible Result:** Starting the network in "Live Mode" successfully routes real background traffic from the host machine into the Kibana dashboard without errors.

### 7. Attack Engine & Safety Constraints
*   **System Boundary:** `/attacks`[cite: 6]
*   **What it builds:** The execution scripts for the offensive tools (`nmap`, `hydra`, `hping3`)[cite: 6, 7]. This unit strictly enforces the Targeting Strictness invariant by hardcoding the destination constraints to the internal virtual subnet (`10.0.0.0/24`)[cite: 6, 7].
*   **Dependencies:** Unit 4 (Target topology must exist) and Unit 3 (Backend process tracking to spawn and kill the attacks).
*   **Visible Result:** Clicking an attack trigger in the UI generates high-priority Suricata alerts and Cowrie credential captures visible in the Kibana iframe within 10 seconds[cite: 7].