import models
import json
import os

products = []
clients = []

def import_base():
	global products, clients
	#products
	products_path = os.path.join('data', 'products.json')
	if os.path.exists(products_path):
		with open(products_path, 'r', encoding='utf-8') as file:
			loaded_data = json.load(file)
		products = [models.Product.from_dict(d) for d in loaded_data]
	else:
		products = []

	#clients
	clients_path = os.path.join('data', 'clients.json')
	if os.path.exists(clients_path):
		with open(clients_path, 'r', encoding='utf-8') as file:
			loaded_data = json.load(file)
		clients = [models.Client.from_dict(d) for d in loaded_data]
	else:
		clients = []

def export_base():
	global products, clients
	folder_path = 'data'
	os.makedirs(folder_path, exist_ok=True)

	products_path = os.path.join(folder_path, 'products.json')
	with open(products_path, 'w', encoding='utf-8') as file:
		json.dump([p.to_dict() for p in products], file, ensure_ascii=False, indent=4)

	clients_path = os.path.join(folder_path, 'clients.json')
	with open(clients_path, 'w', encoding='utf-8') as file:
		json.dump([p.to_dict() for p in clients], file, ensure_ascii=False, indent=4)