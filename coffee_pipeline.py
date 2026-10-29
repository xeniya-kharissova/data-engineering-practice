
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

def transform_orders(records: list) ->tuple[list, list]:

    rejected_records = []
    cleaned_records = []

    for item in records:
        item_name, client_name, price, count = item
        if item_name is None:
            rejected_records.append((item, "Item name is missing"))
            continue
        if client_name is None:
            rejected_records.append((item,"Client name is missing"))
            continue
        if price <= 0:
            rejected_records.append((item, "Invalid price"))
            continue
        if count < 1 or count > 5:
            rejected_records.append((item, "Invalid item count"))
            continue

        clean_item_name = item_name.strip().upper()
        clean_client_name = client_name.strip()

        if clean_item_name not in VALID_MENU:
            rejected_records.append((item, "Item is not in menu"))
            continue

        cleaned_records.append((clean_item_name, clean_client_name, price, count))

    return cleaned_records, rejected_records


if __name__ == "__main__":

    valid, rejected = transform_orders(raw_orders)
    print(f"успешно прошли проверку: {len(valid)} из {len(raw_orders)}.")
    for records in valid:
        print(records)        

    print(f"Не успешно прошли проверку: {len(rejected)} из {len(raw_orders)}.")
    for records in rejected:
            print(records)  






