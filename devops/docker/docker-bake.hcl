group "default" {
  targets = ["task-manager"]
}

target "task-manager" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["mytaskmanager:latest"]
  args = {
    APP_ENV = "dev"
    API_KEY = "harcoded_dev_key"
  }
}
