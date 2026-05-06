# Terraform Modules for Multi-Cloud Infrastructure

Creating reusable, production-ready Terraform modules is essential for maintaining consistent infrastructure across teams. This post covers best practices for building Terraform modules with Terragrunt wrapper.

## Module Structure

Organize your Terraform modules for reusability:

```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── rds/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── ecs/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

## Example VPC Module

```hcl
# modules/vpc/main.tf

resource "aws_vpc" "this" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.common_tags,
    { Name = "${var.environment}-vpc" }
  )
}

resource "aws_subnet" "private" {
  count             = var.az_count
  vpc_id            = aws_vpc.this.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, count.index)
  availability_zone = var.azs[count.index]

  tags = merge(
    var.common_tags,
    { Name = "${var.environment}-private-subnet-${count.index + 1}" }
  )
}

resource "aws_subnet" "public" {
  count                   = var.az_count
  vpc_id                  = aws_vpc.this.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 4, var.az_count + count.index)
  availability_zone       = var.azs[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.common_tags,
    { Name = "${var.environment}-public-subnet-${count.index + 1}" }
  )
}
```

## Using with Terragrunt

```hcl
# terragrunt.hcl

terraform {
  source = "git::https://github.com/your-org/terraform-modules.git//vpc?ref=v1.0.0"
}

inputs = {
  environment = "production"
  vpc_cidr    = "10.0.0.0/16"
  az_count    = 3
  azs         = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  common_tags = {
    Project     = "platform"
    ManagedBy   = "terraform"
    Environment = "production"
  }
}
```

## Key Best Practices

1. **Use Terragrunt** for environment-specific configurations and remote state
2. **Version your modules** using Git tags
3. **Document inputs** thoroughly in README.md
4. **Use validation** with terraform validate and checkov

---

*Tags: Terraform, Terragrunt, IaC, AWS*