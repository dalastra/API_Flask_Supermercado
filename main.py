from fastapi import FastAPI
import os
import csv
from pydantic import BaseModel

app = FastAPI()

# =========================
# CLIENTES
# =========================

clientes_path = 'Clientes.csv'


def gerar_id_cliente():
    ids = []

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            ids.append(int(row[0]))

    if len(ids) == 0:
        return 1

    return max(ids) + 1


def cpf_existe(cpf):
    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "ID":
                continue
            if row[4] == cpf:
                return True
    return False


if not os.path.exists(clientes_path):
    with open(clientes_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"])


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

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue

            Clientes[row[0]] = {
                "nome": row[1],
                "sobrenome": row[2],
                "nascimento": row[3],
                "cpf": row[4]
            }

    return Clientes


@app.post("/clientes")
def add_cliente(cliente: ClienteCriar):

    if len(cliente.cpf) != 11:
        return {"ERRO": "CPF deve ter 11 dígitos"}

    if cpf_existe(cliente.cpf):
        return {"ERRO": "CPF já cadastrado"}

    data = [["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]]

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != 'ID':
                data.append(row)

    novo_id = gerar_id_cliente()

    data.append([
        novo_id,
        cliente.nome,
        cliente.sobrenome,
        cliente.nascimento,
        cliente.cpf
    ])

    with open(clientes_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Cliente adicionado", "id": novo_id}


@app.put("/clientes")
def atualizar_cliente(cliente: ClienteAtualizar):

    data = [["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]]
    encontrado = False

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == cliente.id:
                encontrado = True
                data.append([
                    cliente.id,
                    cliente.nome,
                    cliente.sobrenome,
                    cliente.nascimento,
                    cliente.cpf
                ])
            else:
                data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(clientes_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Cliente atualizado"}


@app.delete("/clientes/{id}")
def del_cliente(id: str):

    data = [["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]]
    encontrado = False

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if row[0] == id:
                encontrado = True
                continue

            data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(clientes_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Cliente deletado"}


# =========================
# PRODUTOS
# =========================

produtos_path = 'Produtos.csv'


def gerar_id_produto():
    ids = []

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            ids.append(int(row[0]))

    if len(ids) == 0:
        return 1

    return max(ids) + 1


if not os.path.exists(produtos_path):
    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "NOME", "FORNECEDOR", "QUANTIDADE"])


class Produto(BaseModel):
    nome: str
    fornecedor: str
    quantidade: int


@app.get("/produtos")
def produtos():
    lista = []

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            lista.append({
                "id": int(row[0]),
                "nome": row[1],
                "fornecedor": row[2],
                "quantidade": int(row[3])
            })

    return lista


@app.post("/produtos")
def add_produto(produto: Produto):

    data = [["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]]

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != 'ID':
                data.append(row)

    novo_id = gerar_id_produto()

    data.append([novo_id, produto.nome, produto.fornecedor, produto.quantidade])

    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Produto criado", "id": novo_id}


@app.put("/produtos/{id}")
def update_produto(id: int, produto: Produto):

    data = [["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]]
    encontrado = False

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == id:
                encontrado = True
                data.append([id, produto.nome, produto.fornecedor, produto.quantidade])
            else:
                data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Produto atualizado"}


@app.delete("/produtos/{id}")
def del_produto(id: str):

    data = [["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]]
    encontrado = False

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if row[0] == id:
                encontrado = True
                continue

            data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Produto deletado"}


# =========================
# ORDENS
# =========================

ordens_path = 'OrdemDeVendas.csv'


def gerar_id_ordem():
    ids = []

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            ids.append(int(row[0]))

    if len(ids) == 0:
        return 1

    return max(ids) + 1


if not os.path.exists(ordens_path):
    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "CLIENTE", "PRODUTO"])


class Ordem(BaseModel):
    cliente_id: int
    produto_id: int


@app.get("/ordens")
def ordens():
    lista = []

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            lista.append({
                "id": int(row[0]),
                "cliente_id": int(row[1]),
                "produto_id": int(row[2])
            })

    return lista


@app.post("/ordens")
def add_ordem(ordem: Ordem):

    data = [["ID", "CLIENTE", "PRODUTO"]]

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != 'ID':
                data.append(row)

    novo_id = gerar_id_ordem()

    data.append([novo_id, ordem.cliente_id, ordem.produto_id])

    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Ordem criada", "id": novo_id}

@app.put("/ordens/{id}")
def update_ordem(id: int, ordem: Ordem):
    
    data = [["ID", "CLIENTE", "PRODUTO"]]
    encontrado = False

    # Lê o CSV
    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            # Se encontrou o ID → atualiza
            if int(row[0]) == id:
                encontrado = True
                data.append([id, ordem.cliente_id, ordem.produto_id])
            else:
                data.append(row)

    # Se não encontrou o ID
    if not encontrado:
        return {"ERRO": "ID não existe"}

    # Reescreve o CSV
    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Ordem atualizada"}

@app.delete("/ordens/{id}")
def del_ordem(id: str):

    data = [["ID", "CLIENTE", "PRODUTO"]]
    encontrado = False

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if row[0] == id:
                encontrado = True
                continue

            data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Ordem deletada"}