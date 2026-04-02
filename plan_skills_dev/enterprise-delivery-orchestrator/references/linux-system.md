# Linux System Adapter

Use this file for authorized defensive tools that run on Linux hosts, servers, or containers.

## Good Fit

- file integrity monitors
- config and permission auditors
- process and service anomaly scanners
- system health and hardening agents
- read-only observability and alerting daemons

## Core Rules

- prefer read-only inspection first
- require explicit capability and permission declarations
- keep service startup and shutdown predictable
- use systemd-friendly logging and exit behavior when relevant
- document filesystem paths, pid handling, and lockfile strategy

## Permissions

Define explicitly:

- files and directories to read
- files or sockets to write
- whether root is required, and why
- how reduced privileges are supported

Reject "run as root" unless the task cannot be completed safely otherwise.

## Safety Checks

- avoid shell pipelines when direct APIs exist
- avoid `shell=True` or equivalent unless tightly bounded
- document cleanup for temp files, sockets, and pid files
- keep background loops stoppable and observable

## Basis

- systemd service model and Linux least-privilege norms should guide service behavior
