resource "azurerm_mssql_server" "sqlserver" {
  name                         = "palmpro-sql-server"
  resource_group_name          = azurerm_resource_group.rg.name
  location                     = azurerm_resource_group.rg.location
  version                      = "12.0"

  administrator_login          = "palmsqladmin"
  administrator_login_password  = "Palm674201!"
}

resource "azurerm_mssql_database" "db" {
  name      = "palmprodb"
  server_id = azurerm_mssql_server.sqlserver.id
}