from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Treeview, Combobox 
import db
import models
import datetime
import re

db.import_base()

try:
	last_id = db.products[-1].product_id
except:
	last_id = 0

current_sort_filter = {}

root = Tk()
root.title('Менеджер магазина')
root.geometry('650x360')
root.config(bg='#494D4E')

data_month_options = ['Месяц', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

# --- Новые списки опций для сортировки ---
current_year = datetime.datetime.now().year
year_options = ['Год'] + [str(y) for y in range(2000, current_year + 1)]
day_options = ['День'] + [str(d) for d in range(1, 32)]
hour_options = ['Час'] + [str(h).zfill(2) for h in range(0, 24)]
minute_options = ['Мин.'] + [str(m).zfill(2) for m in range(0, 60)]
# ----------------------------------------


def sort_column(tree, col, reverse):
    l = [(tree.set(k, col), k) for k in tree.get_children('')]
    
    def sort_key(item):
        value = item[0]
        # Нормализация строки: удаляем пробелы, заменяем запятые на точки
        normalized_value = str(value).strip().replace(',', '.')
        
        try:
            # 1. Попытка сортировки как даты/времени
            if col == 'Дата/Время' or col == 'Date/Time':
                return datetime.datetime.strptime(normalized_value, "%d.%m.%Y %H:%M")
        except ValueError:
            pass
        
        try:
            # 2. Попытка сортировки как числа (Цена, Кол-во, ID)
            # Проверяем, является ли это числом с плавающей точкой
            if '.' in normalized_value:
                return float(normalized_value)
            # Или целым числом
            return int(normalized_value)
        except ValueError:
            # 3. Сортировка как строки (ФИО, Название)
            return normalized_value.lower()

    # Применяем функцию sort_key для всех элементов
    l.sort(key=sort_key, reverse=reverse)

    # Переставляем элементы в отсортированном порядке
    for index, (val, k) in enumerate(l):
        tree.move(k, '', index)

    # Устанавливаем команду для обратной сортировки при следующем клике
    tree.heading(col, command=lambda: sort_column(tree, col, not reverse))
    
def save_changes():
	db.export_base()
	messagebox.showinfo('Сохранение', 'Данные успешно сохранены')

def update_order_tree(orders_list=None):
	if orders_list is None:
		orders_list = db.orders # По умолчанию показываем все заказы

	for i in tree_orders.get_children():
		tree_orders.delete(i)
	
	for order in orders_list:
		tree_orders.insert('', 'end', values=models.Order.unpack(order))

def filter_orders(orders, filters):
	filtered = []
	for order in orders:
		try:
			# Пример: '16.08.2025 14:30'
			dt_obj = datetime.datetime.strptime(order.date_time, "%d.%m.%Y %H:%M")
			match = True
			
			# Фильтр по дате
			if filters['day'] and dt_obj.day != int(filters['day']):
				match = False
			# Месяц в списке data_month_options начинается с индекса 1, filters['month'] = 0 - это 'Месяц' (None)
			if filters['month'] is not None and filters['month'] != 0 and dt_obj.month != filters['month']:
				match = False
			if filters['year'] and dt_obj.year != int(filters['year']):
				match = False
			
			if match: # Если дата совпадает, проверяем время
				h_from = filters['h_from'] if filters['h_from'] is not None else 0
				m_from = filters['m_from'] if filters['m_from'] is not None else 0
				h_to = filters['h_to'] if filters['h_to'] is not None else 23
				m_to = filters['m_to'] if filters['m_to'] is not None else 59
				
				time_from = datetime.time(h_from, m_from)
				time_to = datetime.time(h_to, m_to)
				
				order_time = dt_obj.time()
				
				if order_time < time_from or order_time > time_to:
					# Только если задан хотя бы один параметр времени, применяем фильтр по времени
					if filters['h_from'] is not None or filters['m_from'] is not None or filters['h_to'] is not None or filters['m_to'] is not None:
						match = False
			
			if match:
				filtered.append(order)
		except ValueError:
			# Игнорировать заказы с некорректным форматом даты/времени
			pass
	return filtered

def apply_sorting_filter():
	global current_sort_filter
	
	# Теперь эти переменные являются StringVar
	day = data_day_entry.get()
	month_name = data_month_entry.get()
	year = data_year_entry.get()
	h_from = time_h_from_entry.get()
	m_from = time_m_from_entry.get()
	h_to = time_h_to_entry.get()
	m_to = time_m_ro_entry.get()

	def safe_int(value, default=None):
		try:
			# Проверка на служебные слова/заглушки
			if value in ['День', 'Год', 'Час', 'Мин.', 'Месяц']:
				return default
			return int(value)
		except:
			return default

	current_sort_filter = {
		'day': safe_int(day),
		'month': data_month_options.index(month_name) if month_name in data_month_options else None,
		'year': safe_int(year),
		'h_from': safe_int(h_from),
		'm_from': safe_int(m_from),
		'h_to': safe_int(h_to),
		'm_to': safe_int(m_to),
	}
	
	filtered_orders = filter_orders(db.orders, current_sort_filter)
	update_order_tree(filtered_orders)

def reset_sorting_filter():
	"""Сбрасывает все фильтры сортировки и обновляет список заказов."""
	global current_sort_filter
	
	try:
		# Сброс StringVars до значений по умолчанию
		data_day_entry.set(day_options[0])      # 'День'
		data_month_entry.set(data_month_options[0]) # 'Месяц'
		data_year_entry.set(year_options[0])    # 'Год'
		time_h_from_entry.set(hour_options[0])  # 'Час'
		time_m_from_entry.set(minute_options[0])# 'Мин.'
		time_h_to_entry.set(hour_options[0])    # 'Час'
		time_m_ro_entry.set(minute_options[0])  # 'Мин.'
	except NameError:
		# Пропускаем, если окно сортировки еще не было открыто и StringVars не инициализированы
		pass
	
	# Сброс глобального состояния фильтра
	current_sort_filter = {}
	
	# Обновление главного дерева для показа всех заказов
	update_order_tree(db.orders)

# --- НОВАЯ ФУНКЦИЯ ОТОБРАЖЕНИЯ ОШИБКИ ---
def show_custom_error(parent_window, title, message):
	"""Отображает кастомное окно ошибки, которое гарантированно будет поверх всех окон."""
	error_window = Toplevel(parent_window)
	error_window.title(title)
	error_window.geometry('350x150')
	error_window['bg'] = '#494D4E'
	
	# Настройки модальности и фокуса
	error_window.transient(parent_window) # Делаем окно дочерним
	error_window.grab_set()      # Захватываем ввод
	error_window.focus_set()     # Устанавливаем фокус
	error_window.attributes('-topmost', 1) # Всегда поверх
	
	# Сообщение
	Label(error_window, text=message, bg='#494D4E', fg='white', font=('arial', 12), wraplength=330, justify=LEFT).pack(pady=20, padx=10)
	
	# Кнопка ОК
	Button(error_window, text='ОК', command=error_window.destroy, width=10, font=('arial', 12)).pack(pady=10)
	
	# Принудительное поднятие (для GNOME/Fedora)
	error_window.lift()
	error_window.tk.call('raise', error_window._w)
	
	# Блокируем родительское окно до закрытия окна ошибки
	parent_window.lift()
	error_window.wait_window(error_window)
	
	# Возвращаем фокус родительскому окну
	parent_window.focus_set()

# --- КОНЕЦ НОВОЙ ФУНКЦИИ ---

def add_client_window():
	window = Toplevel(root)
	window.title('Добавить клиента')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

	def add_client():
		new_client = models.Client(fio_entry.get(), phone_entry.get(), email_entry.get())
		db.clients.append(new_client)
		window.destroy()

	fio_label = Label(window, text='ФИО', bg='#494D4E', fg='white', font=('arial', 15))
	fio_label.place(x=0, y=0)
	fio_entry = Entry(window, width=33, font=('arial', 26))
	fio_entry.place(x=0, y=20)
	phone_label = Label(window, text='Номер телефона', bg='#494D4E', fg='white', font=('arial', 15))
	phone_label.place(x=0, y=70)
	phone_entry = Entry(window, width=33, font=('arial', 26))
	phone_entry.place(x=0, y=90)
	email_label = Label(window, text='Адрес электронной почты', bg='#494D4E', fg='white', font=('arial', 15))
	email_label.place(x=0, y=140)
	email_entry = Entry(window, width=33, font=('arial', 26))
	email_entry.place(x=0, y=160)
	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=220)
	add = Button(window, text='Добавить', bg='grey', font=('arial', 20), command=add_client)
	add.place(x=485, y=220)

def add_product_window():
	window = Toplevel(root)
	window.title('Добавить товар')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

	def add_product():
		global last_id
		last_id += 1
		new_product = models.Product(product_name_entry.get(), product_price_entry.get(), product_count_entry.get(), last_id)
		db.products.append(new_product)
		window.destroy()

	product_name_label = Label(window, text='Наименование товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_name_label.place(x=0, y=0)
	product_name_entry = Entry(window, width=33, font=('arial', 26))
	product_name_entry.place(x=0, y=20)
	product_price_label = Label(window, text='Цена товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_price_label.place(x=0, y=70)
	product_price_entry = Entry(window, width=33, font=('arial', 26))
	product_price_entry.place(x=0, y=90)
	product_count_label = Label(window, text='Кол-во товара на складе', bg='#494D4E', fg='white', font=('arial', 15))
	product_count_label.place(x=0, y=140)
	product_count_entry = Entry(window, width=33, font=('arial', 26))
	product_count_entry.place(x=0, y=160)
	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=220)
	add = Button(window, text='Добавить', bg='grey', font=('arial', 20), command=add_product)
	add.place(x=485, y=220)

# Функции редактирования клиента/продукта (для пункта 5 и 6)
def edit_client_window(client_data):
	window = Toplevel(root)
	window.title('Изменить клиента')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

	# Находим объект Client по данным из Treeview
	try:
		current_client = next(c for c in db.clients if c.client_fio == client_data[0] and c.client_phone == client_data[1])
	except StopIteration:
		messagebox.showerror("Ошибка", "Клиент не найден в базе.")
		return 

	def edit_client():
		current_client.client_fio = fio_entry.get()
		current_client.client_phone = phone_entry.get()
		current_client.client_email = email_entry.get()
		window.destroy()
		update_order_tree() # Обновляем дерево заказов

	fio_label = Label(window, text='ФИО', bg='#494D4E', fg='white', font=('arial', 15))
	fio_label.place(x=0, y=0)
	fio_entry = Entry(window, width=33, font=('arial', 26))
	fio_entry.insert(0, current_client.client_fio)
	fio_entry.place(x=0, y=20)
	phone_label = Label(window, text='Номер телефона', bg='#494D4E', fg='white', font=('arial', 15))
	phone_label.place(x=0, y=70)
	phone_entry = Entry(window, width=33, font=('arial', 26))
	phone_entry.insert(0, current_client.client_phone)
	phone_entry.place(x=0, y=90)
	email_label = Label(window, text='Адрес электронной почты', bg='#494D4E', fg='white', font=('arial', 15))
	email_label.place(x=0, y=140)
	email_entry = Entry(window, width=33, font=('arial', 26))
	email_entry.insert(0, current_client.client_email)
	email_entry.place(x=0, y=160)
	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=220)
	add = Button(window, text='Сохранить', bg='grey', font=('arial', 20), command=edit_client)
	add.place(x=485, y=220)


def edit_product_window(product_data, update_callback=None):
	window = Toplevel(root)
	window.title('Изменить товар')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

	# Находим объект Product по данным из Treeview
	try:
		product_id = int(product_data[3])
		current_product = next(p for p in db.products if p.product_id == product_id)
	except (StopIteration, ValueError):
		messagebox.showerror("Ошибка", "Товар не найден в базе.")
		return 

	def edit_product():
		current_product.product_name = product_name_entry.get()
		current_product.product_price = product_price_entry.get()
		current_product.product_count = product_count_entry.get()
		window.destroy()
		update_order_tree() # Обновляем дерево заказов
		if update_callback:
			update_callback() # Обновляем Treeview в окне, откуда вызвано редактирование
	
	product_name_label = Label(window, text='Наименование товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_name_label.place(x=0, y=0)
	product_name_entry = Entry(window, width=33, font=('arial', 26))
	product_name_entry.insert(0, current_product.product_name)
	product_name_entry.place(x=0, y=20)
	product_price_label = Label(window, text='Цена товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_price_label.place(x=0, y=70)
	product_price_entry = Entry(window, width=33, font=('arial', 26))
	product_price_entry.insert(0, current_product.product_price)
	product_price_entry.place(x=0, y=90)
	product_count_label = Label(window, text='Кол-во товара на складе', bg='#494D4E', fg='white', font=('arial', 15))
	product_count_label.place(x=0, y=140)
	product_count_entry = Entry(window, width=33, font=('arial', 26))
	product_count_entry.insert(0, current_product.product_count)
	product_count_entry.place(x=0, y=160)
	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=220)
	add = Button(window, text='Сохранить', bg='grey', font=('arial', 20), command=edit_product)
	add.place(x=485, y=220)

def create_order_window():
	window = Toplevel(root)
	window.title('Создать заказ')
	window.geometry('635x600')
	window['bg'] = '#494D4E'
	
	# Установка модальности и фокуса для окна заказа
	window.transient(root) 
	window.grab_set()      
	window.focus_set()     
	
	count = StringVar()
	count.set('1')
	
	selected_product = None
	selected_client = None

	def count_minus():
		try:
			new = int(count.get())
			new = max(1, new - 1)
			count.set(str(new))
		except:
			count.set('1')

	def count_plus():
		try:
			new = int(count.get())
			new += 1
			count.set(str(new))
		except:
			count.set('1')

	def product_search():
		search_data = (product_name_entry.get()).lower()
		for i in tree_product.get_children():
			tree_product.delete(i)
		
		products_to_show = []
		if '$:' in search_data:
			search_term = search_data[2:]
			products_to_show = [p for p in db.products if search_term in p.product_price]
		elif '#:' in search_data:
			search_term = search_data[2:]
			products_to_show = [p for p in db.products if search_term in p.product_count]
		elif search_data.isdigit():
			search_term = int(search_data)
			products_to_show = [p for p in db.products if search_term == p.product_id]
		else:
			products_to_show = [p for p in db.products if search_data in (p.product_name).lower()]

		for product in products_to_show:
			tree_product.insert('', 'end', values=models.Product.unpack(product))

	def people_search():
		search_data = (people_entry.get()).lower()
		for i in tree_people.get_children():
			tree_people.delete(i)
		
		clients_to_show = []
		if '+:' in search_data:
			search_term = search_data[2:]
			clients_to_show = [c for c in db.clients if search_term in c.client_phone]
		elif '@:' in search_data:
			search_term = search_data[2:]
			clients_to_show = [c for c in db.clients if search_term in (c.client_email).lower()]
		else:
			clients_to_show = [c for c in db.clients if search_data in (c.client_fio).lower()]
		
		for person in clients_to_show:
			tree_people.insert('', 'end', values=models.Client.unpack(person))

	# Функции выбора и редактирования
	def on_product_select(event):
		nonlocal selected_product
		item = tree_product.focus()
		values = tree_product.item(item, 'values')
		selected_product = None
		if values:
			# Находим объект Product по ID
			try:
				product_id = int(values[3])
				selected_product = next((p for p in db.products if p.product_id == product_id), None)
			except (IndexError, ValueError):
				pass # Пропустить, если данные некорректны

	def on_client_select(event):
		nonlocal selected_client
		item = tree_people.focus()
		values = tree_people.item(item, 'values')
		selected_client = None
		if values:
			# Находим объект Client по ФИО и телефону
			try:
				selected_client = next((c for c in db.clients if c.client_fio == values[0] and c.client_phone == values[1]), None)
			except IndexError:
				pass # Пропустить, если данные некорректны

	def on_product_double_click(event):
		item = tree_product.focus()
		values = tree_product.item(item, 'values')
		if values:
			edit_product_window(values, product_search) # Передаем функцию для обновления Treeview
	
	def on_client_double_click(event):
		item = tree_people.focus()
		values = tree_people.item(item, 'values')
		if values:
			edit_client_window(values)

	def create_order():
		nonlocal selected_product, selected_client
		
		# 1. Проверка количества
		try:
			order_count = int(count.get())
			if order_count <= 0:
				raise ValueError("Количество должно быть больше 0")
		except ValueError:
			show_custom_error(window, "Ошибка создания заказа", "Некорректное количество.")
			return
		
		# 2. Проверка выбора
		if selected_product is None or selected_client is None:
			show_custom_error(window, "Ошибка создания заказа", "Выберите товар и клиента!")
			return

		# 3. Проверка склада
		try:
			product_count_on_stock = int(selected_product.product_count)
		except ValueError:
			show_custom_error(window, "Ошибка создания заказа", "Некорректное количество на складе.")
			return

		# 4. Проверка доступного количества
		if order_count > product_count_on_stock:
			show_custom_error(window, "Ошибка создания заказа", f"На складе недостаточно товара. В наличии: {product_count_on_stock}")
			return

		# Создание заказа и обновление склада
		new_order = models.Order(selected_product, selected_client, order_count)
		db.orders.append(new_order)
		
		# Обновление количества на складе
		selected_product.product_count = str(product_count_on_stock - order_count)
		
		window.destroy()
		update_order_tree() # Обновление главного Treeview

	#Базовый интерфейс
	product_name_label = Label(window, text='Наименование товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_name_label.place(x=0, y=0)
	product_name_entry = Entry(window, width=28, font=('arial', 26))
	product_name_entry.place(x=0, y=20)
	search_product = Button(window, text='Поиск', bg='grey', font=('arial', 20), command=product_search)
	search_product.place(x=530, y=20)
	people_label = Label(window, text='Заказчик', bg='#494D4E', fg='white', font=('arial', 15))
	people_label.place(x=0, y=225)
	people_entry = Entry(window, width=28, font=('arial', 26))
	people_entry.place(x=0, y=250)
	search_people = Button(window, text='Поиск', bg='grey', font=('arial', 20), command=people_search)
	search_people.place(x=530, y=250)
	count_label = Label(window, text='Кол-во', bg='#494D4E', fg='white', font=('arial', 15))
	count_label.place(x=0, y=455)
	minus_count = Button(window, text='-', bg='grey', font=('arial', 20, 'bold'), command=count_minus)
	minus_count.place(x=0, y=480)
	count_entry = Entry(window, textvariable=count, width=8, font=('arial', 26), justify='center')
	count_entry.place(x=40, y=480)
	plus_count = Button(window, text='+', bg='grey', font=('arial', 20, 'bold'), command=count_plus)
	plus_count.place(x=200, y=480)
	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=550)
	add = Button(window, text='Создать заказ', bg='grey', font=('arial', 20), command=create_order) 
	add.place(x=435, y=550) 

	#Список товаров
	frame_product = Frame(window, width=635, height=150)
	frame_product.place(x=0, y=70)
	frame_product.pack_propagate(False)
	tree_product = Treeview(frame_product, columns=('Наименование', 'Цена', 'Кол-во', 'id'), show='headings')
	tree_product.heading('Наименование', text='Наименование', command=lambda: sort_column(tree_product, 'Наименование', False))
	tree_product.heading('Цена', text='Цена', command=lambda: sort_column(tree_product, 'Цена', False))
	tree_product.heading('Кол-во', text='Кол-во', command=lambda: sort_column(tree_product, 'Кол-во', False))
	tree_product.heading('id', text='id', command=lambda: sort_column(tree_product, 'id', False))
	tree_product.column('Наименование', width=340)
	tree_product.column('Цена', width=100)
	tree_product.column('Кол-во', width=100)
	tree_product.column('id', width=75)
	for product in db.products:
		tree_product.insert('', 'end', values=models.Product.unpack(product))
	scrollbar_product = Scrollbar(frame_product, orient='vertical', command=tree_product.yview)
	tree_product.configure(yscrollcommand=scrollbar_product.set)
	tree_product.pack(side='left', fill='both', expand=True)
	scrollbar_product.pack(side='right', fill='y')

	# Привязка событий
	tree_product.bind('<<TreeviewSelect>>', on_product_select)
	tree_product.bind('<Double-1>', on_product_double_click)

	#Список заказчиков
	frame_people = Frame(window, width=635, height=150)
	frame_people.place(x=0, y=300)
	frame_people.pack_propagate(False)
	tree_people = Treeview(frame_people, columns=('ФИО', 'Телефон', 'Почта'), show='headings')
	tree_people.heading('ФИО', text='ФИО', command=lambda: sort_column(tree_people, 'ФИО', False))
	tree_people.heading('Телефон', text='Телефон', command=lambda: sort_column(tree_people, 'Телефон', False))
	tree_people.heading('Почта', text='Почта', command=lambda: sort_column(tree_people, 'Почта', False))
	tree_people.column('ФИО', width=205)
	tree_people.column('Телефон', width=205)
	tree_people.column('Почта', width=205)
	for person in db.clients:
		tree_people.insert('', 'end', values=models.Client.unpack(person))
	scrollbar_people = Scrollbar(frame_people, orient='vertical', command=tree_people.yview)
	tree_people.configure(yscrollcommand=scrollbar_people.set)
	tree_people.pack(side='left', fill='both', expand=True)
	scrollbar_people.pack(side='right', fill='y')

	# Привязка событий
	tree_people.bind('<<TreeviewSelect>>', on_client_select)
	tree_people.bind('<Double-1>', on_client_double_click)

def sorting_window():
	window = Toplevel(root)
	window.title('Сортировка')
	window.geometry('635x220') # Сделали окно компактнее
	window['bg'] = '#494D4E'

	# --- Инициализация StringVar для всех полей (объявлены глобальными) ---
	global data_day_entry, data_month_entry, data_year_entry
	global time_h_from_entry, time_m_from_entry, time_h_to_entry, time_m_ro_entry

	data_day_entry = StringVar(window)
	data_day_entry.set(day_options[0]) 
	
	data_year_entry = StringVar(window)
	data_year_entry.set(year_options[0])

	data_month_entry = StringVar(window)
	data_month_entry.set(data_month_options[0])

	time_h_from_entry = StringVar(window)
	time_h_from_entry.set(hour_options[0])

	time_m_from_entry = StringVar(window)
	time_m_from_entry.set(minute_options[0])

	time_h_to_entry = StringVar(window)
	time_h_to_entry.set(hour_options[0])

	time_m_ro_entry = StringVar(window)
	time_m_ro_entry.set(minute_options[0])
	# --------------------------------------------------------------------
	
	# 1. Дата (Верхний ряд)
	data_label = Label(window, text='Дата:', bg='#494D4E', fg='white', font=('arial', 15))
	data_label.place(x=0, y=5)
	
	# День (Combobox)
	day_menu = Combobox(window, textvariable=data_day_entry, values=day_options, width=5, font=('arial', 15), state='readonly')
	day_menu.place(x=70, y=5) 
	
	# Месяц (Combobox)
	month_menu = Combobox(window, textvariable=data_month_entry, values=data_month_options, width=8, font=('arial', 15), state='readonly')
	month_menu.place(x=150, y=5) 
	
	# Год (Combobox)
	year_menu = Combobox(window, textvariable=data_year_entry, values=year_options, width=5, font=('arial', 15), state='readonly')
	year_menu.place(x=265, y=5) 

	# 2. Время (Средний ряд)
	time_label = Label(window, text='Время:', bg='#494D4E', fg='white', font=('arial', 15))
	time_label.place(x=0, y=50) 
	
	# Время ОТ
	from_label = Label(window, text='От:', bg='#494D4E', fg='white', font=('arial', 15))
	from_label.place(x=0, y=90) 
	
	# Час ОТ (Combobox)
	h_from_menu = Combobox(window, textvariable=time_h_from_entry, values=hour_options, width=4, font=('arial', 15), state='readonly')
	h_from_menu.place(x=40, y=90)
	
	# Минуты ОТ (Combobox)
	m_from_menu = Combobox(window, textvariable=time_m_from_entry, values=minute_options, width=4, font=('arial', 15), state='readonly')
	m_from_menu.place(x=120, y=90)

	# Время ДО
	to_label = Label(window, text='До:', bg='#494D4E', fg='white', font=('aria l', 15))
	to_label.place(x=0, y=130) 
	
	# Час ДО (Combobox)
	h_to_menu = Combobox(window, textvariable=time_h_to_entry, values=hour_options, width=4, font=('arial', 15), state='readonly')
	h_to_menu.place(x=40, y=130)
	
	# Минуты ДО (Combobox)
	m_to_menu = Combobox(window, textvariable=time_m_ro_entry, values=minute_options, width=4, font=('arial', 15), state='readonly')
	m_to_menu.place(x=120, y=130)
	
	# 3. Кнопки (Нижний ряд)
	cancel = Button(window, text='Закрыть', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=170)
	
	# Кнопка Сброс
	reset_btn = Button(window, text='Сброс', bg='grey', font=('arial', 20), command=reset_sorting_filter)
	reset_btn.place(x=370, y=170) 
	
	apply_sort = Button(window, text='Применить', bg='grey', font=('arial', 20), command=apply_sorting_filter)
	apply_sort.place(x=485, y=170)


def count_check_button():
	window = Toplevel(root)
	window.title('Остатки товаров')
	window.geometry('635x300') 
	window['bg'] = '#494D4E'
	
	selected_product_for_update = None

	def product_search():
		search_data = (search_entry.get()).lower()
		for i in tree_product.get_children():
			tree_product.delete(i)
		
		products_to_show = []
		if '$:' in search_data:
			search_term = search_data[2:]
			products_to_show = [p for p in db.products if search_term in p.product_price]
		elif '#:' in search_data:
			search_term = search_data[2:]
			products_to_show = [p for p in db.products if search_term in p.product_count]
		elif search_data.isdigit():
			search_term = int(search_data)
			products_to_show = [p for p in db.products if search_term == p.product_id]
		else:
			products_to_show = [p for p in db.products if search_data in (p.product_name).lower()]

		for product in products_to_show:
			tree_product.insert('', 'end', values=models.Product.unpack(product))
		
		# Очистка Entry после обновления Treeview
		count_entry.delete(0, END)

	def on_product_select(event):
		nonlocal selected_product_for_update
		item = tree_product.focus()
		values = tree_product.item(item, 'values')
		selected_product_for_update = None
		if values:
			# Находим объект Product по ID
			try:
				product_id = int(values[3])
				selected_product_for_update = next((p for p in db.products if p.product_id == product_id), None)
				# Отображаем текущее кол-во в Entry
				if selected_product_for_update:
					count_entry.delete(0, END)
					count_entry.insert(0, selected_product_for_update.product_count)
			except (IndexError, ValueError):
				pass # Пропустить, если данные некорректны
	
	def on_product_double_click(event):
		item = tree_product.focus()
		values = tree_product.item(item, 'values')
		if values:
			edit_product_window(values, product_search) # Используем ранее созданное окно редактирования

	def save_count():
		nonlocal selected_product_for_update
		if selected_product_for_update:
			try:
				new_count = count_entry.get()
				# Простая проверка на число
				if not re.match(r'^-?\d+$', new_count):
					show_custom_error(window, "Ошибка сохранения", "Количество должно быть целым числом.")
					return

				selected_product_for_update.product_count = new_count
				product_search() # Обновляем Treeview
			except Exception as e:
				show_custom_error(window, "Ошибка сохранения", f"Произошла ошибка при сохранении: {e}")
		else:
			show_custom_error(window, "Ошибка сохранения", "Выберите товар для изменения")

	search = Button(window, text='Поиск', bg='grey', width=6, font=('arial', 20), command=product_search)
	search.place(x=520, y=0)
	search_entry = Entry(window, width=27, font=('arial', 26), fg='black')
	search_entry.place(x=0, y=0)

	frame_product = Frame(window, width=635, height=150)
	frame_product.place(x=0, y=50)
	frame_product.pack_propagate(False)
	tree_product = Treeview(frame_product, columns=('Наименование', 'Цена', 'Кол-во', 'id'), show='headings')
	tree_product.heading('Наименование', text='Наименование', command=lambda: sort_column(tree_product, 'Наименование', False))
	tree_product.heading('Цена', text='Цена', command=lambda: sort_column(tree_product, 'Цена', False))
	tree_product.heading('Кол-во', text='Кол-во', command=lambda: sort_column(tree_product, 'Кол-во', False))
	tree_product.heading('id', text='id', command=lambda: sort_column(tree_product, 'id', False))
	tree_product.column('Наименование', width=340)
	tree_product.column('Цена', width=100)
	tree_product.column('Кол-во', width=100)
	tree_product.column('id', width=75)
	for product in db.products:
		tree_product.insert('', 'end', values=models.Product.unpack(product))
	scrollbar_product = Scrollbar(frame_product, orient='vertical', command=tree_product.yview)
	tree_product.configure(yscrollcommand=scrollbar_product.set)
	tree_product.pack(side='left', fill='both', expand=True)
	scrollbar_product.pack(side='right', fill='y')

	# Привязка событий
	tree_product.bind('<<TreeviewSelect>>', on_product_select)
	tree_product.bind('<Double-1>', on_product_double_click)

	# Интерфейс для изменения количества
	count_label = Label(window, text='Изменить кол-во:', bg='#494D4E', fg='white', font=('arial', 15))
	count_label.place(x=0, y=210)
	count_entry = Entry(window, width=10, font=('arial', 26))
	count_entry.place(x=0, y=240)
	save_btn = Button(window, text='Сохранить', bg='grey', font=('arial', 20), command=save_count)
	save_btn.place(x=195, y=240)
	cancel_btn = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel_btn.place(x=370, y=240)


# Основное окно
add_client = Button(root, text='Добавить клиента', bg='grey', font=('arial', 20), command=add_client_window)
add_client.place(x=0, y=0)
add_order = Button(root, text='Создать заказ', bg='grey', font=('arial', 20), command=create_order_window)
add_order.place(x=263, y=0)
sort = Button(root, text='Сортировка', bg='grey', font=('arial', 20), command=sorting_window)
sort.place(x=477, y=0)
add_product = Button(root, text='Добавить товар', bg='grey', font=('arial', 20), command=add_product_window)
add_product.place(x=0, y=50)
stat = Button(root, text='Статистика', bg='grey', font=('arial', 20))
stat.place(x=235, y=50)
count_check = Button(root, text='Остатки товаров', bg='grey', font=('arial', 20), command=count_check_button)
count_check.place(x=415, y=50)
cancel_button = Button(root, text='Сохранить', bg='grey', font=('arial', 20), command=save_changes)
cancel_button.place(x=490, y=310)
save = Button(root, text='Отменить', bg='grey', font=('arial', 20), command=root.destroy)
save.place(x=0, y=310)

# Список заказов (вместо списка людей)
frame = Frame(root, width=650, height=200)
frame.place(x=0, y=100)
frame.pack_propagate(False)
tree_orders = Treeview(frame, columns=('ФИО', 'Наименование', 'Кол-во', 'Дата/Время'), show='headings')
tree_orders.heading('ФИО', text='ФИО', command=lambda: sort_column(tree_orders, 'ФИО', False))
tree_orders.heading('Наименование', text='Наименование', command=lambda: sort_column(tree_orders, 'Наименование', False))
tree_orders.heading('Кол-во', text='Кол-во', command=lambda: sort_column(tree_orders, 'Кол-во', False))
tree_orders.heading('Дата/Время', text='Дата/Время', command=lambda: sort_column(tree_orders, 'Дата/Время', False))
tree_orders.column('ФИО', width=195)
tree_orders.column('Наименование', width=195)
tree_orders.column('Кол-во', width=100)
tree_orders.column('Дата/Время', width=140)
update_order_tree() # Загрузка заказов
scrollbar = Scrollbar(frame, orient='vertical', command=tree_orders.yview)
tree_orders.configure(yscrollcommand=scrollbar.set)
tree_orders.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

root.mainloop()