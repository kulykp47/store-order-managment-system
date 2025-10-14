import models
import json
import os

products = []
clients = []
orders = [] # Добавлен список для заказов

def import_base():
	global products, clients, orders # Обновлено для orders
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
	
	#orders (Добавлен импорт для заказов)
	orders_path = os.path.join('data', 'orders.json')
	if os.path.exists(orders_path):
		with open(orders_path, 'r', encoding='utf-8') as file:
			loaded_data = json.load(file)
		orders = [models.Order.from_dict(d) for d in loaded_data]
	else:
		orders = []

def export_base():
	global products, clients, orders # Обновлено для orders
	folder_path = 'data'
	os.makedirs(folder_path, exist_ok=True)

	products_path = os.path.join(folder_path, 'products.json')
	with open(products_path, 'w', encoding='utf-8') as file:
		json.dump([p.to_dict() for p in products], file, ensure_ascii=False, indent=4)

	clients_path = os.path.join(folder_path, 'clients.json')
	with open(clients_path, 'w', encoding='utf-8') as file:
		json.dump([p.to_dict() for p in clients], file, ensure_ascii=False, indent=4)

	#orders (Добавлен экспорт для заказов)
	orders_path = os.path.join(folder_path, 'orders.json')
	with open(orders_path, 'w', encoding='utf-8') as file:
		json.dump([o.to_dict() for o in orders], file, ensure_ascii=False, indent=4)