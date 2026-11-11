import csv
from dataclasses import dataclass

VALID_MENU = {"ESPRESSO", "AMERICANO", "CAPPUCCINO", "LATTE", "FLAT WHITE"}
@dataclass
class Orders:
    item_name : str
    client_name : str
    price : float
    count : int

def extract_orders_from_csv(file_path: str) -> list:
    raw_records = []
    with open(file_path, mode = "r", encoding = "utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row or not any(row.values()):
                continue
            raw_records.append(row)

    return raw_records


def transform_orders(records: list[dict]) ->tuple[list[Orders],list[tuple]]:

    rejected_records = []
    cleaned_records = []

    for item in records:
        item_name = item.get("item_name")   
        client_name = item.get("client_name")
        raw_price = item.get("price")
        raw_count = item.get("count")


        if not item_name or not item_name.strip():
            rejected_records.append((item, "Item name is missing"))
            continue

        if not client_name or not client_name.strip():
            rejected_records.append((item, "Client name is missing"))
            continue

        try:
            price = float(raw_price)
            count = int(raw_count)
        except (ValueError, TypeError):
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

        cleaned_records.append((Orders(clean_item_name, clean_client_name, price, count)))

    return cleaned_records, rejected_records

def save_dlq_to_csv(rejected_records: list[tuple], output_path: str) -> None:

    with open(output_path, mode = "w", encoding ="utf-8", newline = "") as file:
        writer = csv.writer(file) 

        writer.writerow(["raw_record", "rejected_reason"])

        for raw_item, reason in rejected_records:
            record_str = ", ".join(str(val) for val in raw_item.values())
            writer.writerow([record_str, reason])

if __name__ == "__main__":

    input_file = "orders.csv"
    error_file = "error.csv"

    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    print("=" * 60)

    #Extraction 
    raw_data = extract_orders_from_csv(input_file)
    print(f"1. [Extract] Прочитано строк из {input_file}: {len(raw_data)}")

    #Clean
    valid, rejected = transform_orders(raw_data)
    total_price = 0
    print(f"2. [Transform] Успешно прошли проверку: {len(valid)} из {len(raw_data)}.")
    for order in valid:
        print(order) 
        total_price+=order.price
    print(f"The total is: {total_price}")       

    #Save errors
    if rejected:
        save_dlq_to_csv(rejected, error_file)
        print(f"\n3. [DLQ] Отчёт об ошибках сохранён в файл: {error_file}")
    print("=" * 60)






