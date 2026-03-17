from fastapi import FastAPI
import os
import csv
from pydantic import BaseModel

app = FastAPI()

# =========================
# CLIENTES
# =========================

clientes_path = 'Clientes.csv'
clientes_id_path = 'clientes_id.txt'


def gerar_id_cliente():
    if not os.path.exists(clientes_id_path):
        with open(clientes_id_path, 'w') as f:
            f.write('0')

    with open(clientes_id_path, 'r') as f:
        ultimo_id = int(f.read())

    novo_id = ultimo_id + 1

    with open(clientes_id_path, 'w') as f:
        f.write(str(novo_id))

    return novo_id


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
    lista = []
    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            lista.append({
                "id": int(row[0]),
                "nome": row[1],
                "sobrenome": row[2],
                "nascimento": row[3],
                "cpf": row[4]
            })
    return lista


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

    data.append([novo_id, cliente.nome, cliente.sobrenome, cliente.nascimento, cliente.cpf])

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
                data.append([cliente.id, cliente.nome, cliente.sobrenome, cliente.nascimento, cliente.cpf])
            else:
                data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(clientes_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Cliente atualizado"}


@app.delete("/clientes/{id}")
def del_cliente(id: int):

    data = [["ID", "NOME", "SOBRENOME", "NASCIMENTO", "CPF"]]
    encontrado = False

    with open(clientes_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:

            # 🔥 ignora linha vazia
            if not row:
                continue

            if row[0] == 'ID':
                continue

            # 🔥 proteção contra erro
            try:
                if int(row[0]) == id:
                    encontrado = True
                    continue
            except:
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
produtos_id_path = 'produtos_id.txt'


def gerar_id_produto():
    if not os.path.exists(produtos_id_path):
        with open(produtos_id_path, 'w') as f:
            f.write('0')

    with open(produtos_id_path, 'r') as f:
        ultimo_id = int(f.read())

    novo_id = ultimo_id + 1

    with open(produtos_id_path, 'w') as f:
        f.write(str(novo_id))

    return novo_id


if not os.path.exists(produtos_path):
    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "NOME", "FORNECEDOR", "QUANTIDADE"])


class Produto(BaseModel):
    id: int
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


@app.put("/produtos")
def update_produto(produto: Produto):

    data = [["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]]
    encontrado = False

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == produto.id:
                encontrado = True
                data.append([produto.id, produto.nome, produto.fornecedor, produto.quantidade])
            else:
                data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(produtos_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Produto atualizado"}


@app.delete("/produtos/{id}")
def del_produto(id: int):

    data = [["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]]
    encontrado = False

    with open(produtos_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == id:
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
ordens_id_path = 'ordens_id.txt'


def gerar_id_ordem():
    if not os.path.exists(ordens_id_path):
        with open(ordens_id_path, 'w') as f:
            f.write('0')

    with open(ordens_id_path, 'r') as f:
        ultimo_id = int(f.read())

    novo_id = ultimo_id + 1

    with open(ordens_id_path, 'w') as f:
        f.write(str(novo_id))

    return novo_id


if not os.path.exists(ordens_path):
    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "CLIENTE", "PRODUTO"])


class Ordem(BaseModel):
    id: int
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


@app.put("/ordens")
def update_ordem(ordem: Ordem):

    data = [["ID", "CLIENTE", "PRODUTO"]]
    encontrado = False

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == ordem.id:
                encontrado = True
                data.append([ordem.id, ordem.cliente_id, ordem.produto_id])
            else:
                data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Ordem atualizada"}


@app.delete("/ordens/{id}")
def del_ordem(id: int):

    data = [["ID", "CLIENTE", "PRODUTO"]]
    encontrado = False

    with open(ordens_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue

            if int(row[0]) == id:
                encontrado = True
                continue

            data.append(row)

    if not encontrado:
        return {"ERRO": "ID não existe"}

    with open(ordens_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {"msg": "Ordem deletada"}