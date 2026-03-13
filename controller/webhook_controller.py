from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ContatoPayload, ContatoUpdatePayload
from service.webhook_service import extrair_tenant_do_token, processar_contato_service, Atualiza_contato
from database import get_session

router = APIRouter(prefix="/webhooks/n8n", tags=["Webhooks"])

@router.post("/contatos")
async def receber_contato(
    payload: ContatoPayload, 
    cnpj_empresa: str = Depends(extrair_tenant_do_token),
    session: AsyncSession = Depends(get_session)
):
    return await processar_contato_service(payload, cnpj_empresa, session)

@router.patch("/contato/{phone_number}")
async def atualiza_dado(
    phone_number: str, 
    payload: ContatoUpdatePayload, 
    cnpj_empresa: str = Depends(extrair_tenant_do_token),
    session: AsyncSession = Depends(get_session)
):
    return await Atualiza_contato(phone_number, payload, cnpj_empresa, session)
