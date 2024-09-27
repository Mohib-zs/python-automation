from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'
vm_name = 'prod'
volume_name = 'prod'

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)


# Get latest snapshot for the volume
def get_latest_snapshot():
    snapshots = list(compute_client.snapshots.list_by_resource_group(resource_group_name))
    volume_snapshots = [snap for snap in snapshots if volume_name in snap.name]
    return max(volume_snapshots, key=lambda snap: snap.time_created)

# Create disk from snapshot
def create_disk_from_snapshot(snapshot):
    disk_name = f"{volume_name}-disk-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    disk_config = {
        'location': snapshot.location,
        'creation_data': {'create_option': 'Copy', 'source_resource_id': snapshot.id},
        'sku': {'name': snapshot.sku.name},
    }
    return compute_client.disks.begin_create_or_update(resource_group_name, disk_name, disk_config).result()

# Attach disk to VM
def attach_disk_to_vm(disk):
    vm = compute_client.virtual_machines.get(resource_group_name, vm_name)
    vm.storage_profile.data_disks.append({
        'lun': len(vm.storage_profile.data_disks),                  #Logical unit number
        'name': disk.name,
        'create_option': 'Attach',
        'managed_disk': {'id': disk.id}
    })
    compute_client.virtual_machines.begin_create_or_update(resource_group_name, vm_name, vm).result()

# Main process
if __name__ == "__main__":
    snapshot = get_latest_snapshot()
    disk = create_disk_from_snapshot(snapshot)
    attach_disk_to_vm(disk)
    print(f"Disk {disk.name} created from {snapshot.name} and attached to {vm_name}")