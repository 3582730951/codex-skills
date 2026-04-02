# macOS System Adapter

Use this file for authorized defensive tools on macOS systems.

## Good Fit

- launchd-backed monitoring tools
- configuration and profile auditors
- file integrity or app bundle inspection tools
- local policy verification and reporting tools

## Core Rules

- prefer documented system APIs and launchd integration
- document app sandbox, filesystem scope, and privacy-sensitive access
- be explicit about plist ownership and launch semantics
- keep install and uninstall clean

## Permissions

Define:

- whether Full Disk Access is required
- which directories, plists, or logs are read
- whether background persistence is required and why

Reject stealth background behavior or vague persistence requirements.

## Safety Checks

- avoid brittle scraping of system command output when stable APIs exist
- document cleanup for launch agents, temp files, and caches
- isolate any privileged operation behind the smallest possible interface

## Basis

- launchd and macOS privacy boundaries should guide architecture
