# Enrollment Error Fix

## Problem
When trying to enroll in a track, you're getting an "Unexpected token '<'" error because the Stripe API keys are not configured.

## Solution

### Step 1: Get Stripe API Keys

1. Go to https://dashboard.stripe.com/test/apikeys
2. Sign up or log in to Stripe
3. Copy your **Publishable key** (starts with `pk_test_`)
4. Copy your **Secret key** (starts with `sk_test_`)

### Step 2: Update Environment Variables

Edit your `.env` file and replace these lines:

```bash
STRIPE_PUBLIC_KEY=pk_test_your-stripe-public-key
STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key
```

With your actual keys:

```bash
STRIPE_PUBLIC_KEY=pk_test_51ABC...
STRIPE_SECRET_KEY=sk_test_51ABC...
```

### Step 3: Restart Backend

```bash
docker restart apranova_backend
```

### Step 4: Update Frontend Environment

Create `frontend/.env.local` with:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_51ABC...
```

### Step 5: Restart Frontend

```bash
# Stop the frontend (Ctrl+C in the terminal where it's running)
# Then restart it
cd frontend
npm run dev
```

## Test the Fix

1. Go to http://localhost:3000/get-started
2. Click "Enroll in Data Professional" or "Enroll in Full-Stack Developer"
3. You should be redirected to Stripe's checkout page
4. Use test card: `4242 4242 4242 4242` with any future expiry date and any CVC

## What Was Fixed

1. **Stripe API compatibility**: Updated error handling from `stripe.error.StripeError` to `stripe.StripeError` for Stripe v13
2. **Error messages**: Now you'll see proper error messages instead of HTML parsing errors

## Quick Test (Without Stripe Setup)

If you want to test without setting up Stripe, you can temporarily modify the enrollment flow to skip payment. But for production, you MUST configure Stripe properly.
