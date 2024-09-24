# terraform {
#   required_providers {
#     azurerm = {
#       source = "hashicorp/azurerm"
#       version = ">= 4.0.1"
#     }
#   }
# }

provider "azurerm" {
  features {}

  subscription_id   = var.subscription_id
  tenant_id         = var.tenant_id
}

provider "kubernetes" {
  host                   = data.azurerm_kubernetes_cluster.default.kube_config.0.host
  client_certificate     = base64decode(data.azurerm_kubernetes_cluster.default.kube_config.0.client_certificate)
  client_key             = base64decode(data.azurerm_kubernetes_cluster.default.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(data.azurerm_kubernetes_cluster.default.kube_config.0.cluster_ca_certificate)
}


#   dynamic "identity" { 
#   for_each = var.client_id == "" || var.client_secret == "" ? ["identity"] : [] 

#   content { 
#     type         = var.identity_type 
#     identity_ids = var.identity_ids 
#   } 
# }
#  dynamic "service_principal" { 
#   for_each = var.client_id != "" && var.client_secret != "" ? ["service_principal"] : [] 

#   content { 
#     client_id     = var.client_id 
#     client_secret = var.client_secret 
#   } 
# }  
