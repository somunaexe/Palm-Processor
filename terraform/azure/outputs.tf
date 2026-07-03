output "resource_group" {
  value = azurerm_resource_group.rg.name
}

output "storage_account" {
  value = azurerm_storage_account.data_lake.name
}

output "sql_server" {
  value = azurerm_mssql_server.sqlserver.name
}

# output "redis_host" {
#   value = azurerm_managed_redis.cache.hostname
# }

output "eventhub_namespace" {
  value = azurerm_eventhub_namespace.ns.name
}