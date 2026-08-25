# Autonomous IoT Cyber Defense System

## Overview

The Autonomous IoT Cyber Defense System is a locally hosted security testing and monitoring platform designed for cybersecurity researchers, analysts, and students to evaluate IoT threat dynamics without requiring physical IoT hardware. The system provides a centralized local web dashboard that orchestrates virtual IoT traffic generation via Containernet/Mininet, captures and analyzes real-time malicious activity using T-Pot (Cowrie honeypot and Suricata IDS), and visualizes intrusion telemetry through an embedded Kibana interface. By supporting seamless toggling between synthetic traffic simulation and live network interface bridging, the platform delivers a controlled, safe environment to study reconnaissance, brute-force, and denial-of-service attacks.

---

## Goals

1. **Hardware-Free IoT Network Simulation:** Deploy dynamic topologies of virtual IoT nodes (smart sensors, cameras, smart plugs) generating realistic MQTT, UDP, and HTTP baseline traffic on a single host.
2. **Integrated Threat Emulation & Honeypot Trapping:** Lure and isolate malicious traffic using a containerized Cowrie honeypot while detecting malicious signatures and volumetric spikes using Suricata IDS.
3. **Dual-Mode Traffic Ingestion:** Enable rapid toggling between software-generated synthetic traffic and physical network interface binding (e.g., `eth0`, `wlan0`).
4. **Unified Telemetry Visualization:** Embed an analytics dashboard into the local web interface via Kibana iframe integration to monitor alerts, session logs, and traffic anomalies in real time.
5. **Safe Attack Orchestration:** Provide one-click automated attack executions (`nmap`, `hydra`, `hping3`) with strict destination subnet constraints to prevent accidental external network flooding.

---

## Core User Flow

1. **Access Web Application:** The user navigates to the locally hosted web dashboard (`http://localhost:<PORT>`) without authentication barriers.
2. **Select Operating Mode:**
   - *Option A (Simulation Mode):* User configures node count (e.g., 10 nodes), device types (temperature sensors, smart cameras), and transmission intervals.
   - *Option B (Live Mode):* User selects an active host network interface (e.g., `eth0`, `wlan0`) to bridge external network traffic into the virtual switch.
3. **Initialize Network Environment:** User clicks **"Start Network"**, triggering the backend to spin up the Containernet/Mininet topology and establish a virtual link (`veth`) to the T-Pot Docker environment.
4. **Trigger Attack Scenarios:** User selects and executes built-in attack vectors from the dashboard (Reconnaissance Scan, SSH/Telnet Brute Force, or SYN Flood).
5. **Inspect Live Analytics:** User monitors intrusion alerts, captured honeypot credentials, and traffic metadata directly inside the embedded T-Pot/Kibana dashboard.
6. **Terminate & Reset:** User clicks **"Stop System"**, prompting the orchestrator to terminate active attack processes, tear down virtual nodes, execute `mn -c` cleanup, and reset the app state to default.

---

## Features

### Network Simulation & Orchestration
- **Containernet-Powered Topologies:** Spawns isolated, lightweight container nodes acting as virtual IoT devices.
- **Multi-Protocol Baseline Generators:** Built-in scripts generating synthetic sensor payloads over MQTT, video frame streams over UDP, and periodic telemetry requests over HTTP.
- **Physical Interface Bridging:** Dynamic binding of local hardware interfaces into the virtual switch for live traffic testing.

### Threat Defense & Monitoring
- **Emulated IoT Services:** Cowrie honeypot emulating vulnerable SSH and Telnet endpoints to capture attacker commands and brute-force credentials.
- **Signature & Anomaly Detection:** Suricata IDS inspecting packet flows across the virtual bridge for known threat signatures and volumetric anomalies.
- **Embedded Telemetry UI:** Direct iframe integration of pre-configured Kibana dashboards displaying alert severity, source IPs, and protocol distributions.

### Attack Execution & Safety Controls
- **Automated Attack Triggers:** Web-driven execution of standard penetration testing tools (`nmap`, `hydra`, `hping3`).
- **Subnet Safety Enforcement:** Hardcoded targeting constraints restricting all automated offensive traffic strictly to the internal virtual subnet (`10.0.0.0/24`).
- **Clean Process Lifecycle:** Automatic PID tracking with process termination and network namespace cleanup on session stop.

---

## Scope

### In Scope
- Single-user, authentication-free local web interface.
- Python backend executing with root privileges on `localhost`.
- In-memory, stateless session management (clean reset on application restart).
- Containernet/Mininet virtual IoT network generation.
- T-Pot integration running Cowrie, Suricata, and Elasticsearch/Kibana via Docker.
- Automated execution of Nmap, Hydra, and Hping3 against virtual targets.
- Embedded Kibana dashboard visualization via iframe.

### Out of Scope
- Multi-tenant cloud SaaS deployment or remote access gateways.
- Multi-user authentication, role-based access control, or database persistence.
- Custom machine learning or deep learning model training/inference for anomaly detection.
- Custom honeypot daemon development from scratch.
- Complex multi-stage exploit payloads or zero-day vulnerability weaponization.
- Standalone custom data-visualization charts bypassing Kibana.

---

## Success Criteria

1. **Topology Generation:** The backend successfully initializes at least 10 virtual IoT nodes generating continuous baseline traffic without interface binding errors.
2. **Traffic Bridging:** Virtual nodes and the physical host interface seamlessly route traffic through the virtual switch to the T-Pot honeypot container.
3. **Attack Detection:** Triggering an automated `hydra` brute-force attack registers captured credentials in Cowrie and logs high-priority alerts in Suricata within 10 seconds.
4. **Dashboard Visualization:** The embedded Kibana iframe renders real-time intrusion events, attack origins, and protocol breakdowns without X-Frame-Options or CORS errors.
5. **Clean Environment Teardown:** Stopping the session cleanly terminates all running subprocesses and removes virtual network interfaces without requiring a system reboot.