# Backend Storage Script for Terraform State File

$resource_group_name    = 'my-app-resources'
$location               = 'centralus'
$storage_account_name   = 'tfbackend21fd4466'
$storage_container_name = 'terraform-backend'
$aks_cluster_name       = 'my-app-aks'

az group create --name $resource_group_name --location $location       #Create a rg (Skip if you've already configured one (Ensure the existing rg location matches the other resources))
az storage account create --resource-group $resource_group_name --name $storage_account_name --sku Standard_LRS        #Create a storage account
az storage account blob-service-properties update --account-name $storage_account_name --resource-group $resource_group_name --enable-versioning       #Enable Blob Versioning
az storage container create --name $storage_container_name --account-name $storage_account_name --auth-mode login            #Create a blob container
# az aks show --resource-group $resourceGroupName --name $aksClusterName --query identity

