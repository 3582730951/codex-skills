# Windows System Adapter

Use this file for authorized defensive tools on Windows desktops or servers.

## Good Fit

- Windows service based monitoring tools
- registry and configuration auditors
- event log collectors
- controlled startup / task inspection tools
- endpoint hardening helpers with explicit authorization

## Core Rules

- prefer documented Windows APIs over shelling out repeatedly
- be explicit about service, scheduled task, registry, and filesystem touch points
- document elevation requirements and reduced-privilege fallback
- keep install / uninstall behavior clean and reversible

## Permissions

Define:

- required privilege level
- required service control actions
- registry paths read or written
- event log channels read

Reject hidden persistence, undocumented autorun changes, or stealth behavior.

## Safety Checks

- avoid broad WMI or PowerShell usage when a narrower API is available
- document rollback for service registration or registry changes
- log security-relevant actions with enough context for operators

## Basis

- Windows service and least-privilege design should guide tool architecture
