# MCP Server Setup for AI-Assisted AWS Deployment

## 🤖 What is MCP?

**Model Context Protocol (MCP)** allows AI assistants to interact with external tools and services. With MCP servers, you can:

- Deploy to AWS using natural language
- Manage infrastructure with AI assistance
- Monitor and troubleshoot automatically
- Execute commands safely with AI guidance

## 🚀 Quick Setup (5 minutes)

### 1. Install UV (Python Package Manager)

**macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or with Homebrew:**
```bash
brew install uv
```

**Verify installation:**
```bash
uv --version
uvx --version
```

### 2. Configure AWS Credentials

```bash
# Install AWS CLI if not already installed
brew install awscli

# Configure AWS credentials
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: us-east-1
# - Default output format: json

# Verify
aws sts get-caller-identity
```

### 3. MCP Servers are Already Configured!

I've created `.kiro/settings/mcp.json` with these MCP servers:

1. **aws-cli** - Execute AWS CLI commands
2. **terraform** - Manage infrastructure
3. **docker** - Build and manage containers
4. **filesystem** - Read/write files
5. **git** - Version control operations

### 4. Restart Kiro

The MCP servers will connect automatically when Kiro restarts.

## 🎯 What You Can Do with AI

### Deploy to AWS
```
"Deploy the ApraNova application to AWS production environment"
```

The AI will:
1. Check AWS credentials
2. Build Docker images
3. Push to ECR
4. Run Terraform apply
5. Initialize database
6. Verify deployment

### Monitor Infrastructure
```
"Show me the status of all ECS services in production"
```

The AI will:
1. List ECS clusters
2. Describe services
3. Show task status
4. Display health checks

### Manage Workspaces
```
"How many workspace containers are currently running?"
```

The AI will:
1. List ECS tasks
2. Filter workspace containers
3. Show resource usage
4. Display costs

### Troubleshoot Issues
```
"Why is the backend service failing?"
```

The AI will:
1. Check service status
2. Read CloudWatch logs
3. Analyze error messages
4. Suggest fixes

### Cost Analysis
```
"What's my AWS bill for this month?"
```

The AI will:
1. Query Cost Explorer
2. Break down by service
3. Compare to last month
4. Suggest optimizations

## 📋 Available MCP Servers

### 1. AWS CLI Server

**Capabilities:**
- Execute any AWS CLI command
- Manage EC2, ECS, RDS, S3, etc.
- Query CloudWatch metrics
- Manage IAM roles and policies

**Example Commands:**
```
"List all ECS clusters"
"Show RDS database status"
"Get CloudWatch logs for backend service"
"Create an S3 bucket for backups"
```

**Auto-approved actions:**
- `aws_cli_describe_*` - Read-only describe commands
- `aws_cli_list_*` - List resources
- `aws_cli_get_*` - Get information

**Requires approval:**
- `aws_cli_create_*` - Create resources
- `aws_cli_delete_*` - Delete resources
- `aws_cli_update_*` - Update resources

### 2. Terraform Server

**Capabilities:**
- Plan infrastructure changes
- Apply Terraform configurations
- Show current state
- Validate configurations

**Example Commands:**
```
"Plan the AWS infrastructure deployment"
"Show the current Terraform state"
"Validate the Terraform configuration"
"Apply the infrastructure changes"
```

**Auto-approved actions:**
- `terraform_plan` - Preview changes
- `terraform_validate` - Check syntax
- `terraform_show` - Display state

**Requires approval:**
- `terraform_apply` - Apply changes
- `terraform_destroy` - Destroy resources

### 3. Docker Server

**Capabilities:**
- Build Docker images
- Push to registries
- Manage containers
- View logs

**Example Commands:**
```
"Build the backend Docker image"
"Push images to ECR"
"Show running containers"
"Get logs from the backend container"
```

**Auto-approved actions:**
- `docker_ps` - List containers
- `docker_images` - List images
- `docker_logs` - View logs

**Requires approval:**
- `docker_build` - Build images
- `docker_push` - Push to registry
- `docker_run` - Start containers

### 4. Filesystem Server

**Capabilities:**
- Read files
- Write files
- List directories
- Search files

**Example Commands:**
```
"Read the AWS deployment plan"
"Show me the Terraform variables"
"List all Python files in the backend"
"Update the environment variables"
```

**Auto-approved actions:**
- `read_file` - Read file contents
- `list_directory` - List directory

**Requires approval:**
- `write_file` - Write to files
- `delete_file` - Delete files

### 5. Git Server

**Capabilities:**
- Check status
- View commits
- Create branches
- Commit changes

**Example Commands:**
```
"Show git status"
"What changed in the last commit?"
"Create a new branch for AWS deployment"
"Commit the infrastructure changes"
```

**Auto-approved actions:**
- `git_status` - Show status
- `git_log` - View history
- `git_diff` - Show changes

**Requires approval:**
- `git_commit` - Commit changes
- `git_push` - Push to remote
- `git_branch` - Create branches

## 🎬 Example AI Workflows

### Workflow 1: Complete AWS Deployment

**You say:**
```
"Deploy ApraNova to AWS production. Use 100 students as the baseline."
```

**AI does:**
1. ✅ Reads deployment plan
2. ✅ Checks AWS credentials
3. ✅ Runs cost calculator (100 students)
4. ✅ Builds Docker images
5. ✅ Pushes to ECR
6. ✅ Runs Terraform plan
7. ⚠️ **Asks for approval** to apply
8. ✅ Applies Terraform
9. ✅ Initializes database
10. ✅ Verifies deployment
11. ✅ Shows access URLs

### Workflow 2: Monitor and Optimize

**You say:**
```
"Check my AWS costs and suggest optimizations"
```

**AI does:**
1. ✅ Queries Cost Explorer
2. ✅ Lists running resources
3. ✅ Identifies idle workspaces
4. ✅ Calculates potential savings
5. ✅ Suggests optimizations:
   - Reduce warm pool size
   - Use Fargate Spot
   - Enable RDS Reserved Instances
6. ⚠️ **Asks if you want to apply**

### Workflow 3: Troubleshoot Issues

**You say:**
```
"The backend service is showing errors. Fix it."
```

**AI does:**
1. ✅ Checks ECS service status
2. ✅ Reads CloudWatch logs
3. ✅ Identifies error: Database connection timeout
4. ✅ Checks RDS status
5. ✅ Finds issue: Security group misconfigured
6. ✅ Suggests fix: Update security group
7. ⚠️ **Asks for approval** to update
8. ✅ Applies fix
9. ✅ Restarts service
10. ✅ Verifies fix

### Workflow 4: Scale Infrastructure

**You say:**
```
"We're expecting 500 students next month. Scale the infrastructure."
```

**AI does:**
1. ✅ Runs cost calculator (500 students)
2. ✅ Shows projected cost: $4,585/month
3. ✅ Updates Terraform variables
4. ✅ Plans infrastructure changes:
   - Increase RDS instance size
   - Increase backend max capacity
   - Adjust warm pool size
5. ⚠️ **Asks for approval**
6. ✅ Applies changes
7. ✅ Monitors deployment
8. ✅ Verifies scaling

## 🔐 Security Features

### Auto-Approval
Only **read-only** operations are auto-approved:
- Listing resources
- Describing status
- Reading logs
- Viewing configurations

### Manual Approval Required
**Destructive** or **expensive** operations require your approval:
- Creating resources
- Deleting resources
- Applying Terraform
- Pushing Docker images
- Committing code

### Credentials
- AWS credentials stored securely in `~/.aws/credentials`
- MCP servers use your existing AWS profile
- No credentials stored in MCP config

## 🛠️ Advanced Configuration

### Custom AWS Profile

Edit `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "aws-cli": {
      "env": {
        "AWS_PROFILE": "apranova-production",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### Multiple Environments

Create separate profiles:
```bash
# Configure production
aws configure --profile apranova-production

# Configure staging
aws configure --profile apranova-staging
```

Switch profiles in MCP config:
```json
{
  "mcpServers": {
    "aws-cli-production": {
      "command": "uvx",
      "args": ["mcp-server-aws-cli"],
      "env": {
        "AWS_PROFILE": "apranova-production"
      }
    },
    "aws-cli-staging": {
      "command": "uvx",
      "args": ["mcp-server-aws-cli"],
      "env": {
        "AWS_PROFILE": "apranova-staging"
      }
    }
  }
}
```

### Add More Auto-Approvals

Edit `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "aws-cli": {
      "autoApprove": [
        "aws_cli_describe_*",
        "aws_cli_list_*",
        "aws_cli_get_*",
        "aws_cli_show_*",
        "aws_cli_view_*"
      ]
    }
  }
}
```

## 🧪 Test MCP Servers

### Test AWS CLI Server
```
"List all S3 buckets"
"Show ECS clusters"
"Get my AWS account ID"
```

### Test Terraform Server
```
"Validate the Terraform configuration"
"Show the Terraform plan"
```

### Test Docker Server
```
"List Docker images"
"Show running containers"
```

### Test Filesystem Server
```
"Read AWS_DEPLOYMENT_PLAN.md"
"List files in the terraform directory"
```

### Test Git Server
```
"Show git status"
"What's in the last commit?"
```

## 📊 Example AI Conversations

### Deploy to AWS
```
You: "I want to deploy ApraNova to AWS. What do I need to do?"

AI: "I'll help you deploy to AWS. Let me check the deployment plan and your AWS setup.

[Reads AWS_DEPLOYMENT_PLAN.md]
[Checks AWS credentials]

Great! You have AWS credentials configured. Here's what we'll do:

1. Build Docker images (backend, frontend, vscode, superset)
2. Push to ECR
3. Deploy infrastructure with Terraform
4. Initialize database
5. Verify deployment

Estimated cost: $1,167/month for 100 students
Deployment time: 15-20 minutes

Ready to proceed?"

You: "Yes, deploy it"

AI: "Starting deployment...

[Builds Docker images]
✅ Backend image built
✅ Frontend image built
✅ VS Code image built
✅ Superset image built

[Pushes to ECR]
✅ Images pushed to ECR

[Runs Terraform plan]
✅ Plan created: 47 resources to create

⚠️ This will create AWS resources and incur costs (~$1,167/month).
Do you want to apply these changes?"

You: "Yes"

AI: "Applying Terraform...
[Progress updates]
✅ VPC created
✅ RDS database created
✅ ECS cluster created
✅ Load balancer created
✅ Lambda function deployed

Deployment complete! 🎉

Access your application:
- Frontend: https://your-alb-dns.amazonaws.com
- Backend: https://your-alb-dns.amazonaws.com/api

Next steps:
1. Configure DNS
2. Create admin user
3. Test workspace provisioning"
```

### Monitor Costs
```
You: "How much am I spending on AWS?"

AI: "Let me check your AWS costs...

[Queries Cost Explorer]

Current month (Nov 2024):
- Total: $1,243
- Daily average: $54

Breakdown by service:
- ECS Fargate: $612 (49%)
- EFS: $298 (24%)
- RDS: $187 (15%)
- ElastiCache: $89 (7%)
- Other: $57 (5%)

Compared to last month: +$76 (+6.5%)

Active resources:
- 4 ECS services running
- 12 workspace containers active
- 1 RDS instance (db.t3.medium)

Optimization suggestions:
1. Reduce warm pool to 2 containers → Save $30/month
2. Use Fargate Spot for workspaces → Save $200/month
3. Enable RDS Reserved Instance → Save $150/month

Total potential savings: $380/month

Would you like me to apply any of these optimizations?"
```

### Troubleshoot
```
You: "Students are reporting slow workspace launch times"

AI: "Let me investigate...

[Checks ECS cluster]
[Checks Lambda logs]
[Checks warm pool status]

Found the issue:

Problem: Warm pool is depleted
- Current warm containers: 0
- Target warm pool size: 3
- Recent launches: 15 in last hour

Root cause: High demand exceeded warm pool capacity

Solution:
1. Increase warm pool size to 5 during peak hours
2. Add auto-scaling for warm pool based on time
3. Optimize container startup time

I can implement these fixes. Would you like me to proceed?"

You: "Yes, fix it"

AI: "Applying fixes...

[Updates Terraform configuration]
✅ Warm pool size increased to 5
✅ Auto-scaling schedule added (9 AM - 9 PM)
✅ Container startup optimizations applied

[Deploys changes]
✅ Changes applied

Testing...
✅ Warm pool replenished (5 containers ready)
✅ Launch time: 1.8 seconds (from warm pool)
✅ Launch time: 24 seconds (on-demand)

Issue resolved! Students should now experience faster workspace launches."
```

## 🚨 Troubleshooting MCP

### MCP Servers Not Connecting

**Check UV installation:**
```bash
uv --version
uvx --version
```

**Reinstall if needed:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Restart Kiro:**
- Close and reopen Kiro
- MCP servers connect on startup

### AWS Credentials Not Working

**Verify credentials:**
```bash
aws sts get-caller-identity
```

**Reconfigure if needed:**
```bash
aws configure
```

**Check profile:**
```bash
cat ~/.aws/credentials
cat ~/.aws/config
```

### MCP Server Errors

**View MCP logs:**
- Open Kiro
- Command Palette → "MCP: Show Logs"

**Reconnect servers:**
- Command Palette → "MCP: Reconnect All Servers"

**Check server status:**
- Kiro sidebar → "MCP Servers" view

## 🎯 Best Practices

### 1. Start with Read-Only Commands
```
"Show me the current AWS infrastructure"
"List all running ECS tasks"
"What's the RDS database status?"
```

### 2. Review Before Applying
Always review Terraform plans before applying:
```
"Show me the Terraform plan"
[Review changes]
"Apply the changes"
```

### 3. Use Staging First
Test in staging before production:
```
"Deploy to staging environment"
[Test thoroughly]
"Deploy to production"
```

### 4. Monitor After Changes
```
"Apply the infrastructure changes"
[Wait 5 minutes]
"Check the health of all services"
```

### 5. Keep Backups
```
"Create a snapshot of the RDS database before upgrading"
```

## 📚 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [AWS CLI Reference](https://docs.aws.amazon.com/cli/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [UV Documentation](https://docs.astral.sh/uv/)

## 🎉 You're Ready!

Now you can deploy and manage AWS infrastructure using natural language with AI assistance!

**Try it:**
```
"Help me deploy ApraNova to AWS"
"Show me my AWS costs"
"Check if all services are healthy"
"Scale the infrastructure for 500 students"
```

The AI will guide you through everything! 🚀
