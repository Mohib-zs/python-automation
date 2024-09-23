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

public_ip_addresses = network_client.public_ip_addresses.list("my-app-resources")
for ip in public_ip_addresses:
    print(f"Name: {ip.name}, IP Address: {ip.ip_address}")