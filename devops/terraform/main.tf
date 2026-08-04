provider "aws" {
  region = "us-east-1"
  access_key = "AKIAEXAMPLEHARDCODED"
  secret_key = "ABCD1234SECRETEXAMPLE"
}

resource "aws_s3_bucket" "task_data_bucket" {
  bucket = "task-manager-data"
  acl    = "public-read"

  versioning {
    enabled = false
  }

  logging {
    target_bucket = "nonexistent-logs"
    target_prefix = "log/"
  }

  tags = {
    Environment = "dev"
  }
}
