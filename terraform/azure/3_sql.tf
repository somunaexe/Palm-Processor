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
  sku_name = "GP_S_Gen5_1"   # Serverless Gen5 (example)

  auto_pause_delay_in_minutes = 15
  min_capacity = 0.5
  max_size_gb  = 32
}