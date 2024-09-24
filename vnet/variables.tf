variable subscription_id {
    type        = string
    sensitive   = true
}
variable tenant_id {
    type        = string
    sensitive   = true
}
# variable service_principal_name {
#   type        = string
#   description = "Name of the service principal"
# }

# variable client_id {
#     description = "Client ID of the service principal"
#     type        = string
# }
# variable client_secret {
#     description = "Client secret of the service principal"
#     type        = string
#     sensitive   = true
# }
# variable rbac_aad_admin_group_object_ids {
#     type        = list(string)
#     sensitive   = true
# }
variable resource_group_name {}
variable vnet_name {}
variable location {}
variable address_space {}
variable subnet_names {}
variable subnet_prefixes {}
variable storage_account_name {}
