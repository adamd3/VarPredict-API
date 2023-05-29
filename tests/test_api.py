import boto3
import pytest
import requests

@pytest.fixture
def file_path():
    return "./model_data/sample_genotypes.tsv"

def test_predict_gene_expression(file_path):
    endpoint = get_api_endpoint()
    url = f"http://{endpoint}:80/predict/"  
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    response_json = response.json()

    assert response.status_code == 200

    print(response_json)

def get_api_endpoint():
    ecs_client = boto3.client('ecs')
    ec2_client = boto3.client('ec2')

    response = ecs_client.list_tasks(
        cluster='varpredict',
        serviceName='varpredict'
    )

    task_arn = response['taskArns'][0]

    response = ecs_client.describe_tasks(
        cluster='varpredict',
        tasks=[task_arn]
    )

    eni_id = response['tasks'][0]['attachments'][0]['details'][1]['value']

    response = ec2_client.describe_network_interfaces(
        NetworkInterfaceIds=[eni_id]
    )

    public_ip = response['NetworkInterfaces'][0]['Association']['PublicIp']

    return public_ip

if __name__ == "__main__":
    test_predict_gene_expression()