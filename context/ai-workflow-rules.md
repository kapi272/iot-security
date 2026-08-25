# AI Workflow Rules

## Approach

Build this project incrementally using a spec-driven workflow. The context files (`project-overview.md`, `architecture.md`, `code-standards.md`) define exactly what to build, the strict system boundaries, and the current state of progress. Always implement strictly against these specs. Do not infer, guess, or invent product behavior, network configurations, or attack scenarios from scratch.

## Scoping Rules

- Work on exactly one feature unit at a time.
- Execute small, verifiable increments over large speculative changes.
- Do not combine unrelated system boundaries in a single implementation step (e.g., do not write Mininet topology scripts and Kibana iframe frontend code in the same step).
- Enforce the `10.0.0.0/24` subnet targeting safety boundary in every applicable offensive script.

## When to Split Work

Split an implementation step if it combines:

- Network namespace manipulation (Containernet/Mininet) and frontend UI state changes.
- High-level API routing and low-level subprocess execution (`subprocess.Popen` for `nmap`/`hydra`).
- Implementation of baseline traffic generators (MQTT/HTTP) and the execution of offensive attack scripts.

If a network simulation or attack sequence cannot be verified end-to-end and cleaned up quickly without leaving orphaned processes, the scope is too broad — split it immediately.

## Handling Missing Requirements

- Do not invent network protocols, attack vectors, or UI states not explicitly defined in the context files.
- If an architectural requirement is ambiguous (e.g., how to bind a physical interface for Live Mode), resolve it in `architecture.md` before writing the code.
- If a requirement is missing, halt implementation and add it as an open question in a `progress-tracker.md` file before continuing.

## Protected Files

Do not modify the following unless explicitly instructed:

- `frontend/index.html` (or equivalent base UI shell) once the layout and Kibana iframe are established.
- `docker-compose.yml` configurations pertaining to the core T-Pot deployment (Cowrie, Suricata, Elasticsearch).
- Mininet or Containernet core library files.

## Keeping Docs in Sync

Update the relevant context file immediately whenever implementation changes:

- System architecture, folder boundaries, or storage models (`architecture.md`).
- Subnet definitions, safety constraints, or code conventions (`code-standards.md`).
- Feature scope and success criteria (`project-overview.md`).

## Before Moving to the Next Unit

1. The current unit functions end-to-end strictly within its defined scope.
2. No invariants defined in `architecture.md` were violated (especially the safety subnet restrictions).
3. The `try...finally` teardown sequence successfully cleans up the network (`mn -c`) and kills all orphaned root PIDs.
4. The local web application starts without errors and the backend binds successfully to `127.0.0.1`.