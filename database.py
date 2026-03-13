from config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = settings.database_url

# Cria a engine de forma assíncrona 
engine = create_async_engine(DATABASE_URL, echo=False)

# Função injeção de dependência para pegar sempre uma sessão de banco de dados limpa
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
