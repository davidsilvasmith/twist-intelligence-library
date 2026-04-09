# TWiST Intelligence Library

A structured intelligence system for This Week in Startups.

## Core idea

Each episode becomes a **Masterclass**.
Each recurring founder becomes a **Living Trajectory**.
The dashboard reads from a central `wiki/dashboard_data.json` file and renders:
- hero episodes
- founder delta cards
- relationship constellation
- anti-portfolio misses
- tactical masterclass sidebars

## Karpathy Compiler architecture

The pipeline has four layers:

1. **Discovery**
   - pull latest episode list from the TWiST YouTube channel feed
   - store ordered episode metadata in `wiki/raw/`

2. **Compilation**
   - one episode at a time
   - Gemini CLI or fallback research produces compressed structured outputs
   - write raw output to `wiki/raw/E####_*.json`
   - write human-readable masterclass files to `wiki/masterclasses/`

3. **Relational hardening**
   - founder pages in `wiki/founders/`
   - company pages in `wiki/companies/`
   - trajectory and anti-portfolio logic verified through external reporting

4. **Presentation sync**
   - Stitch UI export analyzed into a schema map: `wiki/ui_schema_map.json`
   - dashboard hydrated through `wiki/dashboard_data.json`

## Important files

- `wiki/dashboard_data.json`
- `wiki/ui_schema_map.json`
- `wiki/masterclasses/`
- `wiki/raw/`
- `scripts/twist_episode_worker.sh`

## Current status

The plumbing is live. The first three episodes, E2271-E2273, are the priority hardening set for demo readiness.
