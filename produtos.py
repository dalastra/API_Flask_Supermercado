from fastapi import FastAPI
import os
import csv
from pydantic import BaseModel

app = FastAPI()

file_path = 'Produtos.csv'


if not os.path.exists(file_path):    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')


class produto(BaseModel):
    nome: str
    fornecedor: str
    quantidade: int


def gerar_id():
    ultimo = 0

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if len(row) < 4:
                continue

            ultimo = int(row[0])

    return ultimo + 1


@app.get("/produto")
def produtos():
    Produtos = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if len(row) < 4:
                continue

            Produtos.append({
                "id": int(row[0]),
                "nome": row[1],
                "fornecedor": row[2],
                "quantidade": int(row[3])
            })

    return Produtos


@app.get("/produto/{produto_id}")
def read_produto(produto_id:str):

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if len(row) < 4:
                continue

            if str(row[0]) == str(produto_id):
                return {
                    "id": int(row[0]),
                    "nome": row[1],
                    "fornecedor": row[2],
                    "quantidade": int(row[3])
                }
            
    return {"ERRO":"ID não localizado"}


@app.post("/add_produto")
async def add_produto(produto:produto):

    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]

    novo_id = gerar_id()

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if len(row) < 4:
                continue

            data.append(row)

    novo = [novo_id, produto.nome, produto.fornecedor, produto.quantidade]
    data.append(novo)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {
        "id": novo_id,
        "nome": produto.nome,
        "fornecedor": produto.fornecedor,
        "quantidade": produto.quantidade
    }


@app.delete("/del_produto/{produto_id}")
def del_produto(produto_id:str):
    
    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]
    
    produtos = {}
    produto_deletado = None  

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)
    
    cont = False
    for linha in data:
        if linha[0] == produto_id:
            produto_deletado = linha  
            data.pop(data.index(linha))
            cont = True

    if cont != True:
        return {"ERRO":"ID informado não existe"}        
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    

    return {
        "id": produto_deletado[0],
        "nome": produto_deletado[1],
        "fornecedor": produto_deletado[2],
        "quantidade": produto_deletado[3]
    }


@app.put("/update_produto/{produto_id}")
async def update_produto(produto_id: str, produto: produto):
    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]
    
    produtos = {}

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)
        
    cont = False
    for linha in data:
        if linha[0] == produto_id:
            linha[1] = produto.nome
            linha[2] = produto.fornecedor
            linha[3] = produto.quantidade
            cont = True
    
    if cont != True:
        return {"ERRO":"ID informado não existe"}
        
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                produtos= {
                    "id": row[0],
                    "nome": row[1],
                    "fornecedor": row[2],
                    "quantidade": row[3]
                }

    return produtos