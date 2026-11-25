# Incident Response Runbook

This runbook describes how the on-call engineer handles production incidents.
It is intentionally structured with headings, lists and code blocks so that
chunking strategies can be evaluated against realistic documents.

## 1. Severity Levels

Incidents are classified by customer impact.

- **SEV1** - Full outage or data loss. Page the on-call immediately and open a
  bridge call within 10 minutes.
- **SEV2** - Major feature degraded for many customers. Respond within 30
  minutes.
- **SEV3** - Minor degradation or a workaround exists. Handle during business
  hours.

## 2. First Response

When you receive a page, acknowledge it within five minutes. Then confirm the
alert is real by checking the dashboard and recent deploys. If a deploy
happened in the last hour, rolling back is usually the fastest mitigation.

```bash
# Roll back the most recent release
kubectl rollout undo deployment/api -n production
kubectl rollout status deployment/api -n production
```

Do not spend time finding the root cause until customer impact is mitigated.

## 3. Communication

Post updates in the incident channel every 30 minutes for SEV1 and every hour
for SEV2. Each update should state the current impact, what has been tried,
and the next step. Keep the status page in sync with the channel.

### 3.1 Customer-facing messages

Keep them short, factual and free of speculation. Never promise a time for
resolution unless the fix is already deployed and being verified.

## 4. Post-Incident Review

Within five business days, the incident owner writes a blameless review that
covers the timeline, root cause, contributing factors and follow-up actions.
Every action item needs an owner and a due date.
