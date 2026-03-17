# API SUPERMERCADO
# Sistema de Produtos — API FastAPI com CSV

Este projeto é uma API simples construída com *FastAPI*, utilizando um arquivo *CSV* como banco de dados para armazenar produtos.

A API permite:

- Criar produtos  
- Listar produtos  
- Buscar produto por ID  
- Atualizar produto  
- Deletar produto
- ID (único)
- Nome
- Sobrenome
- Data de nascimento (AAAA-MM-DD)
- CPF (único)
- ID da Ordem (único)
- Cliente (ID do cliente)
- Produto (ID do produto) 

---

## Tecnologias Utilizadas

- Python 3.x  
- FastAPI  
- CSV como armazenamento
- Postman
- Virtual Studio Code

---

## Estrutura do Arquivo CSV

O arquivo arquivo.csv é criado automaticamente caso não exista.

Ele segue o formato para clientes:

| ID | NOME | SOBRENOME | DATA DE NASCIMENTO | CPF |
|----|------|-----------|--------------------|-----|

---

Ele segue o formato para produtos:

| ID | NOME | FORNECEDOR | QUANTIDADE |
|----|------|-------------|-----------|

---

Ele segue o formato para ordem de vendas:

| ID DA ORDEM | CLIENTE | PRODUTO |
|-------------|---------|---------|

---

## Funcionalidades (GET, POST, PUT, DELETE)

---

### GET
O método **GET** é utilizado para obter informações do servidor.  
Ele realiza consultas e não altera nenhum dado existente.

---

### POST
O método **POST** é usado para criar novos recursos no servidor.  
Ele adiciona novos registros à base de dados.

---

### PUT
O método **PUT** serve para atualizar completamente um recurso existente.  
Ele substitui os dados antigos pelos novos enviados na requisição.

---

### DELETE
O método **DELETE** é responsável por remover um recurso do servidor.  
Ele exclui registros existentes da base de dados.

---

## ENDPOINTS
### Endpoints da API

#### Clientes
- GET /clientes
- POST /clientes
- PUT /clientes
- DELETE /clientes/{id}

#### Produtos
- GET /produtos
- POST /produtos
- PUT /produtos
- DELETE /produtos/{id}

#### Ordens de Venda
- GET /ordens
- POST /ordens
- PUT /ordens
- DELETE /ordens/{id}

---

## Como Executar o Projeto

### 1. Instale as dependências
(use uma de cada vez)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install "fastapi[standard]"
```

### 2. Rode o programa

```bash
fastapi dev
```
### 3. Postman
Quando você rodar o comando para iniciar o servidor, aparecerá no terminal uma mensagem indicando que a aplicação está funcionando.  

O FastAPI exibirá algo semelhante a:   Server started at http://127.0.0.1:8000

Copie esse endereço (por padrão: `http://127.0.0.1:8000`) e siga os passos abaixo para usar a API no Postman:

1. Abra o Postman.  
2. No campo de URL, cole o endereço do servidor.  
3. Selecione o método HTTP desejado (GET, POST, PUT, DELETE).  
4. Informe o endpoint desejado, por exemplo:
   - `GET http://127.0.0.1:8000/produto`
   - `GET http://127.0.0.1:8000/produto/1`
   - `POST http://127.0.0.1:8000/add_produto`
   - `PUT http://127.0.0.1:8000/update_produto/1`
   - `DELETE http://127.0.0.1:8000/del_produto/1`
5. Para métodos que exigem corpo (POST e PUT), selecione:
   - **Body**
   - **raw**
   - **JSON**
6. Insira os dados no formato correto, por exemplo:
     {
       "nome": "Arroz",
       "fornecedor": "Prato Fino",
       "quantidade": 50
     }
Depois disso, clique em **Send** para enviar a requisição e visualizar a resposta da API.

