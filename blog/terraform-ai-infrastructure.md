# Terraform Modules for Production AI Infrastructure

Infrastructure as Code is essential for deploying AI services reproducibly. This post covers best practices for creating production-ready Terraform modules for AWS AI infrastructure.

## Module Structure

Organize your Terraform modules for AI infrastructure:

```
modules/
├── bedrock-agent/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── knowledge-base/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── ai-vpc/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

## Bedrock Agent Module Example

```hcl
# modules/bedrock-agent/main.tf

resource "aws_bedrock_agent" "this" {
  agent_name        = var.agent_name
  agent_description = var.description
  iam_role_arn      = aws_iam_role.agent.arn

  instruction = var.instructions

  foundation_model = var.model_id

  # Enable trace for debugging
  foundation_model_configuration {
    model_id = var.model_id
  }

  # Agent knowledge base associations
  dynamic "knowledge_base" {
    for_each = var.knowledge_base_ids
    content {
      knowledge_base_id = knowledge_base.value
      description       = "Associated knowledge base"
    }
  }
}

resource "aws_iam_role" "agent" {
  name = "${var.agent_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "bedrock.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "agent_policy" {
  name = "${var.agent_name}-policy"
  role = aws_iam_role.agent.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeAgent",
          "bedrock:Retrieve"
        ]
      }
    ]
  })
}
```

```hcl
# modules/bedrock-agent/variables.tf

variable "agent_name" {
  description = "Name of the Bedrock agent"
  type        = string
}

variable "description" {
  description = "Agent description"
  type        = string
  default     = ""
}

variable "instructions" {
  description = "System instructions for the agent"
  type        = string
  default     = ""
}

variable "model_id" {
  description = "Foundation model ID"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "knowledge_base_ids" {
  description = "List of knowledge base IDs to associate"
  type        = list(string)
  default     = []
}
```

## Using the Module

```hcl
# main.tf

module "ai_agents" {
  source = "./modules/bedrock-agent"

  agent_name    = "customer-support-agent"
  description   = "AI agent for customer support"
  instructions  = <<-EOF
    You are a helpful customer support agent.
    Be concise and professional in your responses.
  EOF
  model_id      = "anthropic.claude-3-sonnet-20240229-v1:0"
  
  knowledge_base_ids = [module.knowledge_base.kb_id]
}

module "knowledge_base" {
  source = "./modules/knowledge-base"

  kb_name        = "product-docs-kb"
  embedding_model = "amazon.titan-embed-text-v1"
  s3_bucket      = aws_s3_bucket.documents.id
}
```

## Testing with Terratest

```go
// tests/bedrock_agent_test.go

package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestBedrockAgent(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/bedrock-agent",
        Vars: map[string]interface{}{
            "agent_name": "test-agent",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // Verify agent was created
    agentID := terraform.Output(t, terraformOptions, "agent_id")
    assert.NotEmpty(t, agentID)
}
```

## Key Best Practices

1. **Use Terragrunt** for environment-specific configurations
2. **Enable drift detection** to catch manual changes
3. **Implement policy-as-code** with checkov
4. **Use remote state** with proper locking (DynamoDB)

---

*Tags: Terraform, IaC, AWS, Infrastructure*