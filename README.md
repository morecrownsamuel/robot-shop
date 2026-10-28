# DevOps Capstone 2 — Robot Shop

This fork is used to practice operating a multi-service application and adding observability: metrics, logs, distributed tracing, an SLO, alerting and incident response.

## Repository
- GitHub fork: https://github.com/morecrownsamuel/robot-shop

## Scope
The capstone instructions prioritize the web, catalogue, cart and payment services; other services should be running as dependencies. Use the supplied Helm chart/configuration and remove Instana agent settings as required by the project instructions. Use the provided load generator only where appropriate.

## Deployment and observability
The intended stack is:
- Robot Shop services and data stores
- Prometheus/Grafana for metrics and a request/error/latency dashboard
- Fluent Bit forwarding logs to Loki for service/error-level searches
- OpenTelemetry configuration with Jaeger to inspect a trace
- An availability SLO, error-budget policy and alert delivered to Slack
- A runbook linked from the alert and a blameless postmortem after the incident drill

Use the configuration files present in this repository and confirm paths before applying commands. The local Minikube control plane became unstable during development; the latest logs showed etcd request timeouts and API-server health failures. Consequently, current live health and end-to-end observability checks are not confirmed.

## Validation checklist
- [ ] Helm chart/configuration can be installed from a clean environment
- [ ] Required services are healthy
- [ ] Dashboard is exported as code and displays requests, errors and latency
- [ ] Logs are searchable in Loki by service and level
- [ ] At least one request trace is visible in Jaeger
- [ ] SLO and error-budget policy are documented
- [ ] Alert fires during the incident drill and links to a runbook
- [ ] Blameless postmortem records impact, timeline, root cause, mitigation and follow-up actions

## Documents
See `docs/` for the SLO/error-budget policy, runbook and postmortem draft. These documents are preparation materials; do not represent an alert, trace or drill as completed unless you have evidence.
