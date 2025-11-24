#!/usr/bin/env python3
"""
AWS Cost Calculator for ApraNova LMS
Estimates monthly costs based on usage patterns
"""

# Pricing (US East 1, as of 2024)
PRICING = {
    # ECS Fargate (per vCPU-hour and GB-hour)
    'fargate_vcpu': 0.04048,
    'fargate_memory': 0.004445,
    
    # RDS PostgreSQL
    'rds_t3_medium': 0.068,  # per hour
    'rds_r5_large': 0.240,   # per hour
    'rds_storage': 0.115,    # per GB-month
    'rds_backup': 0.095,     # per GB-month
    
    # ElastiCache Redis
    'redis_t3_micro': 0.017,   # per hour
    'redis_r5_large': 0.188,   # per hour
    
    # Application Load Balancer
    'alb_hour': 0.0225,
    'alb_lcu': 0.008,
    
    # NAT Gateway
    'nat_hour': 0.045,
    'nat_data': 0.045,  # per GB
    
    # EFS
    'efs_storage': 0.30,  # per GB-month
    'efs_throughput': 6.00,  # per MB/s-month
    
    # S3
    's3_storage': 0.023,  # per GB-month
    's3_requests': 0.0004,  # per 1000 requests
    
    # Lambda
    'lambda_requests': 0.20,  # per 1M requests
    'lambda_duration': 0.0000166667,  # per GB-second
    
    # CloudWatch
    'cloudwatch_logs': 0.50,  # per GB ingested
    'cloudwatch_metrics': 0.30,  # per custom metric
    
    # Data Transfer
    'data_transfer_out': 0.09,  # per GB (first 10TB)
}

def calculate_ecs_cost(vcpu, memory_gb, hours_per_month):
    """Calculate ECS Fargate cost"""
    vcpu_cost = vcpu * PRICING['fargate_vcpu'] * hours_per_month
    memory_cost = memory_gb * PRICING['fargate_memory'] * hours_per_month
    return vcpu_cost + memory_cost

def calculate_workspace_cost(num_students, avg_hours_per_day, warm_pool_size=3):
    """
    Calculate workspace cost with warm pool optimization
    
    Traditional: All students have 24/7 containers
    Optimized: Warm pool + on-demand
    """
    hours_per_month = 730
    
    # Traditional approach (always-on)
    traditional_cost = calculate_ecs_cost(
        vcpu=1,
        memory_gb=2,
        hours_per_month=hours_per_month * num_students
    )
    
    # Optimized approach
    # Warm pool (24/7)
    warm_pool_cost = calculate_ecs_cost(
        vcpu=1,
        memory_gb=2,
        hours_per_month=hours_per_month * warm_pool_size
    )
    
    # On-demand (only when students use)
    avg_hours_per_month = avg_hours_per_day * 30
    on_demand_cost = calculate_ecs_cost(
        vcpu=1,
        memory_gb=2,
        hours_per_month=avg_hours_per_month * num_students
    )
    
    optimized_cost = warm_pool_cost + on_demand_cost
    savings = traditional_cost - optimized_cost
    savings_percent = (savings / traditional_cost) * 100
    
    return {
        'traditional': traditional_cost,
        'optimized': optimized_cost,
        'savings': savings,
        'savings_percent': savings_percent
    }

def calculate_total_cost(num_students, avg_hours_per_day=3):
    """Calculate total monthly cost"""
    
    print("=" * 60)
    print(f"AWS Cost Estimate for {num_students} Students")
    print(f"Average workspace usage: {avg_hours_per_day} hours/day")
    print("=" * 60)
    print()
    
    # Core Services
    print("Core Services:")
    print("-" * 60)
    
    # Frontend (2 tasks, 0.25 vCPU, 0.5 GB)
    frontend_cost = calculate_ecs_cost(0.25, 0.5, 730 * 2)
    print(f"  Frontend (ECS):              ${frontend_cost:>8.2f}")
    
    # Backend (2 tasks, 0.5 vCPU, 1 GB)
    backend_cost = calculate_ecs_cost(0.5, 1, 730 * 2)
    print(f"  Backend (ECS):               ${backend_cost:>8.2f}")
    
    # RDS PostgreSQL
    rds_cost = PRICING['rds_t3_medium'] * 730
    rds_storage_cost = 100 * PRICING['rds_storage']
    print(f"  RDS (db.t3.medium):          ${rds_cost:>8.2f}")
    print(f"  RDS Storage (100 GB):        ${rds_storage_cost:>8.2f}")
    
    # ElastiCache Redis
    redis_cost = PRICING['redis_t3_micro'] * 730
    print(f"  ElastiCache (cache.t3.micro):${redis_cost:>8.2f}")
    
    # ALB
    alb_cost = PRICING['alb_hour'] * 730 + PRICING['alb_lcu'] * 730 * 2
    print(f"  Application Load Balancer:   ${alb_cost:>8.2f}")
    
    # NAT Gateway
    nat_cost = PRICING['nat_hour'] * 730 + PRICING['nat_data'] * 100
    print(f"  NAT Gateway:                 ${nat_cost:>8.2f}")
    
    core_total = (frontend_cost + backend_cost + rds_cost + 
                  rds_storage_cost + redis_cost + alb_cost + nat_cost)
    print(f"  {'Core Services Total:':.<40}${core_total:>8.2f}")
    print()
    
    # Workspace Services
    print("Workspace Services:")
    print("-" * 60)
    
    workspace_costs = calculate_workspace_cost(num_students, avg_hours_per_day)
    
    print(f"  Traditional (24/7 containers):${workspace_costs['traditional']:>8.2f}")
    print(f"  Optimized (warm pool + on-demand):${workspace_costs['optimized']:>8.2f}")
    print(f"  {'Savings:':.<40}${workspace_costs['savings']:>8.2f} ({workspace_costs['savings_percent']:.1f}%)")
    print()
    
    # Storage
    print("Storage:")
    print("-" * 60)
    
    # EFS (10 GB per student)
    efs_storage = num_students * 10 * PRICING['efs_storage']
    print(f"  EFS ({num_students * 10} GB):           ${efs_storage:>8.2f}")
    
    # S3 Backups (5 GB per student)
    s3_storage = num_students * 5 * PRICING['s3_storage']
    print(f"  S3 Backups ({num_students * 5} GB):     ${s3_storage:>8.2f}")
    
    storage_total = efs_storage + s3_storage
    print(f"  {'Storage Total:':.<40}${storage_total:>8.2f}")
    print()
    
    # Lambda & Monitoring
    print("Lambda & Monitoring:")
    print("-" * 60)
    
    # Lambda (10,000 invocations/month)
    lambda_cost = (10000 / 1000000) * PRICING['lambda_requests']
    lambda_cost += 10000 * 0.5 * 256 / 1024 * PRICING['lambda_duration']
    print(f"  Lambda (Workspace Manager):  ${lambda_cost:>8.2f}")
    
    # CloudWatch
    cloudwatch_cost = 20  # Estimated
    print(f"  CloudWatch (Logs + Metrics): ${cloudwatch_cost:>8.2f}")
    
    monitoring_total = lambda_cost + cloudwatch_cost
    print(f"  {'Monitoring Total:':.<40}${monitoring_total:>8.2f}")
    print()
    
    # Data Transfer
    print("Data Transfer:")
    print("-" * 60)
    data_transfer = num_students * 10 * PRICING['data_transfer_out']  # 10 GB per student
    print(f"  Outbound ({num_students * 10} GB):      ${data_transfer:>8.2f}")
    print()
    
    # Total
    print("=" * 60)
    total_cost = (core_total + workspace_costs['optimized'] + 
                  storage_total + monitoring_total + data_transfer)
    print(f"  {'TOTAL MONTHLY COST:':.<40}${total_cost:>8.2f}")
    print(f"  {'Cost per Student:':.<40}${total_cost/num_students:>8.2f}")
    print("=" * 60)
    print()
    
    return total_cost

def compare_scenarios():
    """Compare different usage scenarios"""
    print("\n" + "=" * 60)
    print("Cost Comparison: Different Scenarios")
    print("=" * 60)
    print()
    
    scenarios = [
        (100, 3, "Small School (100 students, 3 hrs/day)"),
        (500, 3, "Medium School (500 students, 3 hrs/day)"),
        (1000, 3, "Large School (1000 students, 3 hrs/day)"),
        (100, 6, "Intensive Program (100 students, 6 hrs/day)"),
    ]
    
    print(f"{'Scenario':<45} {'Monthly Cost':>12} {'Per Student':>12}")
    print("-" * 70)
    
    for num_students, hours, description in scenarios:
        workspace_costs = calculate_workspace_cost(num_students, hours)
        
        # Quick calculation (simplified)
        core = 228  # Fixed core services
        workspace = workspace_costs['optimized']
        storage = num_students * 10 * 0.30 + num_students * 5 * 0.023
        monitoring = 20
        data_transfer = num_students * 10 * 0.09
        
        total = core + workspace + storage + monitoring + data_transfer
        per_student = total / num_students
        
        print(f"{description:<45} ${total:>11.2f} ${per_student:>11.2f}")
    
    print()

def cost_optimization_tips():
    """Print cost optimization tips"""
    print("\n" + "=" * 60)
    print("Cost Optimization Tips")
    print("=" * 60)
    print()
    
    tips = [
        ("Use Fargate Spot", "Save 70% on workspace containers", "$200-500/month"),
        ("Reduce warm pool during off-hours", "Scale down 11 PM - 7 AM", "$50-100/month"),
        ("Increase idle timeout", "45 min instead of 30 min", "$30-50/month"),
        ("Use S3 Intelligent-Tiering", "Auto-archive old backups", "$20-40/month"),
        ("Enable RDS Reserved Instances", "1-year commitment", "$150-200/month"),
        ("Use CloudFront for static assets", "Reduce data transfer", "$30-60/month"),
        ("Compress CloudWatch logs", "Reduce log storage", "$10-20/month"),
    ]
    
    print(f"{'Optimization':<35} {'Benefit':<30} {'Savings':<15}")
    print("-" * 80)
    
    for optimization, benefit, savings in tips:
        print(f"{optimization:<35} {benefit:<30} {savings:<15}")
    
    print()
    print(f"{'Total Potential Savings:':<65} $490-970/month")
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        num_students = int(sys.argv[1])
        avg_hours = float(sys.argv[2]) if len(sys.argv) > 2 else 3
        calculate_total_cost(num_students, avg_hours)
    else:
        # Default: 100 students
        calculate_total_cost(100, 3)
        compare_scenarios()
        cost_optimization_tips()
