from fastapi import FastAPI
import os
import csv
from pydantic import BaseModel

app = FastAPI()

file_path = 'Clientes.csv'

def gerar_id():  #gera o id automaticamente
    ids = []

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            ids.append(int(row[0]))

    if len(ids) == 0:
        return 1
    
    return max(ids) + 1

def cpf_existe(cpf):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "ID":
                continue
            if row[4] == cpf:
                return True
    return False



if not os.path.exists(file_path):    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')


class ClienteCriar(BaseModel):
    nome: str
    sobrenome: str
    nascimento: str
    cpf: str

class ClienteAtualizar(BaseModel):
    id: int
    nome: str
    sobrenome: str
    nascimento: str
    cpf: str


@app.get("/clientes")
def clientes():
    Clientes = {}
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                Clientes[row[0]] = {
                "nome": row[1],
                "sobrenome": row[2],
                "nascimento": row[3],
                "cpf": row[4]
            }
    return Clientes


@app.post("/clientes")
async def add_cliente(cliente: ClienteCriar):

    if len(cliente.cpf) != 11:
        return {"ERRO": "CPF deve ter 11 dígitos"}

    if cpf_existe(cliente.cpf):
        return {"ERRO": "CPF já cadastrado"}

    data = [
        ["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]
    ]

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            data.append(row)

    novo_id = gerar_id()

    novo = [
        novo_id,
        cliente.nome,
        cliente.sobrenome,
        cliente.nascimento,
        cliente.cpf
    ]

    data.append(novo)

    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Cliente adicionado", "id": novo_id}


@app.put("/clientes")
def atualizar_cliente(cliente: ClienteAtualizar):

    Clientes = {}

    # Ler o CSV e montar o dicionário
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == "ID":
                continue

            Clientes[row[0]] = {
                "nome": row[1],
                "sobrenome": row[2],
                "nascimento": row[3],
                "cpf": row[4]
            }

    # Verificar se o cliente existe
    if str(cliente.id) not in Clientes:
        return {"ERRO": "ID informado não existe"}

    # Atualizar os dados no dicionário
    Clientes[str(cliente.id)] = {
        "nome": cliente.nome,
        "sobrenome": cliente.sobrenome,
        "nascimento": cliente.nascimento,
        "cpf": cliente.cpf
    }

    # Reescrever o CSV
    data = [["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]]

    for id_cliente, dados in Clientes.items():
        data.append([
            id_cliente,
            dados["nome"],
            dados["sobrenome"],
            dados["nascimento"],
            dados["cpf"]
        ])

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return Clientes


@app.delete("/clientes/{id}")
def del_cliente(id:str):
    data = [
        ["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]
    ]
    
    Clientes = {}

    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)
    
    cont = False
    for linha in data:
        if linha[0] == id:
            data.pop(data.index(linha))
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
                Clientes[row[0]] = {
                "nome": row[1],
                "sobrenome": row[2],
                "nascimento": row[3],
                "cpf": row[4]
                }

    return Clientes