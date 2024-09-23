from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

action = input("Enter 'start' to start all VMs or 'stop' to deallocate all VMs: ").lower()

# List all VMs in the resource group
vm_list = compute_client.virtual_machines.list(resource_group_name)

if action == 'start':
    # Start all VMs in the resource group
    for vm in vm_list:
        vm_name = vm.name
        print(f"Starting VM: {vm_name}")
        async_vm_start = compute_client.virtual_machines.begin_start(resource_group_name, vm_name)
        async_vm_start.result()  # Wait for the operation to complete
    print("All VMs in the resource group have been started.")

elif action == 'stop':
    # Deallocate all VMs in the resource group
    for vm in vm_list:
        vm_name = vm.name
        print(f"Deallocating VM: {vm_name}")
        async_vm_deallocate = compute_client.virtual_machines.begin_deallocate(resource_group_name, vm_name)
        async_vm_deallocate.result()  # Wait for the operation to complete
    print("All VMs in the resource group have been deallocated.")

else:
    print("Invalid input! Please enter either 'start' or 'stop'.")