terraform {
  backend "azurerm" {
    resource_group_name     = "my-app-resources"
    storage_account_name    = "tfbackend21fd4466"
    container_name          = "terraform-backend"
    key                     = "terraform.vnet-tfstate"
  }
}