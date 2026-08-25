# Spec: Unit 7 - Attack Engine & Safety Constraints

## Objective
Develop the offensive execution engine that launches automated network reconnaissance, dictionary attacks, and volumetric denial-of-service simulations[cite: 6]. This unit strictly enforces the Targeting Strictness invariant by hardcoding and validating destination constraints, ensuring that all automated offensive traffic is restricted strictly to the internal virtual subnet (`10.0.0.0/24`)[cite: 6, 7].

## System Boundary
- **Target:** `/attacks` directory (execution scripts) and `/backend` (API trigger endpoints)[cite: 6].
- **Protected:** Do not alter the virtual node topologies (`/topology`) or modify the core Defense Core logging mechanics[cite: 6]. 

## Implementation Steps

### 1. Enforce Targeting Strictness (Safety Lock)
- In the Python backend, create a strict validation function for the `/api/attacks/trigger` endpoint.
- Hardcode the target destination for all attack scripts to the `10.0.0.0/24` subnet[cite: 6, 7] (or the specific IP of the Cowrie honeypot node within that subnet).
- Ensure the API completely ignores or rejects any user-provided IP payloads that attempt to route attacks outside this internal virtual subnet[cite: 6].

### 2. Develop Attack Execution Scripts
- Inside the `/attacks` directory, write Python or Bash wrapper scripts to execute the following tools as subprocesses[cite: 6]:
  - **Reconnaissance:** Run `nmap` for a subnet sweep and aggressive port scan against the virtual subnet[cite: 7].
  - **Credential Attack:** Run `hydra` to execute a dictionary brute-force attack against the virtual Cowrie honeypot's SSH or Telnet ports[cite: 7].
  - **Denial of Service:** Run `hping3` to launch a SYN flood against the virtual honeypot[cite: 7].

### 3. Track Offensive Processes
- Modify the backend `/api/attacks/trigger` endpoint to launch these attack scripts asynchronously using `subprocess.Popen`[cite: 6].
- Immediately capture the generated Process IDs (PIDs) and append them to the in-memory `active_pids` state array[cite: 6].
- Update the system state to `attacking`[cite: 6].

### 4. Integrate with Teardown Manager
- Verify that the Teardown Manager (built in Unit 3) iterates through the offensive tool PIDs.
- The teardown process must aggressively issue `SIGKILL` commands to stop any lingering `nmap`, `hydra`, or `hping3` processes when "Stop System" is clicked, preventing network interface lockups[cite: 6, 7].

## Verification & Success Criteria
1. **Safety Enforcement:** Attempting to manually pass an external IP (e.g., `8.8.8.8` or a local gateway `192.168.1.1`) to the attack endpoint results in an immediate backend rejection, proving the subnet lock works[cite: 6].
2. **Attack Detection:** Triggering a built-in `hydra` brute-force attack from the frontend successfully executes the subprocess, registers captured credentials in the Cowrie honeypot, and logs high-priority alerts in Suricata within 10 seconds[cite: 7].
3. **Telemetry Visualization:** Attack origins and protocol breakdowns are visible in real-time within the embedded Kibana iframe[cite: 7].
4. **Clean Process Termination:** Clicking "Stop System" successfully kills all active `nmap`, `hydra`, and `hping3` subprocesses, leaving no orphaned attack processes running on the host machine[cite: 6, 7].