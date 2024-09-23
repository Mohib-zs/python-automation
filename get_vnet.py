from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import os
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')

# Authenticate using the default Azure credential (e.g., for CLI or environment variables)
credential = DefaultAzureCredential()

# Create a network management client
network_client = NetworkManagementClient(credential, subscription_id)

# List all virtual networks in the subscription
def list_vnets():
    vnets = network_client.virtual_networks.list_all()

    for vnet in vnets:
        print(f"VNet name: {vnet.name}, Location: {vnet.location}, VNet address prefix: {vnet.address_space.address_prefixes}")

        resource_group_name = vnet.id.split('/')[4]

        subnets = network_client.subnets.list(resource_group_name, vnet.name)

        for subnet in subnets:
            print(f"Subnet name: {subnet.name}, Subnet address prefix: {subnet.address_prefix}")
            

if __name__ == "__main__":                  #Make's sure that the module(file) can only be executed directly and not anywhere else via import 
    list_vnets()


