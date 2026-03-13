from fastapi import Header, HTTPException, Depends
from interface.index import ContatoPayload
from database import database

async def extrair_tenant_do_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou mal formatado.")
    
    token = authorization.split("Bearer ")[1]
    
    # Agora busca o CNPJ no banco de dados com base no token recebido
    query = "SELECT cnpj_empresa FROM empresas WHERE codigo_integracao = :token"
    resultado = await database.fetch_one(query=query, values={"token": token})
    
    if not resultado:
        raise HTTPException(status_code=401, detail="Token inválido. Empresa não encontrada com este código.")
    
    return resultado["cnpj_empresa"]

async def processar_contato_service(payload: ContatoPayload, cnpj_empresa: str):

    query = """
        INSERT INTO clientes (cnpj_empresa, phone_number, cliente)
        VALUES (:cnpj, :telefone, :nome)
        ON DUPLICATE KEY UPDATE cliente = VALUES(cliente);
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar no banco: {str(e)}")