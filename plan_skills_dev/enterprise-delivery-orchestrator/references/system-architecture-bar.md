# System And Architecture Bar

Use this file for system-layer, runtime, kernel, driver, ABI, FFI, JNI, allocator, concurrency, or memory-sensitive work.

This file is also the base gate for authorized defensive system tools. It does not authorize offensive, stealthy, or persistence-heavy malware-like behavior.

## Trigger Surfaces

Load this file if the task touches any of:

- kernel modules, drivers, schedulers, allocators, runtimes
- FFI, JNI, syscall, native handle, ABI boundary
- raw pointers, manual memory management, pinning, lock-free structures
- thread coordination, interrupt/signal context, critical sections, shared mutable state

## Required Extra Artifacts

```text
Concurrency Model:
- Shared states:
- Owners:
- Synchronization strategy:
- Blocking rules:
- Ordering rules:

Ownership And Lifetime Map:
- Resource:
- Owner:
- Creation point:
- Transfer rules:
- Cleanup point:

Failure Domain Table:
- Domain:
- Failure modes:
- Containment:
- Recovery:

Unsafe Boundary Register:
- Boundary:
- Why unsafe / low-level:
- Preconditions:
- Postconditions:
- Cleanup guarantees:
```

## Hard Rules

- Define the concurrency model before coding.
- Every shared mutable state needs an owner and synchronization rule.
- Every resource needs creation, transfer, and cleanup rules.
- Every unsafe or ABI boundary needs preconditions and postconditions.
- Every error path must explain cleanup and observability.
- Do not block in critical, interrupt, or signal-sensitive contexts unless the contract explicitly allows it.
- Do not optimize away correctness explanations.
- For defensive tools, prefer read-only inspection first and document every privileged capability explicitly.
- Reject stealth persistence, hidden injection, or undocumented privilege escalation.

## Systems Reviewer Focus

The systems reviewer should specifically challenge:

- lifetime and ownership holes
- unbounded blocking or allocation
- unclear memory ordering or lock discipline
- partial cleanup on error
- hidden ABI assumptions
- performance changes with no measurement plan

## Architecture Expectations

Architecture work at this layer must define:

- module and failure-domain boundaries
- compatibility and rollback expectations
- observability hooks for post-deploy debugging
- test strategy for concurrency and low-level failure paths

## Basis

- Linux kernel coding style  
  https://kernel.org/doc/html/next/process/coding-style.html
- Rust for Linux coding guidelines  
  https://docs.kernel.org/rust/coding-guidelines.html
