# import os
# import psycopg2
# from dotenv import load_dotenv

# # load_dotenv()

# raw_data = [
#     # (recipient_name, weight_kg, cost, status)
#     ("  Иван Смирнов  ", 2.50, 450.00, "delivered"),     # пробелы и строчные буквы
#     (None, 10.00, 1200.00, "DELIVERED"),                 # пропущено имя (None)
#     ("Ольга Кузнецова", -5.00, 800.00, "IN_TRANSIT"),     # отрицательный вес (аномалия)
#     ("Петр Васильев", 14.20, 1800.00, "  Delivered  "),  # смесь регистра и пробелов
#     ("Анна Смирнова", 0.80, -200.00, "CREATED"),   
#     ("Ксения Харисова", 45.00, 450.00, "CREATED")       # отрицательная цена
# ]

# def clean_shipments_records(records: list) -> list:

#     cleaned_records = []
#     rejected_records = []

   
         

#     for item in records:
#         name, weight, cost, status = item
#         if name is None:
#             rejected_records.append((item, "Отсутствует имя получателя"))

#             continue

#         if weight <= 0 or cost<=0:
#             rejected_records.append((item, "Отрицательный или нулевой вес/цена"))
#             continue

#         if weight > 35:
#             rejected_records.append((item, f"Перевес: {weight-35} кг (максимум 35 кг)"))
#             continue

#         # Стандартизация текста
#         clean_name = name.strip()
#         clean_status = status.strip().upper()

#         cleaned_records.append((clean_name, cost, clean_status))
#     return cleaned_records, rejected_records

# valid_shipments = clean_shipments_records(raw_data)
# print(f"\nУспешно прошли очистку: {len(valid_shipments)} из {len(raw_data)}")
# for records in valid_shipments:
#     print(records)

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


"""QUEQUE"""
# from collections import deque

# def process_task_flow(events: list[tuple[str, str]]) -> list[str]:
#     que = deque()
#     serve_tasks = []
#     for operation_type, task_name in events:
#         if operation_type.lower() == "new":
#             que.append(task_name)
#         elif operation_type.lower() == "cancel" and len(que)>0:
#             que.pop()
#         elif operation_type.lower() == "serve" and len(que)>0:
#             serve_tasks.append(que.popleft())
            
#     return serve_tasks

# events = [
#     ("NEW", "backup_db"),
#     ("NEW", "send_email"),
#     ("NEW", "render_video"),
#     ("CANCEL", ""),            # Отменили последнюю задачу ("render_video")
#     ("SERVE", ""),             # Воркер забрал первую пришедшую задачу ("backup_db")
#     ("NEW", "generate_pdf"),
#     ("SERVE", ""),             # Воркер забрал следующую старейшую задачу ("send_email")
#     ("SERVE", ""),             # Воркер забрал "generate_pdf"
#     ("SERVE", "")              # Очередь пуста, ничего не происходит
# ]

# print(process_task_flow(events))

# from collections import deque

# def round_robin_scheduler(tasks: list[tuple[str, int]], quantum: int) -> list[str]:
#     remaining_processes= deque(tasks)
#     finished_jobs = []
    
#     while remaining_processes:

#         task_name, remaining_time = remaining_processes.popleft()

#         if remaining_time <= quantum:
#             finished_jobs.append(task_name)
#         else:
#             remaining_processes.append((task_name, remaining_time-quantum))

#     return finished_jobs

# tasks = [
#     ("TaskA", 5),
#     ("TaskB", 2),
#     ("TaskC", 4)
# ]
# quantum = 2
# print(round_robin_scheduler(tasks, quantum))

# from collections import deque

# def hot_potato(players: list[str], k: int) -> str:
#     left_players = deque(players)
#     pot_counter = 1

#     while len(left_players)>1:
#         current_player = left_players.popleft()
#         if pot_counter<k:
#             pot_counter+=1
#             left_players.append(current_player)
#         else:
#             pot_counter = 1
#     return left_players[0]

#other option of solving same exersise
# from collections import deque

# def hot_potato(players: list[str], k: int) -> str:
#     left_players = deque(players)

#     while len(left_players) > 1:
#         # 1. k - 1 раз пересаживаем игроков из начала в конец
#         for _ in range(k - 1):
#             left_players.append(left_players.popleft())
        
#         # 2. k-й игрок сгорает — просто удаляем его из очереди
#         left_players.popleft()

#     return left_players[0]

# players = ["Alice", "Bob", "Charlie", "David"]
# k = 2
# print(hot_potato(players, 2))
        

        

