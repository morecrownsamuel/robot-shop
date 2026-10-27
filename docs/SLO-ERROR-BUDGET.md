# Robot Shop SLO and Error-Budget Policy

## 1. Purpose

Define a measurable reliability objective for Robot Shop and a policy for
responding when service reliability deteriorates.

## 2. Service-Level Objective (SLO)

- Service: Robot Shop web application
- Availability target: 99% over a rolling 30-day window
- Measurement: Prometheus Blackbox Exporter probing
  http://web.robot-shop.svc.cluster.local:8080
- Success condition: The probe returns HTTP success (2xx).
- Failure condition: The probe fails or does not return HTTP success.
- Measurement metric: `probe_success`

This is the intended SLO. Actual compliance must be established from
collected Prometheus measurements over the evaluation window.

## 3. Error Budget

For a 30-day window:

- Total time: 43,200 minutes
- Allowed unavailability at 99% availability: 432 minutes
- Error-budget consumption: Failed probe time divided by total measured time
- Remaining budget: 100% minus the percentage consumed

Probe results are sampled measurements and do not prove that every user
request succeeded or failed.

## 4. Alerting Policy

Proposed alert thresholds:

- Warning: Availability below 99% over a sustained evaluation window.
- Critical: Availability below 95% over a sustained evaluation window.
- Immediate investigation: Repeated probe failures or a sustained outage.

These thresholds must be implemented as Prometheus alert rules and
validated before they can be described as active alerts. Slack delivery
must also be configured and tested separately.

## 5. Response Procedure

1. Acknowledge the alert and record the incident start time.
2. Check the Robot Shop web deployment, pods, service endpoints, and events.
3. Inspect Prometheus probe results and relevant Loki logs.
4. Identify the impact and restore service using a controlled, reversible action.
5. Verify application availability after recovery.
6. Record the timeline, contributing factors, recovery steps, and follow-up actions.

## 6. Error-Budget Policy

When the error budget is being consumed rapidly:

- Prioritize reliability fixes over optional changes.
- Avoid risky releases while an active incident is unresolved.
- Review recurring failures and agree on corrective actions.
- Reassess the budget using measured data rather than assumptions.

## 7. Evidence and Review

Retain the Prometheus query or exported results used to assess availability,
the relevant Grafana dashboard, alert-rule configuration, incident evidence,
and the postmortem.

Review the SLO and its measurement method during the final capstone audit.
