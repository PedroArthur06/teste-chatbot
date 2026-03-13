from typing import Optional
from sqlmodel import Field, SQLModel, UniqueConstraint

class Empresa(SQLModel, table=True):
    __tablename__ = "empresas"
    
    id_pk: Optional[int] = Field(default=None, primary_key=True)
    cnpj_empresa: str = Field(max_length=50, unique=True, index=True)
    codigo_integracao: str = Field(max_length=100, unique=True, index=True)


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    # Adicionando explicitamente a Constraint de chave única composta
    __table_args__ = (UniqueConstraint("cnpj_empresa", "phone_number", name="unique_cnpj_phone"),)
    
    id_pk: Optional[int] = Field(default=None, primary_key=True)
    cnpj_empresa: str = Field(max_length=50, foreign_key="empresas.cnpj_empresa")
    phone_number: str = Field(max_length=20)
    cliente: str = Field(max_length=100)
