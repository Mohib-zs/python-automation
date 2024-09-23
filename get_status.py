from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
import os
import time

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

# List all VMs in the resource group
vm_list = compute_client.virtual_machines.list(resource_group_name)


def get_vm_status(vm_name):
    instance_view = compute_client.virtual_machines.instance_view(resource_group_name, vm_name)
    statuses = instance_view.statuses

    vm_status = "Unknown"
    vm_state  = "Unknown"

    for status in statuses:
        if 'PowerState' in status.code:
            vm_status = status.display_status
        if 'ProvisioningState' in status.code or "HealthState" in status.code:
            vm_state = status.display_status

    return vm_status, vm_state


# Function to continuously check the status of VMs
def monitor_vms(interval=60):
    while True:
        print(f"Checking VM status in resource group: {resource_group_name}")
        for vm in compute_client.virtual_machines.list(resource_group_name):
            vm_name = vm.name
            vm_status, vm_state = get_vm_status(vm_name)
            print(f"VM: {vm_name}, Status: {vm_status}, State: {vm_state}")
        
        print("-" * 40)
        time.sleep(interval)  # Wait for the specified interval (in seconds)

# Start monitoring with an interval of 5 minutes (300 seconds)
monitor_vms(interval=30)