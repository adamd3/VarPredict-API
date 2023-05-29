import boto3
import os

execution_role_arn = os.environ['AWS_EXECUTION_ROLE_ARN']
subnet_id = os.environ['AWS_SUBNET_ID']
security_group_id = os.environ['AWS_SECURITY_GROUP_ID']

ecs_client = boto3.client('ecs')

cluster_name = 'varpredict'
response = ecs_client.create_cluster(clusterName=cluster_name)
cluster_arn = response['cluster']['clusterArn']
print(f"Cluster ARN: {cluster_arn}")

task_definition = {
    'family': 'varpredict',
    'executionRoleArn': execution_role_arn,
    'cpu': '256',
    'memory': '512',
    'networkMode': 'awsvpc',
    'requiresCompatibilities': ['FARGATE'],
    'containerDefinitions': [
        {
            'name': 'varpredict',
            'image': 'varpredict:latest',
            'portMappings': [
                {
                    'containerPort': 80,
                    'protocol': 'tcp'
                }
            ],
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': 'varpredict',
                    'awslogs-region': 'eu-north-1',
                    'awslogs-stream-prefix': 'varpredict'
                }
            }
        }
    ]
}
response = ecs_client.register_task_definition(**task_definition)
task_definition_arn = response['taskDefinition']['taskDefinitionArn']
print(f"Task Definition ARN: {task_definition_arn}")

service_name = 'varpredict'
desired_count = 1
launch_type = 'FARGATE'
subnet_ids = [subnet_id]
security_group_ids = [security_group_id]

try:
    response = ecs_client.create_service(
        cluster=cluster_name,
        serviceName=service_name,
        taskDefinition=task_definition_arn,
        desiredCount=desired_count,
        launchType=launch_type,
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': subnet_ids,
                'securityGroups': security_group_ids,
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    service_arn = response['service']['serviceArn']
    print(f"Service ARN: {service_arn}")
except ecs_client.exceptions.ServiceAlreadyExistsException:
    print(f"The service '{service_name}' exists.")
