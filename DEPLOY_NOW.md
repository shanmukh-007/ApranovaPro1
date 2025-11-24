# Deploy to AWS Now - Quick Guide

## ⚠️ IMPORTANT: Rotate Your AWS Credentials!

The credentials you shared are now public. Please:
1. Go to AWS Console → IAM → Users → Deployment-Test
2. Delete the current access key
3. Create a new access key
4. Update ~/.aws/credentials with new credentials

## 🚀 Deploy Basic Infrastructure

### What Will Be Deployed:
- ✅ VPC with public/private subnets
- ✅ RDS PostgreSQL (db.t3.micro)
- ✅ ElastiCache Redis (cache.t3.micro)
- ✅ EFS for storage
- ✅ Application Load Balancer
- ✅ ECS Cluster (ready for tasks)

### NOT Included (as requested):
- ❌ CloudWatch monitoring
- ❌ Lambda workspace manager
- ❌ Auto-scaling policies
- ❌ CloudTrail
- ❌ GuardDuty

## Step-by-Step Deployment

### 1. Set Database Password
```bash
export DB_PASSWORD="YourSecurePassword123!"
```

### 2. Run Deployment
```bash
./deploy-basic-aws.sh
```

This will:
1. Build Docker images (backend, frontend)
2. Create ECR repositories
3. Push images to ECR
4. Deploy infrastructure with Terraform
5. Show you the ALB DNS name

**Estimated time:** 15-20 minutes

### 3. Deploy ECS Tasks (Manual)

After infrastructure is ready, you need to create ECS task definitions and services.

I can help you with this next step once the infrastructure is deployed.

## Current Status

✅ AWS CLI installed
✅ Terraform installed  
✅ AWS credentials configured (Account: 322388074242)
✅ Deployment scripts ready

## Estimated Costs (Basic Setup)

| Resource | Monthly Cost |
|----------|--------------|
| RDS (db.t3.micro) | ~$15 |
| ElastiCache (cache.t3.micro) | ~$12 |
| NAT Gateway | ~$33 |
| ALB | ~$16 |
| EFS | ~$10 (for 30GB) |
| **Total** | **~$86/month** |

Plus ECS Fargate costs when you run tasks (~$30-50/month for 2 tasks).

## Next Steps

1. **Secure credentials** (rotate in AWS Console)
2. **Set DB password**: `export DB_PASSWORD="your-password"`
3. **Deploy**: `./deploy-basic-aws.sh`
4. **Wait 15-20 minutes**
5. **Deploy ECS tasks** (I'll help with this)

Ready to deploy?
