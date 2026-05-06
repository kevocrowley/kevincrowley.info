# Datadog Observability for Production Systems

Setting up comprehensive observability is critical for maintaining 99.9% uptime. This guide covers implementing Datadog monitoring for AWS infrastructure.

## Datadog Agent Installation

```yaml
# datadog-agent.yaml (Kubernetes DaemonSet)

apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: datadog-agent
  namespace: default
spec:
  selector:
    matchLabels:
      app: datadog-agent
  template:
    spec:
      containers:
      - name: datadog-agent
        image: datadog/agent:latest
        env:
        - name: DD_API_KEY
          valueFrom:
            secretKeyRef:
              name: datadog-secret
              key: api-key
        - name: DD_SITE
          value: "datadoghq.eu"
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_LOGS_ENABLED
          value: "true"
        volumeMounts:
        - name: dockersocket
          mountPath: /var/run/docker.sock
```

## AWS Integration

```hcl
# datadog-aws.tf

resource "datadog_integration_aws" "main" {
  account_id  = var.aws_account_id
  role_name   = "DatadogAWSIntegrationRole"

  # Enable specific integrations
  services {
    enabled = true
  }

  # Filter specific regions
  excluded_regions = ["us-gov-west-1", "us-gov-east-1"]

  tags = ["production", "eu-west-1"]
}
```

## Custom Metrics

```python
# custom-metrics.py

from datadog import DogStatsd

statsd = DogStatsd(host="localhost", port=8125)

def record_request_metrics(method, status_code, latency_ms):
    # Increment counter
    statsd.increment(
        "app.requests.count",
        tags=["method:" + method, "status:" + str(status_code)]
    )
    
    # Record latency histogram
    statsd.histogram(
        "app.request.latency",
        latency_ms,
        tags=["method:" + method]
    )

# Usage
record_request_metrics("GET", 200, 45.6)
```

## Alert Configuration

```json
{
  "name": "High Error Rate",
  "type": "query alert",
  "query": "sum(last_5m):sum:app.errors.count{env:production}.as_count() > 100",
  "message": "@pagerduty-sre-team High error rate detected on production. Please investigate.",
  "priority": "high",
  "options": {
    "threshold_windows": {
      "recovery_window": "last_10m",
      "trigger_window": "last_5m"
    }
  }
}
```

## Dashboard Example

Create comprehensive dashboards showing:
- Request rate and latency percentiles
- Error rates by endpoint
- CPU/Memory utilization
- Database connection pool status
- External service dependencies health

## SLO Configuration

```hcl
# datadog-slo.tf

resource "datadog_service_level_objective" "api_availability" {
  name        = "API Availability"
  type        = "metric"
  query       = "sum(last 1h):sum:app.requests.count{status:200}.as_count() / sum(last 1h):sum:app.requests.count.as_count()"
  
  target        = 99.9
  error_budget = 0.1
  
  tags = ["env:production", "service:api"]
}
```

---

*Tags: Datadog, Observability, SRE, Monitoring*