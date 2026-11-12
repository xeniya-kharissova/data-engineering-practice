import csv
from dataclasses import dataclass
from collections.abc import Iterator

VALID_MENU = {"ESPRESSO", "AMERICANO", "CAPPUCCINO", "LATTE", "FLAT WHITE"}
@dataclass
class Orders:
    item_name : str
    client_name : str
    price : float
    count : int

@dataclass
class Order:
    item_name : str
    client_name : str
    price : float
    count : int

    def order_total_cost(self):
        return self.price * self.count
    
def extract_orders_from_csv(file_path: str) -> list:
    raw_records = []
    with open(file_path, mode = "r", encoding = "utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row or not any(row.values()):
                continue
            raw_records.append(row)

    return raw_records
def validate_order(row : dict) -> tuple[Order | None, None | str]:
        if not row["item_name"] and not row["item_name"].strip():
            return (row, "Item name is missing")

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

        cleaned_records.append(Order(clean_item_name, clean_client_name, price, count))

    return cleaned_records, rejected_records
def save_orders_to_csv(cleaned_records : list, output_path : str) -> None:
    with open(output_path, mode = "w", encoding = "utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["item_name", "client_name", "price", "count"])
        writer.writeheader()
        for order in cleaned_records:
            writer.writerow({"item_name":order.item_name, "client_name" : order.client_name, "price" : order.price, "count" : order.count})
            
def save_dlq_to_csv(rejected_records: list[tuple], output_path: str) -> None:

    with open(output_path, mode = "w", encoding ="utf-8", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames= ["item_name", "client_name", "price", "count", "error_reason"]) 

        writer.writeheader()

        for raw_item, reason in rejected_records:
            writer.writerow({**raw_item, "error_reason" : reason})

if __name__ == "__main__":

    input_file = "orders.csv"
    clean_file = "cleaned_orders.csv"
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
    total_price = 0 
    for order in valid:
        print(order)
        total_price+=order.order_total_cost()
    print(f"The total price is: {total_price}")    

    if valid:
        save_orders_to_csv(valid, clean_file)
        print(f"чистые заказы сохранены в файл: {clean_file}")    

    #Save errors
    if rejected:
        save_dlq_to_csv(rejected, error_file)
        print(f"\n3. [DLQ] Отчёт об ошибках сохранён в файл: {error_file}")
    print("=" * 60)






