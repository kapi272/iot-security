# Progress Tracker

Update this file after every meaningful implementation change.

## Current Phase

- Phase 1: Infrastructure and Core Setup

## Current Goal

- Implement Unit 6 - Live Mode Physical Bridging

## Completed

- Unit 1 - Defense Core Initialization (T-Pot Docker Environment)
- Unit 2 - Frontend UI Shell & Kibana Embedding
- Unit 3 - Backend API & Process Teardown Manager
- Unit 4 - Containernet Topology
- Unit 5 - Baseline Traffic Generators
- Unit 6 - Live Mode Physical Bridging

## In Progress

- None

## Next Up

- Unit 7 (TBD)

## Open Questions

- None

## Architecture Decisions

- None

## Session Notes

- Unit 2 completed: Scaffolded Vite/React frontend, integrated Tailwind/Shadcn UI, built `TopNavbar`, `Sidebar`, and `KibanaIframe`. Fixed TypeScript/path alias integration issues with root Next.js configuration.
- Unit 3 completed: Scaffolded FastAPI backend for Teardown Manager, validated process termination handling, and verified the `/api/system/stop` teardown trigger endpoint via curl testing.
- Unit 4 completed: Developed Containernet topology script for generating virtual IoT nodes, established veth bridge to T-Pot Docker network, and successfully integrated the simulation trigger into the backend API.
- Unit 5 completed: Developed lightweight Python traffic generator scripts (MQTT, HTTP, UDP), mounted them into the Containernet nodes using `python:3.9-alpine`, and orchestrated their execution and tracking via the backend lifecycle manager.
- Unit 6 completed: Implemented 'Live Mode' physical interface bridging using Mininet's `Intf` class, added promiscuous mode lifecycle management to the Teardown Manager, and established try/except guards for macOS native execution.
