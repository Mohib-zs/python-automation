from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
from datetime import datetime
import os
import schedule

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

def fetch_vm_status():
    print(f"Fetching VM status at {datetime.now()}...\n")
    
    # List all VMs in the resource group
    vms = compute_client.virtual_machines.list(resource_group_name)
    
    for vm in vms:
        vm_instance = compute_client.virtual_machines.instance_view(resource_group_name, vm.name)
        statuses = vm_instance.statuses
        
        # Get VM power state (running/stopped/etc.)
        power_state = next((status.code.split('/')[-1] for status in vm_instance.statuses if 'PowerState' in status.code), "Unknown")
        
        # Get provisioning state (succeeded/failed/etc.)
        provisioning_state = vm.provisioning_state
        
        print(f"VM Name: {vm.name}")
        print(f"  Power State: {power_state}")
        print(f"  Provisioning State: {provisioning_state}")
        print("-" * 30)

schedule.every(10).seconds.do(fetch_vm_status)
# To check every 6 hours, uncomment the next line
# schedule.every(6).hours.do(fetch_vm_status)

# Run the scheduler
if __name__ == "__main__":
    print("Starting VM status fetch automation...")
    while True:
        schedule.run_pending()