from pydantic import BaseModel, Field
from typing import Optional

class ContatoPayload(BaseModel):

    phone_number: str = Field(..., description="O número de telefone exato do cliente que interagiu com o bot")

    cliente: Optional[str] = Field(None, description="Nome do cliente (se disponível)")
