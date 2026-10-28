# Robot Shop Availability SLO and Error-Budget Policy

## Objective
Provide a measurable availability target for the user-facing Robot Shop application. This is a proposed policy for the capstone and must be connected to real request metrics before it is treated as an operational SLO.

## Service-level indicator (SLI)
**Successful request ratio** = successful HTTP requests / all valid HTTP requests, measured at the web entry point over a rolling 30-day window. Define success as HTTP status 2xx or 3xx; treat 5xx responses and qualifying timeouts as failures. Exclude health probes and explicitly documented invalid requests.

## Service-level objective (SLO)
Target: **99% successful requests over a rolling 30-day window.**

## Error budget
At 99% availability, the error budget is 1% of eligible requests during the same window. For example, out of 100,000 eligible requests, up to 1,000 may fail before the target is missed. Calculate the budget from measured traffic, not estimated request counts.

## Alerting and response
- Alert when the measured success ratio is below the SLO or a sustained error-rate increase consumes the budget rapidly.
- The alert should identify the service, time window, dashboard link and runbook link.
- First response: acknowledge, assess user impact, mitigate, then investigate root cause.
- If the budget is exhausted, prioritize reliability fixes over risky changes until the service recovers.

## Evidence / limitations
This is a documented policy proposal. It is not evidence that a Prometheus SLI, alert rule, Slack delivery or incident drill has been tested. Record the actual metric name, dashboard, alert rule and test timestamp when verified.
