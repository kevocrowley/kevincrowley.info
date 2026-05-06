# Observability for AWS Bedrock Agents

Monitoring AI agents requires more than traditional infrastructure metrics. This post covers implementing comprehensive observability for Bedrock Agents using Prometheus, Grafana, and AWS X-Ray.

## Key Metrics to Track

1. **Agent Invocation Metrics**
   - Request count and rate
   - Latency (p50, p95, p99)
   - Error rate and types
   - Success/failure ratio

2. **Cost Metrics**
   - Token usage (input/output)
   - API request costs
   - Knowledge base queries

3. **Quality Metrics**
   - Retrieval precision
   - Response accuracy (if measurable)
   - User satisfaction scores

## Implementation

### 1. CloudWatch Metrics for Bedrock

```python
import boto3
import json
from datetime import datetime

class BedrockMetrics:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'AWS/Bedrock'
    
    def put_agent_metrics(self, agent_id, metrics):
        """Custom metrics for agent performance."""
        metric_data = [
            {
                'MetricName': 'InvocationLatency',
                'Value': metrics['latency_ms'],
                'Unit': 'Milliseconds',
                'Dimensions': [
                    {'Name': 'AgentId', 'Value': agent_id}
                ]
            },
            {
                'MetricName': 'TokenCount',
                'Value': metrics['tokens'],
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'AgentId', 'Value': agent_id}
                ]
            },
            {
                'MetricName': 'InvocationSuccess',
                'Value': 1 if metrics['success'] else 0,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'AgentId', 'Value': agent_id}
                ]
            }
        ]
        
        self.cloudwatch.put_metric_data(
            Namespace=self.namespace,
            MetricData=metric_data
        )
```

### 2. Lambda Layer for X-Ray Tracing

```python
import boto3
import json
import traceback

# Enable X-Ray tracing
from aws_xray_sdk.core import patch_all
patch_all()

bedrock = boto3.client('bedrock-runtime')

def lambda_handler(event, context):
    # Start custom segment
    with xray_recorder.capture('bedrock-agent-invoke') as segment:
        try:
            agent_id = event['agent_id']
            prompt = event['prompt']
            
            # Add metadata
            segment.put_metadata('agent_id', agent_id)
            segment.put_metadata('prompt_length', len(prompt))
            
            # Invoke Bedrock Agent
            with xray_recorder.capture('bedrock-invoke'):
                response = bedrock.invoke_agent(
                    agentId=agent_id,
                    sessionId=context.aws_request_id,
                    prompt=prompt
                )
            
            # Extract and record response details
            completion = response['completion']
            token_count = estimate_tokens(completion)
            
            segment.put_metadata('response_tokens', token_count)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'completion': completion,
                    'token_count': token_count
                })
            }
            
        except Exception as e:
            segment.put_metadata('error', str(e))
            segment.put_metadata('traceback', traceback.format_exc())
            raise
```

### 3. Grafana Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Bedrock Agent Observability",
    "panels": [
      {
        "title": "Agent Invocation Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(bedrock_agent_invocations[5m])) by (agent_id)",
            "legendFormat": "{{agent_id}}"
          }
        ]
      },
      {
        "title": "Token Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(bedrock_token_count[5m])) by (type)",
            "legendFormat": "{{type}}"
          }
        ]
      },
      {
        "title": "Latency p95",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(bedrock_latency_bucket[5m]))",
            "legendFormat": "p95"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "sum(rate(bedrock_errors[5m])) by (error_type) / sum(rate(bedrock_invocations[5m]))",
            "legendFormat": "{{error_type}}"
          }
        ]
      }
    ]
  }
}
```

## Alerting Rules

```yaml
groups:
- name: bedrock-alerts
  rules:
  - alert: HighAgentLatency
    expr: histogram_quantile(0.95, rate(bedrock_latency_bucket[5m])) > 10000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High agent latency detected"
      
  - alert: HighErrorRate
    expr: sum(rate(bedrock_errors[5m])) / sum(rate(bedrock_invocations[5m])) > 0.05
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "Agent error rate exceeds 5%"
      
  - alert: HighTokenUsage
    expr: sum(rate(bedrock_token_count[1h])) > 1000000
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "High token usage detected"
```

## Conclusion

Comprehensive observability for AI agents requires tracking metrics beyond traditional infrastructure monitoring. X-Ray tracing provides valuable insights into agent execution flow, while custom CloudWatch metrics enable cost and quality tracking.

---

*Tags: Observability, AWS, Bedrock, Prometheus*