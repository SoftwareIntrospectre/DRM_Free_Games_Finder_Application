provider "aws" {
  region = "us-west-2"
}

resource "aws_ecs_cluster" "drm_game_comparison_cluster" {
  name = "drm-game-comparison-cluster"
}

resource "aws_ecs_task_definition" "drm_game_comparison_task" {
  family                   = "drm-game-comparison"
  container_definitions    = file("ecs/task_definition.json")
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
}

resource "aws_ecs_service" "drm_game_comparison_service" {
  name            = "drm-game-comparison-service"
  cluster         = aws_ecs_cluster.drm_game_comparison_cluster.id
  task_definition = aws_ecs_task_definition.drm_game_comparison_task.arn
  desired_count   = 1
}
