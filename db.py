import models
import json
import os

#products
folder_path = 'data'
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, 'products.json')

products = [
	models.Product('Phone', 10000, 6, 1)
]

with open(file_path, 'w', encoding='utf-8') as file:
	json.dump([p.to_dict() for p in products], file, ensure_ascii=False, indent=4)

with open(file_path, 'r', encoding='utf-8') as file:
	loaded_data = json.load(file)
	loaded_products = [models.Product.from_dict(d) for d in loaded_data]

#clients
folder_path = 'data'
os.makedirs(folder_path, exist_ok=True)
file_path = os.path.join(folder_path, 'clients.json')

clients = [
	models.Client('John Doe', '+1123456', 'mail@gmail.com'),
	models.Client('John Doe111', '+11234561111', 'mail@gmail.com11111'),
]

with open(file_path, 'w', encoding='utf-8') as file:
	json.dump([p.to_dict() for p in clients], file, ensure_ascii=False, indent=4)

with open(file_path, 'r', encoding='utf-8') as file:
	loaded_data = json.load(file)
	loaded_products = [models.Client.from_dict(d) for d in loaded_data]

