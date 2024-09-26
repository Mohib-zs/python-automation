from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from dotenv import load_dotenv
from datetime import datetime
import os
import schedule
import time

load_dotenv(".env\\.env")  # take environment variables

subscription_id     = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group_name = 'my-app-resources'

# Initialize the Azure credentials and Compute Management Client
credential     = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, subscription_id)

# Function to delete snapshots except the 2 most recent for each volume
def delete_old_snapshots():
    print(f"Starting snapshot cleanup at {datetime.now()}...\n")
    
    # Fetch all snapshots in the resource group
    snapshots = list(compute_client.snapshots.list_by_resource_group(resource_group_name))

    # Group snapshots by volume name (assuming snapshot name format 'volume-snapshot-...')
    volume_snapshots = {}
    for snap in snapshots:
        volume_name = snap.name.split('-snapshot')[0]
        volume_snapshots.setdefault(volume_name, []).append(snap)
    
    # For each volume, keep only the 2 most recent snapshots and delete the rest
    for volume_name, snaps in volume_snapshots.items():
        snaps.sort(key=lambda snap: snap.time_created, reverse=True)
        for snap in snaps[2:]:  # Skip the 2 most recent snapshots
            print(f"Deleting snapshot: {snap.name}")
            compute_client.snapshots.begin_delete(resource_group_name, snap.name)

    print("Snapshot cleanup completed.\n")

# Schedule the job to run daily at 2:00 AM
schedule.every().day.at("02:00").do(delete_old_snapshots)

# Run the scheduler
if __name__ == "__main__":
    print("Starting snapshot cleanup automation...")
    while True:
        schedule.run_pending()
        time.sleep(60)