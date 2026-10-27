# Robot Shop Blameless Postmortem

**Document status:** Template pending a real or controlled incident  
**Environment:** Kubernetes, namespace `robot-shop`

## 1. Summary
No application outage was observed during the baseline verification conducted on 27 October 2026. Robot Shop returned HTTP 200, all 12 application pods were ready, and Prometheus reported `probe_success = 1`.

This document is a template for recording a future incident. It does not claim that an outage occurred.

## 2. Impact
- Confirmed customer impact: None identified during the baseline check.
- Confirmed outage duration: Not applicable; no outage was observed.
- Data loss: Not assessed; no incident occurred during this exercise.

## 3. Timeline
| Time | Event |
|---|---|
| 17:03 (+01:00) | Prometheus availability sample observed with `probe_success = 1`. |
| During verification | Robot Shop HTTP request returned `200 OK`. |
| During verification | All 12 Robot Shop pods reported Running and ready. |

## 4. Detection
Prometheus Blackbox Exporter checks the Robot Shop web endpoint. Warning and critical availability rules are configured. Alert delivery and Slack notification have not yet been verified.

## 5. Root cause
Not applicable. No failure was induced or observed during this verification.

## 6. What went well
- Application pods were healthy.
- The web endpoint responded successfully.
- Prometheus returned a successful availability probe.
- The verification steps were performed without intentionally disrupting the application.

## 7. What needs improvement
- Implement and verify OpenTelemetry/Jaeger distributed tracing.
- Resolve the Pending Fluent Bit pod to improve log coverage.
- Verify alert firing and notification delivery.
- Conduct a controlled failure-and-recovery drill.

## 8. Action items
| Action | Priority | Status |
|---|---|---|
| Implement and verify distributed tracing | High | Open |
| Restore Fluent Bit coverage on both nodes | High | Open |
| Test alert rules and notification delivery | High | Open |
| Perform controlled failure-and-recovery drill | High | Open |

## 9. Lessons learned
A healthy baseline confirms service availability at the time of measurement, but does not prove outage detection, alert delivery, or recovery. Those capabilities require separate tests and evidence.
