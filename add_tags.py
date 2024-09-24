from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import os
from dotenv import load_dotenv

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'VmResources'
tag_key             = 'environment'
tag_value           = 'prod'

# Initialize Azure client
credential      = DefaultAzureCredential()
compute_client  = ComputeManagementClient(credential, subscription_id)

# Function to add tags to VMs in a resource group
def add_tags_to_vms(resource_group_name, tag_key, tag_value):
    # List all VMs in the specified resource group
    vms = compute_client.virtual_machines.list(resource_group_name)

    for vm in vms:
        # Get current tags, if any
        current_tags = vm.tags if vm.tags else {}

        # Add or update the tag
        current_tags[tag_key] = tag_value

        # Update the VM with the new tags
        print(f"Updating tags for VM: {vm.name}")
        compute_client.virtual_machines.begin_create_or_update(
            resource_group_name=resource_group_name,
            vm_name=vm.name,
            parameters={
                'location': vm.location,
                'tags': current_tags
            }
        ).result()  # Wait for the operation to complete
        print(f"Tags updated for {vm.name}: {current_tags}")

# Add tags to all VMs in the specified resource group
add_tags_to_vms(resource_group_name, tag_key, tag_value)