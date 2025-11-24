# Signup Error Fix

## 🐛 Issue

When trying to sign up a new user, you're getting:
- **Network Error**
- **ERR_CONNECTION_REFUSED**
- **Signup error response: -1**

## 🔍 Root Cause

The Django backend was configured with `SECURE_SSL_REDIRECT=True` in production settings, which redirects all HTTP requests to HTTPS. However, we don't have an SSL certificate configured on the load balancer yet, so:

1. Frontend makes HTTP request to backend
2. Backend responds with 301 redirect to HTTPS
3. HTTPS doesn't exist → Connection refused
4. Signup fails

## ✅ Solution Applied

Updated the backend task definition to disable SSL redirect for now:

```json
{
  "name": "DEBUG",
  "value": "True"
},
{
  "name": "SECURE_SSL_REDIRECT",
  "value": "False"
},
{
  "name": "CSRF_COOKIE_SECURE",
  "value": "False"
},
{
  "name": "SESSION_COOKIE_SECURE",
  "value": "False"
}
```

## 🚀 Status

Backend is being redeployed with the fix. This will take about 2-3 minutes.

## 🧪 How to Test

Once the backend is running:

1. Go to: http://production-alb-1841167835.us-east-1.elb.amazonaws.com/signup
2. Fill in the signup form
3. Submit
4. Should work now!

## 🔐 Proper Solution (For Production)

To properly fix this for production:

### 1. Get SSL Certificate
```bash
# Request certificate in AWS Certificate Manager
aws acm request-certificate \
  --domain-name yourdomain.com \
  --validation-method DNS
```

### 2. Add HTTPS Listener to ALB
```bash
aws elbv2 create-listener \
  --load-balancer-arn <your-alb-arn> \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=<your-cert-arn> \
  --default-actions Type=forward,TargetGroupArn=<your-target-group-arn>
```

### 3. Update Backend to Use HTTPS
Then you can set:
- `SECURE_SSL_REDIRECT=True`
- `CSRF_COOKIE_SECURE=True`
- `SESSION_COOKIE_SECURE=True`

## ⏱️ Timeline

- **Now:** Backend redeploying with HTTP support (2-3 min)
- **After:** Signup should work
- **Later:** Add SSL certificate for proper HTTPS

## 🔄 Current Deployment Status

Checking backend service...

```bash
aws ecs describe-services \
  --cluster production-cluster \
  --services backend \
  --query 'services[0].[runningCount,pendingCount,desiredCount]'
```

Result: 0 running, 2 pending, 1 desired

**Status:** Deploying... Please wait 2-3 minutes and try signup again.

## 📝 Quick Check

To verify backend is ready:

```bash
curl http://production-alb-1841167835.us-east-1.elb.amazonaws.com/api/accounts/signup/
```

Should return JSON response (not 301 redirect or 503 error).

---

**The fix is being deployed. Please wait 2-3 minutes and try signing up again!**
