# 📝 README: Store Manager / Менеджер магазина

## 🌐 Language Selection / Выбор языка

| Language | Action |
| :--- | :--- |
| **English** | Continue reading from the next section. |
| **Русский** | Прокрутите до раздела: [Русский](#-русский). |

---

## 🇬🇧 English

### Store Manager

A simple, desktop-based store management application built with Python and the Tkinter library. It allows you to track products, clients, and orders, and visualize sales statistics over a specific period.

### Features

* **Data Management:** Import and export data (products, clients, orders) to JSON files.
* **Order Tracking:** Record new orders, associating them with existing products and clients.
* **Product Inventory:** Display current product stock levels.
* **Data Visualization (New!):** Generate a **time-series plot** of sales (product count) for a specified date range using `matplotlib`.
* **GUI:** User-friendly graphical interface built with Tkinter.

### Installation and Setup

1.  **Clone the repository (if applicable) or download the files:**
    ```bash
    git clone [your_repo_link]
    cd store-order-managment-system
    ```

2.  **Install the required libraries:**
    This project requires `matplotlib` for the statistics feature.
    ```bash
    pip install matplotlib
    ```

3.  **Run the application:**
    Use the newly created `main.py` file to start the GUI.
    ```bash
    python main.py
    ```

### Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | **Main entry point** for launching the application. |
| `gui.py` | Contains the **Tkinter GUI** structure and logic (buttons, window layout). |
| `db.py` | Handles **data persistence**: importing and exporting data to/from `data/*.json` files. |
| `models.py` | Defines the **data structures** (classes) for `Product`, `Client`, and `Order`. |
| `analysis.py` | Contains the logic for **data processing** and visualization using `matplotlib`. |
| `data/` | Directory where JSON data files (e.g., `products.json`, `orders.json`) are stored. |

---

## 🇷🇺 Русский

### Менеджер магазина

Простое настольное приложение для управления магазином, созданное на Python с использованием библиотеки Tkinter. Оно позволяет отслеживать товары, клиентов и заказы, а также визуализировать статистику продаж за определенный период.

### Функциональность

* **Управление данными:** Импорт и экспорт данных (товаров, клиентов, заказов) в файлы формата JSON.
* **Учет заказов:** Запись новых заказов с привязкой к существующим товарам и клиентам.
* **Остатки товаров:** Отображение текущих запасов товаров на складе.
* **Визуализация данных (Новое!):** Построение **временного графика** продаж (количества товаров) за указанный период с использованием библиотеки `matplotlib`.
* **GUI:** Удобный графический интерфейс, разработанный на Tkinter.

### Установка и запуск

1.  **Клонируйте репозиторий (если применимо) или скачайте файлы:**
    ```bash
    git clone [ссылка_на_ваш_репозиторий]
    cd store-order-managment-system
    ```

2.  **Установите необходимые библиотеки:**
    Для функции статистики требуется библиотека `matplotlib`.
    ```bash
    pip install matplotlib
    ```

3.  **Запуск приложения:**
    Используйте созданный файл `main.py` для запуска графического интерфейса.
    ```bash
    python main.py
    ```

### Структура проекта

| Файл | Описание |
| :--- | :--- |
| `main.py` | **Основная точка входа** для запуска приложения. |
| `gui.py` | Содержит структуру **GUI на Tkinter** и логику (кнопки, расположение окон). |
| `db.py` | Обеспечивает **сохранение данных**: импорт и экспорт данных в/из файлов `data/*.json`. |
| `models.py` | Определяет **структуры данных** (классы) для `Product`, `Client` и `Order`. |
| `analysis.py` | Содержит логику **обработки данных** и визуализации с помощью `matplotlib`. |
| `data/` | Директория, где хранятся файлы данных JSON (например, `products.json`, `orders.json`). |
