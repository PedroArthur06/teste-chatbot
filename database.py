import databases
from config import settings

# Cria a instância do banco
database = databases.Database(settings.database_url)
