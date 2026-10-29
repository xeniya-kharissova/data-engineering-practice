import os
import psycopg2
from dotenv import load_dotenv

# load_dotenv()

raw_data = [
    # (recipient_name, weight_kg, cost, status)
    ("  Иван Смирнов  ", 2.50, 450.00, "delivered"),     # пробелы и строчные буквы
    (None, 10.00, 1200.00, "DELIVERED"),                 # пропущено имя (None)
    ("Ольга Кузнецова", -5.00, 800.00, "IN_TRANSIT"),     # отрицательный вес (аномалия)
    ("Петр Васильев", 14.20, 1800.00, "  Delivered  "),  # смесь регистра и пробелов
    ("Анна Смирнова", 0.80, -200.00, "CREATED"),   
    ("Ксения Харисова", 45.00, 450.00, "CREATED")       # отрицательная цена
]

def clean_shipments_records(records: list) -> list:

    cleaned_records = []
    rejected_records = []

   
         

    for item in records:
        name, weight, cost, status = item
        if name is None:
            rejected_records.append((item, "Отсутствует имя получателя"))

            continue

        if weight <= 0 or cost<=0:
            rejected_records.append((item, "Отрицательный или нулевой вес/цена"))
            continue

        if weight > 35:
            rejected_records.append((item, f"Перевес: {weight-35} кг (максимум 35 кг)"))
            continue

        # Стандартизация текста
        clean_name = name.strip()
        clean_status = status.strip().upper()

        cleaned_records.append((clean_name, cost, clean_status))
    return cleaned_records, rejected_records

valid_shipments = clean_shipments_records(raw_data)
print(f"\nУспешно прошли очистку: {len(valid_shipments)} из {len(raw_data)}")
for records in valid_shipments:
    print(records)

# target_status = 'DELIVERED'
# row_limit = 3

# def safe_fetch_shipments(limit: int = 5):
#     # db_url = os.getenv("DATABASE_URL")
#     db_url = "postgresql://wrong_user:wrong_password@fake_host/fake_db"
#     query = """
#         SELECT recipient_name, cost, status
#         FROM shipments 
#         LIMIT %s;
#     """
#     try:
#         print("Попытка связаться с базой данных...")
#         with psycopg2.connect(db_url) as conn:
#             with conn.cursor() as cur:
#                 cur.execute(query, (limit,))
#                 return cur.fetchall()

#     except psycopg2.OperationalError as err:
#         print(f"[ОШИБКА СЕТИ / БАЗЫ] Не удалось подключиться к NeonDB. Детали: {err}")
#         return[]

#     except psycopg2.Error as err:
#         print(f"[ОШИБКА SQL]: Запрос не выполнен. Детали: {err}")
#         return []

# data = safe_fetch_shipments(3)
# print(f"Итог: получено {len(data)} записей.")



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


# for name, cost, status in rows:
#     print(f"Client: {name} / Cost: {cost} / Status: {status}")



