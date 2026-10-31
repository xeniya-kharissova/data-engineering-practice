import csv


VALID_MENU = {"ESPRESSO", "AMERICANO", "CAPPUCCINO", "LATTE", "FLAT WHITE"}

raw_orders = [
    ("  cappuccino  ", "John", 4.50, 1),
    ("ESPRESSO", None, 3.00, 2),                   # Сбой: пропущено имя (None)
    ("latte", "  Alice  ", -4.00, 1),              # Сбой: отрицательная цена
    ("FLAT WHITE", "Bob", 5.00, 10),               # Сбой: превышение лимита чашек
    ("TIRAMISU", "Emma", 6.50, 1),                 # Сбой: позиция отсутствует в кофейном меню
    ("  Flat White  ", "Michael", 4.80, 2),        # Валидная запись (требует нормализации)
    ("Americano", "Sarah", 0.00, 1),               # Сбой: нулевая стоимость
]

def extract_orders_from_csv(file_path: str) -> list:
    raw_records = []
    with open(file_path, mode = "r", encoding = "utf-8") as file:
        reader = csv.reader(file)

        next(reader, None)

        for row in reader:
            if not row:
                continue
            raw_records.append(row)

    return raw_records


def transform_orders(records: list) ->tuple[list, list]:

    rejected_records = []
    cleaned_records = []


    for item in records:
        if len(item) != 4:
            rejected_records.append((item, "Incorrect column count"))
            continue

        item_name, client_name, raw_price, raw_count = item

        if not item_name or not item_name.strip():
            rejected_records.append((item, "Item name missing"))
            continue

        if not client_name or not client_name.strip():
            rejected_records.append((item, "Name is  missing"))
            continue

        try:
            price = float(raw_price)
            count = int(raw_count)
        except ValueError:
            rejected_records.append((item, "Price or count  is not a valid number"))
            continue

        if price <= 0:
            rejected_records.append((item, "Invalid price: must be > 0"))
            continue

        if count <1 or count >5:
            rejected_records.append((item, "Ivalid item count: must be 1-5"))
            continue

        clean_item_name = item_name.strip().upper()
        clean_client_name = client_name.strip()

        if clean_item_name not in VALID_MENU:
            rejected_records.append((item, f"Item not in menu: '{clean_item_name}'"))
            continue

        cleaned_records.append((clean_item_name, clean_client_name, price, count))

    return cleaned_records, rejected_records

def save_dlq_to_csv(rejected_records: list, output_path: str):
    with open(output_path, mode = "w", encoding ="utf-8", newline = "") as file:
        writer = csv.writer(file) 

        writer.writerow(["raw_record", "rejected_reason"])

        for raw_item, reason in rejected_records:
            record_str = ", ".join(str(field) for field in raw_item)
            writer.writerow([record_str, reason])

if __name__ == "__main__":

    input_file = "orders.csv"
    error_file = "error.csv"

    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ")
    print("=" * 60)

    #Extraction 
    raw_data = extract_orders_from_csv(input_file)
    print(f"1. [Extract] Прочитано строк из {input_file}: {len(raw_data)}")

    #Clean
    valid, rejected = transform_orders(raw_orders)
    print(f"2. [Transform] Успешно прошли проверку: {len(valid)} из {len(raw_data)}.")
    for records in valid:
        print(records)        

    #Save errors
    if rejected:
        save_dlq_to_csv(rejected, error_file)
        print(f"\n3. [DLQ] Отчёт об ошибках сохранён в файл: {error_file}")
    print("=" * 60)






