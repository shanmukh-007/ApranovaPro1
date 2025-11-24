# MCP Quick Reference - AI Commands for AWS Deployment

## 🚀 Setup (One-Time)

```bash
# Run setup script
chmod +x setup-mcp.sh
./setup-mcp.sh

# Restart Kiro
# MCP servers will connect automatically
```

## 💬 AI Commands You Can Use

### Deployment Commands

```
"Deploy ApraNova to AWS production"
"Deploy to staging environment first"
"Show me the deployment plan"
"What will it cost to deploy for 100 students?"
"Build and push Docker images to ECR"
```

### Monitoring Commands

```
"Show me the status of all ECS services"
"Are all services healthy?"
"How many workspace containers are running?"
"Show me the backend logs"
"What's the CPU usage of the database?"
```

### Cost Management

```
"How much am I spending on AWS this month?"
"Show me a cost breakdown by service"
"What are my biggest cost drivers?"
"Suggest ways to reduce costs"
"Calculate costs for 500 students"
```

### Troubleshooting

```
"Why is the backend service failing?"
"Show me recent errors in CloudWatch"
"The workspace launch is slow, investigate"
"Check database connection issues"
"Restart the backend service"
```

### Scaling

```
"Scale the infrastructure for 500 students"
"Increase the backend capacity to 10 tasks"
"Add more warm pool containers"
"Upgrade the database to db.r5.large"
"Show me the current resource limits"
```

### Infrastructure Management

```
"Show me the current Terraform state"
"Plan infrastructure changes"
"Apply the Terraform configuration"
"Destroy the staging environment"
"Create a database snapshot"
```

### Workspace Management

```
"How many students are using workspaces right now?"
"Terminate idle workspace containers"
"Check the warm pool status"
"Launch a test workspace"
"Show workspace launch times"
```

### Security & Compliance

```
"Show me all security groups"
"Check if encryption is enabled"
"List IAM roles and policies"
"Show CloudTrail audit logs"
"Verify backup configuration"
```

## 🎯 Example Workflows

### Complete Deployment

```
You: "I want to deploy ApraNova to AWS for 100 students"

AI: [Reads deployment plan]
    [Calculates costs: $1,167/month]
    [Shows deployment steps]
    "Ready to proceed?"

You: "Yes, deploy it"

AI: [Builds images]
    [Pushes to ECR]
    [Runs Terraform]
    [Initializes database]
    "Deployment complete! 🎉"
```

### Cost Optimization

```
You: "My AWS bill is too high, help me reduce it"

AI: [Analyzes costs]
    [Identifies waste]
    "Found 3 optimizations that save $380/month"
    [Lists suggestions]
    "Apply these changes?"

You: "Yes"

AI: [Applies optimizations]
    "Savings applied! New monthly cost: $787"
```

### Troubleshooting

```
You: "Students can't access their workspaces"

AI: [Checks ECS status]
    [Reads logs]
    [Identifies issue]
    "Found: Warm pool depleted"
    "Fix: Increase warm pool size"
    "Apply fix?"

You: "Yes"

AI: [Updates configuration]
    [Deploys changes]
    "Fixed! Workspaces are accessible now"
```

## 🔐 Auto-Approved vs Manual Approval

### Auto-Approved (No confirmation needed)
- ✅ Reading files
- ✅ Listing resources
- ✅ Viewing logs
- ✅ Describing status
- ✅ Getting information
- ✅ Showing configurations

### Requires Your Approval
- ⚠️ Creating resources
- ⚠️ Deleting resources
- ⚠️ Applying Terraform
- ⚠️ Pushing Docker images
- ⚠️ Modifying infrastructure
- ⚠️ Committing code changes

## 🛠️ MCP Servers Available

| Server | Purpose | Example Command |
|--------|---------|-----------------|
| **aws-cli** | AWS operations | "List all S3 buckets" |
| **terraform** | Infrastructure | "Show Terraform plan" |
| **docker** | Containers | "Build backend image" |
| **filesystem** | Files | "Read deployment plan" |
| **git** | Version control | "Show git status" |

## 📊 Useful Queries

### Infrastructure Status
```
"Give me a complete status report of the AWS infrastructure"
"Show me all running resources and their costs"
"What's the health status of each service?"
```

### Performance Metrics
```
"Show me API response times for the last hour"
"What's the average workspace launch time?"
"How many requests per minute is the backend handling?"
```

### Resource Usage
```
"Show CPU and memory usage for all services"
"Which service is using the most resources?"
"Are we hitting any resource limits?"
```

### Cost Analysis
```
"Compare this month's costs to last month"
"Show me the cost trend for the last 3 months"
"What's the cost per student?"
```

## 🎓 Learning Commands

### Understand Your Infrastructure
```
"Explain the current AWS architecture"
"What does the workspace manager Lambda do?"
"How does the warm pool work?"
"Show me the data flow from user to workspace"
```

### Best Practices
```
"What are the security best practices for this setup?"
"How can I improve performance?"
"What monitoring should I set up?"
"How do I ensure high availability?"
```

## 🚨 Emergency Commands

### Service Down
```
"The application is down, diagnose and fix"
"Restart all services"
"Rollback to the previous deployment"
```

### High Costs
```
"My AWS bill spiked, find out why"
"Terminate all idle resources immediately"
"Show me what's costing the most right now"
```

### Performance Issues
```
"The application is slow, investigate"
"Scale up the backend immediately"
"Check for database bottlenecks"
```

## 💡 Pro Tips

### Be Specific
❌ "Fix the problem"
✅ "The backend service is returning 500 errors, investigate and fix"

### Ask for Explanations
```
"Explain what this Terraform change will do before applying"
"Show me the cost impact of scaling to 500 students"
```

### Use Context
```
"We're expecting 200 students next week, prepare the infrastructure"
"It's Black Friday, scale up for high traffic"
```

### Chain Commands
```
"Deploy to staging, run tests, then deploy to production if tests pass"
"Check costs, suggest optimizations, and apply the top 3 suggestions"
```

## 🔄 Common Workflows

### Daily Operations
```
1. "Show me yesterday's costs and any anomalies"
2. "Check health of all services"
3. "How many students used workspaces yesterday?"
4. "Any errors in the logs?"
```

### Weekly Review
```
1. "Show me this week's cost summary"
2. "What's the average workspace usage?"
3. "Any performance issues this week?"
4. "Suggest optimizations based on usage patterns"
```

### Monthly Planning
```
1. "Show me last month's total costs"
2. "Project costs for next month based on growth"
3. "What infrastructure upgrades do we need?"
4. "Plan capacity for expected student growth"
```

## 📞 Getting Help

### MCP Issues
```
"The MCP servers aren't working, help me troubleshoot"
"Reconnect all MCP servers"
"Show me MCP server logs"
```

### AWS Issues
```
"I'm getting AWS permission errors, what's wrong?"
"My AWS credentials expired, how do I update them?"
"Show me my AWS account limits"
```

### Deployment Issues
```
"The deployment failed, show me why"
"Rollback the last deployment"
"Verify all deployment prerequisites"
```

## 🎯 Quick Start Checklist

- [ ] Run `./setup-mcp.sh`
- [ ] Restart Kiro
- [ ] Test: "Show me my AWS account information"
- [ ] Test: "List all S3 buckets"
- [ ] Test: "Show the Terraform plan"
- [ ] Ready to deploy: "Deploy ApraNova to AWS"

## 📚 Documentation

- **MCP_AWS_SETUP.md** - Complete MCP setup guide
- **AWS_DEPLOYMENT_PLAN.md** - AWS architecture and deployment
- **AWS_QUICK_START.md** - Step-by-step deployment
- **AWS_QUICK_REFERENCE.md** - AWS command reference

---

## Summary

With MCP servers configured, you can now:

✅ Deploy to AWS using natural language  
✅ Monitor infrastructure with AI assistance  
✅ Troubleshoot issues automatically  
✅ Optimize costs intelligently  
✅ Scale infrastructure on demand  

**Just ask the AI, and it will help you!** 🚀
