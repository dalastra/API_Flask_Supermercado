# API SUPERMERCADO
# Sistema de Produtos — API FastAPI com CSV

Este projeto é uma API simples construída com *FastAPI, utilizando um arquivo **CSV* como banco de dados para armazenar produtos.

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
- Uvicorn  
- CSV como armazenamento  

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

## Como Rodar o Projeto

### 1. Instale as dependências

```bash
pip install fastapi uvicorn pydantic
