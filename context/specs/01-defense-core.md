# Spec: Unit 1 - Defense Core Initialization

## Objective
Deploy the T-Pot Docker environment (acting as the Defense Core) containing Suricata (IDS), Cowrie (Honeypot), and the ELK stack (Elasticsearch, Logstash, Kibana). Configure the T-Pot Nginx reverse proxy to explicitly allow Kibana to be embedded within an `<iframe>` served from the local web dashboard, fulfilling the Iframe Sandboxing invariant.

## System Boundary
- **Target:** Docker environment / T-Pot configuration files.
- **Protected:** Do not alter the internal routing or data ingestion pipelines between Suricata, Cowrie, and Logstash. 

## Implementation Steps

### 1. Establish the Docker Environment
- Define or retrieve the standard `docker-compose.yml` required to spin up the minimal T-Pot stack (specifically Cowrie, Suricata, Elasticsearch, Logstash, Kibana, and Nginx).
- Ensure the services bind to the necessary host ports (e.g., Port 22/23 for Cowrie, Port 64297 for the T-Pot Web UI).

### 2. Configure Iframe Sandboxing (Nginx Override)
- Locate the Nginx configuration file responsible for serving the Kibana dashboard within the T-Pot setup.
- Override the default security headers to permit local embedding. 
- **Action:** Remove or comment out `add_header X-Frame-Options "DENY";` (or `SAMEORIGIN`).
- **Action:** Inject a strict Content Security Policy (CSP) that allows framing *only* from localhost origins. Add the following header:
  `add_header Content-Security-Policy "frame-ancestors 'self' http://127.0.0.1:* http://localhost:*";`
- Ensure this configuration is mounted as a volume or applied cleanly so it persists across container restarts.

### 3. Initialize and Spin Up
- Execute the docker-compose command to build and detach the containers (`docker-compose up -d`).
- Verify that Elasticsearch, Kibana, Suricata, and Cowrie achieve a healthy running state.

## Verification & Success Criteria
1. **Container Health:** Running `docker ps` shows Cowrie, Suricata, Elasticsearch, Logstash, Kibana, and Nginx containers are `Up`.
2. **Dashboard Accessibility:** Navigating to `https://127.0.0.1:64297` (or the configured Kibana port) in a browser successfully loads the Kibana UI.
3. **Header Validation:** Executing `curl -I -k https://127.0.0.1:64297` confirms that `X-Frame-Options: DENY` is absent and `Content-Security-Policy: frame-ancestors 'self' http://127.0.0.1:* http://localhost:*` is present in the HTTP response headers.