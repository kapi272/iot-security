# Code Standards

## General

- Keep modules small and single-purpose — separate network orchestration logic from API route handlers.
- Fix root causes, do not layer workarounds — especially regarding lingering network namespaces or orphaned Linux processes.
- Do not mix unrelated concerns — the scripts that generate baseline IoT traffic should not contain attack logic.
- Ensure all repository commits on GitHub are atomic, well-documented, and exclude sensitive environment configurations or raw `.pcap` files.

## Python & Backend Framework (FastAPI / Flask)

- Use explicit type hints (`def start_network(nodes: int) -> dict:`) for all function signatures to ensure predictable behavior.
- Validate unknown external input at system boundaries before trusting it — strictly parse user-provided integers for node counts.
- Wrap all network orchestration and subprocess executions in `try...finally` blocks to guarantee `mn -c` runs if a script crashes.
- Never run arbitrary shell commands from user input; use parameterized subprocess arguments when executing Nmap or Hydra.

## TypeScript & JavaScript (Frontend)

- Strict mode is required throughout the project.
- Avoid `any` — use explicit interfaces or narrowly scoped types for API responses (e.g., `SimulationState`, `AttackResult`).
- Abstract API calls into a dedicated service layer rather than mixing `fetch()` calls directly inside UI components.

## Styling (Tailwind CSS & HTML)

- Utilize Tailwind CSS utility classes for consistent spacing and typography — no hardcoded hex values or inline styles.
- Maintain a clean `tailwind.config.js` file for custom theme extensions instead of scattering arbitrary values in the markup.
- Ensure the embedded Kibana `<iframe>` uses responsive container classes to scale seamlessly across different screen sizes.

## API Routes

- Validate and parse request input before any logic runs — strictly reject any attack payload targeting an IP outside `10.0.0.0/24`.
- Enforce the single-user, localhost-only boundary — reject requests originating from non-loopback network interfaces.
- Return consistent, predictable response shapes (e.g., `{"status": "success", "data": {...}}` or `{"status": "error", "message": "..."}`).

## Data and Storage

- Maintain application state (e.g., active PIDs, simulation status) strictly in-memory during runtime.
- Do not persist execution logs or state to a local database (e.g., SQLite); rely on application restarts to reset the environment.
- Offload all heavy logging and persistent network metadata exclusively to the T-Pot Elasticsearch containers.

## File Organization

- `backend/` — API route handlers, process lifecycle managers, and state validation logic.
- `frontend/` — HTML, TypeScript, Tailwind CSS configuration, and Kibana iframe integration.
- `topology/` — Containernet setup scripts, virtual node configurations, and physical interface bridging logic.
- `traffic_generators/` — Lightweight Python scripts executed inside virtual nodes to generate baseline MQTT, HTTP, and UDP traffic.
- `attacks/` — Execution scripts for Nmap, Hydra, and Hping3 with hardcoded subnet safety boundaries.