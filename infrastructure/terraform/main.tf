# Private Financial Analyst AI — Terraform Infrastructure
# Day 29c — Infrastructure as Code

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# S3 bucket for financial documents
resource "aws_s3_bucket" "financial_docs" {
  bucket = "private-financial-analyst-docs"
  tags = {
    Project     = "Private Financial Analyst AI"
    Environment = "production"
  }
}

# Block all public access to documents
resource "aws_s3_bucket_public_access_block" "financial_docs" {
  bucket                  = aws_s3_bucket.financial_docs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# IAM role for Bedrock access
resource "aws_iam_role" "bedrock_role" {
  name = "financial-analyst-bedrock-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "bedrock.amazonaws.com" }
    }]
  })
}

# Attach Bedrock policy
resource "aws_iam_role_policy_attachment" "bedrock_policy" {
  role       = aws_iam_role.bedrock_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

# Secrets Manager for API keys
resource "aws_secretsmanager_secret" "api_keys" {
  name        = "financial-analyst-api-keys"
  description = "API keys for Private Financial Analyst AI"
}

# Outputs
output "s3_bucket_name" {
  value = aws_s3_bucket.financial_docs.bucket
}

output "bedrock_role_arn" {
  value = aws_iam_role.bedrock_role.arn
}

output "secrets_manager_arn" {
  value = aws_secretsmanager_secret.api_keys.arn
}
