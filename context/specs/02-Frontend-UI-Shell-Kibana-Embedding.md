# Spec: Unit 2 - Frontend UI Shell & Kibana Embedding

## Objective
Build the auth-free, local web interface that serves as the control plane for the Autonomous IoT Cyber Defense System. Implement the official, minimal technical workspace layout defined in the UI Context, build the configuration sidebar for network and attack controls, and embed the T-Pot Kibana telemetry dashboard via an `<iframe>`.

## System Boundary
- **Target:** `/frontend` directory (HTML/JS/CSS or React/Tailwind frontend).
- **Protected:** Do not write backend API routing logic (`/backend`) or network generation scripts (`/topology`) in this unit. Use mock console logs for button click handlers until the backend API is implemented.

## Implementation Steps

### 1. Initialize the Frontend Shell
- Set up the frontend project structure (e.g., React with Vite + Tailwind CSS, or vanilla HTML/JS with Tailwind CDN) inside the `/frontend` directory.
- Implement the CSS color tokens (`--bg-base`, `--bg-surface`, etc.) and typography (Inter for UI, JetBrains Mono for logs) as defined in `ui-context.md`.

### 2. Construct the Layout Shell
- **Top Navigation Bar:** Create a fixed top navbar spanning the full width, containing the project title and a simple status indicator (e.g., "System Idle").
- **Grid / Flex Layout:** Below the navbar, split the viewport into two main sections:
  - **Left Control Sidebar:** A fixed-width sidebar (e.g., `w-72` or `w-80`) with a right border (`--border-default`) and a surface background (`--bg-surface`).
  - **Main Canvas:** A responsive center area that takes up the remaining viewport width and height to house the Kibana dashboard.

### 3. Build the Control Sidebar Components
- **Operating Mode Toggle:** Add a toggle or select dropdown to switch between "Simulation Mode" and "Live Mode".
- **Simulation Parameters:** Add a number input field for "Node Count" (default: 10) and dropdowns for device types (e.g., Camera, Temp Sensor). 
- **Network Controls:** Add a primary "Start Network" button and a "Stop System" button.
- **Attack Triggers (Disabled until Network is Active):** Create a distinct section with buttons for "Reconnaissance (Nmap)", "Brute Force (Hydra)", and "SYN Flood (Hping3)". Use the `--state-error` red accent color for these offensive triggers.

### 4. Embed the Kibana Iframe
- In the Main Canvas area, insert an `<iframe>` element.
- Set the `src` attribute to the local T-Pot Kibana dashboard URL (e.g., `https://127.0.0.1:64297/app/kibana#/dashboard/...`).
- Apply Tailwind utility classes to make the iframe fill the entire main container (`w-full h-full border-none`).

## Verification & Success Criteria
1. **Layout Rendering:** The application renders locally in the browser with the top navbar, left control sidebar, and main canvas clearly defined and matching the dark/light theme tokens.
2. **Iframe Sandboxing Bypass:** The Kibana dashboard successfully loads inside the main canvas without throwing `X-Frame-Options` or `Content-Security-Policy` browser console errors (relying on Unit 1's Nginx configuration).
3. **Responsive Controls:** The sidebar inputs and buttons are clickable and visually respond to interactions, logging placeholder events to the browser console.
4. **Boundary Check:** No backend Python logic or Mininet code was written or modified during this step.