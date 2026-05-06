# MongoDB Atlas Infrastructure with Terraform

Managing MongoDB Atlas clusters with Terraform ensures reproducible, version-controlled database infrastructure. This guide covers creating and managing MongoDB Atlas resources with Terraform.

## Provider Configuration

```hcl
# providers.tf

terraform {
  required_providers {
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.8"
    }
  }
}

provider "mongodbatlas" {
  public_key  = var.public_key
  private_key = var.private_key
}
```

## Creating a Cluster

```hcl
# main.tf

resource "mongodbatlas_cluster" "main" {
  project_id   = var.project_id
  name         = var.cluster_name
  cluster_type = "REPLICASET"
  provider_name = "AWS"

  # Backup configuration
  cloud_backup = true

  # Auto-scaling
  auto_scaling_disk_gb_enabled = true

  # Instance size
  provider_instance_size_name = "M10"

  # AWS region
  provider_region_name = "EU_WEST_1"

  # Replication
  replication_specs {
    num_shards = 1
    regions_config {
      region_name       = "EU_WEST_1"
      electable_nodes   = 3
      priority          = 7
      read_only_nodes   = 0
    }
  }

  tags = var.common_tags
}
```

## Network Peering

```hcl
# network-peering.tf

resource "mongodbatlas_network_peering" "aws" {
  project_id       = var.project_id
  provider_name    = "AWS"
  account_id       = var.aws_account_id
  vpc_id           = var.vpc_id
  route_table_id   = var.route_table_id
  cluster_name     = mongodbatlas_cluster.main.name
}
```

## Database User

```hcl
# database-user.tf

resource "mongodbatlas_database_user" "app" {
  username        = "app_user"
  password        = var.db_password
  project_id      = var.project_id

  auth_database_name = "admin"

  roles {
    role_name     = "readWriteAnyDatabase"
    database_name = "admin"
  }

  labels {
    key   = "environment"
    value = var.environment
  }
}
```

## Key Considerations

1. **Use IP whitelisting** for development, Private Link for production
2. **Enable Cloud Backup** for disaster recovery
3. **Configure alerts** for CPU, storage, and connection metrics
4. **Use IaC** for all database changes - no manual modifications

---

*Tags: MongoDB Atlas, Terraform, Database, AWS*