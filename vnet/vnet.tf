module "my-app-vnet" {
  source  = "Azure/vnet/azurerm"
  version = "4.1.0"

  resource_group_name          = var.resource_group_name
  vnet_name                    = var.vnet_name
  use_for_each                 = true 
  vnet_location                = var.location
  address_space                = var.address_space
  subnet_prefixes              = var.subnet_prefixes
  subnet_names                 = var.subnet_names
}

# NAT Gateway configuration
resource "azurerm_public_ip" "nat_gateway_ip" {
  name                  = "nat-gateway-ip"
  location              = var.location
  resource_group_name   = var.resource_group_name
  allocation_method     = "Static"
  sku                   = "Standard"
}

resource "azurerm_nat_gateway" "nat_gateway" {
  name                    = "my-nat-gateway"
  location                = var.location
  resource_group_name     = var.resource_group_name
  sku_name                = "Standard"
  idle_timeout_in_minutes = 10
}

resource "azurerm_nat_gateway_public_ip_association" "nat_gateway_ip_association" {
  nat_gateway_id        = azurerm_nat_gateway.nat_gateway.id 
  public_ip_address_id  = azurerm_public_ip.nat_gateway_ip.id 
}

resource "azurerm_subnet_nat_gateway_association" "subnet_nat_associations" {
  for_each = toset(["private-subnet-1", "private-subnet-2", "private-subnet-3"])

  subnet_id       = module.my-app-vnet.vnet_subnets_name_id[each.key]
  nat_gateway_id  = azurerm_nat_gateway.nat_gateway.id 
}
# resource "azurerm_route_table" "route_table" {
#   name                = "my-route-table"
#   location            = var.location
#   resource_group_name = var.resource_group_name
# }

# # Add routes to the route table
# resource "azurerm_route" "route" {
#   name                   = "my-route"
#   resource_group_name     = var.resource_group_name
#   route_table_name        = azurerm_route_table.route_table.name
#   address_prefix          = "0.0.0.0/0"                # Destination address range
#   next_hop_type           = "Internet"                 # Can be Internet, VirtualAppliance, etc.
#   next_hop_in_ip_address  = null                       # Only needed for VirtualAppliance
# }

# # Associate the route table with a subnet
# resource "azurerm_subnet_route_table_association" "subnet_route_table_association" {
#   for_each = toset(["private-subnet-1", "private-subnet-2", "private-subnet-3"])

#   subnet_id      = module.my-app-vnet.vnet_subnets_name_id[each.key]
#   route_table_id = azurerm_route_table.route_table.id
# }
