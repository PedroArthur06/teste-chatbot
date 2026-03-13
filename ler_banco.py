import asyncio
from database import database
import json

async def checar_banco():
    # Conecta ao banco de dados MySQL
    await database.connect()
    
    print("\n" + "="*40)
    print("🔍 VERIFICANDO O BANCO DE DADOS (MYSQL)")
    print("="*40)
    
    # 1. Trazer todas as empresas cadastradas
    empresas = await database.fetch_all("SELECT * FROM empresas")
    print("\n🏢 EMPRESAS EXISTENTES:")
    if not empresas:
        print("Nenhuma empresa encontrada.")
    for emp in empresas:
        print(f" - ID: {emp['id_pk']} | CNPJ: {emp['cnpj_empresa']} | Token: {emp['codigo_integracao']}")

    # 2. Trazer todos os clientes/contatos cadastrados
    clientes = await database.fetch_all("SELECT * FROM clientes")
    print("\n👥 CLIENTES/CONTATOS SALVOS:")
    if not clientes:
        print("Nenhum cliente salvo ainda.")
    for cli in clientes:
        print(f" - ID: {cli['id_pk']} | Empresa(CNPJ): {cli['cnpj_empresa']} | Tel: {cli['phone_number']} | Nome: {cli['cliente']}")
    print("\n" + "="*40 + "\n")
    
    await database.disconnect()

if __name__ == "__main__":
    # Roda a função assíncrona
    asyncio.run(checar_banco())


# ./venv/bin/python ler_banco.py
