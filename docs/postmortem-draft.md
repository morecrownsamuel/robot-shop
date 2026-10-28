# Blameless Postmortem — Minikube Control-Plane Instability (Draft)

**Status:** Draft based on troubleshooting evidence; review and correct timestamps before submission.

## Summary
The local Minikube Kubernetes control plane became unstable. `minikube status` reported the host and kubelet running while the API server was in error. Kubernetes API requests intermittently failed with TLS handshake timeouts, EOF/stream errors, and health checks reported etcd failures.

## Impact
Kubernetes management operations and reliable verification of deployed workloads were blocked. The current health of Voting App, Robot Shop and monitoring components could not be confirmed during the incident. Previously successful application and Helm rollback demonstrations remain historical evidence but do not prove current health.

## Detection
The incident was detected through failed `kubectl` requests and `minikube status`. Container logs showed etcd transaction/request timeouts and slow operations, including deadline-exceeded errors.

## Timeline (fill exact times from terminal history)
- Initial symptom: Kubernetes API calls began failing intermittently.
- Diagnosis: API server health check reported etcd failure; etcd operations were taking unusually long and timing out.
- Mitigation attempted: checked Minikube status/logs and reviewed host/WSL configuration. Cluster remained unstable.
- Outcome at time of writing: stopped repeating the same API checks to protect time for capstone submission work; no destructive cluster reset was performed.

## Root cause
**Not yet confirmed.** Available logs establish etcd/control-plane instability but do not prove a single root cause. Resource pressure or storage/runtime performance are hypotheses, not confirmed findings.

## Contributing factors / lessons
- Repeatedly retrying the same failing API checks consumed time without changing the evidence.
- Local cluster instability blocked end-to-end verification.
- A better stop condition is needed: after repeated identical failures, pause, preserve logs and pivot to non-destructive diagnostics or submission tasks.

## What went well
- Existing GitHub repositories and configuration were preserved.
- Earlier successful Voting App and Helm rollback demonstrations had been recorded.
- Destructive reset/prune commands were avoided.

## Corrective actions
- [ ] Capture a concise final cluster diagnostic when time permits.
- [ ] Review Docker Desktop/WSL resource and disk usage before further cluster recovery.
- [ ] Keep README and deployment instructions reproducible.
- [ ] Save screenshots/logs for previously successful application and rollback demonstrations.
- [ ] Reattempt live health verification only after the control plane is stable.

## Caveat
This is a draft incident report, not a completed instructor-led chaos drill. No claim is made that a controlled fault injection, alert firing or recovery drill occurred.
