import asyncio
from sqlmodel import select
from models import Empresa, Cliente
from database import get_session

async def checar_banco():
    print("\n" + "="*40)
    print("🔍 VERIFICANDO O BANCO DE DADOS (MYSQL + SQLMODEL)")
    print("="*40)
    
    # Pegamos do generator uma sessão fresca
    async for session in get_session():
        
        # 1. Trazer todas as empresas cadastradas via ORM
        empresas = (await session.execute(select(Empresa))).scalars().all()
        print("\n🏢 EMPRESAS EXISTENTES:")
        if not empresas:
            print("Nenhuma empresa encontrada.")
        for emp in empresas:
            print(f" - ID: {emp.id_pk} | CNPJ: {emp.cnpj_empresa} | Token: {emp.codigo_integracao}")

        # 2. Trazer todos os clientes/contatos cadastrados via ORM
        clientes = (await session.execute(select(Cliente))).scalars().all()
        print("\n👥 CLIENTES/CONTATOS SALVOS:")
        if not clientes:
            print("Nenhum cliente salvo ainda.")
        for cli in clientes:
            print(f" - ID: {cli.id_pk} | Empresa(CNPJ): {cli.cnpj_empresa} | Tel: {cli.phone_number} | Nome: {cli.cliente}")
        
        print("\n" + "="*40 + "\n")
        break # Fura o loop generator pra acabar a execução

if __name__ == "__main__":
    asyncio.run(checar_banco())
