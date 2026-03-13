import databases

DATABASE_URL = "mysql+aiomysql://myuser:mypassword@localhost:3306/telenova"

database = databases.Database(DATABASE_URL)
