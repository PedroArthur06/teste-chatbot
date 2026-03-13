from fastapi import APIRouter, Depends
from interface.index import ContatoPayload
from service.webhook_service import extrair_tenant_do_token, processar_contato_service

router = APIRouter(prefix="/webhooks/n8n", tags=["Webhooks"])

@router.post("/contatos")
async def receber_contato(
    payload: ContatoPayload, 
    cnpj_empresa: str = Depends(extrair_tenant_do_token)
):
    return await processar_contato_service(payload, cnpj_empresa)
