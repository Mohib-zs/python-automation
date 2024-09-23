provider "azurerm" {
  features {}

  subscription_id   = var.subscription_id
}

variable subscription_id {
  type = string
}

variable subnet_address_prefix {}
variable vnet_address_prefix {}
variable env_prefix {}
variable location {}
variable my_ip {}
variable vm_size {}
variable vm_username {}
variable vm_names {}

locals {
  custom_data = <<CUSTOM_DATA
#!/bin/bash
sudo -i
cat << EOF > /etc/customdata.sh
sudo apt update && sudo apt -y upgrade
sudo apt install -y docker.io
sudo systemctl start docker
sudo usermod -aG docker devuser
docker run -p 8080:80 nginx 
EOF
chmod +x /etc/customdata.sh
sudo /etc/customdata.sh
CUSTOM_DATA

  user_data = file("startup-script.sh")
}

data "azurerm_resource_group" "my-app" {
  name     = "${var.env_prefix}-resources"
}

resource "azurerm_virtual_network" "my-app" {
  name                = "${var.env_prefix}-vnet"
  resource_group_name = data.azurerm_resource_group.my-app.name
  location            = var.location
  address_space       = var.vnet_address_prefix
}

resource "azurerm_subnet" "my-app" {
  name                 = "${var.env_prefix}-subnet-1"
  resource_group_name  = data.azurerm_resource_group.my-app.name
  virtual_network_name = azurerm_virtual_network.my-app.name
  address_prefixes     = var.subnet_address_prefix
}

resource "azurerm_network_security_group" "my-app" {
  name                = "${var.env_prefix}-nsg"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.my-app.name

  security_rule {
    name                       = "SSH"
    priority                   = 300
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "${var.my_ip}"
    destination_address_prefix = "*"
  }
  
  security_rule {
    name                       = "web-host"
    priority                   = 320
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8080"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }  

}

resource "azurerm_public_ip" "my-app" {
  for_each            = toset(var.vm_names)
  name                = "${each.value}-public-ip"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.my-app.name
  allocation_method   = "Dynamic"
  sku                 = "Basic"
}

resource "azurerm_network_interface" "my-app" {
  for_each            = toset(var.vm_names)
  name                = "${each.value}-nic"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.my-app.name

  ip_configuration {
    name                          = "${each.value}-ipconfig"
    subnet_id                     = azurerm_subnet.my-app.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.my-app[each.value].id
  }
}

resource "azurerm_network_interface_security_group_association" "my-app" {
  for_each                      = azurerm_network_interface.my-app
  network_interface_id          = each.value.id
  network_security_group_id     = azurerm_network_security_group.my-app.id
}

data "azurerm_ssh_public_key" "my-app" {
  name                = "my-app-key-pair"
  resource_group_name = "${var.env_prefix}-resources"
}

resource "azurerm_linux_virtual_machine" "my-app" {
  for_each              = toset(var.vm_names)
  name                  = each.value
  location              = var.location
  resource_group_name   = data.azurerm_resource_group.my-app.name
  network_interface_ids = [azurerm_network_interface.my-app[each.value].id]
  size                  = var.vm_size
  admin_username        = var.vm_username

  admin_ssh_key {
    username   = var.vm_username
    public_key = data.azurerm_ssh_public_key.my-app.public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}