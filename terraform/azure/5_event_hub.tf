resource "azurerm_eventhub_namespace" "ns" {
  name                = "palmpro-eh-namespace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  capacity            = 1
}

resource "azurerm_eventhub" "hub" {
  name                = "sensor-stream"
  namespace_id        = azurerm_eventhub_namespace.ns.id
  # resource_group_name = azurerm_resource_group.rg.name

  partition_count   = 2
  message_retention = 1
}