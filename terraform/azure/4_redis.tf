# resource "azurerm_managed_redis" "cache" {
#   name                = "palmpro-redis"
#   location            = azurerm_resource_group.rg.location
#   resource_group_name = azurerm_resource_group.rg.name
#   sku_name            = "Balanced_B0"

#   default_database {}
# }