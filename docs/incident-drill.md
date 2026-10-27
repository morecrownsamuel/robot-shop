# Robot Shop Incident Drill Record

**Date:** 27 October 2026  
**Environment:** Kubernetes, namespace `robot-shop`  
**Drill type:** Healthy-baseline and monitoring verification  
**Outcome:** Passed

## Objective
Verify that Robot Shop is running and that Prometheus is collecting its availability probe.

## Evidence collected

| Check | Observed result | Status |
|---|---|---|
| Robot Shop pods | 12/12 Running and ready | Pass |
| Web deployment | 1 desired, 1 available replica | Pass |
| HTTP request | `http://localhost:8080` returned `200 OK` | Pass |
| Prometheus probe | `probe_success = 1` | Pass |
| Web service endpoint | `172.31.36.103:8080` | Present |

Prometheus target:
`http://web.robot-shop.svc.cluster.local:8080`

Prometheus sample observed:
`27 October 2026, 17:03:03 (+01:00)`

## Limitations
This exercise verified healthy operation and monitoring. It did not simulate an outage, verify alert firing, test Slack delivery, or demonstrate recovery from a failure. Those tests remain outstanding.

## Follow-up actions
1. Implement and verify distributed tracing with OpenTelemetry and Jaeger.
2. Resolve incomplete Fluent Bit coverage caused by one Pending pod.
3. Configure and test alert notifications if required by the capstone.
4. Perform a controlled failure-and-recovery drill and record the alert and recovery evidence.
