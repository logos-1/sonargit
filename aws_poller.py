import boto3
import time

def check_instance_status(instance_id):
    ec2_client = boto3.client('ec2', region_name='us-east-1')

    # Noncompliant: Custom polling loop instead of using a waiter
    while True:
        response = ec2_client.describe_instance_status(
            InstanceIds=[instance_id],
            IncludeAllInstances=True
        )

        if not response['Statuses']:
             time.sleep(10)
             continue

        instance_status = response['Statuses'][0]['InstanceStatus']['Status']
        if instance_status == 'ok':
            break

        time.sleep(10)
