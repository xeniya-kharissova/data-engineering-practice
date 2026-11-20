import csv
from dataclasses import dataclass
from collections.abc import Iterator
from collections import Counter, defaultdict
import time 
from functools import wraps

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
   
def measure_time(func):
    @wraps(func)   
    def wrapper(*args,**kwargs):
        start = time.perf_counter()
        try:
            result = func(*args,**kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            print(f"[TIME] {func.__name__} выполнилась за {elapsed:.4f} сек.")
        
    return wrapper


def retry(retries : int = 3, delay : float = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for trial in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    print(f"[UNEXPECTED ERROR] | [TRIAL] : {trial+1} | [REASON] : {e}")
                    if trial+1 == retries : raise
                    time.sleep(delay)
        return wrapper
    return decorator
    
@measure_time   
@retry(retries=3, delay=0.5)
def process_orders_pipeline(input_path : str, clean_path :str, error_path : str) -> dict:
    stats = {"total":0, "clean" : 0, "error" : 0, "revenue" : 0}
    drinks_sold = Counter()
    revenue_by_client = defaultdict(float)
    error_reasons = Counter()
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
                drinks_sold[order.item_name]+=order.count
                order_cost = order.order_total_cost()
                revenue_by_client[order.client_name]+=order_cost
                stats["revenue"]+=order_cost
                c_writer.writerow({"item_name" : order.item_name, "client_name" : order.client_name, "price" : order.price, "count" : order.count})
            else:
                stats["error"] +=1
                error_reasons[reason]+=1
                e_writer.writerow({**raw_row, "error_reason" : reason})
    stats["top_drinks"] = drinks_sold.most_common()
    stats["revenue_by_client"] = dict(revenue_by_client)
    stats["error_reasons"] = error_reasons.most_common()
    return stats



if __name__ == "__main__":

    input_file = "orders.csv"
    clean_file = "cleaned_orders.csv"
    error_file = "error.csv"

    print("=" * 60)
    print("СТАРТ ОБРАБОТКИ ФАЙЛА ЗАКАЗОВ (DictReader)")
    print("=" * 60)
    print(process_orders_pipeline(input_file, clean_file, error_file))
    print("Имя функции:", process_orders_pipeline.__name__)





