# Robot Shop Incident Runbook

## Purpose
Triage user-facing failures, elevated errors or latency in Robot Shop. Use this runbook from the alert; do not delete the cluster or data as an initial response.

## 1. Assess impact
1. Record alert time, affected endpoint/service, error rate, latency and whether users are affected.
2. Open the Grafana dashboard and compare request volume, 5xx rate and latency against the normal baseline.
3. Check recent deployments or configuration changes.

## 2. Check service health
When the Kubernetes API is healthy, use read-only checks first:

```bash
kubectl get pods -A
kubectl get svc -n robot-shop
kubectl get events -n robot-shop --sort-by=.lastTimestamp
```

If the Kubernetes API is unavailable, record that as an infrastructure/control-plane incident and avoid repeated API calls or destructive resets. Check the container runtime/host health separately and preserve existing data.

## 3. Investigate signals
- **Metrics:** identify which service first shows increased errors, latency or restarts.
- **Logs:** query Loki by service and error level around the incident time; redact secrets and personal data.
- **Traces:** inspect a representative slow/failed request in Jaeger and identify the slow dependency span.
- **Dependencies:** check database/cache/message broker health before restarting application services.

## 4. Mitigate safely
Prefer rollback of a known bad release, restoring a known-good configuration, or scaling a confirmed overloaded service if capacity allows. Capture evidence before changes. Do not run `terraform destroy`, `minikube delete`, `docker system prune`, or remove persistent volumes as routine mitigation.

## 5. Verify recovery
Confirm successful requests and latency return to baseline, required services are healthy, and the alert clears. Record the exact checks and timestamps. If metrics/logging/tracing are unavailable, state that verification limitation explicitly.

## 6. Close out
Create a blameless postmortem: impact, timeline, detection, contributing factors, what went well, what did not, and tracked corrective actions with owners/dates.

## Escalation
Escalate if the control plane remains unavailable, data integrity is at risk, or recovery requires destructive changes. Preserve logs and current configuration before attempting repair.
