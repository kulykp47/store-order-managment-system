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
	def __init__(self, order_product, order_client):
		super(Order, self).__init__()
		self.order_product = order_product
		self.order_client = order_client
		self.date = datetime.date.today()

						