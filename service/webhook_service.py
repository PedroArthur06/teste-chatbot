from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import ContatoPayload
from database import database
import pymysql

security = HTTPBearer()

async def extrair_tenant_do_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    
    # Agora busca o CNPJ no banco de dados com base no token recebido
    query = "SELECT cnpj_empresa FROM empresas WHERE codigo_integracao = :token"
    resultado = await database.fetch_one(query=query, values={"token": token})
    
    if not resultado:
        raise HTTPException(status_code=401, detail="Token inválido. Empresa não encontrada com este código.")
    
    return resultado["cnpj_empresa"]

async def processar_contato_service(payload: ContatoPayload, cnpj_empresa: str):

    query = """
        INSERT INTO clientes (cnpj_empresa, phone_number, cliente)
        VALUES (:cnpj, :telefone, :nome) AS new_data
        ON DUPLICATE KEY UPDATE cliente = new_data.cliente;
    """
    
    nome = payload.cliente if payload.cliente else "Desconhecido"
    
    try:
        await database.execute(
            query=query, 
            values={"cnpj": cnpj_empresa, "telefone": payload.phone_number, "nome": nome}
        )
        return {
            "status": "sucesso", 
            "mensagem": f"Contato {payload.phone_number} salvo para a empresa {cnpj_empresa}."
        }
    except pymysql.err.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Erro de integridade referencial: {str(e)}")
    except pymysql.err.OperationalError as e:
        raise HTTPException(status_code=503, detail=f"Erro operacional do banco de dados (ex: desconexão): {str(e)}")
    except pymysql.err.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")