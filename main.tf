provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "task_manager" {
  ami           = "ami-08c40ec9ead489470"  # Update with preferred Ubuntu AMI
  instance_type = "t2.micro"

  tags = {
    Name = "TaskManagerServer"
  }
}
