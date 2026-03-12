from fastapi import FastAPI
import os
import csv
from pydantic import BaseModel
import clientes

app = FastAPI()

file_path = 'OrdemDeVendas.csv'

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

if not os.path.exists(file_path):    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID", "CLIENTE", "PRODUTO"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')
