# Workspace Manager Module
# Handles on-demand workspace provisioning with auto-termination

# DynamoDB table for workspace state
resource "aws_dynamodb_table" "workspace_state" {
  name           = "${var.environment}-workspace-state"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "task_arn"
  
  attribute {
    name = "user_id"
    type = "S"
  }
  
  attribute {
    name = "task_arn"
    type = "S"
  }
  
  attribute {
    name = "status"
    type = "S"
  }
  
  global_secondary_index {
    name            = "StatusIndex"
    hash_key        = "status"
    projection_type = "ALL"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  tags = {
    Name = "${var.environment}-workspace-state"
  }
}

# Security Group for Workspace Containers
resource "aws_security_group" "workspace" {
  name_prefix = "${var.environment}-workspace-"
  description = "Security group for workspace containers"
  vpc_id      = var.vpc_id
  
  ingress {
    description = "VS Code"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  ingress {
    description = "Superset"
    from_port   = 8088
    to_port     = 8088
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.environment}-workspace-sg"
  }
}

# ECS Task Definition for VS Code
resource "aws_ecs_task_definition" "vscode" {
  family                   = "${var.environment}-workspace-vscode"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.workspace_cpu
  memory                   = var.workspace_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  
  container_definitions = jsonencode([{
    name  = "workspace"
    image = var.vscode_image
    
    portMappings = [{
      containerPort = 8080
      protocol      = "tcp"
    }]
    
    environment = [
      {
        name  = "PASSWORD"
        value = ""
      }
    ]
    
    command = ["--auth", "none", "--bind-addr", "0.0.0.0:8080", "."]
    
    mountPoints = [{
      sourceVolume  = "efs"
      containerPath = "/home/coder/project"
      readOnly      = false
    }]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.workspace.name
        "awslogs-region"        = data.aws_region.current.name
        "awslogs-stream-prefix" = "vscode"
      }
    }
  }])
  
  volume {
    name = "efs"
    
    efs_volume_configuration {
      file_system_id     = var.efs_id
      transit_encryption = "ENABLED"
      
      authorization_config {
        iam = "ENABLED"
      }
    }
  }
}

# ECS Task Definition for Superset
resource "aws_ecs_task_definition" "superset" {
  family                   = "${var.environment}-workspace-superset"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.workspace_cpu
  memory                   = var.workspace_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn
  
  container_definitions = jsonencode([{
    name  = "workspace"
    image = var.superset_image
    
    portMappings = [{
      containerPort = 8088
      protocol      = "tcp"
    }]
    
    environment = [
      {
        name  = "SUPERSET_LOAD_EXAMPLES"
        value = "yes"
      }
    ]
    
    mountPoints = [{
      sourceVolume  = "efs"
      containerPath = "/app/superset_home"
      readOnly      = false
    }]
    
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.workspace.name
        "awslogs-region"        = data.aws_region.current.name
        "awslogs-stream-prefix" = "superset"
      }
    }
  }])
  
  volume {
    name = "efs"
    
    efs_volume_configuration {
      file_system_id     = var.efs_id
      transit_encryption = "ENABLED"
      
      authorization_config {
        iam = "ENABLED"
      }
    }
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "workspace" {
  name              = "/ecs/${var.environment}/workspace"
  retention_in_days = 7
}

# IAM Role for ECS Execution
resource "aws_iam_role" "ecs_execution" {
  name = "${var.environment}-workspace-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution" {
  role       = aws_iam_role.ecs_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# IAM Role for ECS Task
resource "aws_iam_role" "ecs_task" {
  name = "${var.environment}-workspace-task-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ecs-tasks.amazonaws.com"
      }
    }]
  })
}

# EFS Access Policy
resource "aws_iam_role_policy" "efs_access" {
  name = "efs-access"
  role = aws_iam_role.ecs_task.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientWrite"
      ]
      Resource = "arn:aws:elasticfilesystem:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:file-system/${var.efs_id}"
    }]
  })
}

# Lambda Function for Workspace Manager
resource "aws_lambda_function" "workspace_manager" {
  filename         = "${path.module}/lambda.zip"
  function_name    = "${var.environment}-workspace-manager"
  role             = aws_iam_role.lambda.arn
  handler          = "workspace_manager.lambda_handler"
  source_code_hash = filebase64sha256("${path.module}/lambda.zip")
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 256
  
  environment {
    variables = {
      ECS_CLUSTER          = var.ecs_cluster_name
      VSCODE_TASK_DEF      = aws_ecs_task_definition.vscode.family
      SUPERSET_TASK_DEF    = aws_ecs_task_definition.superset.family
      SUBNETS              = join(",", var.private_subnet_ids)
      SECURITY_GROUP       = aws_security_group.workspace.id
      DYNAMODB_TABLE       = aws_dynamodb_table.workspace_state.name
      WARM_POOL_SIZE       = var.warm_pool_size
      IDLE_TIMEOUT_MINUTES = var.idle_timeout_minutes
    }
  }
  
  vpc_config {
    subnet_ids         = var.private_subnet_ids
    security_group_ids = [aws_security_group.workspace.id]
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda" {
  name = "${var.environment}-workspace-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda Policies
resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "lambda_ecs" {
  name = "ecs-access"
  role = aws_iam_role.lambda.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecs:RunTask",
          "ecs:StopTask",
          "ecs:DescribeTasks",
          "ecs:ListTasks"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.workspace_state.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# EventBridge Rule for Activity Monitoring (every 5 minutes)
resource "aws_cloudwatch_event_rule" "monitor_workspaces" {
  name                = "${var.environment}-monitor-workspaces"
  description         = "Monitor workspace activity every 5 minutes"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "monitor_workspaces" {
  rule      = aws_cloudwatch_event_rule.monitor_workspaces.name
  target_id = "workspace-manager"
  arn       = aws_lambda_function.workspace_manager.arn
  
  input = jsonencode({
    action = "monitor"
  })
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.workspace_manager.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.monitor_workspaces.arn
}

# Data sources
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
