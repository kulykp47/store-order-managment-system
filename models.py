import datetime

class Product:
	def __init__(self, product_name, product_price, product_count, product_id):
		super(Product, self).__init__()
		self.product_name = product_name
		self.product_price = product_price
		self.product_count = product_count
		self.product_id = product_id

	def to_dict(self):
		return {'product_name': self.product_name, 'product_price': self.product_price, 'product_count': self.product_count, 'product_id': self.product_id}

	@staticmethod
	def from_dict(data):
		return Product(data['product_name'], data['product_price'], data['product_count'], data['product_id'])

	def unpack(data):
		return [data.product_name, data.product_price, data.product_count, data.product_id]

class Client:
	def __init__(self, client_fio, client_phone, client_email):
		super(Client, self).__init__()
		self.client_fio = client_fio
		self.client_phone = client_phone
		self.client_email = client_email

	def to_dict(self):
		return {'client_fio': self.client_fio, 'client_phone': self.client_phone, 'client_email': self.client_email}

	@staticmethod
	def from_dict(data):
		return Client(data['client_fio'], data['client_phone'], data['client_email'])

	def unpack(data):
		return [data.client_fio, data.client_phone, data.client_email]

class Order:
	def __init__(self, order_product, order_client, order_count, date_time=None):
		super(Order, self).__init__()
		self.order_product = order_product # Product object
		self.order_client = order_client # Client object
		self.order_count = order_count
		if date_time is None:
			now = datetime.datetime.now()
			self.date_time = now.strftime("%d.%m.%Y %H:%M") # день.месяц.год час:минута
		else:
			self.date_time = date_time
	
	def to_dict(self):
		return {'order_product': self.order_product.to_dict(), 
				'order_client': self.order_client.to_dict(), 
				'order_count': self.order_count,
				'date_time': self.date_time}

	@staticmethod
	def from_dict(data):
		product = Product.from_dict(data['order_product'])
		client = Client.from_dict(data['order_client'])
		return Order(product, client, data['order_count'], data['date_time'])

	def unpack(data):
		return [data.order_client.client_fio, data.order_product.product_name, data.order_count, data.date_time]