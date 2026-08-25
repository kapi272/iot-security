# Spec: Unit 6 - Live Mode Physical Bridging

## Objective
Implement the "Live Mode" functionality that allows the user to bypass virtual IoT node generation and instead bind a physical host network interface (e.g., `eth0` or `wlan0`) directly to the virtual switch (`s1`)[cite: 7]. This effectively pipes real external network traffic into the T-Pot Defense Core (Suricata and Cowrie) for live monitoring and analysis[cite: 7].

## System Boundary
- **Target:** `/topology` directory (specifically the network initialization logic) and `/backend` API parameter handling[cite: 6].
- **Protected:** Do not alter the virtual node creation loops established in Unit 4; isolate the new logic using conditionals based on the selected operating mode. Do not modify the T-Pot container configurations.

## Implementation Steps

### 1. Update Backend API Payload
- Modify the existing `/api/network/start` endpoint in the backend to explicitly process two new payload parameters:
  - `mode`: A string value of either `"simulated"` or `"live"`[cite: 7].
  - `interface`: A string representing the physical interface to bind (e.g., `"eth0"`), applicable only when in live mode[cite: 7].

### 2. Implement Interface Bridging Logic
- In the `/topology` script, wrap the virtual node creation (from Unit 4) in an `if mode == "simulated":` block.
- Create an `elif mode == "live":` block. Inside this block:
  - Instantiate the virtual switch (`s1`) and the `veth` bridge to the T-Pot environment.
  - Use Mininet's `Intf` class (or equivalent system bridging commands) to attach the designated physical hardware interface (e.g., `eth0`) directly to the `s1` switch[cite: 7].

### 3. Configure Promiscuous Routing (If Required)
- Ensure the physical interface is configured to allow traffic to flow into the virtual switch so Suricata can inspect it.
- If necessary, apply temporary `ip link set <interface> promisc on` commands via subprocess during the live mode initialization.

### 4. Update the Teardown Manager
- Ensure that the Teardown Manager gracefully detaches the physical interface from the virtual switch when "Stop System" is clicked[cite: 7].
- The teardown process must not drop the host machine's primary internet or network connection during cleanup.

## Verification & Success Criteria
1. **Conditional Execution:** Sending a "Start Network" payload with `mode="live"` successfully creates the virtual switch without spinning up any virtual Alpine containers.
2. **Interface Binding:** The backend console confirms the physical interface (e.g., `eth0`) is bound to the virtual switch without raising "Device or resource busy" or permission errors[cite: 7].
3. **Live Telemetry:** Real background traffic from the host network successfully routes into the T-Pot environment and appears on the embedded Kibana dashboard.
4. **Safe Teardown:** Clicking "Stop System" cleanly unbinds the interface, leaving the host machine's physical network connection fully intact and functional without requiring a system reboot[cite: 7].