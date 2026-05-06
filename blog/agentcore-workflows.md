# Level 2 On-Call: Incident Response Best Practices

As an SRE providing Level 2 on-call support, having a solid incident response process is critical. This post covers best practices for handling production incidents effectively.

## Incident Response Flow

```
Detect -> Triage -> Mitigate -> Resolve -> Post-Mortem
```

## Detection & Triage

When an alert fires, follow this checklist:

1. **Acknowledge the alert** in PagerDuty within SLA window
2. **Assess impact** - Is this user-facing? Revenue-impacting?
3. **Gather context** - Check Datadog/Grafana dashboards, recent deployments
4. **Determine severity** - P1/P2/P3/P4

## Quick Mitigation Steps

```bash
# Check current system state
aws ec2 describe-instance-status --instance-ids i-xxx

# Check application health
curl -f https://api.example.com/health

# Review recent logs
aws logs filter-log-events --log-group /aws/ecs/app --filter-pattern "ERROR"
```

## Communication Template

```markdown
# Incident: [Brief Title]
Severity: P2
Status: Investigating
Impact: 15% of users experiencing slow response times

Timeline:
- 14:00 - Alert triggered (high latency)
- 14:05 - Acknowledge alert
- 14:15 - Identified DB connection pool exhaustion
- 14:20 - Scaling up RDS instance

Next Steps:
- Continue monitoring
- Update status page
- Schedule post-mortem
```

## Post-Mortem Template

1. **Summary**: What happened and impact
2. **Timeline**: Detailed sequence of events
3. **Root Cause**: Why did this happen?
4. **Corrective Actions**: What will we fix?
5. **Prevention**: How to prevent recurrence?

## Key Takeaways

- Always document during incident, not after
- Focus on blameless post-mortems
- Automate detection and remediation where possible
- Practice incident scenarios regularly

---

*Tags: SRE, On-Call, Incident Response, DevOps*