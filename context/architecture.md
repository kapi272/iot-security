# Architecture Context

## Stack

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Frontend/UI** | HTML/JS/CSS (or React/Vue) + Kibana Iframe | Renders the dashboard controls and embeds the T-Pot visualization for real-time threat telemetry. |
| **Backend API** | Python (e.g., FastAPI or Flask) | Serves the web interface, manages API requests, and orchestrates subprocesses (requires `root` privileges). |
| **Network Simulation** | Containernet / Mininet | Virtualizes the IoT network, creating lightweight host nodes, virtual switches, and routing simulated traffic. |
| **Defense Core** | T-Pot (Suricata + Cowrie via Docker) | Acts as the IDS and honeypot layer to intercept malicious traffic, log brute-force credentials, and flag network anomalies. |
| **Logging & Analytics** | Elasticsearch + Logstash + Kibana (ELK) | Handles high-volume log ingestion from Suricata/Cowrie and powers the embedded visualization iframe. |
| **Attack Engine** | Nmap, Hydra, Hping3 + Bash/Python Scripts | Executes automated network reconnaissance, dictionary attacks, and volumetric denial-of-service simulations. |

## System Boundaries

- `/backend` — Owns the web server execution, API endpoints, process lifecycle management (starting/stopping tasks), and PID tracking.
- `/frontend` — Owns the user interface, state toggles (Live vs. Simulated), API request logic, and the embedded Kibana `<iframe>`.
- `/topology` — Owns the Containernet setup scripts, virtual node configurations, physical interface bridging (`eth0`), and virtual switch (`s1`) instantiation.
- `/traffic_generators` — Owns the lightweight Python scripts executed inside virtual nodes to generate baseline MQTT, HTTP, and UDP traffic.
- `/attacks` — Owns the execution scripts for offensive tools (Nmap, Hydra, Hping3), strictly enforcing targeting parameters.

## Storage Model

- **In-Memory (Python State)**: Ephemeral runtime data, including active Process IDs (PIDs), simulation status flags (e.g., `idle`, `simulating`, `attacking`), and active topology presets. This resets completely upon application restart.
- **T-Pot Elasticsearch (Database)**: High-volume persistent data handled entirely by the Docker environment. This includes Suricata IDS alerts, Cowrie honeypot command session logs, and network metadata.
- **File System (Static Storage)**: Configuration files (`.json`), attack scripts (`.sh` or `.py`), and baseline traffic scripts. No SQLite, PostgreSQL, or local databases are used by the web application.

## Auth and Access Model

- **Authentication Model**: The web dashboard is entirely auth-free. It is designed for single-user, direct access on the host machine. 
- **Execution Access**: The Python backend must run with `root`/`sudo` privileges to manipulate Linux network namespaces, create virtual bridges, and execute offensive network tools.
- **Network Exposure**: The web server binds strictly to `127.0.0.1` (localhost) to ensure the control panel cannot be accessed remotely by other devices on the physical network.

## Background Task Models

- **Baseline Traffic Generation**: When a simulation starts, the backend spawns asynchronous, detached processes inside the Containernet virtual nodes (e.g., MQTT publisher loops) that run continuously until the simulation is halted.
- **Offensive Execution**: Attack triggers launch tools like `hydra` or `hping3` as asynchronous background subprocesses. The backend tracks their PIDs to stream output logs back to the UI or kill them upon user request.

## Invariants

1. **Targeting Strictness**: Attack scripts must strictly hardcode and enforce targeting to the internal virtual subnet (e.g., `10.0.0.0/24`). The application must never allow user input to route attacks to the physical local area network or default gateway.
2. **Stateless Backend**: The web application must remain strictly stateless regarding execution history. It must not persist runtime state or attack logs to a local database; a server restart must guarantee a clean, default environment.
3. **Mandatory Teardown**: The backend must wrap simulation executions in a `try...finally` block (or equivalent). The `finally` block must explicitly execute `mn -c` (Mininet clean) and aggressively kill orphaned background PIDs (`nmap`, `hydra`, `hping3`) to prevent network namespace corruption.
4. **Iframe Sandboxing**: The T-Pot Nginx configuration must specifically modify the `X-Frame-Options` header to allow embedding exclusively from the local web dashboard's origin, preventing clickjacking or unauthorized external framing.