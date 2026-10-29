# # =====================================================================
# 1. DICTIONARY AGGREGATION (Simulating SQL GROUP BY)
# =====================================================================
# shipments = [
# {"id": 1, "recipient": "Иван Смирнов", "cost": 450.0, "status": "DELIVERED"},
#     {"id": 2, "recipient": "Ольга Кузнецова", "cost": 1800.0, "status": "DELIVERED"},
#     {"id": 3, "recipient": "Сергей Морозов", "cost": 3200.0, "status": "RETURNED"},
#     {"id": 4, "recipient": "Анна Новикова", "cost": 850.0, "status": "DELIVERED"},
# ]

# #total_revenue = 0
# #считаем итоговую выручку
# # for item in shipments:
# #     if item["status"] == "DELIVERED":
# #         total_revenue+=item["cost"]

# # print(f"Итоговая выручка: {total_revenue} руб")

# revenue_by_status = {}

# for item in shipments:
#     status = item["status"]
#     cost = item["cost"]

#     if status not in revenue_by_status:
#         revenue_by_status[status] = 0.00

#     revenue_by_status[status]+=cost

# print(f"Сводка по статусам: {revenue_by_status}")

# # =====================================================================
# # 2. SYNTHETIC DATA GENERATION (Faker + Random)
# # =====================================================================
# import random
# from faker import Faker

# fake = Faker("en_US")

# STATUSES = ["DELIVERED", "IN_TRANSIT", "CANCELED", "RETURNED"]
# WAREHOUSE_IDS = [1, 2, 3, 4]

# def generate_shipment() -> dict:
#     """Generate a single synthetic logistics order matching the database schema."""
#     return {
#         "warehouse_id": random.choice(WAREHOUSE_IDS),
#         "recipient_name": fake.name(),
#         # Courier delivery weight limit: 0.5 to 35.0 kg
#         "weight_kg": round(random.uniform(0.5, 35.0), 2),
#         "cost": round(random.uniform(10.0, 300.0), 2),
#         "status": random.choice(STATUSES),
#     }

# shipment_batch = [generate_shipment() for _ in range (3)]

# for item in shipment_batch:
#     print(item)




# import os
# import random
# from typing import List, Dict, Any
# from dotenv import load_dotenv
# from faker import Faker
# import psycopg2
# from psycopg2.extras import execute_values

# # Load environment variables from .env file into memory before opening connections
# load_dotenv() 
# fake = Faker("en_US")

# STATUSES = ["CREATED", "IN_TRANSIT", "DELIVERED", "RETURNED"]

# VALID_WAREHOUSE_IDS = [1, 2, 3, 4]

# def generate_shipment_batch(batch_size: int = 100) -> List[Dict[str, Any]]:
#     """
#     Generate a batch of synthetic shipment records matching the target schema.
    
#     Args:
#         batch_size: Number of dictionary records to create.
        
#     Returns:
#         List of dictionaries where each dictionary represents a single row.
#     """
#     batch =[]
#     for _ in range(batch_size):
#         record = {
#             "warehouse_id": random.choice(VALID_WAREHOUSE_IDS),
#             "recipient_name": fake.name(),
#             # Clamping delivery package weight to typical courier limits (0.5 to 35.0 kg)
#             "weight_kg": round(random.uniform(0.5, 35.0), 2),
#             "cost": round(random.uniform(10.0, 300.0), 2),
#             "status": random.choice(STATUSES),
#         }
#         batch.append(record)
#     return batch

# def insert_shipments(shipments: List[Dict[str, Any]]) -> None:
#     """
#     Bulk-insert generated shipment dictionaries into the PostgreSQL database.
    
#     Args:
#         shipments: List of shipment records to be persisted.
#     """
#     db_url = os.getenv("DATABASE_URL")
#     if not db_url:
#         raise ValueError("DATABASE_URL variable is missing from the environment.")

#     records_to_insert = [
#         (
#             item["warehouse_id"],
#             item["recipient_name"],
#             item["weight_kg"],
#             item["cost"],
#             item["status"],
#         )
#         for item in shipments
#     ]

#     query = """
#         INSERT INTO shipments (warehouse_id, recipient_name, weight_kg, cost, status)
#         VALUES %s;
#     """
#     with psycopg2.connect(db_url) as conn:
#         with conn.cursor() as cur:
#             execute_values(cur, query, records_to_insert)

#     print(f"Successfully loaded {len(records_to_insert)} records into NeonDB.")

# if __name__=="__main__":
#     test_batch = generate_shipment_batch(batch_size = 10)
#     insert_shipments(test_batch)


# =====================================================================
# 6. БЕЗОПАСНОЕ ЧТЕНИЕ ДАННЫХ И РАСПАКОВКА (Parameterized SELECT)
# =====================================================================
# Правило: никогда не вставлять переменные в SQL через f-строки!
# Передаем параметры строго вторым аргументом в execute() через кортеж.
# import os
# import psycopg2
# from dotenv import load_dotenv

# load_dotenv()
# db_url = os.getenv("DATABASE_URL")

# target_status = 'DELIVERED'
# row_limit = 3

# query = """
#     SELECT 
#     recipient_name, cost, status
#     FROM shipments
#     WHERE status = %s
#     LIMIT %s;
# """

# with psycopg2.connect(db_url) as conn:
#     with conn.cursor() as cur:

#         #отправляем sql запрос серверу
#         cur.execute(query, (target_status, row_limit))

#         #берем ответ из буфера в переменную rows
#         rows = cur.fetchall()

# print(f"Получено строк: {len(rows)}")

# #допустимый, но не оптимальный вариант - доставать по индексам кортежа. 
# # если, к примеру поменять колонки местами, то порядок нарушится.
# # for row in rows:
# #     # row — это кортеж. Достаем элементы по индексам: 0, 1, 2
# #     name = row[0]
# #     cost = row[1]
# #     status = row[2]
# #     print(f"Client: {name} / Cost: {cost} / Status: {status}")

# #более безопасный прием - распаковка кортежей
# for name, cost, status in rows:
#     print(f"Client: {name} / Cost: {cost} / Status: {status}")
# #ВАЖНО: Python вообще ничего не знает об именах колонок из SQL
# #  — распаковка происходит исключительно по порядку (по позиции), слева направо
# # порядок колонок в SELECT должен в точности повторять порядок переменных в цикле

# """SQL INJECTION"""
# #Почему f-строки в SQL строго запрещены?
# # Это уязвимость номер один в мире баз данных — SQL-инъекция (SQL Injection).

# # злоумышленник может ввести вместо статуса:
# # ' OR 1=1; DROP TABLE shipments; --

# # Как передавать параметры правильно в psycopg2
# # Параметры всегда передаются отдельно от текста запроса через плейсхолдер %s,
# # а вторым аргументом в cur.execute() отдаётся кортеж со значениями

# =====================================================================
# 7. БЕЗОПАСНАЯ ОБРАБОТКА ОШИБОК БАЗЫ ДАННЫХ (try - except)
# =====================================================================
# try: зона риска (сеть, внешние файлы, запросы к БД)
# except ИмяОшибки as err: запасной план действий при сбое конкретного типа

# import psycopg2

# def demo_safe_database_query(db_url: str):
#     try:
#         with psycopg2.connect(db_url) as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT 1;")
#                 return cur.fetchall()
                
#     except psycopg2.OperationalError as err:
#         # Проблемы со связью: неверный хост/пароль или оборван интернет
#         print(f"Ошибка подключения к базе: {err}")
#         return []
        
#     except psycopg2.Error as err:
#         # Ошибки уровня SQL: неверный синтаксис, несуществующая колонка
#         print(f"Ошибка выполнения SQL: {err}")
#         return []

# =====================================================================
# 8. ОЧИСТКА И ВАЛИДАЦИЯ ДАННЫХ (Data Cleaning & Validation)
# =====================================================================
# None проверяется строго через `is None`
# .strip() удаляет невидимые пробелы по краям
# .upper() / .lower() приводят к единому регистру
# continue пропускает бракованную запись и переходит к следующей

# def clean_record_example(records: list) -> list:
#     valid_data = []

#     for name, weight, cost, status in records:
#         # 1. Проверка обязательных полей
#         if name is None:
#             continue

#         # 2. Бизнес-правила (границы значений)
#         if weight <= 0 or weight > 35 or cost <= 0:
#             continue

#         # 3. Нормализация текста
#         clean_name = name.strip()
#         clean_status = status.strip().upper()

#         valid_data.append((clean_name, clean_status, cost))

#     return valid_data