from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os
from dotenv import load_dotenv

load_dotenv(".env\\env.env")  # take environment variables

subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

# Authenticate using the default Azure credential (e.g., for CLI or environment variables)
credential = DefaultAzureCredential()

# Create a network management client
network_client = NetworkManagementClient(credential, subscription_id)

# List all virtual networks in the subscription
def list_vnets():
    vnets = network_client.virtual_networks.list_all()

    for vnet in vnets:
        print(f"VNet name: {vnet.name}, Location: {vnet.location}, ID: {vnet.id}")

if __name__ == "__main__":
    list_vnets()


