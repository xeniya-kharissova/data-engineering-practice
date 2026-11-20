from dataclasses import dataclass
from functools import wraps
import time
import csv
# class CoffeeOrder:
#     def __init__(self, item_name : str, price : float, count : int):
#         self.item_name = self._clean_name(item_name)
#         self.price = price
#         self.count = count
#     def _clean_name(self, raw_name : str) -> str:
#         return raw_name.strip().upper()
#     def get_total(self, discount : float = 0.00) -> float :
#         total_price = self.price * self.count
#         if discount > 0:
#             total_price *=(1-discount)
#         return total_price

# order = CoffeeOrder("   latte   ", 250.0, 1)
# print(order.item_name)

# class NumArray:

#     def __init__(self, nums: list[int]):
#         self.prefix = self._create_prefix(nums)

#     def _create_prefix(self, initial_array):
#         pref = [0] * (len(initial_array)+1)
#         for i in range(1, len(initial_array) + 1):
#             pref[i] = pref[i-1] + initial_array[i-1]
#         return pref

#     def sumRange(self, left: int, right: int) -> int:
#         return self.prefix[right+1] - self.prefix[left]
        
# num_array = NumArray([-2, 0, 3, -5, 2, -1])
# print(num_array.sumRange(0,2))

# from dataclasses import dataclass

# @dataclass
# class Order:
#     item_name : str
#     client_name : str
#     price : float
#     count : int

#     def calculate_total(self):
#         return self.price*self.count

# order = Order("LATTE", "Алексей", 250.0, 2)
# print(order)
# print(order.calculate_total())


# from dataclasses import dataclass

# @dataclass
# class DeliveryOrder(Order):
    
#     delivery_fee: float

#     def calculate_total(self):
#         return super().calculate_total() + self.delivery_fee
    
# order = DeliveryOrder("CAPPUCCINO", "Мария", 300.0, 1, 150)
# print(order.calculate_total())

# @dataclass
# class Order:
#     item_name : str
#     client_name : str
#     price : float
#     count : int
#     def _calculate_tax(self) -> float:
#         return self.price * self.count * 0.10
#     def final_price(self):
#         return self._calculate_tax()

# @dataclass
# class TakeawayOrder(Order):
#     cup_fee : float = 0.5
#     def final_price(self):
#         base_price = super().final_price()
#         return base_price + (self.cup_fee * self.count)

# @dataclass
# class VipOrder(Order):
#     discount_rate : float = 0.20
#     def final_price(self):
#         base_price = super().final_price()
#         return base_price * (1 - self.discount_rate)
# def calculate_shift_revenue(orders : list[Order]) -> float:
#     total_price = 0
#     for order in orders:
#         total_price += order.final_price()
#     return round(total_price, 2)

# if __name__ == "__main__":
#     shift_orders = [
#         Order("ESPRESSO", "Alex", 3.0, 2),
#         TakeawayOrder("LATTE", "Kate", 5.0, 2, cup_fee=0.5),
#         VipOrder("CAPPUCCINO", "Max", 4.0, 1, discount_rate=0.20),
#     ]

#     for order in shift_orders:
#         print(f"{order.client_name}: {order.final_price():.2f}")

#     total = calculate_shift_revenue(shift_orders)
#     print(f"Выручка за смену: {total}")

# def log_call(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         print(f"[START] Вызов {func.__name__} | args={args} | kwargs={kwargs}")
#         result = func(*args,**kwargs)
#         print(f"[END] {func.__name__} вернула: {result}")
#         return result
#     return wrapper
# @log_call
# def calc_total(price : float = 4.5, count : int = 2) ->float:
#     return price * count

# if __name__ == "__main__":
#     print(calc_total(2, count = 1))

def retry(retries : int = 3, delay : float = 1.0 ):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1,retries+1):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e: 
                    print(f"[UNEXPECTED ERROR ON TRY {i}] | [ERROR REASON : {e} ]")   
                    if i == retries : raise   
                    time.sleep(delay) 
        return wrapper
    return decorator

attempt = [0]
@retry(retries=3,delay=0.5)
def fetch_data(attempts):
    attempts[0]+=1
    if attempts[0]<3:
        raise ConnectionError("Сервер не отвечает")
    return "success"


if __name__ == "__main__":
    print(fetch_data(attempt))

    