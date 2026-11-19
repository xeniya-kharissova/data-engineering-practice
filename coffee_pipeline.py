import csv
from dataclasses import dataclass
from collections.abc import Iterator

VALID_MENU = {"ESPRESSO", "AMERICANO", "CAPPUCCINO", "LATTE", "FLAT WHITE"}


@dataclass
class Order:
    item_name : str
    client_name : str
    price : float
    count : int

    def order_total_cost(self):
        return self.price * self.count
    
def extract_orders_from_csv(file_path: str) -> Iterator[dict]:
    with open(file_path, mode = "r", encoding = "utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not row or not any(row.values()):
                continue
            yield row

def validate_order(row : dict) -> tuple[Order | None, None | str]:
        item_name = str(row.get("item_name") or "").strip().upper()
        if not item_name:
            return (None, "Item name is missing")
        if item_name not in VALID_MENU:
            return (None, "Item is not in menu")
        client_name = str(row.get("client_name") or "").strip().upper()
        if not client_name:
            return(None, "Cleint name is missing")
        try:
            price = float(row.get("price", 0))
        except (TypeError, ValueError):
            return (None, "Price must be either fraction or integer")
        if price<=0:
            return(None, "Price must be > 0")

        try:
            count = int(row.get("count", 0))
        except (TypeError, ValueError):
            return (None, "Amount of cups must be integer")
        if count < 1 or count>5:
            return (None, "Amount of cups must be beyween 1 and 5")
        order = Order(item_name, client_name, price, count)
        return (order, None)
        

# def transform_orders(records: list[dict]) ->tuple[list[Order],list[tuple]]:

#     rejected_records = []
#     cleaned_records = []

#     for item in records:
#         item_name = item.get("item_name")   
#         client_name = item.get("client_name")
#         raw_price = item.get("price")
#         raw_count = item.get("count")


#         if not item_name or not item_name.strip():
#             rejected_records.append((item, "Item name is missing"))
#             continue

#         if not client_name or not client_name.strip():
#             rejected_records.append((item, "Client name is missing"))
#             continue

#         try:
#             price = float(raw_price)
#             count = int(raw_count)
#         except (ValueError, TypeError):
#             rejected_records.append((item, "Price or count  is not a valid number"))
#             continue

#         if price <= 0:
#             rejected_records.append((item, "Invalid price: must be > 0"))
#             continue

#         if count <1 or count >5:
#             rejected_records.append((item, "Ivalid item count: must be 1-5"))
#             continue

#         clean_item_name = item_name.strip().upper()
#         clean_client_name = client_name.strip()

#         if clean_item_name not in VALID_MENU:
#             rejected_records.append((item, f"Item not in menu: '{clean_item_name}'"))
#             continue

#         cleaned_records.append(Order(clean_item_name, clean_client_name, price, count))

    # return cleaned_records, rejected_records
# def save_orders_to_csv(cleaned_records : list, output_path : str) -> None:
#     with open(output_path, mode = "w", encoding = "utf-8", newline="") as file:
#         writer = csv.DictWriter(file, fieldnames=["item_name", "client_name", "price", "count"])
#         writer.writeheader()
#         for order in cleaned_records:
#             writer.writerow({"item_name":order.item_name, "client_name" : order.client_name, "price" : order.price, "count" : order.count})
            
# def save_dlq_to_csv(rejected_records: list[tuple], output_path: str) -> None:

#     with open(output_path, mode = "w", encoding ="utf-8", newline = "") as file:
#         writer = csv.DictWriter(file, fieldnames= ["item_name", "client_name", "price", "count", "error_reason"]) 

#         writer.writeheader()

#         for raw_item, reason in rejected_records:
#             writer.writerow({**raw_item, "error_reason" : reason})

def process_orders_pipeline(input_path : str, clean_path :str, error_path : str) -> dict:
    stats = {"total":0, "clean" : 0, "error" : 0, "revenue" : 0}
    with open(clean_path, mode = "w", encoding="utf-8", newline="") as clean_file, open (error_path, mode = "w", encoding="utf-8",newline="") as error_file:
        c_writer = csv.DictWriter(clean_file, fieldnames=["item_name", "client_name", "price", "count"])
        e_writer = csv.DictWriter(error_file, fieldnames=["item_name", "client_name", "price", "count", "error_reason"])
        c_writer.writeheader()
        e_writer.writeheader()
        for raw_row in extract_orders_from_csv(input_path):
            stats["total"]+=1
            order, reason = validate_order(raw_row)
            if order:
                stats["clean"]+=1
                stats["revenue"]+=order.order_total_cost()
                c_writer.writerow({"item_name" : order.item_name, "client_name" : order.client_name, "price" : order.price, "count" : order.count})
            else:
                stats["error"] +=1
                e_writer.writerow({**raw_row, "error_reason" : reason})
    return stats



if __name__ == "__main__":

    input_file = "orders.csv"
    clean_file = "cleaned_orders.csv"
    error_file = "error.csv"

    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    print("=" * 60)
    print(process_orders_pipeline(input_file, clean_file, error_file))






