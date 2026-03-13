import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app

BASE_URL = "http://test"
pytestmark = pytest.mark.asyncio

async def test_inserir_cliente_novo_empresa_1():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer token_teste_123"},
            json={
                "phone_number": "5511000000000",
                "cliente": "Cliente Teste Automatizado 1"
            }
        )
        
    assert response.status_code == 200
    dados = response.json()
    assert dados["status"] == "sucesso"

async def test_inserir_cliente_duplicado_empresa_1():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer token_teste_123"},
            json={"phone_number": "5511000000000", "cliente": "Cliente Teste Automatizado 1"}
        )
        response = await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer token_teste_123"},
            json={"phone_number": "5511000000000", "cliente": "Cliente Teste Automatizado 1 EDITADO"}
        )
        
    assert response.status_code == 200
    assert response.json()["status"] == "sucesso"

async def test_inserir_mesmo_numero_outra_empresa():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer token_teste_123"},
            json={"phone_number": "5599777777777", "cliente": "João na Empresa 1"}
        )
        response_empresa_2 = await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer token_empresa_2"},
            json={"phone_number": "5599777777777", "cliente": "João na Empresa 2"}
        )
        
    assert response_empresa_2.status_code == 200
    assert response_empresa_2.json()["status"] == "sucesso"

async def test_token_invalido_deve_falhar():
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as client:
        response = await client.post(
            "/webhooks/n8n/contatos",
            headers={"Authorization": "Bearer TOKEN_FALSO_INVENTADO"},
            json={"phone_number": "5511999999999", "cliente": "Invasor"}
        )
        
    assert response.status_code == 401
