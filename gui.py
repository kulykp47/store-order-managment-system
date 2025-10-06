from tkinter import *
from datetime import datetime
from tkinter.ttk import Treeview, Scrollbar, Combobox
import ctypes
import platform

if platform.system() == 'Windows':
	try:
		ctypes.windll.shcore.SetProcessDpiAwareness(1)
	except:
		pass

root = Tk()
root.title('test')
root.geometry('650x500')
root['bg'] = '#494D4E'

def add_client_window():
	window = Toplevel(root)
	window.title('test')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

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
	add = Button(window, text='Добавить', bg='grey', font=('arial', 20))###
	add.place(x=485, y=220)

def create_order_window():
	window = Toplevel(root)
	window.title('test')
	window.geometry('635x600')
	window['bg'] = '#494D4E'
	count = StringVar()
	count.set(0)

	#функции
	def count_minus():
		new = int(count.get())
		new -= 1
		count.set(str(new))
	def count_plus():
		new = int(count.get())
		new += 1
		count.set(str(new))


	#Базовый интерфейс
	product_name_label = Label(window, text='Наименование товара', bg='#494D4E', fg='white', font=('arial', 15))
	product_name_label.place(x=0, y=0)
	product_name_entry = Entry(window, width=28, font=('arial', 26))
	product_name_entry.place(x=0, y=20)
	search_product = Button(window, text='Поиск', bg='grey', font=('arial', 20))
	search_product.place(x=530, y=20)
	people_label = Label(window, text='Заказчик', bg='#494D4E', fg='white', font=('arial', 15))
	people_label.place(x=0, y=225)
	people_entry = Entry(window, width=28, font=('arial', 26))
	people_entry.place(x=0, y=250)
	search_people = Button(window, text='Поиск', bg='grey', font=('arial', 20))
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
	add = Button(window, text='Добавить', bg='grey', font=('arial', 20))###
	add.place(x=485, y=550)

	#Список товаров(тестовая база)
	data = [
	('1', 'Тетрадь 96', '200', '17'),###########################
	('2', 'Ручка', '100', '215'),
	('3', 'Карандаш', '50', '200')
	]
	frame_product = Frame(window, width=635, height=150)
	frame_product.place(x=0, y=70)
	frame_product.pack_propagate(False)
	tree_product = Treeview(frame_product, columns=('id','Наименование', 'Цена', 'Кол-во'), show='headings')
	tree_product.heading('id', text='id')
	tree_product.heading('Наименование', text='Наименование')
	tree_product.heading('Цена', text='Цена')
	tree_product.heading('Кол-во', text='Кол-во')
	tree_product.column('id', width=75)
	tree_product.column('Наименование', width=340)
	tree_product.column('Цена', width=100)
	tree_product.column('Кол-во', width=100)
	for product in data:
		tree_product.insert('', 'end', values=product)
	scrollbar_product = Scrollbar(frame_product, orient='vertical', command=tree_product.yview)
	tree_product.configure(yscrollcommand=scrollbar_product.set)
	tree_product.pack(side='left', fill='both', expand=True)
	scrollbar_product.pack(side='right', fill='y')
	#Список заказчиков(тестовая база)
	data = [
	('Иванов Иван Иванович', '+79595881212', 'ivanov@gmail.com'),
	('Друн Фоговоч Друнов', '+7123456789', 'bebra@gmail.com'),
	]
	frame_people = Frame(window, width=635, height=150)
	frame_people.place(x=0, y=300)
	frame_people.pack_propagate(False)
	tree_people = Treeview(frame_people, columns=('ФИО', 'Телефон', 'Почта'), show='headings')
	tree_people.heading('ФИО', text='ФИО')
	tree_people.heading('Телефон', text='Телефон')
	tree_people.heading('Почта', text='Почта')
	tree_people.column('ФИО', width=205)
	tree_people.column('Телефон', width=205)
	tree_people.column('Почта', width=205)
	for person in data:
		tree_people.insert('', 'end', values=person)
	scrollbar_people = Scrollbar(frame_people, orient='vertical', command=tree_people.yview)
	tree_people.configure(yscrollcommand=scrollbar_people.set)
	tree_people.pack(side='left', fill='both', expand=True)
	scrollbar_people.pack(side='right', fill='y')

	###############
	def sort_column(tv, col, reverse):
		def try_num(value):
			try:
				return int(value)
			except ValueError:
				return value
		items = [(try_num(tv.set(k, col)), k) for k in tv.get_children('')]
		items.sort(reverse=reverse)
		for index, (val, k) in enumerate(items):
			tv.move(k, '', index)
		tv.heading(col, command=lambda: sort_column(tv, col, not reverse))

	tree_people.heading('ФИО', text='ФИО', command=lambda: sort_column(tree_people, 'ФИО', False))
	tree_people.heading('Телефон', text='Телефон', command=lambda: sort_column(tree_people, 'Телефон', False))
	tree_people.heading('Почта', text='Почта', command=lambda: sort_column(tree_people, 'Почта', False))
	tree_product.heading('id', text='id', command=lambda: sort_column(tree_product, 'id', False))
	tree_product.heading('Наименование', text='Наименование', command=lambda: sort_column(tree_product, 'Наименование', False))
	tree_product.heading('Цена', text='Цена', command=lambda: sort_column(tree_product, 'Цена', False))
	tree_product.heading('Кол-во', text='Кол-во', command=lambda: sort_column(tree_product, 'Кол-во', False))
def add_product_window():
	window = Toplevel(root)
	window.title('test')
	window.geometry('635x270')
	window['bg'] = '#494D4E'

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
	add = Button(window, text='Добавить', bg='grey', font=('arial', 20))###
	add.place(x=485, y=220)
def sorting_window():
	window = Toplevel(root)
	window.title('test')
	window.geometry('635x180')
	window['bg'] = '#494D4E'

	data_label = Label(window, text='Выберите дату заказа', bg='#494D4E', fg='white', font=('arial', 15))
	data_label.place(x=0, y=0)

	data_day_options = [i for i in range(1, 32)]
	data_day_options = ['День'] + data_day_options
	data_day_entry = Combobox(window, values=data_day_options, state='readonly', width=6, font=('arial', 15))
	data_day_entry.current(0)
	data_day_entry.place(x=0, y=20)
	data_month_options = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
	data_month_options = ['Месяц'] + data_month_options
	data_month_entry = Combobox(window, values=data_month_options, state='readonly', width=15, font=('arial', 15))
	data_month_entry.current(0)
	data_month_entry.place(x=90, y=20)
	data_year_options = [i for i in range(2000, (datetime.now().year)+1)]
	data_year_options = ['Год'] + data_year_options
	data_year_entry = Combobox(window, values=data_year_options, state='readonly', width=6, font=('arial', 15))
	data_year_entry.current(0)
	data_year_entry.place(x=280, y=20)

	time_label = Label(window, text='Временной диапазон', bg='#494D4E', fg='white', font=('arial', 15))
	time_label.place(x=0, y=50)
	time_h_options = [str(i).zfill(2) for i in range(0, 24)];
	time_h_options = ['Час'] + time_h_options
	time_h_from_entry = Combobox(window, values=time_h_options, state='readonly', width=5, font=('arial', 15))
	time_h_from_entry.current(0)
	time_h_from_entry.place(x=0, y=70)
	split_label_from = Label(window, text=':', bg='#494D4E', fg='white', font=('arial', 15))
	split_label_from.place(x=75, y=70)
	time_m_options = [str(i).zfill(2) for i in range(0, 61)];
	time_m_options = ['Минут'] + time_m_options
	time_m_from_entry = Combobox(window, values=time_m_options, state='readonly', width=8, font=('arial', 15))
	time_m_from_entry.current(0)
	time_m_from_entry.place(x=90, y=70)
	to_label = Label(window, text='-', bg='#494D4E', fg='white', font=('arial', 15))
	to_label.place(x=200, y=70)
	time_h_to_options = ['Час'] + time_h_options
	time_h_to_entry = Combobox(window, values=time_h_options, state='readonly', width=5, font=('arial', 15))
	time_h_to_entry.current(0)
	time_h_to_entry.place(x=220, y=70)
	split_label_from = Label(window, text=':', bg='#494D4E', fg='white', font=('arial', 15))
	split_label_from.place(x=295, y=70)
	time_m_ro_options = [str(i).zfill(2) for i in range(0, 61)];
	time_m_ro_options = ['Минут'] + time_m_options
	time_m_ro_entry = Combobox(window, values=time_m_options, state='readonly', width=8, font=('arial', 15))
	time_m_ro_entry.current(0)
	time_m_ro_entry.place(x=310, y=70)

	cancel = Button(window, text='Отмена', bg='grey', font=('arial', 20), command=window.destroy)
	cancel.place(x=0, y=130)
	apply_sort = Button(window, text='Применить', bg='grey', font=('arial', 20))###
	apply_sort.place(x=465, y=130)

	

#Базовый интерфейс
add_client = Button(root, text='Добавить клиента', bg='grey', font=('arial', 20), command=add_client_window)###
add_client.place(x=0, y=0)
create_order = Button(root, text='Создать заказ', bg='grey', font=('arial', 20), command=create_order_window)###
create_order.place(x=263, y=0)
sorting = Button(root, text='Сортировка', bg='grey', font=('arial', 20), command=sorting_window)
sorting.place(x=477, y=0)
add_product = Button(root, text='Добавить товар', bg='grey', font=('arial', 20), command=add_product_window)###
add_product.place(x=0, y=50)
statistic = Button(root, text='Статистика/анализ по магазину', bg='grey', font=('arial', 20))
statistic.place(x=235, y=50)
order_base_label = Label(root, text='Список заказов', bg='#494D4E', fg='white', font=('arial', 15))
order_base_label.place(x=0, y=110)
search = Button(root, text='Поиск', bg='grey', width=6, font=('arial', 20))
search.place(x=540, y=130)
search_entry = Entry(root, width=28, font=('arial', 26), fg='black')
search_entry.place(x=0, y=130)

cancel = Button(root, text='Отмена', bg='grey', font=('arial', 20), command=root.destroy)
cancel.place(x=0, y=450)
add = Button(root, text='Добавить', bg='grey', font=('arial', 20))###
add.place(x=500, y=450)

#Список людей(тестовая база)
data = [
('Иванов Иван Иванович', '+79595881212', 'ivanov@gmail.com'),
('Друн Фоговоч Друнов', '+7123456789', 'bebra@gmail.com')#####################################
]
frame = Frame(root, width=650, height=200)
frame.place(x=0, y=190)
tree = Treeview(frame, columns=('ФИО', 'Телефон', 'Почта'), show='headings')
tree.heading('ФИО', text='ФИО')
tree.heading('Телефон', text='Телефон')
tree.heading('Почта', text='Почта')
tree.column('ФИО', width=210)
tree.column('Телефон', width=210)
tree.column('Почта', width=210)
for person in data:
	tree.insert('', 'end', values=person)
scrollbar = Scrollbar(frame, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side='left')
scrollbar.pack(side='right', fill='y')

root.mainloop()