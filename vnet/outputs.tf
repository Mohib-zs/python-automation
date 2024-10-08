output "gateway_ips" {
  value = azurerm_public_ip.nat_gateway_ip.ip_address 
}

output "subnet_ids" {
  value = module.my-app-vnet.vnet_subnets_name_id
}

output "vnet_id" {
  value = module.my-app-vnet.vnet_id
}
