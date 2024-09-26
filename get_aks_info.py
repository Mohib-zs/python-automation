from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from dotenv import load_dotenv
import os

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'

def list_aks_clusters(subscription_id):
    # Authenticate using DefaultAzureCredential
    credential = DefaultAzureCredential()

    # Create a ContainerServiceClient
    client = ContainerServiceClient(credential, subscription_id)

    # List AKS clusters
    aks_clusters = client.managed_clusters.list()

    # Print details of each AKS cluster
    for cluster in aks_clusters:
        # Extract the resource group from the cluster's resource ID
        resource_group = cluster.id.split("/")[4]

        # Get the desired properties
        name = cluster.name
        location = cluster.location
        status = cluster.provisioning_state
        state = cluster.power_state.code
        endpoint = cluster.fqdn                         #Also known as API server
        kubernetes_version = cluster.kubernetes_version

        # Print cluster details
        print(f"Name: {name}")
        print(f"Resource Group: {resource_group}")
        print(f"Location: {location}")
        print(f"Status: {status}")
        print(f"State: {state}")
        print(f"Endpoint: {endpoint}")
        print(f"Kubernetes Version: {kubernetes_version}")
        print("-" * 60)

if __name__ == "__main__":
    
    list_aks_clusters(subscription_id)