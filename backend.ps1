# Backend Storage Script for Terraform State File

$resourceGroupName  = 'my-app-resources'
$location           = 'centralus'
$accountName        = 'tfbackend21fd4466'
$storageAccountName = 'terraform-backend'
$aksClusterName     = 'my-app-aks'

az group create --name $resourceGroupName --location $location       #Create a rg (Skip if you've already configured one (Ensure the existing rg location matches the other resources))
az storage account create --resource-group $resourceGroupName --name $accountName --sku Standard_LRS        #Create a storage account
az storage account blob-service-properties update --account-name $accountName --resource-group $resourceGroupName --enable-versioning       #Enable Blob Versioning
az storage container create --name $storageAccountName --account-name $accountName --auth-mode login            #Create a blob container
# az aks show --resource-group $resourceGroupName --name $aksClusterName --query identity

