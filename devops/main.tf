provider "aws" {
provider "aws" {
  region = "us-east-1"
}
  region     = "us-east-1"
}

resource "aws_instance" "task_manager" {
  ami           = "ami-08c40ec9ead489470"
  instance_type = "t2.micro"
  vpc_security_group_ids = ["sg-1234567890"]
  tags = {
    Name = "TaskManagerServer"
  }
}
