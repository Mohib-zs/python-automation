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


# Function to filter 'prod' volumes and create snapshots
def create_snapshots():
    print(f"Starting snapshot creation at {datetime.now()}...")
    
    # List disks in the resource group and filter 'prod' volumes
    volumes = compute_client.disks.list_by_resource_group(resource_group_name)
    prod_volumes = [vol for vol in volumes if 'prod' in vol.name.lower()]
    
    for vol in prod_volumes:
        snapshot_name = f"{vol.name}-snapshot-{datetime.now().strftime('%Y-%m-%d-%H-%M')}"
        snapshot_params = {
            'location': vol.location,
            'creation_data': {
                'create_option': 'Copy',
                'source_uri': vol.id
            },
            'disk_size_gb': vol.disk_size_gb
        }

        # Create the snapshot
        compute_client.snapshots.begin_create_or_update(resource_group_name, snapshot_name, snapshot_params)
        print(f"Snapshot created for {vol.name}: {snapshot_name}")

# Schedule the snapshot job every day at 1:00 AM
schedule.every().day.at("01:00").do(create_snapshots)

# Run the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60)