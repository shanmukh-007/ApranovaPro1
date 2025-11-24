"""
AWS Lambda Function: Workspace Manager
Handles on-demand workspace provisioning with auto-termination
"""
import boto3
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# AWS Clients
ecs = boto3.client('ecs')
dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

# Environment Variables
CLUSTER_NAME = os.environ['ECS_CLUSTER']
VSCODE_TASK_DEF = os.environ['VSCODE_TASK_DEF']
SUPERSET_TASK_DEF = os.environ['SUPERSET_TASK_DEF']
SUBNETS = os.environ['SUBNETS'].split(',')
SECURITY_GROUP = os.environ['SECURITY_GROUP']
TABLE_NAME = os.environ['DYNAMODB_TABLE']
WARM_POOL_SIZE = int(os.environ.get('WARM_POOL_SIZE', '3'))
IDLE_TIMEOUT = int(os.environ.get('IDLE_TIMEOUT_MINUTES', '30'))

# DynamoDB Table
table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
    """
    Main Lambda handler
    
    Actions:
    - launch: Launch workspace for user
    - monitor: Check and terminate idle workspaces
    - terminate: Manually terminate workspace
    - warm_pool: Maintain warm pool
    """
    action = event.get('action', 'monitor')
    
    print(f"Action: {action}, Event: {json.dumps(event)}")
    
    try:
        if action == 'launch':
            return launch_workspace(event)
        elif action == 'monitor':
            return monitor_workspaces()
        elif action == 'terminate':
            return terminate_workspace(event)
        elif action == 'warm_pool':
            return maintain_warm_pool()
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Unknown action: {action}'})
            }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def launch_workspace(event: Dict) -> Dict:
    """
    Launch workspace container for user
    
    Flow:
    1. Check if user already has running workspace
    2. Try to assign from warm pool
    3. If no warm container, launch on-demand
    4. Return workspace URL
    """
    user_id = event['user_id']
    workspace_type = event.get('workspace_type', 'vscode')  # 'vscode' or 'superset'
    
    print(f"Launching {workspace_type} workspace for user {user_id}")
    
    # Check if user already has running workspace
    existing = get_user_workspace(user_id)
    if existing and existing['status'] == 'running':
        print(f"User {user_id} already has running workspace")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ready',
                'url': existing['url'],
                'task_arn': existing['task_arn'],
                'startup_time': 0
            })
        }
    
    # Try to get warm container
    warm_container = get_warm_container(workspace_type)
    
    if warm_container:
        print(f"Assigning warm container to user {user_id}")
        # Assign warm container to user
        assign_container_to_user(warm_container, user_id)
        
        # Launch replacement warm container
        launch_warm_container(workspace_type)
        
        # Record metrics
        record_metric('WorkspaceLaunchTime', 0, 'Seconds')
        record_metric('WarmPoolHit', 1, 'Count')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ready',
                'url': warm_container['url'],
                'task_arn': warm_container['task_arn'],
                'startup_time': 0,
                'source': 'warm_pool'
            })
        }
    else:
        print(f"No warm container available, launching on-demand")
        # Launch on-demand
        start_time = datetime.now()
        task_arn = launch_ecs_task(user_id, workspace_type)
        
        # Wait for task to be running
        wait_for_task_running(task_arn)
        
        # Get task details
        task_info = get_task_info(task_arn)
        url = get_task_url(task_info, workspace_type)
        
        startup_time = (datetime.now() - start_time).total_seconds()
        
        # Record in DynamoDB
        table.put_item(Item={
            'user_id': user_id,
            'task_arn': task_arn,
            'workspace_type': workspace_type,
            'status': 'running',
            'last_activity': datetime.now().isoformat(),
            'url': url,
            'created_at': datetime.now().isoformat(),
            'ttl': int((datetime.now() + timedelta(days=7)).timestamp())
        })
        
        # Record metrics
        record_metric('WorkspaceLaunchTime', startup_time, 'Seconds')
        record_metric('WarmPoolMiss', 1, 'Count')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'status': 'ready',
                'url': url,
                'task_arn': task_arn,
                'startup_time': startup_time,
                'source': 'on_demand'
            })
        }


def monitor_workspaces() -> Dict:
    """
    Monitor all running workspaces and terminate idle ones
    
    Checks:
    - Last activity timestamp
    - If idle > IDLE_TIMEOUT, terminate
    """
    print("Monitoring workspaces for idle timeout")
    
    # Get all running workspaces
    response = table.scan(
        FilterExpression='#status = :running',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':running': 'running'}
    )
    
    terminated_count = 0
    active_count = 0
    
    for item in response['Items']:
        user_id = item['user_id']
        task_arn = item['task_arn']
        last_activity = datetime.fromisoformat(item['last_activity'])
        idle_time = datetime.now() - last_activity
        
        print(f"User {user_id}: idle for {idle_time.total_seconds() / 60:.1f} minutes")
        
        if idle_time > timedelta(minutes=IDLE_TIMEOUT):
            print(f"Terminating idle workspace for user {user_id}")
            terminate_workspace({'task_arn': task_arn, 'reason': 'idle_timeout'})
            terminated_count += 1
        else:
            active_count += 1
    
    # Maintain warm pool
    maintain_warm_pool()
    
    # Record metrics
    record_metric('ActiveWorkspaces', active_count, 'Count')
    record_metric('TerminatedWorkspaces', terminated_count, 'Count')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'active': active_count,
            'terminated': terminated_count
        })
    }


def terminate_workspace(event: Dict) -> Dict:
    """
    Terminate workspace container
    
    Steps:
    1. Stop ECS task
    2. Update DynamoDB status
    3. Record metrics
    """
    task_arn = event['task_arn']
    reason = event.get('reason', 'manual')
    
    print(f"Terminating workspace: {task_arn}, reason: {reason}")
    
    try:
        # Stop ECS task
        ecs.stop_task(
            cluster=CLUSTER_NAME,
            task=task_arn,
            reason=reason
        )
        
        # Update DynamoDB
        table.update_item(
            Key={'task_arn': task_arn},
            UpdateExpression='SET #status = :stopped, stopped_at = :now',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':stopped': 'stopped',
                ':now': datetime.now().isoformat()
            }
        )
        
        print(f"Workspace terminated: {task_arn}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'status': 'terminated'})
        }
    except Exception as e:
        print(f"Error terminating workspace: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def maintain_warm_pool() -> Dict:
    """
    Maintain warm pool of ready containers
    
    Ensures WARM_POOL_SIZE containers are always ready
    """
    print(f"Maintaining warm pool (target: {WARM_POOL_SIZE})")
    
    # Count current warm containers
    warm_vscode = count_warm_containers('vscode')
    warm_superset = count_warm_containers('superset')
    
    print(f"Current warm pool: vscode={warm_vscode}, superset={warm_superset}")
    
    # Launch missing warm containers
    vscode_needed = max(0, WARM_POOL_SIZE - warm_vscode)
    superset_needed = max(0, WARM_POOL_SIZE - warm_superset)
    
    for _ in range(vscode_needed):
        launch_warm_container('vscode')
    
    for _ in range(superset_needed):
        launch_warm_container('superset')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'vscode_warm': warm_vscode + vscode_needed,
            'superset_warm': warm_superset + superset_needed
        })
    }


# Helper Functions

def launch_ecs_task(user_id: str, workspace_type: str) -> str:
    """Launch ECS Fargate task"""
    task_def = VSCODE_TASK_DEF if workspace_type == 'vscode' else SUPERSET_TASK_DEF
    
    response = ecs.run_task(
        cluster=CLUSTER_NAME,
        taskDefinition=task_def,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': SUBNETS,
                'securityGroups': [SECURITY_GROUP],
                'assignPublicIp': 'DISABLED'
            }
        },
        overrides={
            'containerOverrides': [{
                'name': 'workspace',
                'environment': [
                    {'name': 'USER_ID', 'value': str(user_id)},
                    {'name': 'WORKSPACE_TYPE', 'value': workspace_type}
                ]
            }]
        },
        tags=[
            {'key': 'user_id', 'value': str(user_id)},
            {'key': 'type', 'value': workspace_type},
            {'key': 'managed_by', 'value': 'workspace_manager'}
        ]
    )
    
    return response['tasks'][0]['taskArn']


def launch_warm_container(workspace_type: str) -> str:
    """Launch warm container (not assigned to user)"""
    return launch_ecs_task('warm_pool', workspace_type)


def wait_for_task_running(task_arn: str, timeout: int = 60):
    """Wait for ECS task to reach RUNNING state"""
    import time
    start = time.time()
    
    while time.time() - start < timeout:
        response = ecs.describe_tasks(
            cluster=CLUSTER_NAME,
            tasks=[task_arn]
        )
        
        if response['tasks']:
            status = response['tasks'][0]['lastStatus']
            if status == 'RUNNING':
                return
        
        time.sleep(2)
    
    raise TimeoutError(f"Task {task_arn} did not reach RUNNING state")


def get_task_info(task_arn: str) -> Dict:
    """Get task details"""
    response = ecs.describe_tasks(
        cluster=CLUSTER_NAME,
        tasks=[task_arn]
    )
    return response['tasks'][0]


def get_task_url(task_info: Dict, workspace_type: str) -> str:
    """Get workspace URL from task info"""
    # Get private IP
    for attachment in task_info['attachments']:
        if attachment['type'] == 'ElasticNetworkInterface':
            for detail in attachment['details']:
                if detail['name'] == 'privateIPv4Address':
                    ip = detail['value']
                    port = 8080 if workspace_type == 'vscode' else 8088
                    return f"http://{ip}:{port}"
    
    raise ValueError("Could not determine task URL")


def get_user_workspace(user_id: str) -> Optional[Dict]:
    """Get user's current workspace"""
    response = table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id},
        ScanIndexForward=False,
        Limit=1
    )
    
    if response['Items']:
        return response['Items'][0]
    return None


def get_warm_container(workspace_type: str) -> Optional[Dict]:
    """Get available warm container"""
    response = table.scan(
        FilterExpression='user_id = :warm AND workspace_type = :type AND #status = :running',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':warm': 'warm_pool',
            ':type': workspace_type,
            ':running': 'running'
        },
        Limit=1
    )
    
    if response['Items']:
        return response['Items'][0]
    return None


def count_warm_containers(workspace_type: str) -> int:
    """Count warm containers of given type"""
    response = table.scan(
        FilterExpression='user_id = :warm AND workspace_type = :type AND #status = :running',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':warm': 'warm_pool',
            ':type': workspace_type,
            ':running': 'running'
        },
        Select='COUNT'
    )
    return response['Count']


def assign_container_to_user(container: Dict, user_id: str):
    """Assign warm container to user"""
    table.update_item(
        Key={'task_arn': container['task_arn']},
        UpdateExpression='SET user_id = :uid, last_activity = :now',
        ExpressionAttributeValues={
            ':uid': user_id,
            ':now': datetime.now().isoformat()
        }
    )


def record_metric(metric_name: str, value: float, unit: str):
    """Record CloudWatch metric"""
    try:
        cloudwatch.put_metric_data(
            Namespace='ApraNova/Workspace',
            MetricData=[{
                'MetricName': metric_name,
                'Value': value,
                'Unit': unit,
                'Timestamp': datetime.now()
            }]
        )
    except Exception as e:
        print(f"Error recording metric: {str(e)}")
