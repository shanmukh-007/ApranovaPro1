#!/bin/bash
# Update ECS Services to use Public Subnets (No NAT Gateway)

set -e

CLUSTER="production-cluster"
REGION="us-east-1"
PUBLIC_SUBNETS="subnet-02002e074cdf57f66,subnet-0c9a2d59f05c62330"
ECS_SG="sg-0463d9e4cedff4a45"
BACKEND_TG="arn:aws:elasticloadbalancing:us-east-1:322388074242:targetgroup/production-backend-tg/53f6431f37581c66"
FRONTEND_TG="arn:aws:elasticloadbalancing:us-east-1:322388074242:targetgroup/production-frontend-tg/81154200cca29f97"

echo "🔄 Updating ECS services to use public subnets..."

# Register task definitions
echo "📝 Registering backend task definition..."
aws ecs register-task-definition --cli-input-json file://backend-task-def.json --region $REGION

echo "📝 Registering frontend task definition..."
aws ecs register-task-definition --cli-input-json file://frontend-task-def.json --region $REGION

# Check if services exist
echo "🔍 Checking if services exist..."
BACKEND_EXISTS=$(aws ecs describe-services --cluster $CLUSTER --services apranova-backend --region $REGION 2>&1 | grep -c "ACTIVE\|DRAINING" || echo "0")
FRONTEND_EXISTS=$(aws ecs describe-services --cluster $CLUSTER --services apranova-frontend --region $REGION 2>&1 | grep -c "ACTIVE\|DRAINING" || echo "0")

if [ "$BACKEND_EXISTS" -gt "0" ]; then
    echo "🔄 Updating backend service..."
    aws ecs update-service \
        --cluster $CLUSTER \
        --service apranova-backend \
        --task-definition backend \
        --desired-count 1 \
        --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNETS],securityGroups=[$ECS_SG],assignPublicIp=ENABLED}" \
        --region $REGION
else
    echo "✨ Creating backend service..."
    aws ecs create-service \
        --cluster $CLUSTER \
        --service-name apranova-backend \
        --task-definition backend \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNETS],securityGroups=[$ECS_SG],assignPublicIp=ENABLED}" \
        --load-balancers "targetGroupArn=$BACKEND_TG,containerName=backend,containerPort=8000" \
        --region $REGION
fi

if [ "$FRONTEND_EXISTS" -gt "0" ]; then
    echo "🔄 Updating frontend service..."
    aws ecs update-service \
        --cluster $CLUSTER \
        --service apranova-frontend \
        --task-definition frontend \
        --desired-count 1 \
        --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNETS],securityGroups=[$ECS_SG],assignPublicIp=ENABLED}" \
        --region $REGION
else
    echo "✨ Creating frontend service..."
    aws ecs create-service \
        --cluster $CLUSTER \
        --service-name apranova-frontend \
        --task-definition frontend \
        --desired-count 1 \
        --launch-type FARGATE \
        --network-configuration "awsvpcConfiguration={subnets=[$PUBLIC_SUBNETS],securityGroups=[$ECS_SG],assignPublicIp=ENABLED}" \
        --load-balancers "targetGroupArn=$FRONTEND_TG,containerName=frontend,containerPort=3000" \
        --region $REGION
fi

echo ""
echo "✅ Services updated to use public subnets!"
echo ""
echo "⏳ Waiting for services to stabilize (this may take 2-3 minutes)..."
sleep 30

echo ""
echo "📊 Service Status:"
aws ecs describe-services --cluster $CLUSTER --services apranova-backend apranova-frontend --region $REGION --query 'services[*].[serviceName,status,runningCount,desiredCount]' --output table

echo ""
echo "🎯 Running Tasks:"
aws ecs list-tasks --cluster $CLUSTER --region $REGION

echo ""
echo "🌐 Application URL:"
echo "http://production-alb-1841167835.us-east-1.elb.amazonaws.com"
echo ""
echo "💰 Monthly Savings: $33 (NAT Gateway removed)"
echo "📉 New Monthly Cost: ~$101 (down from $134)"
