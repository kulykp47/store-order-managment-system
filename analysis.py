import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
import db
import models

def parse_and_filter_orders(start_date_str, end_date_str):
    date_format_input = "%d.%m.%Y"
    date_format_order = "%d.%m.%Y %H:%M"
    
    try:
        start_date = datetime.strptime(start_date_str, date_format_input).date()
        end_date = datetime.strptime(end_date_str, date_format_input).date()
        
        if start_date > end_date:
            return "Начальная дата не может быть позже конечной."
            
    except ValueError:
        return "Ошибка формата даты. Используйте формат ДД.ММ.ГГГГ."

    daily_sales = defaultdict(float)
    
    for order in db.orders:
        try:
            order_datetime = datetime.strptime(order.date_time, date_format_order)
            order_date = order_datetime.date()
            
            if start_date <= order_date <= end_date:
                daily_sales[order_date] += order.order_count
                
        except ValueError:
            continue

    if not daily_sales:
        return "Нет данных за выбранный период."

    dates = sorted(daily_sales.keys())
    counts = [daily_sales[date] for date in dates]

    return dates, counts


def visualize_orders(start_date_str, end_date_str):
    result = parse_and_filter_orders(start_date_str, end_date_str)
    
    if isinstance(result, str):
        return result

    dates, counts = result
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(dates, counts, marker='o', linestyle='-')
    
    plt.title(f'Количество проданных товаров за период: {start_date_str} - {end_date_str}')
    plt.xlabel('Дата')
    plt.ylabel('Количество проданных товаров')
    plt.grid(True)
    plt.gcf().autofmt_xdate()
    
    plt.show()
    
    return "График успешно построен."