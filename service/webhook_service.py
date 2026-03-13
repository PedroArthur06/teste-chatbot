from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from schemas import ContatoPayload, ContatoUpdatePayload
from database import get_session
from models import Empresa, Cliente
import pymysql
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

security = HTTPBearer()

# Pega o ID no banco de dados com base no token recebido usando SQLModel
async def extrair_tenant_do_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
):
    token = credentials.credentials
    
    # Busca com SQLModel/SQLAlchemy
    statement = select(Empresa).where(Empresa.codigo_integracao == token)
    result = await session.execute(statement)
    empresa = result.scalars().first()
    
    if not empresa:
        raise HTTPException(status_code=401, detail="Token inválido. Empresa não encontrada com este código.")
    
    return empresa.cnpj_empresa

# Insere ou atualiza o contato no banco de dados usando ORM
async def processar_contato_service(
    payload: ContatoPayload, 
    cnpj_empresa: str,
    session: AsyncSession
):
    nome = payload.cliente if payload.cliente else "Desconhecido"
    telefone = payload.phone_number
    
    try:
        # Tenta buscar se o cliente já existe para essa empresa e telefone
        statement = select(Cliente).where(Cliente.phone_number == telefone).where(Cliente.cnpj_empresa == cnpj_empresa)
        result = await session.execute(statement)
        cliente = result.scalars().first()
        
        if cliente:
            # Upsert - Atualiza o nome existente
            cliente.cliente = nome
        else:
            # Upsert - Cria um novo
            cliente = Cliente(cnpj_empresa=cnpj_empresa, phone_number=telefone, cliente=nome)
            session.add(cliente)
            
        await session.commit()
        await session.refresh(cliente)
        
        return {
            "status": "sucesso", 
            "mensagem": f"Contato {telefone} processado para a empresa {cnpj_empresa} com ID {cliente.id_pk}."
        }
        
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro de integridade referencial: {str(e.orig)}")
    except OperationalError as e:
        await session.rollback()
        raise HTTPException(status_code=503, detail=f"Erro operacional do banco de dados (ex: desconexão): {str(e.orig)}")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")

# Atualiza algum dado do cliente
async def Atualiza_contato(
    phone_number: str, 
    payload: ContatoUpdatePayload, 
    cnpj_empresa: str,
    session: AsyncSession
):
    try:
        statement = select(Cliente).where(Cliente.phone_number == phone_number).where(Cliente.cnpj_empresa == cnpj_empresa)
        result = await session.execute(statement)
        cliente = result.scalars().first()
        
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado para esta empresa e telefone.")
            
        cliente.cliente = payload.cliente
        await session.commit()
        
        return {
            "status": "sucesso", 
            "mensagem": f"Contato {phone_number} atualizado para a empresa {cnpj_empresa}."
        }
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Errointerno: {str(e)}")